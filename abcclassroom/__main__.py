import argparse
import sys

from argparse import ArgumentParser
from getpass import getpass

import github3 as gh3

from . import template
from . import feedback as fdback
from . import config as cf
from .quickstart import create_dir_struct
from .clone import clone_student_repos


def quickstart():
    parser = ArgumentParser(description=create_dir_struct.__doc__)
    parser.add_argument(
        "course_name",
        nargs="?",
        default="course-directory",
        help="Name of course. Use dashes-rather-than spaces for your name.",
    )
    parser.add_argument(
        "-f",
        action="store_true",
        help="""Option to override the existing folder structure made by this
        function previously.""",
    )
    args = parser.parse_args()
    course_name = args.course_name
    create_dir_struct(course_name, args.f)


def init():
    """
    Setup GitHub credentials for later. Make sure that there is a valid
    GitHub authentication yaml file, and if there isn't, create a valid file.
    """

    gh_auth = cf.get_github_auth()

    # check the token we have is still valid by attempting to login with
    # the token we have if this fails we need a new one
    if gh_auth.get("token") is not None:
        try:
            # We have to use the GitHub API to find out if our login
            # credentials actually work, this is why we call `me()`
            gh = gh3.login(token=gh_auth["token"])
            gh.me()
            print("GitHub token present and valid.")
            return

        except gh3.exceptions.AuthenticationFailed:
            # need to get a new token
            pass

    print("GitHub token is missing or expired. Populating")
    user = input("GitHub username: ")
    password = ""

    while not password:
        password = getpass("Password for {0}: ".format(user))

    note = "ABC-classroom workflow helper"
    note_url = "https://github.com/earthlab/abc-classroom"
    scopes = ["repo", "read:user"]

    def two_factor():
        code = ""
        while not code:
            # The user could accidentally press Enter before being ready,
            # let's protect them from doing that.
            code = input("Enter 2FA code: ")
        return code

    gh = gh3.github.GitHub()
    gh.login(username=user, password=password, two_factor_callback=two_factor)
    try:
        auth = gh.authorize(user, password, scopes, note, note_url)

        cf.set_github_auth({"token": auth.token, "id": auth.id})

    except gh3.exceptions.UnprocessableEntity:
        print(
            "Failed to create a access token for you. Please visit "
            "https://github.com/settings/tokens and delete any access "
            "token with the name 'ABC-classroom workflow helper' and run "
            "`abc-init` again."
        )
        sys.exit(1)


def clone():
    """
    Clone the student repositories for the assignment and (optionall) copies
    notebook files into the course_materials 'submitted' directory. Clones into
    the clone_dir directory, as specified in config.yml.

    Requires that you have filename of student roster
    defined in config.yml and that the roster file exists.

    By default, if a local directory with the name of the repo already exists,
    pulls from github to update. Use the --skip-existing flag if you don't want
    to update existing repos.
    """
    parser = argparse.ArgumentParser(description=clone.__doc__)
    parser.add_argument(
        "assignment",
        help="""Name of assignment. Must match assignment name in
        course_materials directories""",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="""Do not attempt to update repositories that have already been
        cloned.""",
    )
    args = parser.parse_args()

    clone_student_repos(args)


def feedback():
    """
    Copies feedback reports to local student repositories and (optionally)
    pushes to github. Assumes files are in the directory
    course_materials/feedback/student/assignment. Copies all files in the
    source directory.
    """
    parser = argparse.ArgumentParser(description=feedback.__doc__)
    parser.add_argument(
        "assignment",
        help="""Name of assignment. Must match name in course_materials
        feedback directory""",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="""Also pushes files to student repositories on GitHub
        (default = False; only copies files to local repos)""",
    )
    parser.add_argument(
        "--scrub",
        action="store_true",
        help="""Cleans out hidden tests from notebooks when used.""",
    )
    args = parser.parse_args()
    fdback.copy_feedback(args)


def new_template():
    """
    Create a new assignment template repository: creates local directory,
    copy / create required files, intialize as git repo, and (optionally)
    create remote repo on GitHub and push local repo to GitHub. Will open
    git editor to ask for commit message if custom message requested.
    """
    parser = argparse.ArgumentParser(description=new_template.__doc__)
    parser.add_argument(
        "assignment",
        help="""Name of assignment. Must match name in
        course_materials/release directory""",
    )
    parser.add_argument(
        "--custom-message",
        action="store_true",
        help="""Use a custom commit message for git. Will open the default
        git text editor for entry (if not set, uses default message 'Initial
        commit').""",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="""Also perform the GitHub operations (create remote repo on
        GitHub and push to remote (by default, only does local repository
        setup)""",
    )
    parser.add_argument(
        "--mode",
        choices=["delete", "fail", "merge"],
        default="fail",
        help="""Action if template directory already exists. Choices are:
        delete = delete contents before proceeding (except .git directory);
        merge = keep existing dir, overwrite existing files, add new files
        (Default = fail).""",
    )
    args = parser.parse_args()

    template.new_update_template(args)


