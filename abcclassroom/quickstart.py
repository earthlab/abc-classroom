"""
abc-classroom.quickstart
========================

"""

import os
from pathlib import Path
from shutil import copy, rmtree
from . import config as cf
from abcclassroom import __file__


def path_to_example(dataset):
    """
    Construct a file path to an example dataset, assuming the dataset is
    contained in the 'example-data' directory of the abc-classroom package.
    Adapted from the PySAL package.

    Parameters
    ----------
    dataset: string
        Name of a dataset to access (e.g., "config.yml")

    Returns
    -------
    Path object
        A concrete Path object to the dataset
    """
    abcclassroom_path = Path(__file__).parent
    dataset_path = Path(abcclassroom_path, "example-data", dataset)
    if not dataset_path.exists():
        raise FileNotFoundError(
            dataset + " not found in abc-classroom example-data directory."
        )
    return dataset_path


def create_dir_struct(course_name="course_dir", force=False, working_dir=None):
    """
    Create a directory structure that can be used to start an abc-classroom
    course. This includes a main directory, two sub directories for templates
    and cloned files, and a start to a configuration file.

    This is the tmplementation of athe bc-quickstart script; it is called
    directly from main.
    """
    # Making sure the sample configuration file is where it's supposed to be.
    config = path_to_example("config.yml")
    if not os.path.exists(config):
        raise ValueError(
            """Sample config.yml configuration file can't be located at {},
            please ensure abc-classroom has been installed
            correctly""".format(
                config
            )
        )
    # Assigning the custom folder name if applicable
    if " " in course_name:
        raise ValueError(
            "Spaces not allowed in custom course name: {}. Please use hyphens instead.".format(
                course_name
            )
        )
    if working_dir is None:
        working_dir = os.getcwd()
    main_dir = os.path.join(working_dir, course_name)
    if force and os.path.isdir(main_dir):
        rmtree(main_dir)
    # Make sure that the main_dir doesn't exist already
    if os.path.isdir(main_dir):
        raise ValueError(
            """
            Ooops! It looks like the directory {} already exists on your
            computer. You might have already run quickstart in this directory.
            Consider using a different course name, deleting the existing
            directory, or running quikstart with the -f flag to force overwrite
            the existing directory.""".format(
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
        Created abc-classroom directory structure in '{}',
        including template and cloning directories and a configuration file,
        'config.yml'. To proceed, please create / move your sample roster
        and course_materials directory into '{}' and check the config file
        settings.""".format(
            main_dir, course_name
        )
    )
