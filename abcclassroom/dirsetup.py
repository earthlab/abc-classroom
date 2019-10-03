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
    Gets the path to an example dataset.

    Parameters
    ----------
    dataset : string
        stringy boi
    """
    abcclassroom_path = os.path.split(abcclassroom.__file__)[0]
    data_dir = os.path.join(abcclassroom_path, "example-data")
    data_files = os.listdir(data_dir)
    if dataset not in data_files:
        raise KeyError(dataset + " not found in abc-classroom example data.")
    return os.path.join(data_dir, dataset)


def directory_setup():
    """
    Set up template directory to store a course in. Creates the course directory, template directory,
    cloned directory, and adds in a template configuration file.
    """
    # Creating the default names for the cloned and template repos.
    cloned = "cloned_repos"
    template = "template_repos"
    course = "course_dir"
    # Making sure the configuration file is where it's supposed to be.
    config = path_to_example("sample_config.yml")
    if not os.path.exists(config):
        raise ValueError(
            "Configuration file can't be located, please ensure abc-classroom has been installed correctly"
        )
    # Allows users to rename the cloned and template repos.
    parser = argparse.ArgumentParser(description=directory_setup.__doc__)
    parser.add_argument(
        "--course_repo",
        help="Name of the main course repository"
    )
    parser.add_argument(
        "--cloned_repo",
        help="Name of the repository to hold the cloned files"
    )
    parser.add_argument(
        "--template_repo",
        help="Name of the repository to hold the template files"
    )
    parser.add_argument(
        "--override_existing",
        help="Option to override the existing folder structure made by this function previously."
    )
    args = parser.parse_args()
    # Assigning the custom folder names if applicable
    if args.cloned_repo:
        cloned = args.cloned_repo
    if args.template_repo:
        template = args.template_repo
    if args.course_repo:
        course = args.course_repo
    main_dir = os.path.join(os.getcwd(), course)
    if args.override_existing == "True" and os.path.isdir(main_dir):
        shutil.rmtree(main_dir)
    # Make sure that the main_dir doesn't exist already
    if os.path.isdir(main_dir):
        raise ValueError("Direcoty setup has already been run in this directory.")
    # Making all the needed directories and subdirectories, and creating the configuration file.
    os.mkdir(main_dir)
    cloned_dir = os.path.join(main_dir, cloned)
    template_dir = os.path.join(main_dir, template)
    os.mkdir(cloned_dir)
    os.mkdir(template_dir)
    shutil.copy(config, main_dir)

