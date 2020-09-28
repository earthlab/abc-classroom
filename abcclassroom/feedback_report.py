"""
abc-classroom.feedback-report
==============================

"""

import subprocess
from pathlib import Path
import csv

import nbclean
import nbformat as nf

from . import config as cf


def remove_notebook_test_cells(nb):
    """
    Clean the notebook's hidden cells using tags.

    Parameters
    ----------
        nb: A string or notebook node as read in by nbformat.

    Return
    ------
        The notebook with any cells tagged with 'hide'
        removed.
    """

    cleaner = nbclean.NotebookCleaner(nb)
    cleaner.clear(kind="content", tag="hide")

    # Scrub all hidden tests from the notebook
    text_replace_begin = "### BEGIN HIDDEN TESTS"
    text_replace_end = "### END HIDDEN TESTS"
    cleaner.replace_text(text_replace_begin, text_replace_end)

    return cleaner.ntbk


# Create a function that opens a notebook from a specific dir, cleans it
# Saves the cleaned notebook to some place and moves the html to another place


def creat_clean_report(assignment_name):
    """This function will take a notebook from a dir structure as follows:
    dir/student-name/assignment-name/file-names.ipynb It will then open the
    file,
    clean and save the output as file-name-cleaned.ipynb.

    Important: this assumes that we are cleaning jupyter notebooks. This will
    not work on any other file format for feedback!!

    For the time being I will save the cleaned notebook to a tmp dir that
    will then be deleted once the html is created."""

    # TODO: I think we do this a bunch so is it worth a helper for it
    config = cf.get_config()
    roster_filename = cf.get_config_option(config, "roster", True)
    course_dir = cf.get_config_option(config, "course_directory", True)
    materials_dir = cf.get_config_option(config, "course_materials", True)

    # This code was taken from the feedback.py module. It should become a
    # helper potentially if we end up using it.
    try:
        # This assumes the feedback directory exists. but we should test that
        # it exists
        autograded_dir = Path(course_dir, materials_dir, "autograded")
        with open(roster_filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = row["github_username"]

                # Create path to autograded directory
                path_to_notebooks = Path(
                    autograded_dir, student, assignment_name
                )
                graded_notebooks = path_to_notebooks.glob("*.ipynb")
                print(path_to_notebooks)
                # Iterate through each source file notebook
                for anotebook in graded_notebooks:
                    print("Cleaning answers from:", anotebook)
                    # Open & clean the notebook
                    # I'm not sure if nbclean supports a posixpath object?
                    # We could convert this to a string but for now coding it
                    # all out so it works
                    ntbk = nf.read(anotebook, nf.NO_CONVERT)
                    ntbk_cleaned = remove_notebook_test_cells(ntbk)

                    # Write the cleaned file
                    # Create a temp cleaned file name:
                    temp_cleaned_notebook = Path(
                        anotebook.parents[0], "graded_" + anotebook.name
                    )

                    nf.write(nb=ntbk_cleaned, fp=temp_cleaned_notebook)

                    # Move to feedback directory
                    # Create path to feedback dir
                    # This is a hack - but it's not super intuititve to just
                    # manipulate the path as it's a posix object. you have to
                    # use .parents. i 'm sure we can do better however at
                    # manipulating these paths as all w have to do is replace
                    # autograded with feedback in this case!
                    feedback_dir_path = Path(
                        course_dir,
                        materials_dir,
                        "feedback",
                        student,
                        assignment_name,
                    )
                    # This probably should make the directory
                    if not feedback_dir_path.is_dir():
                        print(
                            "Making feedback directory for student: {}"
                            " ".format(student)
                        )
                    # Finally write the notebook out to html
                    # Need to look into this bu ti had to install
                    # install -c conda-forge jupyter_contrib_nbextensions
                    subprocess.call(
                        [
                            "jupyter",
                            "nbconvert",
                            "--to",
                            "html",
                            temp_cleaned_notebook,
                        ]
                    )

    except FileNotFoundError as err:
        print("Oops  - something went wrong - not sure what  tho just yet:")
        print(" ", err)
