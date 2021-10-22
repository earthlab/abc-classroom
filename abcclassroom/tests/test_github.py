# Tests for github script

import pytest
import github3 as gh3
import abcclassroom.github as github


# Creating an OrganizationObject that will run instead of
# github3.create_repository
class OrganizationObject(object):
    # Should this have a static decorator on it?
    @staticmethod
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
    """Trest that a remote repository that doesn't exist fails."""
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


#
#
def test_check_student_repo_fail(monkeypatch):
    """A student repo that doesn't exist should fail"""
    monkeypatch.setattr(gh3, "login", mock_login)
    # TODO if we use github3 there is a speciicaly Not FoundError exception
    #  that should be captures here
    with pytest.raises(Exception):
        github.check_student_repo_exists("earthlab", "not", "student")


# TODO: i don't understand this test.
# you could have any number of branches locally so how is this looking for main
# or master. this test i think isn't reproducible.
# I've updated this to use git status which seems to work but i will see if it
# works on CI. this assumes that git is setup in the envt just a note...
def test_call_git_with_branch(fake_process):
    """Testing that _call_git helper function works"""
    # When a function uses
    # subprocess.run instead of called gh3 directly, it's  difficult to
    # fake with monkeypatch. There's a package developed specifically for this
    # called fake_process that allows subprocesses to be faked. As you can see
    # below, if I supply the subprocess that will be run, alongside the stdout
    # expected from that function being run, it will allow for fake running of
    # the subprocess call.

    # TODO: I think we want something that will always be reproducible
    # this will get the current branch git rev-parse --abbrev-ref HEAD
    # Git status always starts with on branch - does it? it does on MAC
    fake_process.register_subprocess(["git", "status"], stdout=["On branch"])
    ret = github._call_git("status")
    assert "On branch" in ret.stdout


#
#
# def test_clone_repo_pass(fake_process):
#     """Test that cloning a repository works."""
#     fake_process.register_subprocess(
#         [
#             "git",
#             "-C",
#             "test_dir",
#             "clone",
#             "git@github.com:earthlab/abc-classroom.git",
#         ],
#         stderr=b"Cloning into 'abc-classroom'...\n",
#     )
#     try:
#         github.clone_repo("earthlab", "abc-classroom", "test_dir")
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
