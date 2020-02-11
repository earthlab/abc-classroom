import os
import pytest
from pathlib import Path
import abcclassroom.quickstart as quickstart
import abcclassroom.config as cf


def test_path_to_example():
    # with filename that should exist
    filename = "config.yml"
    config_path = quickstart.path_to_example(filename)

    # with filename that doesn't exist
    filename = "filethatdoesntexist.txt"
    with pytest.raises(FileNotFoundError):
        config_path = quickstart.path_to_example(filename)


def test_quickstart_default(tmp_path):
    """
    Test that abc-quickstart without arguments creates the default
    "abc_course" main directory, config file and two subdirectories.
    """
    quickstart.create_dir_struct(working_dir=tmp_path)
    # check that main dir and config created
    main_dir = Path(tmp_path, "abc_course")
    assert main_dir.is_dir()
    assert Path(main_dir, "config.yml").is_file()
    # check contents of config
    config = cf.get_config(main_dir)
    assert cf.get_config_option(config, "course_directory") == str(main_dir)

    # check that subdirectories created
    template_dir = cf.get_config_option(config, "template_dir")
    assert Path(main_dir, template_dir).is_dir()
    clone_dir = cf.get_config_option(config, "clone_dir")
    assert Path(main_dir, clone_dir).is_dir()


def test_quickstart_custom_name(tmp_path):
    """
    Test that abc-quickstart works with a custom name.
    """
    custom_name = "pytest_dir_custom_name"
    quickstart.create_dir_struct(custom_name, working_dir=tmp_path)
    main_dir = Path(tmp_path, custom_name)
    assert main_dir.is_dir()
    assert Path(main_dir, "config.yml").is_file()
    # check contents of config
    config = cf.get_config(main_dir)
    assert cf.get_config_option(config, "course_directory") == str(main_dir)

    # check that subdirectories created
    template_dir = cf.get_config_option(config, "template_dir")
    assert Path(main_dir, template_dir).is_dir()
    clone_dir = cf.get_config_option(config, "clone_dir")
    assert Path(main_dir, clone_dir).is_dir()


def test_quickstart_bad_name():
    """
    Test that abc-quickstart fails with a improperly formatted name.
    """
    with pytest.raises(ValueError, match="Spaces not"):
        quickstart.create_dir_struct("bad name")


def test_quickstart_remake_existing(tmp_path):
    """
    Test that abc-quickstart fails when using the same name for a course twice.
    """
    quickstart.create_dir_struct(
        "python_test_dir_custom_name", working_dir=tmp_path
    )
    with pytest.raises(FileExistsError, match="Ooops! "):
        quickstart.create_dir_struct(
            "python_test_dir_custom_name", working_dir=tmp_path
        )


def test_quickstart_remove_existing(tmp_path):
    """
    Test that abc-quickstart doesn't fail when using the same name for a course
    twice with the -f argument.
    """
    custom_name = "python_test_dir_custom_name"
    quickstart.create_dir_struct(custom_name, working_dir=tmp_path)
    quickstart.create_dir_struct(custom_name, True, working_dir=tmp_path)
    main_dir = Path(tmp_path, custom_name)
    assert main_dir.is_dir()
    assert Path(main_dir, "config.yml").is_file()
