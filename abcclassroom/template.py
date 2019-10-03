"""
abc-classroom.template
===================

"""
from . import config as cf
from . import github as GH

def create_template_dir(config):
    template_dir = cf.get_config_option(config,"template_dir",True)
    organization = cf.get_config_option(config,"organization",True)
    assignment = cf.get_config_option(config,"assignment",True)
    # Set up the name of the template repo and create the dir
    orgname = organization
    # if there is a shortname defined, use that in path
    if exists "organization-shortname" in config:
        orgname = config["organization-shortname"]
    template_repo_name = orgname + '-' + assignment + '-template'
    template_dir = os.path.join(template_dir,template_repo_name)
    try:
        os.mkdir(template_repo_name)
        print("Creating new directory at {}".format(template_repo_name))
    except FileExistsError as fee:
        print("directory {} already exists; delete or move before re-running".format(template_repo_name))
        sys.exit(1)
    return template_repo_name

def match_patterns(target_list, pattern_list):
    """Return the list of strings in target_list that match any of the
    Unix-style wildcard patterns in pattern_list
    """
    matches = []
    for p in pattern_list:
        matches.extend(fnmatch.filter(target_list, pattern))
    return matches

def copy_assigment_files(config, template_repo_name):
    """Copy all of the required files into the template repo directory.

    Required files are those in the nbgrader release/assignment dir that
    match the patterns listed in the config.
    """

    print("Getting assignment files")
    nbgrader_dir = cf.get_config_option(config,"nbgrader_dir",True)
    release_dir = os.path.join(nbgrader_dir,'release', assignment)
    if not os.path.exists(release_dir):
        print("nbgrader release directory {} does not exist; exiting\n".format(release_dir))
        sys.exit(1)
    patterns = cf.get_config_option(config,"template_patterns",False)
    if len(patterns) == 0:
        print(
            "Warning: No template_patterns specified; no files "
            "will be copied to template repository"
            )
    else:
        nfiles = 0
        all_files = os.listdir(release_dir)
        matched_files = match_patterns(all_files, patterns)
        for f in matched_files:
            fpath = os.path.join(release_dir,file)
            print("copying {} to {}".format(fpath,template_repo_name))
            shutil.copy(fpath,template_repo_name)
            nfiles += 1
        print("Copied {} files".format(nfiles))

def create_extra_files(config, template_dir):
    """Create any extra files as specified in the config """
    extra_files = cf.get_config_option(config,"extra_files",False)
    for file in extra_files:
        contents = config["extra_files"][file]
        if len(contents)>0:
            if file == "README.md":
                firstline = ""
                assignment = cf.get_config_option(config,"assignment",False)
                coursename = cf.get_config_option(config,"course_name",False)
                if assignment and coursename:
                    first_line = "# {}: {}\n".format(assignment, coursename)
                else:
                    first_line = "# README"
                contents.insert(0,first_line)
            write_file(template_dir,file,contents)

def do_local_git_things(template_dir):
    """Run git init, git add, git commit on the local template repository
    directory. Only add and commit if the repo has changed.
    """
    # local git things - initialize, add, commit
    GH.git_init(template_dir)
    if GH.repo_changed(template_dir):
        message = get_commit_message()
        if not message:
            print("Empty commit message, exiting.")
            sys.exit(1)
        GH.commit_all_changes(template_dir, message)
