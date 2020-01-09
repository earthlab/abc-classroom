"""
abc-classroom.template
======================

"""
import os
import sys
import shutil
from pathlib import Path

from . import config as cf
from . import github
from . import utils


def new_update_template(args):
    """
    Creates or updates an assignment template repository. Implementation of both the new_template and update_template console scripts (which perform the same basic functions but with different command line arguments and defaults).

    Creates an assignment entry in the config file if one does not already exist.
    """
    print("Loading configuration from config.yml")
    config = cf.get_config()
    template_dir = cf.get_config_option(config, "template_dir", True)

    # create the local git repository
    assignment = args.assignment
    template_repo_path = create_template_dir(config, assignment, args.mode)
    print("repo path: {}".format(template_repo_path))
    copy_assignment_files(config, template_repo_path, assignment)
    create_extra_files(config, template_repo_path, assignment)
    github.init_and_commit(template_repo_path, args.custom_message)

    # create / append assignment entry in config
    course_dir = cf.get_config_option(config, "course_directory", True)
    cf.set_config_option(
        config,
        "assignments",
        assignment,
        append_value=True,
        configpath=course_dir,
    )

    # optional github steps
    if args.github:
        organization = cf.get_config_option(config, "organization", True)
        repo_name = os.path.basename(template_repo_path)
        token = cf.get_github_auth()["token"]

        create_or_update_remote(
            template_repo_path, organization, repo_name, token
        )


def create_or_update_remote(
    template_repo_path, organization, repo_name, token
):
    remote_exists = github.remote_repo_exists(organization, repo_name, token)
    if not remote_exists:
        print("Creating remote repo {}".format(repo_name))
        # create the remote repo on github and push the local repo
        # (will print error and return if repo already exists)
        github.create_repo(organization, repo_name, token)

    try:
        github.add_remote(template_repo_path, organization, repo_name, token)
    except RuntimeError as e:
        print("Remote already added to local repository")
        pass

    print("Pushing any changes to remote repository on GitHub")
    try:
        github.push_to_github(template_repo_path, "master")
    except RuntimeError as e:
        print(
            "Push to github failed. This is usually because there are changes on the remote that you do not have locally. Here is the github error:"
        )
        print(e)


def create_template_dir(config, assignment, mode="fail"):
    """
    Creates a new directory in template_dir that will become the
    template repository for the assignment. If directory exists and mode is  merge, do nothing. If directory exists and mode is delete, remove contents but leave .git directory.
    """
    course_dir = cf.get_config_option(config, "course_directory", True)
    template_parent_dir = cf.get_config_option(config, "template_dir", True)
    parent_path = utils.get_abspath(template_parent_dir, course_dir)

    # check that parent directory for templates exists, and create it if it does not
    if not os.path.isdir(parent_path):
        print(
            "Creating new directory for template repos at {}".format(
                parent_path
            )
        )
        os.mkdir(parent_path)

    repo_name = assignment + "-template"
    template_path = Path(parent_path, repo_name)
    dir_exists = template_path.is_dir()
    if not dir_exists:
        template_path.mkdir()
        print("Creating new template repo at {}".format(template_path))
    else:
        if mode == "fail":
            print(
                "Directory {} already exists; re-run with '--mode merge' or '--mode delete', or delete / move directory before re-running".format(
                    template_path
                )
            )
            sys.exit(1)
        elif mode == "merge":
            print(
                "Template directory {} already exists; will keep directory but overwrite existing files with same names".format(
                    template_path
                )
            )
        else:
            # mode == delete
            print(
                "Template directory {} already exists; deleting existing files but keeping .git directory, if exists.".format(
                    template_path
                )
            )
            # temporarily move the .git dir to the parent of the template_path
            gitdir = Path(template_path, ".git")
            if gitdir.exists():
                target = Path(Path(template_path).parent, ".tempgit")
                gitdir.replace(target)

                # remove template_path and re-create with same name
                shutil.rmtree(template_path)
                Path(template_path).mkdir()

                # and then move the .git dir back
                target.replace(gitdir)

    return template_path


def copy_assignment_files(config, template_repo, assignment):
    """Copy all of the files from the course_materials/release directory for the
    assignment into the template repo directory.
    """

    print("Getting assignment files")
    course_dir = cf.get_config_option(config, "course_directory", True)
    materials_dir = cf.get_config_option(config, "course_materials", True)
    parent_path = utils.get_abspath(materials_dir, course_dir)
    release_dir = os.path.join(parent_path, "release", assignment)
    if not os.path.exists(release_dir):
        print(
            "release directory {} does not exist; exiting\n".format(
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
        # overwrites if fpath exists in template_repo
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
                if assignment:
                    first_line = "# {}".format(assignment)
                else:
                    first_line = "# README"
                contents.insert(0, first_line)
            utils.write_file(template_repo, file, contents)
