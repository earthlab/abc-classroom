"""
abc-classroom.template
======================

"""
import os
import shutil
from pathlib import Path

from . import config as cf
from . import git as abcgit
from . import github as abcgithub
from . import auth
from . import utils


def new_update_template(args):
    """
    Command line function that creates or updates an assignment template
    repository. Implementation of
    both the new_template and update_template console scripts (which perform
    the same basic functions but with different command line arguments and
    defaults).

    Creates an assignment entry in the config file if one does not already
    exist.

    Parameters
    ----------
    args : command line arguments
    """

    try:
        create_template(
            mode=args.mode,
            push_to_github=args.github,
            commit_message=args.commit_message,
            assignment_name=args.assignment,
        )
    except FileNotFoundError as fnfe:
        # if the assignment does not exist in course_materials/release
        print(fnfe)
    except FileExistsError as fee:
        # if mode = fail and assignment repository already exists
        print(fee)


def create_template(
    assignment_name,
    mode="fail",
    push_to_github=False,
    commit_message="Initial commit",
):
    """
    Classroom package function that creates or updates an assignment template
    repository. Implementation of
    both the new_template and update_template console scripts (which perform
    the same basic functions but with different command line arguments and
    defaults).

    Creates an assignment directory in template_dir if it does not exist
    already. Copies files from course_materials/release and from
    extra_files, initializes as a git repo, and commits all changes.

    Creates an assignment entry in the config file if one does not already
    exist.

    If push_to_github = True, then also pushes to github (creating the
    remote repository if it does not already exist).

    Parameters
    ----------
    push_to_github : boolean
        True if you want to push to GH
    mode : merge, fail
    commit_message : string
        Sets a custom git commit message. For new templates, default is
        "Initial commit" and for updating templates, default is
        "Updating assignment"
    assignment_name : string
        name of the assignment
    """

    print("Loading configuration from config.yml")
    try:
        config = cf.get_config()
    except (FileNotFoundError, RuntimeError) as err:
        print(err)
        return
    # Set up the path to the assignment files, which are in
    # course_dir/materials_dir/release/assignment_name
    course_dir = cf.get_config_option(config, "course_directory", True)
    materials_dir = cf.get_config_option(config, "course_materials", True)
    # I think this should be moved above where it created the directory
    parent_path = utils.get_abspath(materials_dir, course_dir)
    release_path = Path(parent_path, "release", assignment_name)

    # Check to see if there is an assignment with that name in the
    # release directory, if not, fail gracefully
    try:
        release_path.resolve(strict=True)
    except FileNotFoundError as e:
        print(e)
        raise FileNotFoundError(
            "Oops, it looks like the assignment - {} - does not exist"
            "in the location that I expected it: \n{}. \nDid "
            "you spell the assignment name correctly and is there a "
            "directory at this path?".format(assignment_name, release_path)
        )

    # If the assignment exists, then create directory
    template_repo_path = create_template_dir(config, assignment_name, mode)

    # and copy files
    copy_files_to_template_repo(
        config, template_repo_path, assignment_name, release_path
    )

    # Create the local git repository and commit changes
    abcgit.init_and_commit(template_repo_path, commit_message)

    # Create / append assignment entry in config - this should only happen if
    # the assignment above exists...
    print("Updating assignment list in config")
    course_dir = cf.get_config_option(config, "course_directory", True)
    cf.set_config_option(
        config,
        "assignments",
        assignment_name,
        append_value=True,
        configpath=course_dir,
    )

    # Optional - push files to GitHub
    if push_to_github:
        organization = cf.get_config_option(config, "organization", True)
        repo_name = os.path.basename(template_repo_path)
        token = auth.get_github_auth()["access_token"]

        create_or_update_remote(
            template_repo_path, organization, repo_name, token
        )


