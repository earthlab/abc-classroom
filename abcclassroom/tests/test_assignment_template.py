# Tests for assignment-template console script workflow

import pytest
import os
from pathlib import Path
import abcclassroom.template as abctemplate


# Tests for create_template_dir method
def test_create_template_dir(default_config, tmp_path):
    """
    Tests that create_template_dir with default mode "fail" creates a directory with the expected name.
    """
    default_config["course_directory"] = tmp_path
    template_path = abctemplate.create_template_dir(
        default_config, "test_assignment"
    )
    assert os.path.isdir(template_path)
    assert (
        template_path
        == "{}/test_template/tc-test_assignment-template".format(tmp_path)
    )


def test_create_template_dir_fail_when_exists(default_config, tmp_path):
    """
    Tests that create_template_dir with default mode "fail" does indeed fail with  sys.exit when the directory already exists.
    """
    default_config["course_directory"] = tmp_path
    template_path = abctemplate.create_template_dir(
        default_config, "test_assignment"
    )
    # run it again! fail!
    with pytest.raises(SystemExit):
        template_path = abctemplate.create_template_dir(
            default_config, "test_assignment"
        )


def test_create_template_dir_merge_when_exists(default_config, tmp_path):
    """
    Tests that create_template_dir with default mode "fail" does indeed fail with  sys.exit when the directory already exists.
    """
    default_config["course_directory"] = tmp_path
    template_path = abctemplate.create_template_dir(
        default_config, "test_assignment"
    )
    # run it again! merge!
    template_path = abctemplate.create_template_dir(
        default_config, "test_assignment", "merge"
    )


def test_create_template_dir_delete_when_exists(default_config, tmp_path):
    """
    Tests that create_template_dir with default mode "fail" does indeed fail with  sys.exit when the directory already exists.
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

    # # default mode = "merge"
    # # should be three extra_files after merge
    # config["extra_files"] = {
    #     "newtestfile.txt": ["line1", "line2"],
    #     "README.md": ["line1", "line2"],
    # }
    # tpath= Path(template_path)
    # nfiles = len(tpath.glob(*))
    # template_path = abctemplate.create_template_dir(
    #         self.config, "test_assignment","merge"
    #     )
    # assert len(tpath.glob(*)) = nfiles+1
    # # default mode = delete
    # template_path = abctemplate.create_template_dir(
    #         self.config, "test_assignment","delete"
    #     )


def test_coursename_config_options(tmp_path):
    # test that it fails if neither short_coursename or course_name is set
    localconfig = {
        "template_dir": "test_template",
        "course_directory": tmp_path,
    }
    with pytest.raises(SystemExit):
        template_path = abctemplate.create_template_dir(
            localconfig, "test_assignment"
        )


# Tests for copy_assignment_files method
def test_copy_assignment_files(default_config, tmp_path):
    # test that contents are the same for target and source directory
    default_config["course_directory"] = tmp_path
    assignment = "assignment1"
    # first, set up the test nbgrader directory
    nbpath = Path.joinpath(
        tmp_path, default_config["nbgrader_dir"], "release", assignment
    )
    nbpath.mkdir(parents=True)
    # create some temporary files
    Path.joinpath(nbpath, "file1.txt").touch()
    Path.joinpath(nbpath, "file2.txt").touch()
    template_repo = abctemplate.create_template_dir(default_config, assignment)
    abctemplate.copy_assignment_files(
        default_config, template_repo, assignment
    )
    assert os.listdir(nbpath) == os.listdir(template_repo)


def test_copy_assignment_files_fails_nodir(default_config, tmp_path):
    # test that fails if nbgrader dir does not exist
    default_config["course_directory"] = tmp_path
    assignment = "assignment1"
    template_repo = abctemplate.create_template_dir(default_config, assignment)
    with pytest.raises(SystemExit):
        abctemplate.copy_assignment_files(
            default_config, template_repo, assignment
        )


# Tests for create_extra_files method
def test_create_extra_files(default_config, tmp_path):
    default_config["course_directory"] = tmp_path
    assignment = "assignment1"
    template_repo = abctemplate.create_template_dir(default_config, assignment)
    abctemplate.create_extra_files(default_config, template_repo, assignment)
    assert Path(template_repo, "testfile.txt").exists()
    f = open(Path(template_repo, "testfile.txt"))
    assert f.readline() == "line1\n"


def test_create_extra_files_readme(default_config, tmp_path):
    # tests for the special README.md case
    default_config["course_directory"] = tmp_path
    course_name = default_config["course_name"]
    assignment = "assignment1"
    template_repo = abctemplate.create_template_dir(default_config, assignment)
    abctemplate.create_extra_files(default_config, template_repo, assignment)
    assert Path(template_repo, "README.md").exists()
    f = open(Path(template_repo, "README.md"))
    assert f.readline() == "# {}: {}\n".format(course_name, assignment)

    # test when course_name not set
    del default_config["course_name"]
    abctemplate.create_extra_files(default_config, template_repo, assignment)
    assert Path(template_repo, "README.md").exists()

    f = open(Path(template_repo, "README.md"))
    assert f.readline() == "# README\n"


# def test_do_local_git_things(template_dir, custom_message):
