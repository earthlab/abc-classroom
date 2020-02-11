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
        raise FileNotFoundError(dataset_path)
    return dataset_path


def create_dir_struct(course_name="abc_course", force=False, working_dir=None):
    """
    Create a directory structure that can be used to start an abc-classroom
    course. This includes a main directory, two sub directories for templates
    and cloned files, and a start to a configuration file.

    This is the tmplementation of the abc-quickstart script; it is called
    directly from main.
    """
    # Making sure the sample configuration file is where it's supposed to be.
    try:
        config_path = path_to_example("config.yml")
    except FileNotFoundError as err:
        print(
            """Sample config.yml configuration file cannot be located at {},
        please ensure abc-classroom has been installed
        correctly""".format(
                err
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
    main_dir = Path(working_dir, course_name)

    # Check if the main_dir doesn't exist already
    if main_dir.is_dir():
        if force:
            rmtree(main_dir)
        else:
            raise FileExistsError(
                """
                Ooops! It looks like the directory {} already exists on your
                computer. You might have already run quickstart in this directory.
                Consider using a different course name, deleting the existing
                directory, or running quikstart with the -f flag to force overwrite
                the existing directory.""".format(
                    course_name
                )
            )
    # make the main course directory and copy the config file there
    main_dir.mkdir()
    copy(config_path, main_dir)

    # now we can use config functions to read / write config
    config = cf.get_config(main_dir)
    config["course_directory"] = str(main_dir)
    cf.write_config(config, main_dir)
    clone_dir = cf.get_config_option(config, "clone_dir")
    template_dir = cf.get_config_option(config, "template_dir")

    # make the required subdirectories
    Path(main_dir, clone_dir).mkdir()
    Path(main_dir, template_dir).mkdir()

    print(
        """
        Created abc-classroom directory structure in '{}',
        including template and clone directories and a configuration file,
        'config.yml'. To proceed, please create / move your course roster
        and course_materials directory into '{}' and check the config file
        settings.""".format(
            main_dir, course_name
        )
    )
