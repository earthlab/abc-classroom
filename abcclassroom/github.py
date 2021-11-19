"""
abc-classroom.github
====================
"""

# Methods for accessing the GitHub API. See auth.py for methods
# related to setting up authorization and git.py
# for command line git operations.

import github3 as gh3


def remote_repo_exists(org, repository, token=None):
    """Check if the remote repository exists for the organization."""

    try:
        g = gh3.login(token=token)
        g.repository(org, repository)

    except Exception:
        return False

    return True


def create_repo(org, repository, token):
    """Create a repository in the provided GitHub organization."""
    github_obj = gh3.login(token=token)
    organization = github_obj.organization(org)
    print(
        "Creating new repository {} at https://github.com/{}".format(
            repository, org
        )
    )
    try:
        organization.create_repository(repository)
    except gh3.exceptions.UnprocessableEntity:
        print(
            "Error: organization {} already has a repository named {}".format(
                org, repository
            )
        )


###################################################
# Methods below are from before the re-factoring.
# Retaining for reference, but with no guarantee
# about correct function.


# def check_student_repo_exists(org, course, student, token=None):
#     """Check if the student has a repository for the course.
#
#     It happens that students delete their repository or do not accept the
#     invitation to the course. In either case they will not have a repository
#     yet.
#     """
#     # temporarily change log level of github3.py as it prints weird messages
#     # XXX could be done more nicely with a context manager maybe
#     gh3_log = logging.getLogger("github3")
#     old_level = gh3_log.level
#     gh3_log.setLevel("ERROR")
#
#     try:
#         g = gh3.login(token=token)
#         repository = "{}-{}".format(course, student)
#         g.repository(org, repository)
#
#     except Exception as e:
#         raise e
#
#     finally:
#         gh3_log.setLevel(old_level)
#
#
# def close_existing_pullrequests(
#     org, repository, branch_base="new-material-", token=None
# ):
#     """Close all oustanding course material update Pull Requests
#
#     If there are any PRs open in a student's repository that originate from
#     a branch starting with `branch_base` as name and created by the user
#     we are logged in we close them.
#     """
#     g = gh3.login(token=token)
#     me = g.me()
#     repo = g.repository(org, repository)
#     for pr in repo.pull_requests(state="open"):
#         origin = pr.head.label
#         origin_repo, origin_branch = origin.split(":")
#         if origin_branch.startswith(branch_base) and pr.user == me:
#             pr.create_comment(
#                 "Closed in favor of a new Pull Request to "
#                 "bring you up-to-date."
#             )
#             pr.close()
#
#
# def create_pr(org, repository, branch, message, token):
#     """Create a Pull Request with changes from branch"""
#     msg_parts = message.split("\n\n")
#     if len(msg_parts) == 1:
#         title = msg = msg_parts[0]
#     else:
#         title = msg_parts[0]
#         msg = "\n\n".join(msg_parts[1:])
#
#     g = gh3.login(token=token)
#     repo = g.repository(org, repository)
#     repo.create_pull(title, "master", branch, msg)
#
#
# def fetch_student(org, course, student, directory, token=None):
#     """Fetch course repository for `student` from `org`
#
#     The repository will be cloned into a sub-directory in `directory`.
#
#     Returns the directory in which to find the students work.
#     """
#     # use ssh if there is no token
#     if token is None:
#         fetch_command = [
#             "git",
#             "clone",
#             "git@github.com:{}/{}-{}.git".format(org, course, student),
#         ]
#     else:
#         fetch_command = [
#             "git",
#             "clone",
#             "https://{}@github.com/{}/{}-{}.git".format(
#                 token, org, course, student
#             ),
#         ]
#     subprocess.run(
#         fetch_command,
#         cwd=directory,
#         check=True,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#
#     return os.path.join(directory, "{}-{}".format(course, student))
