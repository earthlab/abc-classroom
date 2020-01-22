import os
import pytest
from abcclassroom.quickstart import create_dir_struct as quickstart


def test_quickstart_default(tmp_path):
    """
    Test that abc-quickstart without arguments creates the default
    "course_dir" main directory and all expected folders and outputs.
    """
    quickstart(working_dir=tmp_path)
    main_dir = os.path.join(tmp_path, "course_dir")
    assert os.path.isdir(main_dir)
    assert os.path.isfile(os.path.join(main_dir, "config.yml"))
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert (
            "course_directory"
            and "template_dir"
            and "clone_dir" in data.read()
        )
    assert os.path.isdir(os.path.join(main_dir, "template_dir"))
    assert os.path.isdir(os.path.join(main_dir, "clone_dir"))


def test_quickstart_custom_name(tmp_path):
    """
    Test that abc-quickstart works with a custom name.
    """
    custom_name = "pytest_dir_custom_name"
    quickstart(custom_name, working_dir=tmp_path)
    main_dir = os.path.join(tmp_path, custom_name)
    assert os.path.isdir(main_dir)
    assert os.path.isfile(os.path.join(main_dir, "config.yml"))
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert custom_name and "template_dir" and "clone_dir" in data.read()
    assert os.path.isdir(os.path.join(main_dir, "template_dir"))
    assert os.path.isdir(os.path.join(main_dir, "clone_dir"))


def test_quickstart_bad_name():
    """
    Test that abc-quickstart fails with a improperly formatted name.
    """
    with pytest.raises(ValueError, match="Spaces not"):
        quickstart("bad name")


def test_quickstart_remake_existing(tmp_path):
    """
    Test that abc-quickstart fails when using the same name for a course twice.
    """
    quickstart("python_test_dir_custom_name", working_dir=tmp_path)
    with pytest.raises(ValueError, match="Ooops! "):
        quickstart("python_test_dir_custom_name", working_dir=tmp_path)


def test_quickstart_remove_existing(tmp_path):
    """
    Test that abc-quickstart doesn't fail when using the same name for a course twice and the -f argument.
    """
    custom_name = "python_test_dir_custom_name"
    quickstart(custom_name, working_dir=tmp_path)
    quickstart(custom_name, True, working_dir=tmp_path)
    main_dir = os.path.join(tmp_path, custom_name)
    assert os.path.isdir(main_dir)
    assert os.path.isfile(os.path.join(main_dir, "config.yml"))
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert (
            "course_directory"
            and "template_dir"
            and "clone_dir" in data.read()
        )
    assert os.path.isdir(os.path.join(main_dir, "template_dir"))
    assert os.path.isdir(os.path.join(main_dir, "clone_dir"))
