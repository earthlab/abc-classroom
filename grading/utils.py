import sys
from contextlib import contextmanager
from IPython import get_ipython


def flush_inline_matplotlib_plots():
    """
    Flush matplotlib plots immediately, rather than asynchronously.
    Basically, the inline backend only shows the plot after the entire
    cell executes, which means we can't easily use a contextmanager to
    suppress displaying it. See https://github.com/jupyter-widgets/ipywidgets/issues/1181/
    and https://github.com/ipython/ipython/issues/10376 for more details. This
    function displays flushes any pending matplotlib plots if we are using
    the inline backend.

    Stolen from https://github.com/jupyter-widgets/ipywidgets/blob/4cc15e66d5e9e69dac8fc20d1eb1d7db825d7aa2/ipywidgets/widgets/interaction.py#L35
    """
    if 'matplotlib' not in sys.modules:
        # matplotlib hasn't been imported, nothing to do.
        return

    try:
        import matplotlib as mpl
        from ipykernel.pylab.backend_inline import flush_figures
    except ImportError:
        return

    if mpl.get_backend() == 'module://ipykernel.pylab.backend_inline':
        flush_figures()


@contextmanager
def hide_outputs():
    """
    Context manager for hiding outputs from display() calls.

    IPython handles matplotlib outputs specially, so those are supressed too.
    """
    ipy = get_ipython()
    if ipy is None:
        # Not running inside ipython!
        yield
        return
    old_formatters = ipy.display_formatter.formatters
    ipy.display_formatter.formatters = {}
    try:
        yield
    finally:
        flush_inline_matplotlib_plots()
        ipy.display_formatter.formatters = old_formatters
