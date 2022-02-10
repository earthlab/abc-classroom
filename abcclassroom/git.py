"""
abc-classroom.git
=================
"""

# Methods for command line git operations. See github.py for
# methods that involve the GitHub API

import subprocess


def check_git_ssh():
    """Tests that ssh access to GitHub is set up correctly on the users
    computer.

    Throws a RuntimeError if setup is not working.
    """
    cmd = ["ssh", "-T", "git@github.com"]
    try:
        subprocess.run(
            cmd,
            check=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        # We ALWAYS will get here, because that subprocess call returns
        # a non-zero exit code whether ssh access is set up correctly or
        # not. Must check output.
        subprocess_out = e.stderr
        if not subprocess_out:
            subprocess_out = e.stdout
        if subprocess_out.startswith("Hi"):
            # if everything set up correctly, the ssh test returns output
            # starting with 'Hi username!'
            pass
        elif subprocess_out.startswith("Warning: Permanently"):
            # if the user has set up ssh keys, but hasn't logged in yet,
            # they will need to verify the RSA fingerprint
            # If they do so, the message is 'Warning: Permanently
            # added 'github.com' (RSA) to the list of known hosts.'
            print(subprocess_out)
            pass
        else:
            # possible reasons to get here include 1. no ssh key set up;
            # 2. ssh key has incorrect permissions; 3. remote host
            # identification changed. We print the error message for
            # the user and point them to github documentation for help.
            print("Encountered this error checking ssh access to git:")
            print(subprocess_out)
            docURL = "https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh"  # noqa
            print(
                """Your ssh access to github is not set up correctly; see
            {}.""".format(
                    docURL
                )
            )
            raise RuntimeError(subprocess_out)
    except FileNotFoundError as e:
        # we get here if ssh is not installed. The error message is
        # [Errno 2] No such file or directory: 'ssh'
        print(e)
        if "No such file or directory: 'ssh'" in str(e):
            print(
                """Did not find `ssh` command. Make sure that open-ssh
                is installed on your operating system."""
            )


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


def clone_repo(organization, repo, dest_dir):
    """Clone `repository` from `org` into a sub-directory in `directory`.

    Raises RuntimeError if ssh keys not set up correctly, or if git clone
    fails for other reasons.

    Parameters
    ----------
    organization : string
        A string with the name of the organization to clone from
    repo : string
        A string with the name of the GitHub repository to clone
    dest_dir : string
        Path to the destination directory
        TODO: is this a full path, path object or string - what format is
        dest_dir in
    Returns
    -------
    Cloned github repository in the destination directory specified.
    """

    try:
        # first, check that local git set up with ssh keys for github
        check_git_ssh()
        url = "git@github.com:{}/{}.git".format(organization, repo)
        print("cloning:", url)
        _call_git("-C", dest_dir, "clone", url)
    except RuntimeError as e:
        raise e


def add_remote(directory, organization, remote_repo):
    remote_url = "git@github.com:{}/{}.git".format(organization, remote_repo)
    _call_git("remote", "add", "origin", remote_url, directory=directory)


def repo_changed(directory):
    """Determine if the Git repository in directory is dirty"""
    ret = _call_git("status", "--porcelain", directory=directory)
    return bool(ret.stdout)


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


def init_and_commit(directory, commit_message):
    """Run git init, git add, git commit on given directory. Checks git status
    first and does nothing if no changes.
    """
    # local git things - initialize, add, commit
    # note that running git init on an existing repo is safe, so no need
    # to check anything first
    git_init(directory)
    _master_branch_to_main(directory)
    if repo_changed(directory):
        commit_all_changes(directory, commit_message)
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
    """Push `branch` of the repository in `directory` back to GitHub"""
    try:
        # first, check that local git set up with ssh keys for github
        check_git_ssh()
        _call_git(
            "push", "--set-upstream", "origin", branch, directory=directory
        )
    except RuntimeError as e:
        raise e


def pull_from_github(directory, branch="main"):
    """Pull `branch` of local repo in `directory` from GitHub"""
    try:
        # first, check that local git set up with ssh keys for github
        check_git_ssh()
        _call_git("pull", "origin", branch, directory=directory)
    except RuntimeError as e:
        raise e


def git_init(directory, defaultbranch="main"):
    """Initialize git repository"""
    _call_git("init", directory=directory)
