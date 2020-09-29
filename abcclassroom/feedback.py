"""
abc-classroom.feedback
======================

"""

from pathlib import Path
import csv
import shutil
import sys

from . import config as cf
from . import github


def copy_feedback_files(
    assignment, roster_filename, course_dir, materials_dir, clone_dir
):
    """
    Copies feedback reports from materials directory to student repos,
    returning a list of the present student repositories.

    Parameters:
    -----------
    assignment : string
        The name of the assignment

    roster_filename : string
        The csv file containing the student roster

    course_dir : string
        The top-level directory for the course

    materials_dir : string
        The directory containing the course materials (the nbgrader directory,
        if you are using nbgrader)

    clone_dir : string
        The directory containing the cloned students repositories

    """

    feedback_dir = Path(course_dir, materials_dir, "feedback")
    print("Copying feedback files from {}".format(feedback_dir))
    student_repos = []
    with open(roster_filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                student = row["github_username"]
                source_files = Path(feedback_dir, student, assignment).glob(
                    "*"
                )
                repo = "{}-{}".format(assignment, student)
                destination_dir = Path(clone_dir, repo)
                if not destination_dir.is_dir():
                    print(
                        """Local student repository {} does not exist;
                        skipping student""".format(
                            destination_dir
                        )
                    )
                    continue
                student_repos.append(destination_dir)
                for f in source_files:
                    print(
                        "Copying {} to {}".format(
                            f.relative_to(course_dir), destination_dir
                        )
                    )
                    shutil.copy(f, destination_dir)
            except FileNotFoundError as err:
                print("Missing file or directory:")
                print(" ", err)
        # if we didn't find any repos, there is probably something wrong
        if len(student_repos) == 0:
            print(
                """No repositories found in {} for assignment {};
                exiting""".format(
                    clone_dir, assignment
                )
            )
            sys.exit(1)
        return student_repos


def git_commit_push(student_repos, do_github_push):
    """
    Commits and (optionally) pushes feedback reports.

    Parameters:
    -----------

    student_repos : list of Path objects
        The student repos that contain copied feedback files

    do_github_push : Boolean
        Whether or not to push to github

    """

    for repository in student_repos:
        try:
            repo_dir = repository.name
            pathparts = repo_dir.split("-")
            assignment = pathparts[0]
            student = pathparts[1]
            github.commit_all_changes(
                repository,
                msg="Adding feedback for assignment {}".format(assignment),
            )
        except RuntimeError as err:
            print("Error committing changes for {}".format(student))
            print(err)
        if do_github_push:
            github.push_to_github(repository)


def copy_feedback(args):
    """
    Copies feedback reports to local student repositories, commits the
    changes, and (optionally) pushes to github. Assumes files are in the
    directory course_materials/feedback/student/assignment. Copies all files
    in the source directory.
    """
    assignment = args.assignment
    do_github_push = args.github

    print("Loading configuration from config.yml")
    config = cf.get_config()

    # get various paths from config
    roster_filename = cf.get_config_option(config, "roster", True)
    course_dir = cf.get_config_option(config, "course_directory", True)
    clone_dir = cf.get_config_option(config, "clone_dir", True)
    materials_dir = cf.get_config_option(config, "course_materials", True)

    student_repos = copy_feedback_files(
        assignment, roster_filename, course_dir, materials_dir, clone_dir
    )
    git_commit_push(student_repos, do_github_push)
