import ast
import os
import inspect

from contextlib import redirect_stderr, redirect_stdout

import nbformat
import papermill as pm

from nbclean import NotebookCleaner

from .utils import hide_outputs

try:
    from IPython.core.inputsplitter import IPythonInputSplitter
except ImportError:
    raise ImportError('IPython needs to be installed for notebook grading')


def split_notebook(notebook, student_path, autograder_path):
    """Split a master notebook into student and autograder notebooks"""
    print('Processing', notebook)

    _, nb_name = os.path.split(notebook)
    base_name, extension = os.path.splitext(nb_name)

    # create test files and notebook for the student
    nb = NotebookCleaner(notebook)
    nb.create_tests(tag='private',
                    oktest_path=base_name,
                    base_dir=autograder_path)
    nb.create_tests(tag='public',
                    oktest_path=base_name,
                    base_dir=student_path)
    text_replace_begin = '### BEGIN SOLUTION'
    text_replace_end = '### END SOLUTION'
    nb.replace_text(text_replace_begin, text_replace_end)

    nb.save(os.path.join(student_path, nb_name))

    # create test files for the autograder
    nb = NotebookCleaner(notebook)
    nb.create_tests(tag='private',
                    oktest_path=base_name,
                    base_dir=autograder_path)
    nb.create_tests(tag='public',
                    oktest_path=base_name,
                    base_dir=autograder_path)


def find_check_definition(tree):
    """Walk an AST and check for definitions of a function called `check`

    Return True if one is found, False otherwise.
    """
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.FunctionDef):
            continue
        if stmt.name == 'check':
            return True
    return False


def find_check_assignment(tree):
    """Walk an AST and check for assignments to a variable called `check`

    Return True if one is found, False otherwise.
    """
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.Assign):
            continue
        # check id for tuple target
        target_names = []
        for target in stmt.targets:
            if isinstance(target, tuple):
                target_names += [t.id for t in target]
            else:
                target_names.append(target.id)
        if 'check' in target_names:
            return True
    return False


class CheckCallWrapper(ast.NodeTransformer):
    """NodeTransformer visits and replaces nodes in place.
    CheckCallWrapper finds nodes with check(..) and replaces it with
    check_results_<secret>(check(...))"""

    def __init__(self, secret):
        self.secret = secret

    def node_constructor(self, expression):
        """Creates node that wraps expression in a list (check_results_XX) append call"""
        args = [expression]
        func = ast.Attribute(
            value=ast.Name(id='check_results_{}'.format(self.secret),
                           ctx=ast.Load()),
            attr='append',
            ctx=ast.Load(),
            keywords=[]
            )
        return ast.Call(func=func, args=args, keywords=[])

    def visit_Call(self, node):
        # test case is if check is .check
        if isinstance(node.func, ast.Attribute):
            return node
        elif node.func.id == 'check':
            return self.node_constructor(node)
        else:
            return node


def execute_notebook(nb_path):
    """Execute a notebook under grading conditions"""
    graded_nb_path = os.path.splitext(nb_path)[0] + '-graded.ipynb'

    # read in input notebook and check the source for shenanigans
    nb = nbformat.read(nb_path, as_version=4)
    source = ""
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue

        isp = IPythonInputSplitter(line_input_checker=False)
        cell_source = isp.transform_cell(cell.source)
        source += cell_source

    tree = ast.parse(source)
    print(source)
    # no points for you if you try and cheat
    # XXX add a check for people importing a function called `check`
    if find_check_assignment(tree) or find_check_definition(tree):
        return

    # run the notebook
    pm.execute_notebook(nb_path, graded_nb_path)

    graded_nb = nbformat.read(graded_nb_path, as_version=4)
    return graded_nb


def execute_notebook2(nb, secret='secret', initial_env=None,
                      ignore_errors=False):
    """Execute notebook & return the global environment that results from execution.

    If ignore_errors is True, exceptions are swallowed.

    nb is passed in as a dictionary that's a parsed ipynb file
    """
    results_name = 'check_results_%s' % secret
    if initial_env:
        global_env = initial_env.copy()
    else:
        global_env = {}

    global_env[results_name] = []

    source = ""
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            # transform the input to executable Python
            # FIXME: use appropriate IPython functions here
            isp = IPythonInputSplitter(line_input_checker=False)
            cell_source = isp.transform_cell(''.join(cell['source']))
            #exec(cell_source, global_env)
            source += cell_source

    tree = ast.parse(source)
    print(source)
    # no points for you if you try and cheat
    if find_check_assignment(tree) or find_check_definition(tree):
        return global_env

    # wrap check(..) calls into a check_results_X.append(check(..))
    transformer = CheckCallWrapper(secret)
    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)

    cleaned_source = compile(tree, filename="nb-ast", mode="exec")

    with hide_outputs():
        try:
            with open('/dev/null', 'w') as f, redirect_stdout(f), redirect_stderr(f):
                exec(cleaned_source, global_env)
        except:
            if not ignore_errors:
                raise
    return global_env


def _global_anywhere(varname):
    """
    Return global with given name in any frame in the call stack

    Throws NameError if no such global exists anywhere in the call stack
    """
    # This should not be a recursive function, since that modifies the stack!
    cur_frame = inspect.currentframe().f_back
    while cur_frame is not None:
        if varname in cur_frame.f_globals:
            return cur_frame.f_globals[varname]
        cur_frame = cur_frame.f_back
    raise NameError(f'{varname} not found in any globals in the stack')
