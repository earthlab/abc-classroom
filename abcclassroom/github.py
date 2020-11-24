"""
abc-classroom.github
====================

"""

import os
import logging
import random
import string
import subprocess
import sys

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
        if not err:
            err = e.stdout.decode("utf-8")
        raise RuntimeError(err) from e

    return ret


def remote_repo_exists(org, repository, token=None):
    """Check if the remote repository exists for the organization."""

    try:
        g = gh3.login(token=token)
        g.repository(org, repository)

    except Exception:
        return False

    return True


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


def clone_repo(organization, repo, dest_dir):
    """Clone `repository` from `org` into a sub-directory in `directory`.
    Assumes you have ssh keys setup for github (rather than using GitHub API
    token)."""
    # If ssh  it not setup correctly -  or however we want to authenticate,
    # we need a
    # friendly message about that
    # We should add some message about what is being cloned here - the  url
    # works
    url = "git@github.com:{}/{}.git".format(organization, repo)
    print("cloning:", url)
    _call_git("-C", dest_dir, "clone", url)


def create_repo(org, repository, token):
    """Create a repository in the provided GitHub organization."""
    github_obj = gh3.login(token=token)
    organization = github_obj.organization(org)
    print(
        "Creating new repository {} at https://github.com/{}".format(
            repository, org
        )
    )
    try:
        organization.create_repository(repository)
    except gh3.exceptions.UnprocessableEntity:
        print(
            "Error: organization {} already has a repository named {}".format(
                org, repository
            )
        )


def add_remote(directory, organization, remote_repo, token):
    remote_url = "https://{}@github.com/{}/{}".format(
        token, organization, remote_repo
    )
    _call_git("remote", "add", "origin", remote_url, directory=directory)


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
    """Run git add, git commit on a given directory. Checks git status
    first and does nothing if no changes.
    """
    if msg is None:
        raise ValueError("Commit message can not be empty.")
    if repo_changed(directory):
        _call_git("add", "*", directory=directory)
        _call_git("commit", "-a", "-m", msg, directory=directory)
    else:
        print("No changes in repository {}; doing nothing".format(directory))


def init_and_commit(directory, custom_message=False):
    """Run git init, git add, git commit on given directory. Checks git status
    first and does nothing if no changes.
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
                sys.exit(1)  # sys is undefined - ask karen about this
        commit_all_changes(directory, message)
    else:
        print("No changes to local repository.")


def push_to_github(directory, branch="master"):
    """Push `branch` back to GitHub"""
    try:
        _call_git(
            "push", "--set-upstream", "origin", branch, directory=directory
        )
    except RuntimeError as e:
        raise e


def pull_from_github(directory, branch="master"):
    """Pull `branch` of local repo in `directory` from GitHub"""
    try:
        _call_git("pull", "origin", branch, directory=directory)
    except RuntimeError as e:
        raise e


def git_init(directory):
    """Initialize git repository"""
    _call_git("init", directory=directory)


###################################################
# Methods below are from before the re-factoring.
# Retaining for reference, but with no guarantee
# about correct function.


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
