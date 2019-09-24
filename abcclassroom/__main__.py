import argparse
import datetime
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import os.path as op

from getpass import getpass

import github3 as gh3

from ruamel.yaml import YAML

import nbformat

from . import ok
from .distribute import find_notebooks, render_circleci_template
from .notebook import split_notebook
from . import github as GH
from .utils import copytree, P, input_editor


def get_github_auth():
    """
    Check to see if there is an existing github authentication
    and load the authentication.

    Returns
    -------
    ruamel.yaml.comments.CommentedMap
        Yaml object that contains the token and id for a github session.
        If yaml doesn't exists, return an empty dictionary.
    """
    yaml = YAML()
    try:
        with open(op.expanduser("~/.abc-classroom.tokens.yml")) as f:
            config = yaml.load(f)
        return config["github"]

    except FileNotFoundError:
        return {}


def set_github_auth(auth_info):
    """
    Set the github authentication information. Put the token and id authentication
    information into a yaml file if it doesn't already exist.

    Parameters
    ----------
    auth_info : dictionary
        The token and id authentication information from github stored in a
        dictionary object.
    """
    yaml = YAML()
    config = {}
    if get_github_auth():
        with open(op.expanduser("~/.abc-classroom.tokens.yml")) as f:
            config = yaml.load(f)

    config["github"] = auth_info

    with open(op.expanduser("~/.abc-classroom.tokens.yml"), "w") as f:
        yaml.dump(config, f)


def get_config():
    yaml = YAML()
    with open(P("config.yml")) as f:
        config = yaml.load(f)
    return config


def set_config(config):
    yaml = YAML()
    with open(P("config.yml"), "w") as f:
        yaml.dump(config, f)


def init():
    """
    Setup GitHub credentials for later. Make sure that there is a valid GitHub authentication
    yaml file, and if there isn't one, create a valid file.
    """

    gh_auth = get_github_auth()

    # check the token we have is still valid by attempting to login with
    # the token we have if this fails we need a new one
    if gh_auth.get("token") is not None:
        try:
            # We have to use the GitHub API to find out if our login
            # credentials actually work, this is why we call `me()`
            gh = gh3.login(token=gh_auth["token"])
            gh.me()
            print("GitHub token present and valid.")
            return

        except gh3.exceptions.AuthenticationFailed:
            # need to get a new token
            pass

    print("GitHub token is missing or expired. Populating")
    user = input("GitHub username: ")
    password = ""

    while not password:
        password = getpass("Password for {0}: ".format(user))

    note = "ABC-classroom workflow helper"
    note_url = "https://github.com/earthlab/abc-classroom"
    scopes = ["repo", "read:user"]

    def two_factor():
        code = ""
        while not code:
            # The user could accidentally press Enter before being ready,
            # let's protect them from doing that.
            code = input("Enter 2FA code: ")
        return code

    gh = gh3.github.GitHub()
    gh.login(username=user, password=password, two_factor_callback=two_factor)
    try:
        auth = gh.authorize(user, password, scopes, note, note_url)

        set_github_auth({"token": auth.token, "id": auth.id})

    except gh3.exceptions.UnprocessableEntity:
        print(
            "Failed to create a access token for you. Please visit "
            "https://github.com/settings/tokens and delete any access "
            "token with the name 'ABC-classroom workflow helper' and run "
            "`abc-init` again."
        )
        sys.exit(1)


