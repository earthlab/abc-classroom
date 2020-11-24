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
def default_config():
    """
    A config dictionary with default values.
    """
    config = {
        "template_dir": "test_template",
        "course_materials": "nbgrader",
        "clone_dir": "cloned-repos",
        "files_to_ignore": [".DS_Store", ".ipynb_checkpoints", "junk.csv"],
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
    a_config = cf.get_config(configpath=path_to_course)
    a_config["course_directory"] = path_to_course
    os.chdir(path_to_course)
    return course_name, a_config


@pytest.fixture
def course_structure_assignment(sample_course_structure, tmp_path):
    """Creates an assignment within the default course structure directory
    with several files including system files that we want to ignore."""
    course_name, a_config = sample_course_structure
    assignment_name = "demo_assignment1"
    release_path = Path(
        tmp_path,
        course_name,
        a_config["course_materials"],
        "release",
        assignment_name,
    )
    release_path.mkdir(parents=True)
    release_path.joinpath("file1.txt").touch()
    release_path.joinpath("file2.ipynb").touch()
    release_path.joinpath(".DS_Store").touch()
    print(release_path)

    return a_config, assignment_name, release_path