def create_or_update_remote(
    template_repo_path, organization, repo_name, token
):
    """
    Push template repo to GitHub. If remote does not yet exist, creates it
    before pushing.

    Parameters
    ----------
    template_repo_path : string
        The path to the template repo on your local computer.
    organization : string
        The name of the organization where your GitHub Classroom lives.
    repo_name : string
        The name of the template repository to create on GitHub
    token : github token
        Used to authenticate with GitHub via the API. Created by running
        ``abc-init``

    """
    remote_exists = abcgithub.remote_repo_exists(
        organization, repo_name, token
    )
    if not remote_exists:
        print("Creating remote repo {}".format(repo_name))
        # create the remote repo on github and push the local repo
        # (will print error and return if repo already exists)
        abcgithub.create_repo(organization, repo_name, token)

    try:
        abcgit.add_remote(template_repo_path, organization, repo_name)
    except RuntimeError:
        print("Remote already added to local repository.")
        pass

    print("Pushing any changes to remote repository on GitHub.")
    try:
        abcgit.push_to_github(template_repo_path, "main")
    except RuntimeError as e:
        print(
            """Push to github failed. This is usually because there are
            changes on the remote that you do not have locally. Here is the
            git error:"""
        )
        print(e)


def create_template_dir(config, assignment, mode="fail"):
    """
    Creates a new directory in template_dir that will become the template
    repository for the assignment. If directory exists and mode is merge,
    do nothing. If directory exists and mode is delete, remove contents but
    leave .git directory.
    """
    course_dir = cf.get_config_option(config, "course_directory", True)
    template_parent_dir = cf.get_config_option(config, "template_dir", True)
    parent_path = Path(utils.get_abspath(template_parent_dir, course_dir))

    # check that parent directory for templates exists, and create it
    # if it does not
    if not parent_path.is_dir():
        print(
            "Creating new directory for template repos at {}".format(
                parent_path.relative_to(course_dir)
            )
        )
        parent_path.mkdir()

    repo_name = assignment + "-template"
    template_path = Path(parent_path, repo_name)
    dir_exists = template_path.is_dir()
    if not dir_exists:
        template_path.mkdir()
        print(
            "Creating new template repo at {}".format(
                template_path.relative_to(course_dir)
            )
        )
    else:
        if mode == "fail":
            raise FileExistsError(
                "Oops! The directory specified: {} already exists "
                "for this course; "
                "re-run with --mode merge' or '--mode delete', "
                "or delete / move directory before re-running"
                ". ".format(template_path.relative_to(course_dir))
            )
        elif mode == "merge":
            print(
                "The directory specified: {} already exists for this"
                " course; will keep directory but overwrite existing files "
                "with same names".format(template_path.relative_to(course_dir))
            )
        else:
            # mode == delete
            print(
                """Directory {} already exists for this course; deleting
                existing files but keeping .git directory, if it
                exists.""".format(
                    template_path.relative_to(course_dir)
                )
            )
            # Temporarily move the .git dir to the parent of the
            # template_path (i.e. the template_repos dir in the config)
            # We do this to avoid issues if the local repo has already been
            # pushed to github (if we re-create a new repo, will get error
            # about unrelated histories when pushing)
            gitdir = Path(template_path, ".git")
            if gitdir.exists():
                target = Path(Path(template_path).parent, ".tempgit")
                gitdir.replace(target)

                # remove template_path and re-create with same name
                shutil.rmtree(template_path)
                Path(template_path).mkdir()

                # and then move the .git dir back
                target.replace(gitdir)
            else:
                # remove template_path and re-create with same name
                shutil.rmtree(template_path)
                Path(template_path).mkdir()

    return template_path


def copy_files_to_template_repo(
    config, template_repo_path, assignment, release_path
):
    """
    Copies files and directories for the assignment recursively into the
    local template repository. Looks in release_dir and extra_files for
    files to copy.

    If extra_files contains a readme, updates the readme with the assignment
    name.

    Excludes files and directories that match patterns in files_to_ignore.
    """

    # get config options
    files_to_ignore = cf.get_config_option(config, "files_to_ignore", False)
    course_dir = cf.get_config_option(config, "course_directory", True)

    # copy assignment-specific files
    utils.copy_files(release_path, template_repo_path, files_to_ignore)

    # copy extra_files
    extra_files_path = Path(course_dir, "extra_files")
    try:
        utils.copy_files(extra_files_path, template_repo_path, files_to_ignore)
        # and add the assignment name to the readme, if it exists
        readme_path = Path(template_repo_path, "README.md")
        if readme_path.exists():
            add_assignment_to_readme(readme_path, assignment)
    except FileNotFoundError:
        print("No extra_files directory found")
        pass


def add_assignment_to_readme(path_to_readme, assignment):
    with open(path_to_readme) as readme:
        lines = readme.readlines()
        if len(lines) > 0:
            lines[0] = "# Assignment {}\n".format(assignment)
            utils.write_file(path_to_readme, lines)
