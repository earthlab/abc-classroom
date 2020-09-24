# Tests for new-template and update-template scripts

import pytest
import os
from pathlib import Path

import abcclassroom.template as abctemplate
import abcclassroom.github as github
import abcclassroom.config as cf


@pytest.fixture
def config_file(default_config, tmp_path):
    """
    Writes the config to a file in tmp_path
    """
    cf.write_config(default_config, tmp_path)


def test_create_template_dir(default_config, tmp_path):
    """
    Tests that create_template_dir with default mode "fail" creates a
    directory with the expected name.
    """
    default_config["course_directory"] = tmp_path
    templates_dir = default_config["template_dir"]
    assignment = "test_assignment"
    template_path = abctemplate.create_template_dir(default_config, assignment)
    assert os.path.isdir(template_path)

    assert template_path == Path(
        tmp_path, templates_dir, "{}-template".format(assignment)
    )


def test_create_template_dir_fail_when_exists(default_config, tmp_path):
    """
    Tests that create_template_dir with default mode "fail" does indeed
    fail with sys.exit when the directory already exists.
    """
    default_config["course_directory"] = tmp_path
    abctemplate.create_template_dir(default_config, "test_assignment")
    # run it again! fail!
    with pytest.raises(SystemExit):
        abctemplate.create_template_dir(default_config, "test_assignment")


def test_create_template_dir_merge_when_exists(default_config, tmp_path):
    """
    Tests that create_template_dir with mode "merge" does not fail when
    directory already exists.
    """
    default_config["course_directory"] = tmp_path
    abctemplate.create_template_dir(default_config, "test_assignment")
    # run it again! merge!
    abctemplate.create_template_dir(default_config, "test_assignment", "merge")


def test_create_template_dir_delete_when_exists(default_config, tmp_path):
    """
    Tests that create_template_dir with mode "delete" re-creates the
    directory with the same contents.
    """
    default_config["course_directory"] = tmp_path
    template_path = abctemplate.create_template_dir(
        default_config, "test_assignment"
    )
    # run it again! delete!
    contents_before = list(Path(template_path).glob("*"))
    template_path = abctemplate.create_template_dir(
        default_config, "test_assignment", "delete"
    )
    contents_after = list(Path(template_path).glob("*"))
    assert contents_before == contents_after


def test_move_git_dir(default_config, tmp_path):
    """
    Tests that we correctly move (and move back) a .git directory in the
    template repo when running in delete mode.
    """
    default_config["course_directory"] = tmp_path
    template_path = abctemplate.create_template_dir(
        default_config, "test_assignment"
    )
    github.init_and_commit(template_path, False)
    assert Path(template_path, ".git").exists()
    template_path = abctemplate.create_template_dir(
        default_config, "test_assignment", "delete"
    )
    assert Path(template_path, ".git").exists()


# Tests for copy_assignment_files method
def test_copy_assignment_files(default_config, tmp_path):
    """"test that contents are the same for target and source directory
    """
    default_config["course_directory"] = tmp_path
    assignment = "assignment1"
    files_to_ignore = [".DS_Store", ".ipynb_checkpoints"]
    default_config["files_to_ignore"] = files_to_ignore
    # first, set up the test course materials directory
    # and create some temporary files
    cmpath = Path(
        tmp_path, default_config["course_materials"], "release", assignment
    )
    cmpath.mkdir(parents=True)
    cmpath.joinpath("file1.txt").touch()
    cmpath.joinpath("file2.txt").touch()
    cmpath.joinpath(".DS_Store").touch()

    template_repo = abctemplate.create_template_dir(default_config, assignment)
    abctemplate.copy_assignment_files(
        default_config, template_repo, assignment
    )
    # Test that both text files have been moved to the template dir but that
    # the system .DS_Store is not there
    for afile in os.listdir(cmpath):
        if afile not in files_to_ignore:
            assert afile in os.listdir(template_repo)
        else:
            print(afile)
            assert afile not in os.listdir(template_repo)

    assert os.listdir(cmpath).sort() == os.listdir(template_repo).sort()


def test_copy_assignment_files_fails_nodir(default_config, tmp_path):
    # test that fails if course_materials dir does not exist
    default_config["course_directory"] = tmp_path
    assignment = "assignment1"
    template_repo = abctemplate.create_template_dir(default_config, assignment)
    with pytest.raises(SystemExit):
        abctemplate.copy_assignment_files(
            default_config, template_repo, assignment
        )


# Test for create_extra_files method
def test_create_extra_files(default_config, tmp_path):
    default_config["course_directory"] = tmp_path
    assignment = "assignment1"

    # create the extra_files dir and some extra files
    readme_contents = ["# readme\n", "\n", "another line\n"]
    Path(tmp_path, "extra_files").mkdir()
    Path(tmp_path, "extra_files", ".gitignore").touch()
    with open(Path(tmp_path, "extra_files", "readme.md"), "w") as f:
        f.writelines(readme_contents)

    template_repo = abctemplate.create_template_dir(default_config, assignment)
    abctemplate.create_extra_files(default_config, template_repo, assignment)
    assert Path(template_repo, "readme.md").exists()
    assert Path(template_repo, ".gitignore").exists()


# Test for adding assignment name to readme contents


def test_add_assignment_to_readme(tmp_path):
    assignment = "assignment1"
    path_to_readme = Path(tmp_path, "testreadme.md")
    readme_contents = ["# readme\n", "\n", "another line\n"]
    with open(path_to_readme, "w") as f:
        f.writelines(readme_contents)
    abctemplate.add_assignment_to_readme(path_to_readme, assignment)
    f = open(path_to_readme, "r")
    assert f.readline() == "# Assignment {}\n".format(assignment)
