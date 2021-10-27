# Tests for github script

import pytest
import github3 as gh3
import abcclassroom.github as github
import os
from unittest import mock


# Creating an OrganizationObject that will run instead of
# github3.create_repository
class OrganizationObject(object):
    # TODO: Should this have a static decorator on it?
    # @staticmethod
    def create_repository(self, repository):
        if repository == "test_repo":
            return True


# Creating a MockResponse object to be returned when trying to log into github
class MockResponse(object):
    def repository(self, org, repository, token=None):
        if org == "earthlab" and repository == "abc-classroom":
            pass
        elif org == "earthlab" and repository == "test-student":
            pass
        else:
            raise Exception

    def organization(self, org):
        return OrganizationObject()


# Function to return Mock Response for login.
def mock_login(token=None):
    return MockResponse()


# Function to replace check_ssh
def mock_check_ssh():
    """stuff here"""
    # I'm not sure if this is really what we want?
    # We could also mock up an ssh key in a temp directory?
    return print("Pretending ssh is all setup nicely?")


# so if you run the check repo g.repository(org, repository) it returns the
# text below if the repo exists. but i don't know if that is the return from
# the package OR the api
# g.repository(org, repository)
# Out[57]: <Repository [earthlab/earthpy]>


def test_remote_repo_exists_pass(monkeypatch):
    """If the remote repo exists, return True"""
    # Creating the fake function that will replace gh3.login with mock_login.
    monkeypatch.setattr(gh3, "login", mock_login)
    # Running this function with the newly faked function inside of it.
    assert github.remote_repo_exists("earthlab", "abc-classroom")


def test_remote_repo_exists_fail(monkeypatch):
    """Test that a remote repository that doesn't exist fails."""
    monkeypatch.setattr(gh3, "login", mock_login)
    assert not github.remote_repo_exists("bad_org", "bad_repo")


# NOTE: Updated to run git status so it works universally
def test_call_git_status(fake_process):
    """Testing that _call_git helper function works"""
    # When a function uses
    # subprocess.run instead of called gh3 directly, it's  difficult to
    # fake with monkeypatch. There's a package developed specifically for this
    # called pytest_process and has a fake_process object. This objects that
    # allows subprocesses to be mocked.

    # TODO - is this really mocking the subprocess call?
    fake_process.register_subprocess(["git", "status"], stdout=["On branch"])
    ret = github._call_git("status")
    assert "On branch" in ret.stdout


# TODO: This test assumes a dir called "test_dir" exists and it doesnt exist.
# Is this a space for a fixture / temp dir setup?


@pytest.fixture()
def example_student_repo():
    """A fixture with an example student repo."""
    # TODO can a fixture take a variable like a function can?
    # or should this only create the git dir and let the calling function worry
    # about changing the directory?
    sample_dir = os.path.join("assignment-1", "course-test-student")
    if not os.path.isdir(sample_dir):
        os.makedirs(sample_dir)
    # do we need this to be a git repo? probably would be useful for other
    # tests


# def mock_clone(example_student_repo, a_directory, tmp_path, test):
#     """Takes a repo that has been mock cloned and places it in the intended
#     directory. """
#     # When it's mocking it seems to replace each variable in the function in
#     # a weird unexpected way. - example_student_repo = '-C', a_directory =
#     # 'assignment-1', tmp_path = 'clone', test =
#     # 'git@github.com:earthlab/course-test-student.git'
#
#     # TODO: make this so it's drops the example dir in the dir_path location
#     #tmp_path = "."
#     # Create the rep
#     #a_directory = "test_dir"
#     clone_path = os.path.join(tmp_path, a_directory)
#     print("clone_path is", clone_path)
#     os.chdir(clone_path)
#     # Move repo to location
#     return example_student_repo()

# stackoverflow.com/questions/25692440/mocking-a-subprocess-call-in-python


