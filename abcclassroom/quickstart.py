"""
abc-classroom.quickstart
========================

"""

import os
from shutil import copy, rmtree
from argparse import ArgumentParser
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


def create_dir_struct():
    """
    Create a directory structure that can be used to start an abc-classroom course. This includes a main directory,
    two sub directories for templates and cloned files, and a start to a configuration file.
    """
    # Creating the default names for the cloned and template repos.
    course = "course-dir"
    # Making sure the configuration file is where it's supposed to be.
    config = path_to_example("config.yml")
    if not os.path.exists(config):
        raise ValueError(
            "config.yml configuration file can't be located, please ensure abc-classroom has been installed correctly"
        )
    # Allows users to rename the cloned and template repos.
    parser = ArgumentParser(description=create_dir_struct.__doc__)
    parser.add_argument(
        "--course_name", help="Name of the main course repository"
    )
    parser.add_argument(
        "-f",
        action="store_true",
        help="Option to override the existing folder structure made by this function previously.",
    )
    args = parser.parse_args()
    # Assigning the custom folder name if applicable
    if args.course_name:
        course = args.course_name
        if " " in course:
            raise ValueError(
                "Spaces not allowed in custom course name {}. Please use hyphens instead.".format(
                    course
                )
            )
    main_dir = os.path.join(os.getcwd(), course)
    if args.f and os.path.isdir(main_dir):
        rmtree(main_dir)
    # Make sure that the main_dir doesn't exist already
    if os.path.isdir(main_dir):
        raise ValueError(
            """
            Ooops! It looks like the directory {} already exists on your computer. You might have already 
            run quickstart in this directory. Consider using another course name or deleting the existing directory 
            if you do not need it.""".format(
                course
            )
        )
    # Making all the needed directories and subdirectories, and creating the configuration file.
    dir_names = [
        main_dir,
        os.path.join(main_dir, "cloned_dirs"),
        os.path.join(main_dir, "assignment_repos"),
    ]
    for directories in dir_names:
        os.mkdir(directories)
    copy(config, main_dir)
    if args.course_name:
        with open(os.path.join(course, "config.yml"), "r") as file:
            filedata = file.read()
            filedata = filedata.replace("course-name", args.course_name)
        with open(os.path.join(course, "config.yml"), "w") as file:
            file.write(filedata)
    print(
        """
        Directory structure created to begin using abc-classroom at {}. 
        All directories needed and a configuration file to modify have been created. To proceed, please 
        move your sample roster and nbgrader directory into {} created by quickstart.""".format(
            main_dir, course
        )
    )
