"""
abc-classroom.github
====================

"""

import os
import logging
import random
import string
import subprocess

import github3 as gh3

from .utils import input_editor


def _call_git(*args, directory=None):
    cmd = ["git"]
    cmd.extend(args)
    try:
        ret = subprocess.run(
            cmd,
            cwd=directory,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8")
        if err:
            msg = err.split(":")[1].strip()
        else:
            msg = e.stdout.decode("utf-8")
        raise RuntimeError(msg) from e

    return ret


def check_student_repo_exists(org, course, student, token=None):
    """Check if the student has a repository for the course.

    It happens that students delete their repository or do not accept the
    invitation to the course. In either case they will not have a repository
    yet.
    """
    # temporarily change log level of github3.py as it prints weird messages
    # XXX could be done more nicely with a context manager maybe
    gh3_log = logging.getLogger("github3")
    old_level = gh3_log.level
    gh3_log.setLevel("ERROR")

    try:
        g = gh3.login(token=token)
        repository = "{}-{}".format(course, student)
        g.repository(org, repository)

    except Exception as e:
        raise e

    finally:
        gh3_log.setLevel(old_level)


def fetch_student(org, course, student, directory, token=None):
    """Fetch course repository for `student` from `org`

    The repository will be cloned into a sub-directory in `directory`.

    Returns the directory in which to find the students work.
    """
    # use ssh if there is no token
    if token is None:
        fetch_command = [
            "git",
            "clone",
            "git@github.com:{}/{}-{}.git".format(org, course, student),
        ]
    else:
        fetch_command = [
            "git",
            "clone",
            "https://{}@github.com/{}/{}-{}.git".format(
                token, org, course, student
            ),
        ]
    subprocess.run(
        fetch_command,
        cwd=directory,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return os.path.join(directory, "{}-{}".format(course, student))


def close_existing_pullrequests(
    org, repository, branch_base="new-material-", token=None
):
    """Close all oustanding course material update Pull Requests

    If there are any PRs open in a student's repository that originate from
    a branch starting with `branch_base` as name and created by the user
    we are logged in we close them.
    """
    g = gh3.login(token=token)
    me = g.me()
    repo = g.repository(org, repository)
    for pr in repo.pull_requests(state="open"):
        origin = pr.head.label
        origin_repo, origin_branch = origin.split(":")
        if origin_branch.startswith(branch_base) and pr.user == me:
            pr.create_comment(
                "Closed in favor of a new Pull Request to "
                "bring you up-to-date."
            )
            pr.close()


def create_pr(org, repository, branch, message, token):
    """Create a Pull Request with changes from branch"""
    msg_parts = message.split("\n\n")
    if len(msg_parts) == 1:
        title = msg = msg_parts[0]
    else:
        title = msg_parts[0]
        msg = "\n\n".join(msg_parts[1:])

    g = gh3.login(token=token)
    repo = g.repository(org, repository)
    repo.create_pull(title, "master", branch, msg)


def create_repo(org, repository, directory, token):
    """Create a repository in the provided GitHub organization, adds that
    repo as a remote to the local repo in directory, and pushes the
    directory.
    """
    github_obj = gh3.login(token=token)
    organization = github_obj.organization(org)
    print(
        "Creating new repository {} at https://github.com/{}".format(
            repository, org
        )
    )
    try:
        organization.create_repository(repository)
    except gh3.exceptions.UnprocessableEntity as err:
        print(
            "Error: organization {} already has a repository named {}".format(
                org, repository
            )
        )
        print("Not adding remote to local repo or pushing to github.")
        return

    _call_git(
        "remote",
        "add",
        "origin",
        "https://{}@github.com/{}/{}".format(token, org, repository),
        directory=directory,
    )
    push_to_github(directory, "master")


def repo_changed(directory):
    """Determine if the Git repository in directory is dirty"""
    ret = _call_git("status", "--porcelain", directory=directory)
    return bool(ret.stdout)


def new_branch(directory, name=None):
    """Create a new git branch in directory"""
    if name is None:
        postfix = "".join(
            [random.choice(string.ascii_letters) for n in range(4)]
        )
        name = "new-material-{}".format(postfix)

    _call_git("checkout", "-b", name, directory=directory)

    return name


def get_commit_message():
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
    return message


def commit_all_changes(directory, msg=None):
    if msg is None:
        raise ValueError("Commit message can not be empty.")

    _call_git("add", "*", directory=directory)
    _call_git("commit", "-a", "-m", msg, directory=directory)


def init_and_commit(directory, custom_message=False):
    """Run git init, git add, git commit on given directory.
    """
    # local git things - initialize, add, commit
    # note that running git init on an existing repo is safe, so no need
    # to check anything first
    git_init(directory)
    if repo_changed(directory):
        message = "Initial commit"
        if custom_message:
            message = get_commit_message()
            if not message:
                print("Empty commit message, exiting.")
                sys.exit(1)
        commit_all_changes(directory, message)


def push_to_github(directory, branch):
    """Push `branch` back to GitHub"""
    _call_git("push", "--set-upstream", "origin", branch, directory=directory)


def git_init(directory):
    """Initialize git repository"""
    _call_git("init", directory=directory)
