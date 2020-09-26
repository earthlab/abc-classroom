# from pathlib import Path
#
# import abcclassroom.feedback as abcfeedback
#
# # import abcclassroom.config as cf
#
#
# def test_html_copies(default_config, tmp_path):
#     """Test that an html feedback report added to a repo copies over. """
#
#     assignment = "assignment1"
#     default_config["course_directory"] = tmp_path
#
#     # Setup student cloned directory with a single notebook
#     # (this could be a fixture?)
#     clone_path = Path(
#         tmp_path, "cloned_repos", assignment, "assignment1-test-student"
#     )
#     clone_path.mkdir(parents=True)
#     clone_path.joinpath("assignment1-test-student.ipynb").touch()
#
#     # Setup feedback directory
#     feedback_path = Path(
#         tmp_path, "nbgrader", "feedback", "test-student", assignment
#     )
#     feedback_path.mkdir(parents=True)
#     feedback_path.joinpath("assignment1-test-student.html").touch()
#
#     # Return feedback -- this requires a config file
#     abcfeedback.copy_feedback_files(assignment, github=None)
#
#     # Add html file to one student's directory
#
#     # Run abc-feedback
