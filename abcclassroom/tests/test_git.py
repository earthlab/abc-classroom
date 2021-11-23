"""
Tests for git and github methods
"""

import os
import sys
import subprocess
from pathlib import Path
import unittest.mock as mock
import pytest

import abcclassroom.git as abcgit


# Function to replace check_ssh
def mock_check_ssh():
    """Mock that returns a successful message following what Git returns."""
    # TODO: Lets see how often i use this fixture. would be easy to patch
    # via a mock object too...
    return sys.stdout.write(
        "Hi username! You've successfully authenticated \n"
    )


# TODO - do we need this??
def mock_call_git():
    """A basic mock that returns a RuntimeError"""

    # TODO: can i write to stderr as a return value perhaps? test this
    # sys.stderr.write("Some git error here - test this")
    raise RuntimeError("Some git error here - test this")


@pytest.fixture()
def example_student_repo(tmpdir):
    """A fixture that creates an example student repo.
    This can be run in a temp dir to avoid messing with a dev's local
    environment. This allows us to test init and other repo functions
    without needing to create files in our tests each time."""

    repo_dir = Path(tmpdir, "assignment-1", "course-test-student")
    repo_dir.mkdir(parents=True, exist_ok=True)
    a_file = Path(repo_dir, "README.md")
    a_file.write_text("Some text in the readme")

    return repo_dir


@pytest.fixture()
def example_student_repo_git(tmpdir, example_student_repo):
    """A fixture with an initialized git repo"""

    import contextlib

    # Create the repo dir
    repo_path = example_student_repo
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        # This just suppresses print messages so we aren't getting extra
        # stdout to weed through
        abcgit.init_and_commit(repo_path)
    return repo_path


# TODO: add an  actual check here for the standard out
def test_check_git_ssh_pass():
    """When ssh is setup correctly, the check should run and pass with no
    output."""
    with mock.patch("subprocess.run"):
        # Skip actually running the subprocess call and return the expected
        # output
        subprocess.run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="", stderr="Hi username"
        )
        # Here this should just run and pass
        # I don't think we need an assert unless we add a message for
        # successful check to the function. Then we get a return output that
        # can be tested
        abcgit.check_git_ssh()


def test_check_git_ssh_warning(capsys):
    """Test what happens when ssh is setup but user hasn't logged in"""
    with mock.patch("subprocess.run"):
        # Skip actually running the subprocess call and return the expected
        # output. We always trigger a CalledProcessError in this function
        subprocess.run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="", stderr="Warning: Permanently"
        )

        abcgit.check_git_ssh()
        captured_output = capsys.readouterr().out.splitlines()
        assert captured_output[0].startswith("Warning:")


def test_check_git_ssh_error(capsys):
    """Test what happens when ssh is not setup - should raise RuntimeError"""
    with mock.patch("subprocess.run"):
        # Skip running subprocess call, return the expected error
        subprocess.run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="", stderr="Encountered this error"
        )
        with pytest.raises(RuntimeError):
            abcgit.check_git_ssh()
        captured_output = capsys.readouterr().out.splitlines()
        assert captured_output[0].startswith("Encountered this error")


# NOTE: Updated to run git status so it works universally
# TODO: i am cheating and mocking git status and forcing a return. is this
#  even useful? Also does status really need to be mocked? Does CI have status
# setup because perhaps this is something we can just run without a mock?
def test_call_git_status(capsys):
    """Test that _call_git helper function runs as expected"""
    with mock.patch("abcclassroom.git._call_git", return_value="On branch"):
        ret = abcgit._call_git("status")
    assert "On branch" in ret


# TODO i am not sure how to set this up but what happens if git isn't setup
#  and you try to run _call_git?


def test_clone_repo_pass(monkeypatch, example_student_repo, capsys, tmp_path):
    """Test that clone_repo works as expected. This test assumes that git
    clone runs as it should and just tests that the correct message is
    returned.

    TODO: this currently does NOT test that the clone goes to the right
    location. I don't think we can do that without actually calling clone
    because this is part of the clone command.

    """

    # Fixture creates demo student repo in case we do want to test location
    # need to talk this through however because right now we don't need this -
    # right now this test is kind of weak in what it actually does.
    os.chdir(tmp_path)
    example_student_repo

    # Mock the subprocess.run and check_git_ssh
    with mock.patch("subprocess.run", return_value=""), mock.patch(
        "abcclassroom.git.check_git_ssh", return_value=mock_check_ssh()
    ):
        abcgit.clone_repo(
            organization="earth55lab", repo="earthpy", dest_dir="assignment-1"
        )
    captured = capsys.readouterr()
    lines = captured.out.splitlines()

    assert lines[1].startswith("Cloning: git@github")