@mock.patch("subprocess.run")
def test_clone_repo_pass2(
    mock_subproc_run, monkeypatch, example_student_repo, capsys
):

    # This fixture will drop an example git
    # repo for us to check that it exists assignment-1/course-test-student"
    example_student_repo
    # Replace check_github_ssh with a pass (Assume that works - is that ok??)
    monkeypatch.setattr(github, "check_git_ssh", mock_check_ssh)

    # Mock the subprocess call
    process_mock = mock.Mock()
    attrs = {"communicate.return_value": ("output", "error")}
    process_mock.configure_mock(**attrs)
    mock_subproc_run.return_value = process_mock
    github.clone_repo(
        organization="earth55lab", repo="earthpy", dest_dir="assignment-1"
    )
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    # assert captured.out starts with "cloning: git@github"
    # TODO do we also want to create a mock repo for it to check?
    # TODO: this is not actually the text that git clone sends to st out
    assert lines[1].startswith("Successfully cloned: git@github")
    # Cloning into 'eartehpy'...  # ERROR: Repository not found.  # fatal:
    # Could not read from remote repository.


# CLONE: Test what happens when you clone into a directory that hasn't been
# created
# yet


@mock.patch("subprocess.run")
def test_clone_repo_bad_repo(
    mock_subproc_run, monkeypatch, example_student_repo, capsys
):
    """Test what happens when you clone into a directory that hasn't been
    created yet. This should return a RuntimeError"""

    # This fixture will drop an example git
    # repo for us to check that it exists assignment-1/course-test-student"

    example_student_repo
    # Replace check_github_ssh with a pass (Assume that works - is that ok??)
    monkeypatch.setattr(github, "check_git_ssh", mock_check_ssh)

    # This is telling me it can't import github.clone_repo
    with mock.patch(
        "abcclassroom.github.clone_repo",
        side_effect=RuntimeError(),
    ):
        with pytest.raises(RuntimeError):
            e = github.clone_repo(
                organization="earthlab",
                repo="edarthpy",
                dest_dir="assignment-2",
            )
            print("The error is", e)
    # Mock the subprocess call
    # process_mock = mock.Mock()
    # mock.Mock(side_effect=RuntimeError(github.clone_repo))
    # attrs = {"communicate.return_value": ("error")}
    # process_mock.side_effect = RuntimeError(mock.Mock('error'))
    # How do i tell the mocked object to return the error here?
    # process_mock.configure_mock(**attrs)
    # mock_subproc_run.return_value = process_mock

    # with pytest.raises(RuntimeError):
    #     github.clone_repo(
    #         organization="earthlab", repo="edarthpy", dest_dir="assignment-2"
    #     )
    # captured = capsys.readouterr()
    # lines = captured.out.splitlines()
    # assert captured.out starts with "cloning: git@github"
    # print("Error:", lines[1], captured.err)
    # TODO do we also want to create a mock repo for it to check?
    # TODO: this is not actually the text that git clone sends to st out
    # assert lines[1].startswith("RuntimeError: Cloning into 'eaorth'")
    # This should return RuntimeError: Cloning into 'eaorth'...  # ERROR:
    # Repository not found.


# CLONE: test what happens when you clone and the remote doesn't exist


# TODO: ok i just tested this. it's definitely not skipping the clone.
# def test_clone_repo_pass(fake_process, monkeypatch, example_student_repo):
#     """Test that a repo is correctly cloned to the right location."""
#
#     # Replace check_github_ssh with a pass (Assume that works - is that ok??)
#     # Here i'm confused because i would think we're replacing _call_git with
#     # a mock function so it doesn't try to clone
#     monkeypatch.setattr(github, "check_git_ssh", mock_check_ssh)
#
#     # it is actually cloning hte data. we want to monkey patch around the
#     # entire function i think or somehow use the faek subprocess to fake the
#     # call
#     git_commands = [
#             "git",
#             "-C",
#             "assignment-1",
#             "clone",
#             "git@github.com:earthlab/abc-classroom.git",
#         ]
#     fake_process.register_subprocess(git_commands,
#                          stderr=b"Cloning into 'abc-classroom'...\n" )
#     # Not sure why it keeps telling me it's not registered so adding this
#     fake_process.allow_unregistered(True)
#     # Create the dir needed for the assignment (clone doesnt do this)
#     # once this works we can use a tmp path fixture for it
#     example_student_repo
#     # Run the fake process - i thought we're testing clone_repo
#     process = github.clone_repo(organization="earthlab",
#                       repo="test",
#                       dest_dir="assignment-1")
#     # Create the new directory
#     out, _ = process.communicate()
#     print(out)
#     # # Replace _call_git with the returned repo
#     # monkeypatch.setattr(github, "_call_git", mock_clone)
#     # organization, repo, dest_dir
#
#     assert os.path.isdir('assignment-1')


