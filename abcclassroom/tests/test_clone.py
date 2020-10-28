# Tests for clone script

import pytest
from pathlib import Path

import abcclassroom.clone as abcclone
import abcclassroom.config as cf

# TODO - this should be a fixture
test_data = {
    "assignment": "assignment1",
    "students": ["bert", "alana"],
    "files": ["nb1.ipynb", "nb2.ipynb", "script.py", "junk.csv"],
}

# TODO: We might have a version of this fixture in conftest


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

# TODO: Test what happens when a student is listed but not repo for that
#  student is found (so the gh username is missing or misspelled


def test_roster_missing(sample_course_structure, tmp_path):
    """Test that when the roster is missing things fail gracefully."""
    # config = sample_course_structure
    assignment_name = "test_assignment"

    with pytest.raises(FileNotFoundError, match="Cannot find roster file"):
        abcclone.clone_repos(assignment_name, skip_existing=False)


def test_roster_missing_github_name(sample_course_structure, capsys):
    """Test that when the roster is missing a student gh username."""

    course_name, config = sample_course_structure
    assignment_name = "test_assignment"

    path_to_course = Path(config["course_directory"])
    # Mess up the roster file
    roster_path = path_to_course.joinpath("classroom_roster.csv")
    roster_path.touch()
    roster_path.write_text(
        '"identifier","github_username","github_id","name" \n'
        '"student-id","","student-gh-id",'
        '"student-name1" \n "student-id","","",'
        '"student-name2"'
    )
    abcclone.clone_repos(assignment_name, skip_existing=False)

    captured = capsys.readouterr()
    expected_string = "Oops! The following students are missing github"
    assert expected_string in captured.out


def test_roster_wrong_format(sample_course_structure):
    """Test that when the roster is missing a correct header fail
    gracefully."""

    course_name, config = sample_course_structure
    assignment_name = "test_assignment"

    path_to_course = Path(config["course_directory"])
    # Mess up the roster file
    roster_path = path_to_course.joinpath("classroom_roster.csv")
    roster_path.touch()
    roster_path.write_text(
        '"identifier","githubb_username","github_id","name" \n'
        '"student-id","student-gh-name","student-gh-id",'
        '"student-name"'
    )

    with pytest.raises(KeyError, match="Oops! Please check your roster file"):
        abcclone.clone_repos(assignment_name, skip_existing=False)


# TODO: Test that when the roster is empty it fails gracefully

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

        good_files = ["nb1.ipynb", "nb2.ipynb", "script.py"]

        for file in good_files:
            assert Path(
                materials_dir, "submitted", s, assignment, file
            ).exists()
        assert (
            Path(
                materials_dir, "submitted", s, assignment, "junk.csv"
            ).exists()
            is False
        )


def test_copy_assignment_files_optional_files(
    default_config, test_files, tmp_path
):
    materials_dir = Path(
        default_config["course_directory"], default_config["course_materials"]
    )
    assignment = test_data["assignment"]
    students = test_data["students"]
    default_config["files_to_ignore"] = [
        ".DS_Store",
        ".ipynb_checkpoints",
        "junk.csv",
        "*.py",
    ]
    for s in students:
        abcclone.copy_assignment_files(default_config, s, assignment)

        good_files = ["nb1.ipynb", "nb2.ipynb"]

        for file in good_files:
            assert Path(
                materials_dir, "submitted", s, assignment, file
            ).exists()
        assert (
            Path(
                materials_dir, "submitted", s, assignment, "junk.csv"
            ).exists()
            is False
        )
