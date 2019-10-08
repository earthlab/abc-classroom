"""
abc-classroom.dir-setup
========================

"""

import os
import shutil
import argparse
import abcclassroom


def path_to_example(dataset):
    """
    Construct a file path to an example dataset.
    This file defines helper functions to access data files in this directory,
    to support examples. Adapted from the PySAL package.

    Parameters
    ----------
    dataset: string
        Name of a dataset to access (e.g., "sample_config.yml")
            
    Returns
    -------
    string
        A file path (string) to the dataset
    """
    abcclassroom_path = os.path.split(abcclassroom.__file__)[0]
    data_dir = os.path.join(abcclassroom_path, "example-data")
    data_files = os.listdir(data_dir)
    if dataset not in data_files:
        raise KeyError(dataset + " not found in abc-classroom example data.")
    return os.path.join(data_dir, dataset)


def create_dir_struct():
    """
    Creates a directory structure that can be used to start an abc-classroom course. This includes a main directory,
    two sub directories for templates and cloned files, and a sample configuration file.
    """
    # Creating the default names for the cloned and template repos.
    course = "course_dir"
    # Making sure the configuration file is where it's supposed to be.
    config = path_to_example("sample_config.yml")
    if not os.path.exists(config):
        raise ValueError(
            "Configuration file can't be located, please ensure abc-classroom has been installed correctly"
        )
    # Allows users to rename the cloned and template repos.
    parser = argparse.ArgumentParser(description=create_dir_struct.__doc__)
    parser.add_argument(
        "--course_name",
        help="Name of the main course repository"
    )
    parser.add_argument(
        "-f",
        action='store_true',
        help="Option to override the existing folder structure made by this function previously."
    )
    args = parser.parse_args()
    # Assigning the custom folder name if applicable
    if args.course_name:
        course = args.course_name
    main_dir = os.path.join(os.getcwd(), course)
    if args.f and os.path.isdir(main_dir):
        shutil.rmtree(main_dir)
    # Make sure that the main_dir doesn't exist already
    if os.path.isdir(main_dir):
        raise ValueError(
            "Quickstart has already been run in this directory for that course name."
        )
    # Making all the needed directories and subdirectories, and creating the configuration file.
    os.mkdir(main_dir)
    cloned_dir = os.path.join(main_dir, "cloned_files")
    template_dir = os.path.join(main_dir, "template_files")
    os.mkdir(cloned_dir)
    os.mkdir(template_dir)
    shutil.copy(config, main_dir)
    if args.course_name:
        with open(os.path.join(course, "sample_config.yml"), "r") as file:
            filedata = file.read()
            filedata = filedata.replace("earth-analytics-bootcamp", args.course_name)
        with open(os.path.join(course, "sample_config.yml"), "w") as file:
            file.write(filedata)
    print("""
    Directory structure created to begin using abc-classroom. All directories needed and a sample configuration file 
    have been created. To proceed, please move your sample roster and nbgrader directory into the main directory 
    created by quickstart.
    """)
