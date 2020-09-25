import subprocess

import nbclean
import nbformat as nf


def remove_notebook_test_cells(nb):

    """
    Clean the notebook's hidden cells using tags.

    Parameters
    ----------
        nb: A path to notebook instance as read in by nbformat.

    Return
    ------
        The notebook with any cells tagged with 'hide'
        removed.
    """

    cleaner = nbclean.NotebookCleaner(nb)
    cleaner.clear(kind="content", tag="hide")

    # Replace all hidden tests with nothing in the notebook
    text_replace_begin = "### BEGIN HIDDEN TESTS"
    text_replace_end = "### END HIDDEN TESTS"
    cleaner.replace_text(text_replace_begin, text_replace_end)

    return cleaner.ntbk


ntbk_path = "bootcamp-03-github.ipynb"
# Write the file
ntbk = nf.read(ntbk_path, nf.NO_CONVERT)
ntbk = remove_notebook_test_cells(ntbk)
nf.write(nb=ntbk, fp="notebook-test.ipynb")

# Finally write the notebook out to html
subprocess.call(
    ["jupyter", "nbconvert", "--to", "html", "notebook-test.ipynb"]
)


# os.chdir(
#     "/Users/leahwasser/github/1-bootcamp-course/delete-me/bootcamp-2020-03-github-adamancer"
# )
