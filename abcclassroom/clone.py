"""
abc-classroom.clone
======================

"""

import csv
from pathlib import Path

from os.path import isdir, join

from . import config as cf
from . import github
from . import utils


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
        github.pull_from_github(destination_dir)
    else:
        github.clone_repo(organization, repo, clone_dir)


def clone_student_repos(args):
    """Iterates through the student roster, clones each repo for this
    assignment into the directory specified in the config, and then copies the
    notebook files into the 'course_materials/submitted' directory, based on
    course_materials set in config.yml."""

    assignment_name = args.assignment
    skip_existing = args.skip_existing

    print("Loading configuration from config.yml")
    config = cf.get_config()
    roster_filename = cf.get_config_option(config, "roster", True)
    course_dir = cf.get_config_option(config, "course_directory", True)
    clone_dir = cf.get_config_option(config, "clone_dir", True)
    organization = cf.get_config_option(config, "organization", True)
    materials_dir = cf.get_config_option(config, "course_materials", False)

    if materials_dir is None:
        print(
            "No course_materials directory set in config.yml. Will clone "
            "repositories but will not copy any assignment files."
        )
    try:
        # Create the assignment subdirectory path and ensure it exists
        Path(course_dir, clone_dir, assignment_name).mkdir(exist_ok=True)
        missing = []
        with open(roster_filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                student = row["github_username"]
                # expected columns: identifier,github_username,github_id,name
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


def include_patterns(patterns):
    """Factory function that can be used with copytree() ignore parameter.

    Arguments define a sequence of glob-style patterns
    that are used to specify what files to NOT ignore.
    Creates and returns a function that determines this for each directory
    in the file hierarchy rooted at the source directory when used with
    shutil.copytree().

    Parameters
    -----------
    patterns: list
        List of strings file extensions to be copied. Should be a string of
        what it's expected the file name will end in.
    """

    # We might want to move this to utils, as it is a helper for copytree

    def _ignore_patterns(path, names):
        keep = set(
            name
            for pattern in patterns
            for name in names
            if name.endswith(pattern)
        )
        ignore = set(
            name
            for name in names
            if name not in keep and not isdir(join(path, name))
        )
        return ignore

    return _ignore_patterns


def copy_assignment_files(
    config, student, assignment_name, copy_file_types=[".py", ".ipynb"]
):
    """Copies all notebook files from clone_dir to course_materials/submitted.
    Will overwrite any existing files with the same name.

    Parameters
    -----------
    config: dict
        config file returned as a dictionary from get_config()
    student: string
        Name of the student who's files are being copied
    assignment_name: string
        Name of the assignment for which files are being copied
    copy_file_types: list
        List of strings file extensions to be copied. Should be a string of
        what it's expected the file name will end in.

    """
    course_dir = cf.get_config_option(config, "course_directory", True)
    materials_dir = cf.get_config_option(config, "course_materials", False)
    clone_dir = cf.get_config_option(config, "clone_dir", True)
    repo = "{}-{}".format(assignment_name, student)

    # Copy files from the cloned_dirs/assignment name directory

    source_dir = Path(course_dir, clone_dir, assignment_name, repo)
    destination = Path(
        course_dir, materials_dir, "submitted", student, assignment_name
    )
    destination.mkdir(parents=True, exist_ok=True)
    print("Copying files from {} to {}".format(Path(source_dir), destination))

    # Using the copytree function from util to make copying easier
    utils.copytree(
        source_dir, destination, ignore=include_patterns(copy_file_types)
    )
