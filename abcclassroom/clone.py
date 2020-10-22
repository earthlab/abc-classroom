"""
abc-classroom.clone
======================

"""

import csv
from pathlib import Path
from shutil import copy

from . import config as cf
from . import github as gh


def clone_or_update_repo(organization, repo, clone_dir, skip_existing):
    """
    Tries to clone the single repository 'repo' from the organization. If the
    local repository already exists, pulls instead of cloning (unless the
    skip flag is set, in which case it does nothing).

    Parameters
    ----------
    organization : string
        Organization where your GitHub classroom lives.
    repo : string
        Name of the student's GitHub repo.
    clone_dir : string
        Name of the clone directory.
    skip_existing : boolean
        True if you wish to skip copying files to existing repos.
    """
    destination_dir = Path(clone_dir, repo)
    if destination_dir.is_dir():
        # if path exists, pull instead of clone (unless skip_existing)
        if skip_existing:
            print(
                "Local repo {} already exists; skipping".format(
                    destination_dir
                )
            )
            return
        gh.pull_from_github(destination_dir)
    else:
        gh.clone_repo(organization, repo, clone_dir)


def clone_student_repos(args):
    """This is the CLI implementation of clone repos

    Parameters
    ----------
    args : string argument inputs
        Arguments include the assignment name (string) and skip existing (
        boolean?)

    """

    assignment_name = args.assignment
    skip_existing = args.skip_existing

    clone_repos(assignment_name, skip_existing)


def clone_repos(assignment_name, skip_existing):
    """Iterates through the student roster, clones each repo for this
    assignment into the directory specified in the config, and then copies the
    notebook files into the 'course_materials/submitted' directory, based on
    course_materials set in config.yml.

    Parameters
    ----------
    assignment_name : string
        The name of the assignment to clone repos for
    skip_existing : boolean
        Not sure what this does yet!

    Returns
    --------
    This returns the cloned student repos and also moves each notebook file
    into the nbgrader "submitted" directory.
    """

    print("Loading configuration from config.yml")
    config = cf.get_config()
    roster_filename = cf.get_config_option(config, "roster", True)
    course_dir = cf.get_config_option(config, "course_directory", True)
    clone_dir = cf.get_config_option(config, "clone_dir", True)
    organization = cf.get_config_option(config, "organization", True)
    materials_dir = cf.get_config_option(config, "course_materials", False)

    if materials_dir is None:
        print(
            "Oops! I couldn't find a course_materials directory location "
            "in your config.yml file. I will just clone all of the student"
            "repositories. I can't copy any assignment files to a "
            "course_materials directory."
        )
    # This is a really large try block and makes it hard to figure out where
    # things fail. perhaps break out into a few sub try / excepts?
    try:
        # Create the assignment subdirectory path and ensure it exists
        Path(course_dir, clone_dir, assignment_name).mkdir(exist_ok=True)
        missing = []
        # If it can't find the roster file you'll get a FileNotFoundError
        # Also what happens if the roster is not in the correct format??
        with open(roster_filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = row["github_username"]
                # Expected columns: identifier,github_username,github_id,name
                repo = "{}-{}".format(assignment_name, student)
                try:
                    clone_or_update_repo(
                        organization,
                        repo,
                        Path(clone_dir, assignment_name),
                        skip_existing,
                    )
                    if materials_dir is not None:
                        copy_assignment_files(config, student, assignment_name)
                except RuntimeError:
                    missing.append(repo)
        if len(missing) == 0:
            print("All successful; no missing repos")
        else:
            print("Could not clone or update the following repos: ")
            for r in missing:
                print(" {}".format(r))

    except FileNotFoundError as err:
        print("Cannot find roster file: {}".format(roster_filename))
        print(err)


def copy_assignment_files(config, student, assignment_name):
    """Copies all notebook files from clone_dir to course_materials/submitted.
    Will overwrite any existing files with the same name.

    Parameters
    -----------
    config: dict
        config file returned as a dictionary from get_config()
    student:
    assignment_name: string
        Name of the assignment for which files are being copied

    """
    course_dir = cf.get_config_option(config, "course_directory", True)
    materials_dir = cf.get_config_option(config, "course_materials", False)
    clone_dir = cf.get_config_option(config, "clone_dir", True)
    repo = "{}-{}".format(assignment_name, student)

    # Copy files from the cloned_dirs/assignment name directory
    # TODO - right now this ONLY copies notebooks but we may want to copy
    # other file types like .py files as well.
    files = Path(course_dir, clone_dir, assignment_name, repo).glob("*.ipynb")
    destination = Path(
        course_dir, materials_dir, "submitted", student, assignment_name
    )
    destination.mkdir(parents=True, exist_ok=True)
    print(
        "Copying files from {} to {}".format(
            Path(clone_dir, repo), destination
        )
    )
    # We are copying files here source: clone dir -> nbgrader submitted
    # TODO: use the copy files helper - in this case it's only copying .ipynb
    # files
    # but i could see someone wanting to copy other types of files such as .py
    # So it may make sense to implement a copy files helper here as well even
    # tho it's adding a bit of additional steps - it's still a very small
    # operation
    for f in files:
        print("copying {} to {}".format(f, destination))
        copy(f, destination)
