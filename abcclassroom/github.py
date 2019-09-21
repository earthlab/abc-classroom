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

from .utils import _call_git


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
    g = gh3.login(token=token)
    organization = g.organization(org)
    title = "Template repository for {}".format(repository)
    organization.create_repository(repository, title)

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


def commit_all_changes(directory, msg=None):
    if msg is None:
        raise ValueError("Commit message can not be empty.")

    _call_git("add", "*", directory=directory)
    _call_git("commit", "-a", "-m", msg, directory=directory)


def push_to_github(directory, branch):
    """Push `branch` back to GitHub"""
    _call_git("push", "--set-upstream", "origin", branch, directory=directory)


def git_init(directory):
    """Initialize git repository"""
    _call_git("init", directory=directory)