def grade():
    """Grade student's work"""
    parser = argparse.ArgumentParser(description="Grade student repository.")
    parser.add_argument(
        "--date",
        default=datetime.datetime.today().date(),
        type=valid_date,
        help=("Assumed date when grading assignments " "(default: today)"),
    )
    parser.add_argument(
        "--student",
        default=None,
        action="append",
        help=(
            "Student name to grade, use flag multiple times "
            "to select several students "
            "(default: all students)"
        ),
    )
    parser.add_argument(
        "--assignment",
        default=None,
        action="append",
        help=(
            "Assignment to grade, use flag multiple times "
            "to select several assignments "
            "(default: all assignments)"
        ),
    )
    args = parser.parse_args()

    now = args.date

    config = get_config()
    course = config["courseName"]

    if args.student is None:
        students = config["students"]
    else:
        students = args.student

    if args.assignment is None:
        assignments = config["assignments"]
    else:
        assignments = args.assignment

    for student in students:
        print("Fetching work for %s..." % student)
        cwd = P("graded", student)

        # always delete and recreate student's directories
        if os.path.exists(cwd):
            shutil.rmtree(cwd)
        os.makedirs(cwd)

        # Use HTTPS and tokens to avoid access problems
        # `git clone https://<token>@github.com/owner/repo.git`
        fetch_command = [
            "git",
            "clone",
            "https://{}@github.com/{}/{}-{}.git".format(
                get_github_auth()["token"],
                config["organisation"],
                course,
                student,
            ),
            student,
        ]
        try:
            subprocess.run(
                fetch_command,
                cwd=P("graded"),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as err:
            print("Fetching work with '%s' failed:" % " ".join(fetch_command))
            print()
            print(err.stderr.decode("utf-8"))
            print()
            print("Skipping this student.")
            continue

        print("Grading work...")
        for assignment in assignments:
            # only grade assignments that are due or have been explicitly
            # requested by command-line flag
            deadline_date = config["assignments"][assignment]["deadline"]
            if deadline_date > now and args.assignment is None:
                print('Skipping assignment "{}".'.format(assignment))

            # remove check files so we only use a clean copy from this repo
            # instead of trusting students
            for notebook in glob.glob(
                P("graded", student, "%s/*.ipynb" % assignment)
            ):
                print("Grading {}".format(notebook))
                notebook = op.split(notebook)[-1]

                tests_path = P(
                    "graded", student, assignment, op.splitext(notebook)[0]
                )
                if os.path.exists(tests_path):
                    shutil.rmtree(tests_path)

                autograder_path = P(
                    "autograder", assignment, op.splitext(notebook)[0]
                )
                copytree(autograder_path, tests_path)

                results = ok.grade_notebook(
                    P("graded", student, assignment, notebook)
                )

                print("Points:")
                for res in results:
                    print(res)

            print(
                "🎉 Top marks for {} on assignment {}.".format(
                    student, assignment
                )
            )
        print()


def distribute():
    """Create or update student repositories"""
    parser = argparse.ArgumentParser(description="Distribute work to students")
    parser.add_argument(
        "--template",
        action="store_true",
        help="Create template repository only (default: False)",
    )
    args = parser.parse_args()

    student_repo_template = P("student")

    print("Using %s to create the student template." % student_repo_template)
    print("Loading configuration from config.yml")

    config = get_config()

    if args.template:
        print("Creating template repository.")
        repo_name = "{}-{}".format(config["courseName"], "template")
        with tempfile.TemporaryDirectory() as d:
            copytree(P("student"), d)
            GH.git_init(d)
            GH.commit_all_changes(d, "Initial commit")
            try:
                GH.create_repo(
                    config["organisation"],
                    repo_name,
                    d,
                    get_github_auth()["token"],
                )
            except gh3.exceptions.UnprocessableEntity as e:
                print(e.msg)
                print(
                    "This is probably because the template repository "
                    "already exists."
                )

        print(
            "Visit https://github.com/{}/{}".format(
                config["organisation"], repo_name
            )
        )

    else:
        default_message = """
        # Please enter the commit message for your changes. Lines starting
        # with '#' will be ignored, and an empty message aborts the commit.
        # This message will be used as commit and Pull Request message."""
        message = input_editor(default_message)
        message = "\n".join(
            [
                line
                for line in message.split("\n")
                if not line.strip().startswith("#")
            ]
        )

        if not message:
            print("Empty commit message, exiting.")
            sys.exit(1)

        for student in config["students"]:
            print("Fetching work for %s..." % student)

            try:
                GH.check_student_repo_exists(
                    config["organisation"],
                    config["courseName"],
                    student,
                    token=get_github_auth()["token"],
                )
            except gh3.exceptions.NotFoundError as e:
                print(
                    "Student {} does not have a repository for this "
                    "course, maybe they have not accepted the invitation "
                    "yet? Skipping them for now.".format(student)
                )
                continue

            with tempfile.TemporaryDirectory() as d:
                student_dir = GH.fetch_student(
                    config["organisation"],
                    config["courseName"],
                    student,
                    directory=d,
                    token=get_github_auth()["token"],
                )
                # Copy assignment related files to the template repository
                copytree(P("student"), student_dir)

                if GH.repo_changed(student_dir):
                    # only close outstanding PRs if we are about to make a
                    # new PR. Otherwise we can skip this.
                    repo = "{}-{}".format(config["courseName"], student)
                    GH.close_existing_pullrequests(
                        config["organisation"],
                        repo,
                        token=get_github_auth()["token"],
                    )

                    branch = GH.new_branch(student_dir)

                    GH.commit_all_changes(student_dir, message)
                    GH.push_to_github(student_dir, branch)
                    GH.create_pr(
                        config["organisation"],
                        repo,
                        branch,
                        message,
                        get_github_auth()["token"],
                    )

                else:
                    print("Everything up to date.")


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def author():
    """Create student repository and autograding tests"""
    parser = argparse.ArgumentParser(description="Author student repository.")
    parser.add_argument(
        "--date",
        default=datetime.datetime.today().date(),
        type=valid_date,
        help=("Assumed date when preparing assignments " "(default: today)"),
    )
    args = parser.parse_args()

    config = get_config()
    now = args.date

    if os.path.exists(P("student")):
        shutil.rmtree(P("student"))
    os.makedirs(P("student"))

    if os.path.exists(P("autograder")):
        shutil.rmtree(P("autograder"))

    for assignment in config["assignments"]:
        release_date = config["assignments"][assignment]["release"]
        if release_date > now:
            continue

        student_path = P("student", assignment)
        master_path = P("master", assignment)

        if not os.path.isdir(master_path):
            print(
                "Error: There is no material in '{}' for "
                "assignment '{}'".format(master_path, assignment)
            )
            sys.exit(1)

        # copy over everything, including master notebooks. They will be
        # overwritten by split_notebook() below
        shutil.copytree(master_path, student_path)

        if os.path.exists(P("student", assignment, ".ipynb_checkpoints")):
            shutil.rmtree(P("student", assignment, ".ipynb_checkpoints"))

        for notebook in glob.glob(P("master/%s/*.ipynb" % assignment)):
            split_notebook(notebook, student_path, P("autograder", assignment))

    # Create additional files
    for target, source in config["extra_files"].items():
        shutil.copyfile(P(source), P("student", target))

    # Create the grading token file which is used by the notebook bot
    # to access the CircleCI build artefacts
    grading_token = P("student", ".grading.token")
    with open(grading_token, "w") as f:
        f.write(config["tokens"]["circleci"])

    # Create the required CircleCI configuration
    # the template only needs the basename, not the .ipynb extension
    notebook_paths = [f[:-6] for f in find_notebooks(P("student"))]
    circleci = render_circleci_template(notebook_paths)

    os.makedirs(P("student", ".circleci"))
    circleci_yml = P("student", ".circleci", "config.yml")
    with open(circleci_yml, "w") as f:
        f.write(circleci)

    print(
        "Inspect `{}/` to check it looks as you "
        "expect.".format(P("student"))
    )
