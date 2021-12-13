import argparse

from argparse import ArgumentParser

from . import template
from . import feedback as fdback
from . import auth as abcauth
from . import git as abcgit

from .quickstart import create_dir_struct
from .clone import clone_student_repos
from .roster import create_roster


def quickstart():
    parser = ArgumentParser(description=create_dir_struct.__doc__)
    parser.add_argument(
        "course_name",
        nargs="?",
        default="course-directory",
        help="Name of course. Use dashes-rather-than spaces for your name.",
    )
    parser.add_argument(
        "-f",
        action="store_true",
        help="""Option to override the existing folder structure made by this
        function previously.""",
    )
    args = parser.parse_args()
    course_name = args.course_name
    create_dir_struct(course_name, args.f)


def init():
    """
    Setup git and GitHub credentials for later. 1. Make sure that there
    is a valid GitHub authentication yaml file, and if there isn't,
    create a valid file; 2. Check that ssh access to GitHub via git
    commands is working.
    """

    print("Step 1: Setting up GitHub API access")
    abcauth.check_or_generate_token()

    print(
        """Step 2: Checking ssh access to GitHub. If you have not
        connected before, you will see a message with an RSA fingerprint
        asking if you want to continue connecting. Enter yes.
        """
    )
    try:
        abcgit.check_git_ssh()
        print(
            """Running git commands that access GitHub via SSH seems to
        be configured correctly"""
        )
    except RuntimeError:
        pass


def clone():
    """
    Clone the student repositories for the assignment and (optionall) copies
    notebook files into the course_materials 'submitted' directory. Clones into
    the clone_dir directory, as specified in config.yml.

    Requires that you have filename of student roster
    defined in config.yml and that the roster file exists.

    By default, if a local directory with the name of the repo already exists,
    pulls from github to update. Use the --skip-existing flag if you don't want
    to update existing repos.
    """
    parser = argparse.ArgumentParser(description=clone.__doc__)
    parser.add_argument(
        "assignment",
        help="""Name of assignment. Must match assignment name in
        course_materials directories""",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="""Do not attempt to update repositories that have already been
        cloned.""",
    )
    parser.add_argument(
        "--no-submitted",
        action="store_false",
        help="""Skip moving files from cloned repo to submitted.""",
    )
    args = parser.parse_args()

    clone_student_repos(args)


def feedback():
    """
    Copies feedback reports to local student repositories and (optionally)
    pushes to github. Assumes files are in the directory
    course_materials/feedback/student/assignment. Copies all files in the
    source directory.
    """
    parser = argparse.ArgumentParser(description=feedback.__doc__)
    parser.add_argument(
        "assignment",
        help="""Name of assignment. Must match name in course_materials
        feedback directory""",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="""Also pushes files to student repositories on GitHub
        (default = False; only copies files to local repos)""",
    )
    parser.add_argument(
        "--scrub",
        action="store_true",
        help="""Cleans out hidden tests from notebooks when used.""",
    )
    args = parser.parse_args()
    fdback.copy_feedback(args)


def new_template():
    """
    Create a new assignment template repository: creates local directory,
    copy / create required files, intialize as git repo, and (optionally)
    create remote repo on GitHub and push local repo to GitHub. Will open
    git editor to ask for commit message if custom message requested.
    """
    parser = argparse.ArgumentParser(description=new_template.__doc__)
    parser.add_argument(
        "assignment",
        help="""Name of assignment. Must match name in
        course_materials/release directory""",
    )
    parser.add_argument(
        "--custom-message",
        action="store_true",
        help="""Use a custom commit message for git. Will open the default
        git text editor for entry (if not set, uses default message 'Initial
        commit').""",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="""Also perform the GitHub operations (create remote repo on
        GitHub and push to remote (by default, only does local repository
        setup)""",
    )
    parser.add_argument(
        "--mode",
        choices=["delete", "fail", "merge"],
        default="fail",
        help="""Action if template directory already exists. Choices are:
        delete = delete contents before proceeding (except .git directory);
        merge = keep existing dir, overwrite existing files, add new files
        (Default = fail).""",
    )
    args = parser.parse_args()

    template.new_update_template(args)


def roster():
    """Given a csv file containing a roster downloaded from Github
    Classroom, creates new roster for use by nbgrader.
    Two operations:
    1. Adds an `id` column that contains the github username.
    2. Attempts to split the `name` column into two new columns,
    first_name and last_name.
    Saves the new file in the course_materials directory using the
    filename `nbgrader_roster.csv` unless you specify an alternate name.
    Fails if output file already exists.
    """
    parser = argparse.ArgumentParser(description=roster.__doc__)
    parser.add_argument(
        "github_roster",
        help="""A csv file in the format downloaded from GitHub Classroom.
        Must contain github_username column.""",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        default="nbgrader_roster.csv",
        help="""The name of the new roster file. Default is
        nbgrader_roster.csv. Created in the course_materials directory,
        as defined in config.yml""",
    )
    parser.add_argument(
        "-n",
        "--namecolumn",
        default="name",
        help="""The column to split to make the new columns
        first_name and last_name. Default is 'name'.""",
    )
    args = parser.parse_args()
    create_roster(args.github_roster, args.outfile, args.namecolumn)


def update_template():
    """
    Updates an existing assignment template repository: update / add new and
    changed files, then push local changes to GitHub. Will open git editor
    to ask for commit message.
    """
    parser = argparse.ArgumentParser(description=update_template.__doc__)
    parser.add_argument(
        "assignment",
        help="""Name of assignment. Must match name in course_materials/release
        directory""",
    )
    parser.add_argument(
        "--mode",
        choices=["delete", "merge"],
        default="merge",
        help="""What to do with existing contents of template directory.
        Choices are: delete = remove contents before proceeding (leaving .git
        directory); merge = overwrite existing files add new files
        (Default = merge).""",
    )
    args = parser.parse_args()
    # now set the additional args (so that it matches the keys in add_template
    # and we can use the same implementation methods)
    setattr(args, "github", True)
    setattr(args, "custom_message", True)
    template.new_update_template(args)
