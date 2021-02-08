# Tests for git and github methods
from pathlib import Path

import abcclassroom.github as abcgit


def test_init_and_commit(default_config, tmp_path):
    """
    Tests that we can create a directory, initialize it as a git repo,
    and commit some changes.
    """
    repo_dir = Path(tmp_path, "init-and-commit")
    repo_dir.mkdir()
    a_file = Path(repo_dir, "testfile.txt")
    a_file.write_text("Some text")
    abcgit.init_and_commit(repo_dir)
    assert Path(repo_dir, ".git").exists()
    git_return = abcgit._call_git("log", directory=repo_dir)
    assert git_return.stdout.startswith("commit")


def test_master_branch_to_main_repeatedly(tmp_path):
    """
    Tests that we can sucessfully change the default master branch to
    main, and nothing bad happends if we try and do it again
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
    Tests that changing the name of the master branch in a initialized
    repo without commits works.
    """
    repo_dir = Path(tmp_path, "change-master-no-commits")
    repo_dir.mkdir()
    abcgit.git_init(repo_dir)
    abcgit._master_branch_to_main(repo_dir)
