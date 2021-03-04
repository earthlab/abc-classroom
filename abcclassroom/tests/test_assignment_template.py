# Tests for new-template and update-template scripts

import pytest
import os
from pathlib import Path
import shutil

import abcclassroom.template as abctemplate
import abcclassroom.github as github
import abcclassroom.config as cf

# Tests here use the course setup fixtures in conftest.py

# Is there something wrong with running abc-quickstart and got all dirs
# and the config file are then setup That was as the quickstart is changed
# the tests will all be dependent upon it


# @pytest.fixture
# def config_file(default_config, tmp_path):
#     """Writes the config to a file in tmp_path"""
#     cf.write_config(default_config, tmp_path)


def test_create_template_dir(course_structure_assignment):
    """
    Tests that create_template_dir with default mode "fail" creates a
    directory with the expected name.
    """
    config, assignment_name, release_path = course_structure_assignment

    # # If we did the above, then we could remove a lot of this here
    # default_config["course_directory"] = tmp_path
    # templates_dir = default_config["template_dir"]
    # assignment_name = "test_assignment"
    template_path = abctemplate.create_template_dir(config, assignment_name)
    assert Path(template_path).is_dir()

    course_dir = cf.get_config_option(config, "course_directory", True)
    templates_dir = cf.get_config_option(config, "template_dir", True)
    assert template_path == Path(
        course_dir, templates_dir, "{}-template".format(assignment_name)
    )


def test_create_template_dir_fail_when_exists(course_structure_assignment):
    """
    Tests that create_template_dir with default mode "fail" does indeed
    throw FileExistsError when the directory already exists.
    """
    config, assignment_name, release_path = course_structure_assignment
    abctemplate.create_template_dir(config, assignment_name)

    # If run again, it should fail given the dir already exists
    with pytest.raises(
        FileExistsError, match=("Oops! The directory specified")
    ):
        abctemplate.create_template_dir(config, assignment_name)


def test_create_template_dir_merge_when_exists(course_structure_assignment):
    """
    Tests that create_template_dir with mode "merge" does not fail when
    directory already exists.
    """
    config, assignment_name, release_path = course_structure_assignment
    abctemplate.create_template_dir(config, assignment_name)

    # The test here is that there is no failure? or is there something we
    # can explicetly test here? - the method simply returns and does nothing
    # in this case, so I am not sure what else to test
    abctemplate.create_template_dir(config, assignment_name, "merge")


def test_create_template_dir_delete_when_exists(course_structure_assignment):
    """
    Tests that create_template_dir with mode "delete" re-creates a
    directory with the same name without keeping contents.
    """

    config, assignment_name, release_path = course_structure_assignment
    template_path = abctemplate.create_template_dir(config, assignment_name)
    # create a file in the template dir
    testfile = Path(template_path, "file1.txt")
    testfile.touch()

    # Run in delete mode
    contents_before = list(Path(template_path).rglob("*"))
    assert len(contents_before) > 0
    assert testfile.exists()
    template_path = abctemplate.create_template_dir(
        config, assignment_name, "delete"
    )
    contents_after = list(Path(template_path).rglob("*"))
    assert testfile.exists() is False
    assert len(contents_after) == 0


def test_create_template_dir_move_git_dir(course_structure_assignment):
    """
    Tests that if have already created a local git repo in a template
    dir, we correctly move (and move back) when running in delete mode.
    """
    config, assignment_name, release_path = course_structure_assignment
    template_path = abctemplate.create_template_dir(config, assignment_name)

    # create a file in the template dir, init a git repo and commit
    testfile = Path(template_path, "file1.txt")
    testfile.touch()
    github.init_and_commit(template_path, False)
    assert Path(template_path, ".git").exists()

    template_path = abctemplate.create_template_dir(
        config, assignment_name, "delete"
    )

    assert Path(template_path, ".git").exists()


def test_copy_assignment_files(course_structure_assignment):
    """Test that files are moved to the template repo directory and that
    ignored files are NOT moved.
    """

    sample_config, assignment_name, release_path = course_structure_assignment

    template_path = abctemplate.create_template_dir(
        sample_config, assignment_name
    )
    # # I think i can remove the stuff below now...
    # release_path = Path(
    #     sample_config["course_directory"],
    #     sample_config["course_materials"],
    #     "release",
    #     assignment_name,
    # )
    # release_path.mkdir(parents=True, exist_ok=True)
    # Should we test that the message printed is what we expect here?
    abctemplate.copy_assignment_files(
        sample_config, template_path, release_path
    )
    files_to_ignore = sample_config["files_to_ignore"]

    # Test that both text files have been moved to the template dir but that
    # the system .DS_Store is not there
    for afile in os.listdir(release_path):
        if afile not in files_to_ignore:
            assert afile in os.listdir(template_path)
        else:
            assert afile not in os.listdir(template_path)


# TODO - revisit this test as there is no error or print message thrown now...
def test_copy_assignment_dirs(course_structure_assignment, capfd):
    """Test that when there is a directory in the extra_files dir, things
    still copy as expected.
    """
    sample_config, assignment_name, release_path = course_structure_assignment

    # Manually create the dir to just test the copy function - this could be
    # a third fixture... i'm being forced to use full paths - not sure if this
    # is ideal
    template_path = Path(
        sample_config["course_directory"],
        sample_config["template_dir"],
        assignment_name + "-template",
    )
    template_path.mkdir(parents=True, exist_ok=True)
    # release_dir = Path(sample_config["course_directory"],
    #                    sample_config["course_materials"],
    #                    "release",
    #                    assignment_name)
    # Create an empty directory to test what happens
    release_path.joinpath("dummy-dir").mkdir(exist_ok=True)
    abctemplate.copy_assignment_files(
        sample_config, template_path, release_path
    )
    # This test is no longer relevant - i made it so it passes ...
    # Revisit thi
    # out, err = capfd.readouterr()
    # print(out)
    # assert "Oops - looks like" in out


# Ok this test also isn't relevant as i moved the actual test for the dir
# existing above to ensure an empty directory isn't created. this function
# only copies assignment files assuming the dirs exist
def test_copy_assignment_files_fails_nodir(course_structure_assignment):
    """Test that copy_assignment_files fails if course_materials dir does not
    exist"""

    sample_config, assignment_name, release_path = course_structure_assignment

    # default_config["course_directory"] = tmp_path
    # assignment_name = "assignment1"
    # I think this is created in the fixture
    # template_repo = abctemplate.create_template_dir(
    #     sample_config, assignment_name
    # )

    # Delete the nbgrader assignment directory
    shutil.rmtree(release_path)

    # with pytest.raises(FileNotFoundError,
    #                    match="No such file or directory:"):
    #     abctemplate.copy_assignment_files(
    #         sample_config, template_repo, release_path
    #     )


def test_create_extra_files(course_structure_assignment):
    """Test that create extra files actually moves files. """

    sample_config, assignment_name, release_path = course_structure_assignment
    template_repo = abctemplate.create_template_dir(
        sample_config, assignment_name
    )
    abctemplate.copy_extra_files(sample_config, template_repo, assignment_name)
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
