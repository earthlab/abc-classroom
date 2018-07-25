from contextlib import redirect_stderr, redirect_stdout
import inspect
from .utils import hide_outputs

try:
    from IPython.core.inputsplitter import IPythonInputSplitter
except ImportError:
    raise ImportError('IPython needs to be installed for notebook grading')


def execute_notebook(nb, initial_env=None, ignore_errors=False):
    """
    Execute notebook & return the global environment that results from execution.

    If ignore_errors is True, exceptions are swallowed.

    nb is passed in as a dictionary that's a parsed ipynb file
    """
    with hide_outputs():
        if initial_env:
            global_env = initial_env.copy()
        else:
            global_env = {}
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                # transform the input to executable Python
                # FIXME: use appropriate IPython functions here
                isp = IPythonInputSplitter(line_input_checker=False)
                source = isp.transform_cell(''.join(cell['source']))
                try:
                    with open('/dev/null', 'w') as f, redirect_stdout(f), redirect_stderr(f):
                        exec(source, global_env)
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
