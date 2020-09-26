"""
abc-classroom.feedback
======================

"""

from pathlib import Path
import csv
import shutil

from . import config as cf
from . import github


def copy_feedback(args):
    """
    Copies feedback reports to local student repositories, commits the changes,
    and (optionally) pushes to github.
    Assumes feedback files are in the directory
    course_materials/feedback/student/assignment following a typical
    nbgrader structure. Copies all files in the source directory.
    """
    assignment_name = args.assignment
    do_github = args.github

    print("Loading configuration from config.yml")
    config = cf.get_config()

    # get various paths from config
    roster_filename = cf.get_config_option(config, "roster", True)
    course_dir = cf.get_config_option(config, "course_directory", True)
    clone_dir = cf.get_config_option(config, "clone_dir", True)
    materials_dir = cf.get_config_option(config, "course_materials", True)

    try:
        feedback_dir = Path(course_dir, materials_dir, "feedback")
        with open(roster_filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = row["github_username"]
                source_files = Path(
                    feedback_dir, student, assignment_name
                ).glob("*")
                repo_name = "{}-{}".format(assignment_name, student)
                # The repos now live in clone_dir/assignment-name/repo-name
                destination_dir = Path(clone_dir, assignment_name, repo_name)
                if not destination_dir.is_dir():
                    print(
                        "Local student repository {} does not exist; skipping "
                        "student".format(destination_dir)
                    )
                    continue
                for f in source_files:
                    print(
                        "Copying {} to {}".format(
                            f.relative_to(course_dir), destination_dir
                        )
                    )
                    shutil.copy(f, destination_dir)
                github.commit_all_changes(
                    destination_dir,
                    msg="Adding feedback for assignment {}".format(
                        assignment_name
                    ),
                )
                if do_github:
                    github.push_to_github(destination_dir)

    except FileNotFoundError as err:
        print("Missing file or directory:")
        print(" ", err)
