"""
Fixtures to set up basic directory structure, including config and
extra files, for tests.
"""

import os
from pathlib import Path

import pytest

from abcclassroom.quickstart import create_dir_struct
import abcclassroom.config as cf


@pytest.fixture
def test_data():
    """Creates a  course structure with student and file names to ensure
    consistent creation of elements in all fixtures"""
    test_data = {
        "assignment": "assignment1",
        "students": ["bert", "alana"],
        "files": [
            "nb1.ipynb",
            "nb2.ipynb",
            "script.py",
            "junk.csv",
            ".DS_Store",
        ],
    }
    return test_data


@pytest.fixture
def default_config():
    """
    A config dictionary with default values.
    """
    config = {
        "template_dir": "test_template",
        "course_materials": "nbgrader",
        "clone_dir": "cloned-repos",
        "files_to_ignore": [".DS_Store", ".ipynb_checkpoints", "junk.csv"],
        "files_to_grade": [".py", ".ipynb"],
    }
    return config


@pytest.fixture
def config_file(default_config, tmp_path):
    """Writes the config to a file in tmp_path"""
    cf.write_config(default_config, tmp_path)


@pytest.fixture
def sample_course_structure(tmp_path):
    """Creates the quickstart demo directory setup for testing"""
    course_name = "demo-course"
    # Run quickstart
    create_dir_struct(course_name, working_dir=tmp_path)
    # Get config and reset course path - for some reason if the path isn't
    # set here it grabs the config in abc-classroom (tim's old config)
    path_to_course = Path(tmp_path, course_name)
    config = cf.get_config(configpath=path_to_course)
    config["course_directory"] = path_to_course
    os.chdir(path_to_course)
    return course_name, config


@pytest.fixture
def course_structure_assignment(sample_course_structure, tmp_path, test_data):
    """Creates an assignment within the default course structure directory
    with several files including system files that we want to ignore."""
    course_name, config = sample_course_structure
    assignment_name = test_data["assignment"]
    release_path = Path(
        config["course_directory"],
        config["course_materials"],
        "release",
        assignment_name,
    )
    release_path.mkdir(parents=True)
    # Create all assignment files listed in the test_data fixture
    for a_file in test_data["files"]:
        release_path.joinpath(a_file).touch()
    return config, assignment_name, release_path


@pytest.fixture
def course_with_student_clones(
    course_structure_assignment, tmp_path, test_data
):
    """
    Creates the final piece of a typical course including student cloned
    repos for the assignment. Student names and list of files come
    from test_data fixture
    """
    config, assignment_name, release_path = course_structure_assignment

    clone_dir = config["clone_dir"]
    students = test_data["students"]
    # Loop through and create a clone repo for each student and add files
    for s in students:
        repo_name = "{}-{}".format(assignment_name, s)
        assignment_path = Path(
            config["course_directory"], clone_dir, assignment_name, repo_name
        )
        assignment_path.mkdir(parents=True, exist_ok=True)
        for f in test_data["files"]:
            Path(assignment_path, f).touch()
    return config, assignment_name, students
