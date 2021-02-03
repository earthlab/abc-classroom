"""
abc-classroom.template
======================

"""
import os
import shutil
from pathlib import Path
import ntpath

from . import config as cf
from . import github as gh
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
    create_template(
        mode=args.mode,
        push_to_github=args.github,
        custom_message=args.custom_message,
        assignment_name=args.assignment,
    )


def create_template(
    assignment_name, mode="fail", push_to_github=False, custom_message=False
):
    """
    Classroom package function that creates or updates an assignment template
    repository. Implementation of
    both the new_template and update_template console scripts (which perform
    the same basic functions but with different command line arguments and
    defaults).

    Creates an assignment entry in the config file if one does not already
    exist.

    Parameters
    ----------
    push_to_github : boolean
        True if you want to push to GH
    mode : merge, fail
    custom message : boolean (default = False)
        True if you want to push to github.
    assignment_name : string
        name of the assignment
    """

    print("Loading configuration from config.yml")
    config = cf.get_config()

    course_dir = cf.get_config_option(config, "course_directory", True)
    materials_dir = cf.get_config_option(config, "course_materials", True)
    # I think this should be moved above where it created the directory
    parent_path = utils.get_abspath(materials_dir, course_dir)
    release_dir = Path(parent_path, "release", assignment_name)

    # First check to see if there is an assignment with that name in the
    # release directory, if not, fail gracefully
    try:
        release_dir.resolve(strict=True)
    except FileNotFoundError:
        raise FileNotFoundError(
            "Oops, it looks like the assignment - {} - doesn't yet"
            " exist in the location that I expected it: {}. Did "
            "you spell the assignment name correctly and is there a "
            "directory at this path: "
            "?".format(assignment_name, release_dir)
        )

    # If the assignment exists, then create dirs and copy stuff
    template_repo_path = create_template_dir(config, assignment_name, mode)
    copy_assignment_files(config, template_repo_path, release_dir)
    # This is still copying DS_Store -- let's revisit
    copy_extra_files(config, template_repo_path, assignment_name)

    # Create the local git repository and commit changes
    gh.init_and_commit(template_repo_path, custom_message)

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
        token = cf.get_github_auth()["access_token"]

        create_or_update_remote(
            template_repo_path, organization, repo_name, token
        )


def create_or_update_remote(
    template_repo_path, organization, repo_name, token
):
    """
    Push template repo to github creating a new repository or update the
    repo's contents

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
    remote_exists = gh.remote_repo_exists(organization, repo_name, token)
    if not remote_exists:
        print("Creating remote repo {}".format(repo_name))
        # create the remote repo on github and push the local repo
        # (will print error and return if repo already exists)
        gh.create_repo(organization, repo_name, token)

    try:
        gh.add_remote(template_repo_path, organization, repo_name)
    except RuntimeError:
        print("Remote already added to local repository.")
        pass

    print("Pushing any changes to remote repository on GitHub.")
    try:
        gh.push_to_github(template_repo_path, "main")
    except RuntimeError as e:
        print(
            """Push to github failed. This is usually because there are
            changes on the remote that you do not have locally. Here is the
            github error:"""
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
            raise Exception(
                "Oops! The directory specified: {} already exists "
                "for this course; "
                "re-run with --mode merge' or '--mode delete', "
                "or delete / move directory before re-running"
                ". ".format(template_path.relative_to(course_dir))
            )
        elif mode == "merge":
            print(
                "Oops! The directory specified: {} already exists for this"
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
            # Temporarily move the .git dir to the parent of the template_path
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

    return template_path


def copy_assignment_files(config, template_path, release_dir):
    """Copy all of the files from the course_materials/release directory for the
    assignment into the template repo directory.

    Parameters
    ----------
    config: ordered dictionary
        Config file returned by ``get_config()`` that contains paths to the
        course directory, github organization and other custom options
    template_path: Pathlib Path object
        Absolute path to the template repository where the assignment files
        will be copied
    release_dir: Path object
        Path to the released assignment directory

    """

    course_dir = cf.get_config_option(config, "course_directory", True)
    # materials_dir = cf.get_config_option(config, "course_materials", True)

    # Turn this into a try / except? - or did i capture this test above?
    # TODO - Write a test for this. If it fails gracefully we can remove
    # this code
    # if not release_dir.is_dir():
    #     print(
    #         "release directory {} does not exist; exiting\n".format(
    #             release_dir
    #         )
    #     )
    #     sys.exit(1)

    nfiles = 0
    all_files = release_dir.glob("*")

    print(
        "Copying assignment files to {}: ".format(
            template_path.relative_to(course_dir)
        )
    )
    # TODO this could also use the copy files helper - thinking to put it in
    # the utils module
    # Get a list of files to ignore - maybe our default config has some
    # could have some defaults - then remove all files that we want to ignore
    files_to_ignore = cf.get_config_option(config, "files_to_ignore", True)
    files_moved = []
    for afile in all_files:
        afile = Path(afile)
        if afile.is_dir():
            # TODO: Note that as written here, moving directories will fail so
            print(
                "Oops - looks like {} is a directory. Currently I can't "
                "move that for you. Contact the abc-classroom maintainers"
                "if this is a feature that you'd "
                "like".format(afile.relative_to(course_dir))
            )
        else:
            if not ntpath.basename(afile) in files_to_ignore:
                # TODO Removed "relative_to" as This is causing issues between
                #  str  and path
                #  objects --- revisit
                print("Moving: {}".format(afile))
                # Overwrites if afile exists in template_repo
                shutil.copy(afile, template_path)
                files_moved.append(afile)
                nfiles += 1

    print(
        "Copied {} files to your template assignment git repo: {}!".format(
            nfiles, template_path
        )
    )
    print("The files copied include: {}".format(files_moved))


def copy_extra_files(config, template_repo, assignment):
    """Copy any extra files that exist the extra_files directory

    Parameters
    ----------
    config : Path
        Path to the config.yml file??
    template_repo : Path object ?
        Path to the template repo that you wish to copy files over to. ??
    assignment : string
        Name of the assignment that you want to copy files over for.

    """
    course_dir = cf.get_config_option(config, "course_directory", True)
    extra_path = Path(course_dir, "extra_files")

    # TODO - implement helper for this part
    files_to_ignore = cf.get_config_option(config, "files_to_ignore", True)

    if extra_path.is_dir():
        print("Copying extra files: ")
        for f in extra_path.iterdir():
            if not ntpath.basename(f) in files_to_ignore:
                # Move file to new location
                print(" {}".format(f.relative_to(course_dir)))
                shutil.copy(f, template_repo)

        # modify the readme with the assignment name
        readme_path = Path(template_repo, "README.md")
        if readme_path.exists():
            add_assignment_to_readme(readme_path, assignment)


def add_assignment_to_readme(path_to_readme, assignment):
    with open(path_to_readme) as readme:
        lines = readme.readlines()
        if len(lines) > 0:
            lines[0] = "# Assignment {}\n".format(assignment)
            utils.write_file(path_to_readme, lines)
