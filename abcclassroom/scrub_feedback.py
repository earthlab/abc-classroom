"""
abc-classroom.scrub-feedback
============================
"""

import re
import codecs

# This approach borrowed
# from https://github.com/jupyter/nbgrader/issues/1156#issuecomment-502097507


def scrub_feedback(html_path):
    """Scrub out hidden tests from nbgrader html feedback pages.

    We use this to remove hidden tests given all of the nbgrader grade
    information including comments are only stored in the DB. Therefore
    it is more work than expected to generate a nice custom report.

    This will remove all html between ### BEGIN HIDDEN TESTS and ### END
    HIDDEN TESTS. Because I think we sometimes only use one # sign i may add a
    second catch for this.

    Parameters
    ----------
    html_path : string
        Path to HTML file to be cleaned.

    Returns
    -------
    html-file: A cleaned html file without the hidden tests.
        The original file will be overwritten.
    """
    with codecs.open(file, 'r') as html_file:
        orig_html_feedback = html_file.read()

    # Hide hidden tests
    html_clean = re.sub(
        r'<span class="c1">### BEGIN HIDDEN TESTS<\/span>[\w\W]*?'
        r'<span class="c1">### END HIDDEN TESTS<\/span>',
        '',
        orig_html_feedback)
    # Just in case we use just one pound sign
    html_clean = re.sub(
        r'<span class="c1"># BEGIN HIDDEN TESTS<\/span>[\w\W]*?'
        r'<span class="c1"># END HIDDEN TESTS<\/span>',
        '',
        html_clean)

    # Not sure we will need this
    # Hide the traceback (which includes parts of the hidden tests)
    # html = re.sub(
    #     r'(<div class="output_subarea output_text output_error">\n<pre>\n)
    #     (?:(?!<\/div>)[\w\W])*(
    #     <span class="ansi-red-intense-fg ansi-bold">[\w\W]*?<\/pre>)',
    #     r'\1\2',
    #     orig_html_feedback)

    # Write the file - do I need a return?
    with open("new-graded-file.html", "w") as cleaned_html:
        cleaned_html.write(html_clean)


def clean_feedback_html():
    # Go through each html file in the feedback dir and run scrub_feedback


def clean_feedback(args):
    """if we need a cli - this might be better as a option for abc-feedback"""
    assignment_name = args.assignment
    clean_feedback_html(assignment_name)