def update_template():
    """
    Updates an existing assignment template repository: update / add new and
    changed files, then push local changes to GitHub. Will open git editor
    to ask for commit message.
    """
    parser = argparse.ArgumentParser(description=update_template.__doc__)
    parser.add_argument(
        "assignment",
        help="""Name of assignment. Must match name in course_materials/release
        directory""",
    )
    parser.add_argument(
        "--mode",
        choices=["delete", "merge"],
        default="merge",
        help="""What to do with existing contents of template directory.
        Choices are: delete = remove contents before proceeding (leaving .git
        directory); merge = overwrite existing files add new files
        (Default = merge).""",
    )
    args = parser.parse_args()
    # now set the additional args (so that it matches the keys in add_template
    # and we can use the same implementation methods)
    setattr(args, "github", True)
    setattr(args, "custom_message", True)
    template.new_update_template(args)


#########################################
# Everything below here - grade, author, and distribute methods - is from
# before the re-factor, when grading happened
# within abcclassroom. Keeping for reference, but with no guarantees that
# this code is functional.
########################################

# def grade():
#     """Grade student's work"""
#     parser = argparse.ArgumentParser(description="Grade student repository.")
#     parser.add_argument(
#         "--date",
#         default=datetime.datetime.today().date(),
#         type=valid_date,
#         help=("Assumed date when grading assignments " "(default: today)"),
#     )
#     parser.add_argument(
#         "--student",
#         default=None,
#         action="append",
#         help=(
#             "Student name to grade, use flag multiple times "
#             "to select several students "
#             "(default: all students)"
#         ),
#     )
#     parser.add_argument(
#         "--assignment",
#         default=None,
#         action="append",
#         help=(
#             "Assignment to grade, use flag multiple times "
#             "to select several assignments "
#             "(default: all assignments)"
#         ),
#     )
#     args = parser.parse_args()
#
#     now = args.date
#
#     config = get_config()
#     course = config["courseName"]
#
#     if args.student is None:
#         students = config["students"]
#     else:
#         students = args.student
#
#     if args.assignment is None:
#         assignments = config["assignments"]
#     else:
#         assignments = args.assignment
#
#     for student in students:
#         print("Fetching work for %s..." % student)
#         cwd = P("graded", student)
#
#         # always delete and recreate student's directories
#         if os.path.exists(cwd):
#             shutil.rmtree(cwd)
#         os.makedirs(cwd)
#
#         # Use HTTPS and tokens to avoid access problems
#         # `git clone https://<token>@github.com/owner/repo.git`
#         fetch_command = [
#             "git",
#             "clone",
#             "https://{}@github.com/{}/{}-{}.git".format(
#                 get_github_auth()["token"],
#                 config["organisation"],
#                 course,
#                 student,
#             ),
#             student,
#         ]
#         try:
#             subprocess.run(
#                 fetch_command,
#                 cwd=P("graded"),
#                 check=True,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#             )
#         except subprocess.CalledProcessError as err:
#             print(
#               "Fetching work with '%s' failed:" % " ".join(fetch_command)
#             )
#             print()
#             print(err.stderr.decode("utf-8"))
#             print()
#             print("Skipping this student.")
#             continue
#
#         print("Grading work...")
#         for assignment in assignments:
#             # only grade assignments that are due or have been explicitly
#             # requested by command-line flag
#             deadline_date = config["assignments"][assignment]["deadline"]
#             if deadline_date > now and args.assignment is None:
#                 print('Skipping assignment "{}".'.format(assignment))
#
#             # remove check files so we only use a clean copy from this repo
#             # instead of trusting students
#             for notebook in glob.glob(
#                 P("graded", student, "%s/*.ipynb" % assignment)
#             ):
#                 print("Grading {}".format(notebook))
#                 notebook = op.split(notebook)[-1]
#
#                 tests_path = P(
#                     "graded", student, assignment, op.splitext(notebook)[0]
#                 )
#                 if os.path.exists(tests_path):
#                     shutil.rmtree(tests_path)
#
#                 autograder_path = P(
#                     "autograder", assignment, op.splitext(notebook)[0]
#                 )
#                 copytree(autograder_path, tests_path)
#
#                 results = ok.grade_notebook(
#                     P("graded", student, assignment, notebook)
#                 )
#
#                 print("Points:")
#                 for res in results:
#                     print(res)
#
#             print(
#                 "🎉 Top marks for {} on assignment {}.".format(
#                     student, assignment
#                 )
#             )
#         print()
#
#
# def distribute():
#     """Create or update student repositories"""
#     parser = argparse.ArgumentParser(
#         description="Distribute work to students"
#         )
#     parser.add_argument(
#         "--template",
#         action="store_true",
#         help="Create template repository only (default: False)",
#     )
#     args = parser.parse_args()
#
#     student_repo_template = P("student")
#
#     print("Using %s to create the student template." % student_repo_template)
#     print("Loading configuration from config.yml")
#
#     config = get_config()
#
#     if args.template:
#         print("Creating template repository.")
#         repo_name = "{}-{}".format(config["courseName"], "template")
#         with tempfile.TemporaryDirectory() as d:
#             copytree(P("student"), d)
#             gitu.git_init(d)
#             gitu.commit_all_changes(d, "Initial commit")
#             try:
#                 gitu.create_repo(
#                     config["organisation"],
#                     repo_name,
#                     d,
#                     get_github_auth()["token"],
#                 )
#             except gh3.exceptions.UnprocessableEntity as e:
#                 print(e.msg)
#                 print(
#                     "This is probably because the template repository "
#                     "already exists."
#                 )
#
#         print(
#             "Visit https://github.com/{}/{}".format(
#                 config["organisation"], repo_name
#             )
#         )
#
#     else:
#         default_message = """
#         # Please enter the commit message for your changes. Lines starting
#         # with '#' will be ignored, and an empty message aborts the commit.
#         # This message will be used as commit and Pull Request message."""
#         message = input_editor(default_message)
#         message = "\n".join(
#             [
#                 line
#                 for line in message.split("\n")
#                 if not line.strip().startswith("#")
#             ]
#         )
#
#         if not message:
#             print("Empty commit message, exiting.")
#             sys.exit(1)
#
#         for student in config["students"]:
#             print("Fetching work for %s..." % student)
#
#             try:
#                 gitu.check_student_repo_exists(
#                     config["organisation"],
#                     config["courseName"],
#                     student,
#                     token=get_github_auth()["token"],
#                 )
#             except gh3.exceptions.NotFoundError as e:
#                 print(
#                     "Student {} does not have a repository for this "
#                     "course, maybe they have not accepted the invitation "
#                     "yet? Skipping them for now.".format(student)
#                 )
#                 continue
#
#             with tempfile.TemporaryDirectory() as d:
#                 student_dir = gitu.fetch_student(
#                     config["organisation"],
#                     config["courseName"],
#                     student,
#                     directory=d,
#                     token=get_github_auth()["token"],
#                 )
#                 # Copy assignment related files to the template repository
#                 copytree(P("student"), student_dir)
#
#                 if gitu.repo_changed(student_dir):
#                     # only close outstanding PRs if we are about to make a
#                     # new PR. Otherwise we can skip this.
#                     repo = "{}-{}".format(config["courseName"], student)
#                     gitu.close_existing_pullrequests(
#                         config["organisation"],
#                         repo,
#                         token=get_github_auth()["token"],
#                     )
#
#                     branch = gitu.new_branch(student_dir)
#
#                     gitu.commit_all_changes(student_dir, message)
#                     gitu.push_to_github(student_dir, branch)
#                     gitu.create_pr(
#                         config["organisation"],
#                         repo,
#                         branch,
#                         message,
#                         get_github_auth()["token"],
#                     )
#
#                 else:
#                     print("Everything up to date.")
#
#
# def author():
#     """Create student repository and autograding tests"""
#     parser = argparse.ArgumentParser(
#         description="Author student repository."
#         )
#     parser.add_argument(
#         "--date",
#         default=datetime.datetime.today().date(),
#         type=valid_date,
#         help=("Assumed date when preparing assignments " "(default: today)"),
#     )
#     args = parser.parse_args()
#
#     config = get_config()
#     now = args.date
#
#     if os.path.exists(P("student")):
#         shutil.rmtree(P("student"))
#     os.makedirs(P("student"))
#
#     if os.path.exists(P("autograder")):
#         shutil.rmtree(P("autograder"))
#
#     for assignment in config["assignments"]:
#         release_date = config["assignments"][assignment]["release"]
#         if release_date > now:
#             continue
#
#         student_path = P("student", assignment)
#         master_path = P("master", assignment)
#
#         if not os.path.isdir(master_path):
#             print(
#                 "Error: There is no material in '{}' for "
#                 "assignment '{}'".format(master_path, assignment)
#             )
#             sys.exit(1)
#
#         # copy over everything, including master notebooks. They will be
#         # overwritten by split_notebook() below
#         shutil.copytree(master_path, student_path)
#
#         if os.path.exists(P("student", assignment, ".ipynb_checkpoints")):
#             shutil.rmtree(P("student", assignment, ".ipynb_checkpoints"))
#
#         for notebook in glob.glob(P("master/%s/*.ipynb" % assignment)):
#            split_notebook(
#                notebook,
#                student_path,
#                P("autograder",
#                assignment)
#            )
#
#     # Create additional files
#     for target, source in config["extra_files"].items():
#         shutil.copyfile(P(source), P("student", target))
#
#     # Create the grading token file which is used by the notebook bot
#     # to access the CircleCI build artefacts
#     grading_token = P("student", ".grading.token")
#     with open(grading_token, "w") as f:
#         f.write(config["tokens"]["circleci"])
#
#     # Create the required CircleCI configuration
#     # the template only needs the basename, not the .ipynb extension
#     notebook_paths = [f[:-6] for f in find_notebooks(P("student"))]
#     circleci = render_circleci_template(notebook_paths)
#
#     os.makedirs(P("student", ".circleci"))
#     circleci_yml = P("student", ".circleci", "config.yml")
#     with open(circleci_yml, "w") as f:
#         f.write(circleci)
#
#     print(
#         "Inspect `{}/` to check it looks as you "
#         "expect.".format(P("student"))
#     )
