from pytest import raises
import os
import subprocess
from shutil import rmtree


def test_quickstart_default():
    os.system("abc-quickstart")
    main_dir = os.path.join(os.getcwd(), "course-dir")
    assert (
        os.path.isdir(main_dir)
        and os.path.isdir(os.path.join(main_dir, "assignment_repos"))
        and os.path.isdir(os.path.join(main_dir, "cloned_dirs"))
        and os.path.isfile(os.path.join(main_dir, "config.yml"))
    )
    rmtree(main_dir)


def test_quickstart_custom_name():
    os.system("abc-quickstart --course_name python_test_dir_custom_name")
    main_dir = os.path.join(os.getcwd(), "python_test_dir_custom_name")
    assert (
        os.path.isdir(main_dir)
        and os.path.isdir(os.path.join(main_dir, "assignment_repos"))
        and os.path.isdir(os.path.join(main_dir, "cloned_dirs"))
        and os.path.isfile(os.path.join(main_dir, "config.yml"))
    )
    rmtree(main_dir)


def test_quickstart_bad_name():
    stderr = subprocess.run(
        "abc-quickstart --course_name 'bad name'", capture_output=True
    )
    assert "Spaces " in stderr


def test_quickstart_remake_existing():
    os.system("abc-quickstart --course_name python_test_dir_custom_name")
    stderr = stderr = subprocess.run(
        "abc-quickstart --course_name abc-quickstart --course_name python_test_dir_custom_name",
        capture_output=True,
    )
    assert "Ooops! " in stderr


def test_quickstart_remove_existing():
    os.system("abc-quickstart --course_name python_test_dir_custom_name")
    os.system("abc-quickstart --course_name python_test_dir_custom_name -f")
    main_dir = os.path.join(os.getcwd(), "python_test_dir_custom_name")
    assert (
        os.path.isdir(main_dir)
        and os.path.isdir(os.path.join(main_dir, "assignment_repos"))
        and os.path.isdir(os.path.join(main_dir, "cloned_dirs"))
        and os.path.isfile(os.path.join(main_dir, "config.yml"))
    )
    rmtree(main_dir)