def test_clone_repo_bad_repo(
    monkeypatch, example_student_repo, capsys, tmpdir
):
    """Test what happens when you clone into a directory that hasn't been
    created yet. This should return a RuntimeError"""

    # TODO: again this isn't checking that it places the repo in the correct
    #  directory. i think that can only be tested by running the command
    #  because it is placed where it belongs when you call git clone.
    #  alternatively if there is some really creative way to patch over the
    #  part of git clone that hits the GH api and test the part that only
    #  does dir stuff that is another option?

    os.chdir(tmpdir)
    example_student_repo

    with mock.patch(
        "abcclassroom.git.check_git_ssh", return_value=mock_check_ssh()
    ), mock.patch(
        "abcclassroom.git._call_git",
        side_effect=RuntimeError("Error message here"),
    ):
        # Test match output from mock call git - note that because i'm
        # triggering the runtime error above i specify the error message. So
        # here, match= isn't that helpful but it does show us it's catching
        # the side effect but also capturing below the stdout that we expect
        # from abcclassroom.
        with pytest.raises(RuntimeError, match="Error message here"):
            abcgit.clone_repo(
                organization="earthlab",
                repo="eardthpy",
                dest_dir="assignment-1",
            )

    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    # Testing expected stout from clone_repo
    assert lines[2].startswith(
        "Oops, something went wrong when cloning " "earthlab"
    )


# TODO: I'm not sure there is any point of failure here because this doesn't
# check
# that the remote is valid in the function. is that ok?
def test_add_remote(tmpdir, example_student_repo_git):
    """Function that tests the add remote correctly adds a new remote to a
    git repo"""

    repo_path = example_student_repo_git
    abcgit.add_remote(
        directory=repo_path,
        organization="demo-org",
        remote_repo="student-repo",
    )
    # Now check that setting the remote worked
    ret = abcgit._call_git("remote", "-v", directory=repo_path)
    assert ret.stdout.startswith(
        "origin\tgit@github.com:demo-org/student-repo.git (fetch)"
    )


# Test repo changed
def test_repo_changed(tmpdir, example_student_repo_git):
    """Should return True if the repo is dirty"""
    repo_path = example_student_repo_git
    # Make that puppy dirty / change stuff
    a_file = Path(repo_path, "README.md")
    a_file.write_text("Some new text in the readme")
    ret = abcgit.repo_changed(directory=repo_path)
    assert ret


# TODO this test and the above could be in the same test fun. not sure what
#  best practice is here
def test_repo_clean(tmpdir, example_student_repo_git):
    """Should return True if the repo is dirty"""
    repo_path = example_student_repo_git
    ret = abcgit.repo_changed(directory=repo_path)
    assert ret is False


def test_init_and_commit(tmpdir, example_student_repo):
    """
    Test that we can create a directory, initialize it as a git repo,
    and commit some changes.
    """

    # Create the empty repo and initialized it
    os.chdir(tmpdir)
    repo_path = example_student_repo

    abcgit.init_and_commit(repo_path)
    assert Path(repo_path, ".git").exists()
    git_return = abcgit._call_git("log", directory=repo_path)
    assert git_return.stdout.startswith("commit")


# TODO this actually opens up a text editor at the CLI when i run the tests
# i'm really confused by this because i thought it would allow me to pass a
# string to the function and do the rest for me.
def test_init_and_commit_custom_messate(tmpdir, example_student_repo):
    """
    Test that init and commit works when provided a custom message.
    """

    # Create the empty repo and initialized it
    os.chdir(tmpdir)
    repo_path = example_student_repo

    abcgit.init_and_commit(repo_path, custom_message="message here great!")


# TODO - this could use that example repo fixture once again?
def test_master_branch_to_main_repeatedly(tmp_path):
    """
    Tests that we can successfully change the default master branch to
    main, and nothing bad happens if we try and do it again
    """
    repo_dir = Path(tmp_path, "change-master")
    repo_dir.mkdir()
    abcgit.git_init(repo_dir)

    # change the default branch name
    abcgit._master_branch_to_main(repo_dir)
    # in order to test that main exists, we need to add some commits
    a_file = Path(repo_dir, "testfile.txt")
    a_file.write_text("Some text")
    commit_msg = "commit some things"
    abcgit.commit_all_changes(repo_dir, msg=commit_msg)

    # now test the existance of main
    abcgit._call_git(
        "show-ref",
        "--quiet",
        "--verify",
        "refs/heads/main",
        directory=repo_dir,
    )

    # trying again should also work without error
    abcgit._master_branch_to_main(repo_dir)


def test_master_branch_to_main_no_commits(tmp_path):
    """
    Test that changing the name of the master branch in a initialized
    repo without commits works.
    """
    repo_dir = Path(tmp_path, "change-master-no-commits")
    repo_dir.mkdir()
    abcgit.git_init(repo_dir)
    abcgit._master_branch_to_main(repo_dir)
