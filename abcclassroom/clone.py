"""
abc-classroom.clone
======================

"""

import csv
from pathlib import Path

from . import config as cf
from . import github
from . import utils


def make_clone_dir(clone_dir, course_dir):
    """Checks that the clone_dir exists, and creates it if it does not."""

    abspath = Path(utils.get_abspath(clone_dir, course_dir))
    if abspath.is_dir():
        return
    else:
        abspath.mkdir()


def clone_or_update_repo(organization, repo, clone_dir, skip_existing):
    """
    Tries to clone the repository 'repo' from the organization. If the local
    repository already exists, pulls instead of cloning (unless the skip flag
    is set, in which case it does nothing).
    """
    destination_dir = Path(clone_dir, repo)
    if destination_dir.is_dir():
        # if path exists, then pull instead of clone (unless skip_existing)
        if skip_existing:
            print(
                "Local repo {} already exists; skipping".format(
                    destination_dir
                )
            )
            return
        github.pull_from_github(destination_dir)
    else:
        github.clone_repo(organization, repo, clone_dir)


def clone_student_repos(args):
    """Iterates through the student roster, clones each repo for this
    assignment into the directory specified in the config, and then copies the notebook files into the nbgrader 'submitted' directory."""

    assignment = args.assignment
    skip_existing = args.skip_existing

    print("Loading configuration from config.yml")
    config = cf.get_config()
    roster_filename = cf.get_config_option(config, "roster", True)
    course_dir = cf.get_config_option(config, "course_directory", True)
    clone_dir = cf.get_config_option(config, "clone_dir", True)
    organization = cf.get_config_option(config, "organization", True)

    try:
        make_clone_dir(clone_dir, course_dir)
        missing = []
        with open(roster_filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = row["github_username"]
                # expected columns are identifier,github_username,github_id,name
                repo = "{}-{}".format(assignment, student)
                try:
                    clone_or_update_repo(
                        organization, repo, clone_dir, skip_existing
                    )
                except RuntimeError as err:
                    missing.append(student)
        if len(missing) == 0:
            print("All successful; no missing repos")
        else:
            print("Missing repositories for these students: ", missing)

    except FileNotFoundError:
        print("Cannot find roster file".format(roster_filename))
