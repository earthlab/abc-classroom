"""
abc-classroom.quickstart
========================

"""

import os
from shutil import copy, rmtree
from abcclassroom import __file__


def path_to_example(dataset):
    """
    Construct a file path to an example dataset.
    This file defines helper functions to access data files in this directory,
    to support examples. Adapted from the PySAL package.

    Parameters
    ----------
    dataset: string
        Name of a dataset to access (e.g., "config.yml")

    Returns
    -------
    string
        A file path (string) to the dataset
    """
    abcclassroom_path = os.path.split(__file__)[0]
    data_dir = os.path.join(abcclassroom_path, "example-data")
    data_files = os.listdir(data_dir)
    if dataset not in data_files:
        raise KeyError(dataset + " not found in abc-classroom example data.")
    return os.path.join(data_dir, dataset)


def create_dir_struct(course_name="course_dir", f=False, working_dir=None):
    """
    Create a directory structure that can be used to start an abc-classroom course. This includes a main directory,
    two sub directories for templates and cloned files, and a start to a configuration file.
    """
    # Making sure the configuration file is where it's supposed to be.
    config = path_to_example("config.yml")
    if not os.path.exists(config):
        raise ValueError(
            "config.yml configuration file can't be located, please ensure abc-classroom has been installed correctly"
        )
    # Assigning the custom folder name if applicable
    if " " in course_name:
        raise ValueError(
            "Spaces not allowed in custom course name {}. Please use hyphens instead.".format(
                course_name
            )
        )
    if working_dir is None:
        working_dir = os.getcwd()
    main_dir = os.path.join(working_dir, course_name)
    if f and os.path.isdir(main_dir):
        rmtree(main_dir)
    # Make sure that the main_dir doesn't exist already
    if os.path.isdir(main_dir):
        raise ValueError(
            """
            Ooops! It looks like the directory {} already exists on your computer. You might have already
            run quickstart in this directory. Consider using another course name or deleting the existing directory
            if you do not need it.""".format(
                course_name
            )
        )
    # Making all the needed directories and subdirectories, and creating the configuration file.
    dir_names = [
        main_dir,
        os.path.join(main_dir, "clone_dir"),
        os.path.join(main_dir, "template_dir"),
    ]
    for directories in dir_names:
        os.mkdir(directories)
    copy(config, main_dir)
    if course_name:
        with open(os.path.join(main_dir, "config.yml"), "r") as file:
            filedata = file.read()
            filedata = filedata.replace(
                "/Users/karen/awesome-course", main_dir
            )
            filedata = filedata.replace(
                "/Users/me/awesome-course/cloned_dirs",
                os.path.join(main_dir, "clone_dir"),
            )
            filedata = filedata.replace(
                "/Users/me/awesome-course/assignment_repos",
                os.path.join(main_dir, "template_dir"),
            )
        with open(os.path.join(main_dir, "config.yml"), "w") as file:
            file.write(filedata)
    print(
        """
        Directory structure created to begin using abc-classroom at {}.
        All directories needed and a configuration file to modify have been created. To proceed, please
        move your sample roster and course_materials directory into {} created by quickstart.""".format(
            main_dir, course_name
        )
    )
