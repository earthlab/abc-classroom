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
import requests

import github3 as gh3

from .utils import input_editor, get_request
from .config import get_github_auth, set_github_auth


def get_access_token():
    """Get a GitHub access token for the API

    First tries to read from local token file. If token does not exist,
    or is not valid, generates a new token using the OAuth Device Flow.
    https://docs.github.com/en/free-pro-team@latest/developers/apps/
    identifying-and-authorizing-users-for-github-apps#device-flow

    Returns an access token (string).
    """
    # first, we see if we have a saved token
    auth_info = get_github_auth()
    if auth_info:
        try:
            access_token = auth_info["access_token"]
            # if so, is it valid?
            user = _get_authenticated_user(access_token)
            if user is not None:
                print(
                    "Access token is present and valid; successfully "
                    "authenticated as user {}".format(user)
                )
                return access_token
        except KeyError:
            pass

    # otherwise, generate a new token
    print("Generating new access token")
    # client id for the abc-classroom-bot GitHub App
    client_id = "Iv1.8df72ad9560c774c"

    # TODO need to handle cases where the device call fails - wrong client_id,
    # the user could ^C or the internet could be out, or some other
    # unanticipated woe)
    device_code = _get_login_code(client_id)
    access_token = _poll_for_status(client_id, device_code)

    # test the new access token
    user = _get_authenticated_user(access_token)
    if user is not None:
        print("""Successfully authenticated as user {}""".format(user))
    return access_token


def _get_authenticated_user(token):
    """Test the validity of an access token.

    Given a github access token, test that it is valid by making an
    API call to get the authenticated user.

    Returns the GitHub username of the authenticated user if token valid,
    otherwise returns None.
    """

    url = "https://api.github.com/user"
    (status, body) = get_request(url, token)
    try:
        user = body["login"]
        return user
    except KeyError:
        return None


def _get_login_code(client_id):
    """Prompts the user to authorize abc-classroom-bot.

    First part of the Device Flow workflow. Asks user to visit a URL and
    enter the provided code. Waits for user to hit RETURN to continue.
    Returns the device code.
    """

    # make the device call
    header = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"client_id": client_id}
    link = "https://github.com/login/device/code"
    r = requests.post(link, headers=header, json=payload)

    # process the response
    data = r.json()
    status = r.status_code
    if status != 200:
        # print the response if the call failed
        print(r.json())
        return None

    device_code = data["device_code"]
    uri = data["verification_uri"]
    user_code = data["user_code"]

    # prompt the user to enter the code
    print(
        "To authorize this app, go to {} and enter the code {}".format(
            uri, user_code
        )
    )
    input("\nPress RETURN to continue after inputting the code successfully")

    return device_code


def _poll_for_status(client_id, device_code):
    """Polls API to see if user entered the device code

    This is the second step of the Device Flow. Returns an access token, and
    also writes the token to a file in the user's home directory.
    """

    header = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {
        "client_id": client_id,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    r = requests.post(
        "https://github.com/login/oauth/access_token",
        headers=header,
        json=payload,
    )

    data = r.json()
    access_token = data["access_token"]
    set_github_auth({"access_token": access_token})
    return access_token


def _call_git(*args, directory=None):
    cmd = ["git"]
    cmd.extend(args)
    try:
        ret = subprocess.run(
            cmd,
            cwd=directory,
            check=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        err = e.stderr
        if not err:
            err = e.stdout
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


def add_remote(directory, organization, remote_repo):
    remote_url = "git@github.com:{}/{}.git".format(organization, remote_repo)
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
    _master_branch_to_main(directory)
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


def _master_branch_to_main(dir):
    """Change the name of the master branch to main

    Changes the name of the master branch to main for the repo in the
    given directory. Since we create the repo on github first, which now sets
    the default branch to 'main', we need the local repo to match
    in order to be able to push without errors later.
    """

    try:
        # first, verify if the  master branch exists (this is only true
        # if there are commits on the master branch)
        _call_git(
            "show-ref",
            "--quiet",
            "--verify",
            "refs/heads/master",
            directory=dir,
        )
    except RuntimeError:
        # master branch verification fails, so we check for main and create
        # it if it does not exist
        try:
            _call_git(
                "show-ref",
                "--quiet",
                "--verify",
                "refs/heads/main",
                directory=dir,
            )
        except RuntimeError:
            # no main branch, create one
            _call_git("checkout", "-b", "main", directory=dir)
    else:
        # rename branch
        print("master exists, renaming")
        _call_git("branch", "-m", "master", "main", directory=dir)


def push_to_github(directory, branch="main"):
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


def git_init(directory, defaultbranch="main"):
    """Initialize git repository"""
    _call_git("init", directory=directory)


###################################################
# Methods below are from before the re-factoring.
# Retaining for reference, but with no guarantee
# about correct function.


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
