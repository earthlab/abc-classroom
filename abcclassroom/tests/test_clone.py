# Tests for clone script

import pytest
import os
from pathlib import Path

import abcclassroom.clone as abcclone

# TODO - this should be a fixture
test_data = {
    "assignment": "assignment1",
    "students": ["bert", "alana"],
    "files": ["nb1.ipynb", "nb2.ipynb", "junk.csv"],
}

# We might have a version of this in conftest


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
        assignment_path = Path(tmp_path, clone_dir, assignment, repo_name)
        assignment_path.mkdir(parents=True, exist_ok=True)
        for f in files:
            Path(assignment_path, f).touch()


# TODO: Test that the correct message is returned when no course_materials dir
# exists in the config


def test_roster_missing(sample_course_structure, tmp_path):
    """Test that when the roster is missing things fail gracefully."""
    # config = sample_course_structure
    assignment_name = "test_assignment"

    with pytest.raises(FileNotFoundError, match="Cannot find roster file"):
        abcclone.clone_repos(assignment_name, skip_existing=False)


# TODO: Test what happens when the roster exists but has the incorrect format
def test_roster_wrong_format(sample_course_structure, tmp_path):
    """Test that when the roster is missing things fail gracefully."""

    course_name, config = sample_course_structure
    assignment_name = "test_assignment"
    # config = cf.get_config()
    path_to_course = Path(config["course_directory"])
    # Mess up the roster file
    path_to_course.joinpath("classroom_roster.csv").touch()

    # I'm not sure why this actually runs
    abcclone.clone_repos(assignment_name, skip_existing=False)
    print(path_to_course)
    print(os.listdir(path_to_course))
    print(config["roster"])


# test_clone_no_local_repo(default_config, tmp_path, monkeypatch):
# need to mock up github api object for this

# test_clone_local_repo_exists(default_config, tmp_path):
# need to mock up github api object for this
#     # when skip_existing is yes (default)
#     # when skip_existing is no


def test_copy_assignment_files(default_config, test_files):
    materials_dir = Path(
        default_config["course_directory"], default_config["course_materials"]
    )
    assignment = test_data["assignment"]
    students = test_data["students"]
    for s in students:
        abcclone.copy_assignment_files(default_config, s, assignment)

        assert Path(
            materials_dir, "submitted", s, assignment, "nb1.ipynb"
        ).exists()
        assert (
            Path(
                materials_dir, "submitted", s, assignment, "junk.csv"
            ).exists()
            is False
        )
