import os
import subprocess
from shutil import rmtree


def test_quickstart_default():
    """
    Test that the standard run of abc-quickstart creates all expected folders and outputs.
    """
    output = subprocess.run("abc-quickstart", capture_output=True)
    main_dir = os.path.join(os.getcwd(), "course-dir")
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert (
            os.path.isdir(main_dir)
            and os.path.isdir(os.path.join(main_dir, "assignment_repos"))
            and os.path.isdir(os.path.join(main_dir, "cloned_dirs"))
            and os.path.isfile(os.path.join(main_dir, "config.yml"))
            and "Directory structure created" in str(output.stdout)
            and "course-name" in data.read()
        )
    rmtree(main_dir)


def test_quickstart_custom_name():
    """
    Test that abc-quickstart works with a custom name.
    """
    output = subprocess.run("abc-quickstart --course_name python_test_dir_custom_name", capture_output=True)
    main_dir = os.path.join(os.getcwd(), "python_test_dir_custom_name")
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert (
            os.path.isdir(main_dir)
            and os.path.isdir(os.path.join(main_dir, "assignment_repos"))
            and os.path.isdir(os.path.join(main_dir, "cloned_dirs"))
            and os.path.isfile(os.path.join(main_dir, "config.yml"))
            and "Directory structure created" in str(output.stdout)
            and "python_test_dir_custom_name" in data.read()
        )
    rmtree(main_dir)


def test_quickstart_bad_name():
    """
    Test that abc-quickstart fails with a improperly formatted name.
    """
    output = subprocess.run(
        'abc-quickstart --course_name "bad name"', capture_output=True
    )
    assert "Spaces" in str(output.stderr)


def test_quickstart_remake_existing():
    """
    Test that abc-quickstart fails when using the same name for a course twice.
    """
    subprocess.run("abc-quickstart --course_name python_test_dir_custom_name")
    output = subprocess.run(
        "abc-quickstart --course_name abc-quickstart --course_name python_test_dir_custom_name",
        capture_output=True,
    )
    assert "Ooops! " in str(output.stderr)


def test_quickstart_remove_existing():
    """
    Test that abc-quickstart doesn't fail when using the same name for a course twice and the -f argument.
    """
    subprocess.run("abc-quickstart --course_name python_test_dir_custom_name")
    output = subprocess.run("abc-quickstart --course_name python_test_dir_custom_name -f", capture_output=True)
    main_dir = os.path.join(os.getcwd(), "python_test_dir_custom_name")
    with open(os.path.join(main_dir, "config.yml")) as data:
        assert (
            os.path.isdir(main_dir)
            and os.path.isdir(os.path.join(main_dir, "assignment_repos"))
            and os.path.isdir(os.path.join(main_dir, "cloned_dirs"))
            and os.path.isfile(os.path.join(main_dir, "config.yml"))
            and "Directory structure created" in str(output.stdout)
            and "python_test_dir_custom_name" in data.read()
        )
    rmtree(main_dir)
