import os
import pytest
from shutil import rmtree
from abcclassroom.quickstart import create_dir_struct as quickstart


def test_quickstart_default():
    """
    Test that the standard run of abc-quickstart creates all expected folders and outputs.
    """
    quickstart()
    main_dir = os.path.join(os.getcwd(), "course_dir")
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert (
            os.path.isdir(main_dir)
            and os.path.isdir(os.path.join(main_dir, "assignment-template-repos"))
            and os.path.isdir(os.path.join(main_dir, "student-cloned-repos"))
            and os.path.isfile(os.path.join(main_dir, "config.yml"))
            and "course-name" and "assignment-template-repos" and "student-cloned-repos" in data.read()
        )
    rmtree(main_dir)


def test_quickstart_custom_name():
    """
    Test that abc-quickstart works with a custom name.
    """
    quickstart("python_test_dir_custom_name")
    main_dir = os.path.join(os.getcwd(), "python_test_dir_custom_name")
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert (
            os.path.isdir(main_dir)
            and os.path.isdir(os.path.join(main_dir, "assignment-template-repos"))
            and os.path.isdir(os.path.join(main_dir, "student-cloned-repos"))
            and os.path.isfile(os.path.join(main_dir, "config.yml"))
            and "python_test_dir_custom_name" and "assignment-template-repos" and "student-cloned-repos" in data.read()
        )
    rmtree(main_dir)


def test_quickstart_bad_name():
    """
    Test that abc-quickstart fails with a improperly formatted name.
    """
    with pytest.raises(ValueError, match="Spaces not"):
        quickstart("bad name")


def test_quickstart_remake_existing():
    """
    Test that abc-quickstart fails when using the same name for a course twice.
    """
    quickstart("python_test_dir_custom_name")
    main_dir = os.path.join(os.getcwd(), "python_test_dir_custom_name")
    with pytest.raises(ValueError, match="Ooops! "):
        quickstart("python_test_dir_custom_name")
    rmtree(main_dir)


def test_quickstart_remove_existing():
    """
    Test that abc-quickstart doesn't fail when using the same name for a course twice and the -f argument.
    """
    quickstart("python_test_dir_custom_name")
    quickstart("python_test_dir_custom_name", True)
    main_dir = os.path.join(os.getcwd(), "python_test_dir_custom_name")
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert (
                os.path.isdir(main_dir)
                and os.path.isdir(os.path.join(main_dir, "assignment-template-repos"))
                and os.path.isdir(os.path.join(main_dir, "student-cloned-repos"))
                and os.path.isfile(os.path.join(main_dir, "config.yml"))
                and "course-name" and "assignment-template-repos" and "student-cloned-repos" in data.read()
        )
    rmtree(main_dir)
