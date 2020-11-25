"""
abc-classroom.clone
======================

"""

import csv
from pathlib import Path
import shutil

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
    no_submitted = args.no_submitted

    clone_repos(assignment_name, skip_existing, no_submitted)


def clone_repos(assignment_name, skip_existing=False, no_submitted=True):
    """Iterates through the student roster, clones each repo for this
    assignment into the directory specified in the config, and then copies the
    notebook files into the 'course_materials/submitted' directory, based on
    course_materials set in config.yml.

    Parameters
    ----------
    assignment_name : string
        The name of the assignment to clone repos for
    skip_existing : boolean (default=False)
        Do not update files in repositories that have already been cloned.
    no_submitted : boolean (default = True)
        If true, moves assignment files from cloned repo to submitted
        directory for grading. If false files are not moved to submitted
        dir. This might be useful if you want to update the student clone
        but don't want to update the file that was parsed by the autograder

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
            "in your config.yml file. I will only clone all of the student"
            "repositories. I can not copy any assignment files to a "
            "course_materials directory given it does not exist."
        )

    try:
        # Create the assignment subdirectory path and ensure it exists
        Path(course_dir, clone_dir, assignment_name).mkdir(exist_ok=True)
        missing_repos = []
        missing_student_gh = []

        with open(roster_filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            try:
                for row in reader:
                    student = row["github_username"]
                    print(student)
                    # If there is no student gh name skip trying to clone
                    if not student:
                        missing_student_gh.append(row)
                    else:
                        # Expected columns: identifier,github_username,
                        # github_id,name
                        repo = "{}-{}".format(assignment_name, student)
                        try:
                            clone_or_update_repo(
                                organization,
                                repo,
                                Path(clone_dir, assignment_name),
                                skip_existing,
                            )
                            if materials_dir is not None and no_submitted:
                                copy_assignment_files(
                                    config, student, assignment_name
                                )
                                print(
                                    "Copying files to the:",
                                    materials_dir,
                                    "dir",
                                )
                            else:
                                print("Not copying files to submitted")
                        except RuntimeError:
                            missing_repos.append(repo)
            except KeyError as ke:
                raise KeyError(
                    "Oops! Please check your roster file to "
                    "ensure is has the correct "
                    "headers. {}".format(ke)
                )
        if len(missing_repos) == 0 and len(missing_student_gh) == 0:
            print("Great! All repos were successfully cloned!")
        else:
            # Two potential points of failure 1. github repo doesn't exist or
            # 2. missing gh username. Here the message is clear about what
            # is wrong
            if len(missing_repos) > 0:
                print("Could not clone or update the following repos: ")
                for r in missing_repos:
                    print(" {}".format(r))
            if len(missing_student_gh) > 0:
                print(
                    "Oops! The following students are missing github "
                    "usernames in the roster. Consider adding their username "
                    "to your roster.csv file or removing that entry from the "
                    "file altogether."
                )
                for astudent in missing_student_gh:
                    print(" {}".format(astudent))

    except FileNotFoundError as err:
        raise FileNotFoundError(
            "Cannot find roster file: {}".format(roster_filename)
        )
        print(err)


def copy_assignment_files(config, student, assignment_name):
    """Copies all notebook files from clone_dir to course_materials/submitted.
    Will overwrite any existing files with the same name.

    Parameters
    -----------
    config: dict
        config file returned as a dictionary from get_config()
    student: string
        Name of the student whose files are being copied
    assignment_name: string
        Name of the assignment for which files are being copied

    """
    course_dir = cf.get_config_option(config, "course_directory", True)
    materials_dir = cf.get_config_option(config, "course_materials", False)
    clone_dir = cf.get_config_option(config, "clone_dir", True)
    files_to_grade = cf.get_config_option(config, "files_to_grade", False)
    repo = "{}-{}".format(assignment_name, student)

    # Copy files from the cloned_dirs to submitted directory
    source_dir = Path(course_dir, clone_dir, assignment_name, repo)
    destination = Path(
        course_dir, materials_dir, "submitted", student, assignment_name
    )

    destination.mkdir(parents=True, exist_ok=True)
    print("Copying files from {} to {}".format(Path(source_dir), destination))

    # Only move files with extensions needed for grading
    # NOTE: if there is a notebook or script in a subdirectory shutil does not
    # handle the subdirectory - it spits the file back into the main dir.
    for a_file in Path(course_dir, clone_dir, assignment_name, repo).glob(
        r"**/*"
    ):
        # If files to grade is not populated then just move notebooks
        if not files_to_grade:
            files_to_grade = [".ipynb"]
        if a_file.suffix in files_to_grade:
            print("copying {} to {}".format(a_file, destination))
            shutil.copy(a_file, destination)

    # In this case, IF you have a graded html file that will get moved over
    # Using the copytree function from util to make copying easier
    # This also moves subdirectories by default
    # shutil.copytree(
    #     source_dir,
    #     destination,
    #     ignore=shutil.ignore_patterns(*ignore_files),
    #     dirs_exist_ok=True,
    # )
