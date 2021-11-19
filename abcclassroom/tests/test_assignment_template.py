# Tests for new-template and update-template scripts
# Tests here use the course setup fixtures in conftest.py

import pytest
from pathlib import Path

import abcclassroom.template as abctemplate
import abcclassroom.git as abcgit
import abcclassroom.config as cf


def test_create_template(course_structure_assignment):
    """
    Test that the top-level create_template method creates the expected
    template directory with at least one expected file. More detailed
    testing left to called methods.
    """

    config, assignment_name, release_path = course_structure_assignment
    course_dir = Path(config["course_directory"])
    templates_dir = Path(config["template_dir"])

    abctemplate.create_template(
        assignment_name, push_to_github=False, custom_message=False
    )

    expected_template_dir = Path(
        course_dir, templates_dir, "{}-template".format(assignment_name)
    )
    assert expected_template_dir.exists()
    assert Path(expected_template_dir, "readme.md").exists()
    assert Path(expected_template_dir, ".git").exists()


def test_create_template_no_assignment(sample_course_structure):
    """
    Test that top-level create_template raises FileNotFoundError if there
    is no matching assignment in the release directory.
    """
    with pytest.raises(
        FileNotFoundError, match="Oops, it looks like the assignment"
    ):
        abctemplate.create_template(
            "assignment_test", push_to_github=False, custom_message=False
        )


def test_create_template_dir(course_structure_assignment):
    """
    Tests that create_template_dir with default mode "fail" creates a
    directory with the expected name.
    """
    config, assignment_name, release_path = course_structure_assignment

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
    Tests that create_template_dir with mode "merge" does not fail and
    copies additional files when directory already exists.
    """
    config, assignment_name, release_path = course_structure_assignment
    abctemplate.create_template_dir(config, assignment_name)

    # Make some changes to the release dir
    # Create a new file in release_path
    Path(release_path, "new-notebook.ipynb").touch()
    # And re-name an existing file
    Path(release_path, "nb1.ipynb").replace(Path(release_path, "nb-1.ipynb"))
    # re-run with mode==merge, should not fail and should create new file
    abctemplate.create_template_dir(config, assignment_name, "merge")
    assert Path(release_path, "new-notebook.ipynb").exists()
    assert Path(release_path, "nb1.ipynb").exists() is False
    assert Path(release_path, "nb-1.ipynb").exists()


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
    abcgit.init_and_commit(template_path, False)
    assert Path(template_path, ".git").exists()

    template_path = abctemplate.create_template_dir(
        config, assignment_name, "delete"
    )

    assert Path(template_path, ".git").exists()


def test_copy_files_to_template_repo(course_structure_assignment):
    """
    Test that files and directories in the release directory are
    correctly copied to
    template repo, skipping files in the files_to_ignore list.
    """
    config, assignment_name, release_path = course_structure_assignment
    template_path = abctemplate.create_template_dir(config, assignment_name)

    abctemplate.copy_files_to_template_repo(
        config, template_path, assignment_name, release_path
    )

    # Test for specific files that we expect and those we don't -
    #  this depends on the specific test data in conftest.py
    # We can't iterate through release_path and check against
    #  files_to_ignore without re-implementing here the exact
    #  shutil.ignore_patterns factory function used by utils.abccopytree
    assert Path(template_path, "nb1.ipynb").exists()
    assert Path(template_path, ".DS_Store").exists() is False
    assert Path(template_path, "junk.csv").exists() is False
    assert Path(template_path, "subdirectory").is_dir()
    assert Path(template_path, "subdirectory", "nestedscript.py").exists()


def test_copy_files_to_template_repo_extra_files(course_structure_assignment):
    """
    Test that files and directories in the extra_files directory are
    correctly copied to template repo.
    """
    config, assignment_name, release_path = course_structure_assignment
    template_path = abctemplate.create_template_dir(config, assignment_name)

    # create a subdirectory and file in extra_files
    Path("extra_files", ".github").mkdir()
    Path("extra_files", ".github", "workflow.yml").touch()

    abctemplate.copy_files_to_template_repo(
        config, template_path, assignment_name, release_path
    )

    assert Path(template_path, "readme.md").exists()
    assert Path(template_path, ".github").exists()
    assert Path(template_path, ".github", "workflow.yml").exists()


def test_copy_files_to_template_repo_no_extra_files(
    course_structure_assignment,
):
    """
    Test that the copy_files_to_template_repo method does not fail when
    the extra_files dir does not exist.
    """

    config, assignment_name, release_path = course_structure_assignment
    template_path = abctemplate.create_template_dir(config, assignment_name)
    # rename the existing extra_files directory
    Path("extra_files").rename("extra_files_renamed")
    abctemplate.copy_files_to_template_repo(
        config, template_path, assignment_name, release_path
    )
    assert Path(template_path, "readme.md").exists() is False


def test_add_assignment_to_readme(tmp_path):
    """
    Test that add_assignment_to_readme correctly modifies the readme file.
    """
    assignment = "assignment1"
    path_to_readme = Path(tmp_path, "testreadme.md")
    readme_contents = ["# readme\n", "\n", "another line\n"]
    with open(path_to_readme, "w") as f:
        f.writelines(readme_contents)
    abctemplate.add_assignment_to_readme(path_to_readme, assignment)
    f = open(path_to_readme, "r")
    assert f.readline() == "# Assignment {}\n".format(assignment)
