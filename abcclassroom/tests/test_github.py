# Tests for github script

import pytest
import github3 as gh3
import abcclassroom.github as github


# Creating an OrganizationObject that will run instead of
# github3.create_repository
class OrganizationObject(object):
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


def test_remote_repo_exists_pass(monkeypatch):
    """Tesitng that a remote repository exists"""
    # Creating the fake function that will replace gh3.login with mock_login.
    monkeypatch.setattr(gh3, "login", mock_login)
    # Running this function with the newly faked function inside of it.
    assert github.remote_repo_exists("earthlab", "abc-classroom")


def test_remote_repo_exists_fail(monkeypatch):
    """Tesitng that a remote repository that doesn't exist fails"""
    monkeypatch.setattr(gh3, "login", mock_login)
    assert not github.remote_repo_exists("bad_org", "bad_repo")


def test_check_student_repo_pass(monkeypatch):
    """Testing that checking a student repo works"""
    monkeypatch.setattr(gh3, "login", mock_login)
    try:
        github.check_student_repo_exists("earthlab", "test", "student")
        assert True
    except RuntimeError:
        assert False


def test_check_student_repo_fail(monkeypatch):
    """Testing that checking a bad student repo fails"""
    monkeypatch.setattr(gh3, "login", mock_login)
    with pytest.raises(Exception):
        github.check_student_repo_exists("earthlab", "not", "student")


def test_call_git_with_branch(fake_process):
    """Testing that _call_git helper function works"""
    # This type of function requires a different test. When a function usses
    # subprocess.run instead of called gh3 directly, it's very difficult to
    # fake with monkeypatch. There's a package developed specifically for this
    # called fake_process that allows subprocesses to be faked. As you can see
    # below, if I supply the subprocess that will be run, alongside the stdout
    # expected from that function being run, it will allow for fake running of
    # the subprocess call.
    fake_process.register_subprocess(
        ["git", "branch"], stdout=["* fake_branch", "  master"]
    )
    ret = github._call_git("branch")
    assert ret.stdout == b"* fake_branch\n  master\n"


def test_clone_repo_pass(fake_process):
    """Test that cloning a repository works."""
    fake_process.register_subprocess(
        [
            "git",
            "-C",
            "test_dir",
            "clone",
            "git@github.com:earthlab/abc-classroom.git",
        ],
        stderr=b"Cloning into 'abc-classroom'...\n",
    )
    try:
        github.clone_repo("earthlab", "abc-classroom", "test_dir")
        assert True
    except RuntimeError:
        assert False


def test_create_repo_pass(monkeypatch):
    """Test that creating a new repository works."""
    monkeypatch.setattr(gh3, "login", mock_login)
    try:
        github.create_repo(org="earthlab", repository="test_repo", token=None)
        assert True
    except RuntimeError:
        assert False
