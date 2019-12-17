# Tests for clone script

import pytest
import os
from pathlib import Path

import abcclassroom.clone as abcclone
import abcclassroom.github as github

test_data = {
    "assignment": "assignment1",
    "students": ["bert"],
    "files": ["nb1.ipynb", "nb2.ipynb", "junk.csv"],
}


@pytest.fixture
def test_files(default_config, tmp_path):
    """
    Creates the directories for cloning student repos and for holding
    submitted material. Creates two notebook and one non-notebook files.
    """
    default_config["course_directory"] = tmp_path
    clone_dir = default_config["clone_dir"]
    assignment = test_data["assignment"]
    students = test_data["students"]
    files = test_data["files"]
    for s in students:
        repo_name = "{}-{}".format(assignment, s)
        assignment_path = Path(tmp_path, clone_dir, repo_name)
        assignment_path.mkdir(parents=True)
        for f in files:
            Path(assignment_path, f).touch()


# test_clone_no_local_repo(default_config, tmp_path, monkeypatch):
# need to mock up github api object for this

# test_clone_local_repo_exists(default_config, tmp_path):
# need to mock up github api object for this
#     # when skip_existing is yes (default)
#     # when skip_existing is no


def test_copy_assignment_files(default_config, test_files):
    nbgrader_dir = Path(
        default_config["course_directory"], default_config["nbgrader_dir"]
    )
    assignment = test_data["assignment"]
    students = test_data["students"]
    for s in students:
        abcclone.copy_assignment_files(default_config, s, assignment)

        assert Path(
            nbgrader_dir, "submitted", s, assignment, "nb1.ipynb"
        ).exists()
        assert (
            Path(nbgrader_dir, "submitted", s, assignment, "junk.csv").exists()
            == False
        )