# i suspect that this needs a fixture or object that returns a repository
# in a new directory.
# then i guess we can test that the repo contains a .git directory?
# and maybe some files?
# def test_clone_repo_pass1(fake_process, tmp_path):
#     """Test that a cloned repo is saved in the correct location."""
#     os.chdir(tmp_path)
#     # TODO: This forces subprocess to work BUT i'm guessing it won't work on
#     # CI because SSH is not setup. We may want a fixture that creates an envt
#     # with a ssh key available?
#     fake_process.allow_unregistered(True)
#     fake_process.register_subprocess(
#         [
#             "git",
#             "clone" "git@github.com:earthlab/abc-classroom.git",
#         ],
#         stderr=b"Cloning into 'abc-classroom'...\n",
#     )
#     try:
#         github.clone_repo("earthlab", "abc-classroom", ".")
#         # TODO: should we do a dir check here to ensure that correct dir is
#         # actually created and contains expected files??
#         assert True
#     except RuntimeError:
#         assert False


#
#
# def test_create_repo_pass(monkeypatch):
#     """Test that creating a new repository works."""
#     monkeypatch.setattr(gh3, "login", mock_login)
#     try:
#         github.create_repo(org="earthlab",repository="test_repo", token=None)
#         assert True
#     except RuntimeError:
#         assert False


# This is the old tests
# from pathlib import Path
#
# import abcclassroom.github as abcgit
#
#
# def test_init_and_commit(default_config, tmp_path):
#     """
#     Tests that we can create a directory, initialize it as a git repo,
#     and commit some changes.
#     """
#     repo_dir = Path(tmp_path, "init-and-commit")
#     repo_dir.mkdir()
#     a_file = Path(repo_dir, "testfile.txt")
#     a_file.write_text("Some text")
#     abcgit.init_and_commit(repo_dir)
#     assert Path(repo_dir, ".git").exists()
#     git_return = abcgit._call_git("log", directory=repo_dir)
#     assert git_return.stdout.startswith("commit")
#
#
# def test_master_branch_to_main_repeatedly(tmp_path):
#     """
#     Tests that we can sucessfully change the default master branch to
#     main, and nothing bad happends if we try and do it again
#     """
#     repo_dir = Path(tmp_path, "change-master")
#     repo_dir.mkdir()
#     abcgit.git_init(repo_dir)
#
#     # change the default branch name
#     abcgit._master_branch_to_main(repo_dir)
#     # in order to test that main exists, we need to add some commits
#     a_file = Path(repo_dir, "testfile.txt")
#     a_file.write_text("Some text")
#     commit_msg = "commit some things"
#     abcgit.commit_all_changes(repo_dir, msg=commit_msg)
#
#     # now test the existance of main
#     abcgit._call_git(
#         "show-ref",
#         "--quiet",
#         "--verify",
#         "refs/heads/main",
#         directory=repo_dir,
#     )
#
#     # trying again should also work without error
#     abcgit._master_branch_to_main(repo_dir)
#
#
# def test_master_branch_to_main_no_commits(tmp_path):
#     """
#     Tests that changing the name of the master branch in a initialized
#     repo without commits works.
#     """
#     repo_dir = Path(tmp_path, "change-master-no-commits")
#     repo_dir.mkdir()
#     abcgit.git_init(repo_dir)
#     abcgit._master_branch_to_main(repo_dir)


# TODO: https://github.com/earthlab/abc-classroom/issues/361 this function
# isnt' in karen's list of functions to test
# def test_check_student_repo_exists_pass(monkeypatch):
#     """Testing that checking a student repo works"""
#     monkeypatch.setattr(gh3, "login", mock_login)
#     try:
#         github.check_student_repo_exists("earthlab", "test", "student")
#         assert True
#     except RuntimeError:
#         assert False


# TODO: similar to above - this isn't in the list of functions to test.
# This function used to be called in MAIN but is now commented out
# SO i think we should drop these tests
#
# def test_check_student_repo_fail(monkeypatch):
#     """A student repo that doesn't exist should fail"""
#     monkeypatch.setattr(gh3, "login", mock_login)
#     # TODO if we use github3 there is a speciicaly Not FoundError exception
#     #  that should be captures here
#     with pytest.raises(Exception):
#         github.check_student_repo_exists("earthlab", "not", "student")
