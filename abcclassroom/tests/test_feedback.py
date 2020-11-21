# Tests for feedback script

import pytest
from pathlib import Path

import abcclassroom.feedback as abcfeedback
import abcclassroom.github as github

test_data = {
    "assignment": "assignment1",
    "students": ["bert", "ernie"],
    "files": ["feedback.html", "anotherfile.txt"],
}


@pytest.fixture
def create_directories(default_config, tmp_path):
    """
    Creates the directories containing feedback reports and cloned student
    repos. Creates two feedback and one non-feedback files.
    """
    default_config["course_directory"] = tmp_path
    print(default_config)
    materials_dir = default_config["course_materials"]
    clone_dir = default_config["clone_dir"]
    assignment = test_data["assignment"]
    students = test_data["students"]
    files = test_data["files"]
    # create the feedback directory course_dir/materials_dir/feedback
    feedback_path = Path(tmp_path, materials_dir, "feedback").mkdir(
        parents=True
    )
    for f in files:
        Path(feedback_path, f).touch()

    # create the cloned student repos
    for s in students:
        repo_name = "{}-{}".format(assignment, s)
        repo_path = Path(tmp_path, clone_dir, repo_name)
        repo_path.mkdir(parents=True)
        github.init_and_commit(repo_path)


@pytest.fixture
def create_roster_file(default_config, tmp_path):
    """Create a student roster with the single github_username column"""
    default_config["roster"] = "roster.csv"
    with open("roster.csv") as rosterfile:
        rosterfile.write("github_username\n")
        for s in default_config["students"]:
            rosterfile.write("{}\n".format(s))


def test_copy_feedback_files(default_config, tmp_path, create_directories):
    "Tests that copying the feedback files copies both files"
    default_config["course_directory"] = tmp_path
    abcfeedback.copy_feedback_files(default_config)


#
#
# def test_git_commit(default_config, tmp_path):
#     "Tests that changes get commited ok"
# do_github_push = False
# need to create student repos list
# abcfeedback.git_commit_push(student_repos, do_github_push)
