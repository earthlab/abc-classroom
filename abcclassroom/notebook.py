"""
abc-classroom.notebook
======================

"""

import ast
import os

import nbformat
import papermill as pm

from nbclean import NotebookCleaner

from .utils import chdir


try:
    from IPython.core.inputsplitter import IPythonInputSplitter
except ImportError:
    raise ImportError("IPython needs to be installed for notebook grading")


def normalize_kernel_name(notebook):
    nb = nbformat.read(notebook, as_version=4)

    kernelspec = nb.metadata.kernelspec
    if "[conda env:" in kernelspec.display_name:
        if kernelspec.language == "python":
            if nb.metadata.language_info.version.startswith("3."):
                kernelspec.name = "python3"
                kernelspec.display_name = "Python 3"
            else:
                kernelspec.name = "python2"
                kernelspec.display_name = "Python 2"

        nbformat.write(nb, notebook)


def split_notebook(notebook, student_path, autograder_path):
    """Split a master notebook into student and autograder notebooks"""
    print("Processing", notebook)

    _, nb_name = os.path.split(notebook)
    base_name, extension = os.path.splitext(nb_name)

    # create test files and notebook for the student
    nb = NotebookCleaner(notebook)
    nb.create_tests(
        tag="private", oktest_path=base_name, base_dir=autograder_path
    )
    nb.create_tests(tag="public", oktest_path=base_name, base_dir=student_path)
    text_replace_begin = "### BEGIN SOLUTION"
    text_replace_end = "### END SOLUTION"
    nb.replace_text(text_replace_begin, text_replace_end)

    nb.save(os.path.join(student_path, nb_name))
    normalize_kernel_name(os.path.join(student_path, nb_name))

    # create test files for the autograder
    nb = NotebookCleaner(notebook)
    nb.create_tests(
        tag="private", oktest_path=base_name, base_dir=autograder_path
    )
    nb.create_tests(
        tag="public", oktest_path=base_name, base_dir=autograder_path
    )


def find_check_definition(tree):
    """Walk an AST and check for definitions of a function called `check`

    Return True if one is found, False otherwise.
    """
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.FunctionDef):
            continue
        if stmt.name == "check":
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
        if "check" in target_names:
            return True
    return False


def execute_notebook(nb_path):
    """Execute a notebook under grading conditions"""
    graded_nb_path = os.path.splitext(nb_path)[0] + "-graded.ipynb"
    nb_directory = os.path.split(nb_path)[0]

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

    # no points for you if you try and cheat
    # XXX add a check for people importing a function called `check`
    if find_check_assignment(tree) or find_check_definition(tree):
        return

    # run the notebook
    with chdir(nb_directory):
        pm.execute_notebook(nb_path, graded_nb_path)

    graded_nb = nbformat.read(graded_nb_path, as_version=4)
    return graded_nb
