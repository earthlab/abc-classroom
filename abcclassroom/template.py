"""
abc-classroom.template
===================

"""
import os
import sys
import shutil

from . import config as cf
from . import git_utils as gitu
from . import utils

def create_template_dir(config, assignment):
    """
    Creates a new directory in template_dir that will become the template
    repository for the assignment.
    """
    template_dir = cf.get_config_option(config,"template_dir",True)

    # check if the top-level template_dir exists, and create it if it does not
    if not os.path.isdir(template_dir):
        print("Creating new directory for template repos at {}".format(template_dir))
        os.mkdir(template_dir)
    # Set up the name of the template repo and create the dir
    # if there is a shortname defined, use that in path
    course_name = cf.get_config_option(config,"short_coursename")
    if course_name is None:
        course_name = cf.get_config_option(config,"course_name")
    if course_name is None:
        print("Error: One of course_name or short_coursename must be set in config.yml")
        sys.exit(1)

    repo_name = course_name + '-' + assignment + '-template'
    template_dir_path = os.path.join(template_dir,repo_name)
    try:
        os.mkdir(template_dir_path)
        print("Creating new template repo at {}".format(template_dir_path))
    except FileExistsError as fee:
        print("Directory {} already exists; delete or move before re-running".format(template_dir_path))
        sys.exit(1)
    return template_dir_path

def copy_assigment_files(config, template_repo_name, assignment):
    """Copy all of the files from the nbgrader release directory for the
    assignment into the template repo directory.
    """

    print("Getting assignment files")
    nbgrader_dir = cf.get_config_option(config,"nbgrader_dir",True)
    release_dir = os.path.join(nbgrader_dir,'release', assignment)
    if not os.path.exists(release_dir):
        print("nbgrader release directory {} does not exist; exiting\n".format(release_dir))
        sys.exit(1)
    nfiles = 0
    all_files = os.listdir(release_dir)
    #matched_files = match_patterns(all_files, patterns)
    for file in all_files:
        fpath = os.path.join(release_dir,file)
        print("copying {} to {}".format(fpath,template_repo_name))
        shutil.copy(fpath,template_repo_name)
        nfiles += 1
    print("Copied {} files".format(nfiles))

def create_extra_files(config, template_repo_name, assignment):
    """Create any extra files as specified in the config """
    extra_files = cf.get_config_option(config,"extra_files",False)
    nfiles = len(extra_files)
    print("Creating {} extra files".format(nfiles))
    for file in extra_files:
        contents = config["extra_files"][file]
        if len(contents)>0:
            if file == "README.md":
                firstline = ""
                coursename = cf.get_config_option(config,"course_name",False)
                if assignment and coursename:
                    first_line = "# {}: {}".format(assignment, coursename)
                else:
                    first_line = "# README"
                contents.insert(0,first_line)
            utils.write_file(template_repo_name,file,contents)

def do_local_git_things(template_dir):
    """Run git init, git add, git commit on the local template repository
    directory. Only add and commit if the repo has changed.
    """
    # local git things - initialize, add, commit
    gitu.git_init(template_dir)
    if gitu.repo_changed(template_dir):
        message = gitu.get_commit_message()
        if not message:
            print("Empty commit message, exiting.")
            sys.exit(1)
        gitu.commit_all_changes(template_dir, message)
