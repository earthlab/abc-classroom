"""
abc-classroom.template
======================

"""
import os
import sys
import shutil

from . import config as cf
from . import gitutils as gitu
from . import utils


def create_template_dir(config, assignment, mode):
    """
    Creates a new directory in template_dir that will become the
    template repository for the assignment.
    """
    course_dir = cf.get_config_option(config, "course_directory", True)
    template_dir = cf.get_config_option(config, "template_dir", True)
    parent_path = utils.get_abspath(template_dir, course_dir)

    # check that course_dir/template_dir exists, and create it if it does not
    if not os.path.isdir(parent_path):
        print(
            "Creating new directory for template repos at {}".format(
                parent_path
            )
        )
        os.mkdir(parent_path)

    # Set up the name of the template repo and create the dir
    # if there is a shortname defined, use that in path
    course_name = cf.get_config_option(config, "short_coursename")
    if course_name is None:
        course_name = cf.get_config_option(config, "course_name")
    if course_name is None:
        print(
            "Error: One of course_name or short_coursename must be set in config.yml"
        )
        sys.exit(1)

    repo_name = course_name + "-" + assignment + "-template"
    template_path = os.path.join(parent_path, repo_name)
    dir_exists = os.path.exists(template_path)
    if not dir_exists:
        os.mkdir(template_path)
        print("Creating new template repo at {}".format(template_path))
    else:
        if mode == "fail":
            print(
                "Directory {} already exists; delete or move before re-running".format(
                    template_path
                )
            )
            sys.exit(1)
        if mode == "merge":
            print(
                "Template directory {} already exists but mode is 'merge'; will keep directory but overwrite existing files with same names".format(
                    template_path
                )
            )
    return template_path


def copy_assignment_files(config, template_repo, assignment):
    """Copy all of the files from the nbgrader release directory for the
    assignment into the template repo directory.
    """

    print("Getting assignment files")
    course_dir = cf.get_config_option(config, "course_directory", True)
    nbgrader_dir = cf.get_config_option(config, "nbgrader_dir", True)
    parent_path = utils.get_abspath(nbgrader_dir, course_dir)
    release_dir = os.path.join(parent_path, "release", assignment)
    if not os.path.exists(release_dir):
        print(
            "nbgrader release directory {} does not exist; exiting\n".format(
                release_dir
            )
        )
        sys.exit(1)
    nfiles = 0
    all_files = os.listdir(release_dir)
    # matched_files = match_patterns(all_files, patterns)
    for file in all_files:
        fpath = os.path.join(release_dir, file)
        print("copying {} to {}".format(fpath, template_repo))
        shutil.copy(fpath, template_repo)
        nfiles += 1
    print("Copied {} files".format(nfiles))


def create_extra_files(config, template_repo, assignment):
    """Create any extra files as specified in the config """
    extra_files = cf.get_config_option(config, "extra_files", False)
    nfiles = len(extra_files)
    print("Creating {} extra files".format(nfiles))
    for file in extra_files:
        contents = config["extra_files"][file]
        if len(contents) > 0:
            if file == "README.md":
                firstline = ""
                coursename = cf.get_config_option(config, "course_name", False)
                if assignment and coursename:
                    first_line = "# {}: {}".format(coursename, assignment)
                else:
                    first_line = "# README"
                contents.insert(0, first_line)
            utils.write_file(template_repo, file, contents)
