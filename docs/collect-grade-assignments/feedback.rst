.. _abc-feedback:

Push Feedback to GitHub Student Repos
--------------------------------------

The the final step in the **abc-classroom** workflow is pushing feedback
from the instructor to the students through their GitHub repositories for the
assignment. Running::

    abc-feedback assignment-name

1. iterates through students in the roster
2. copies files from ``course_materials/feedback/student/assignment-name`` directory into student's cloned repository located here: ``cloned_dir/assignment-student`` directory.

If you want to also push the feedback reports to the student repository on
GitHub (using ``git push``) use the ``--github`` option (see below).::

    abc-feedback assignment-name --githhub

Note that when you use the ``--github`` flag, the files are added to the repo as a
direct comment (not a pull request). So you will want to tell the students to
check their repo after pushing out the feedback files.

By default ``abc-feedback`` only copies the files to each cloned student repo
in your local directory.

Command-line Arguments
======================

Run ``abc-feedback -h`` to see details of command line parameters::

  $ abc-feedback -h
  usage: abc-feedback [-h] [--github] assignment

  Copies feedback reports to local student repositories and (optionally) pushes to github. Assumes files
  are in the directory course_materials/feedback/student/assignment. Copies all files in the source
  directory.

  positional arguments:
    assignment  Name of assignment. Must match name in course_materials feedback directory

  optional arguments:
    -h, --help  show this help message and exit
    --github    Also pushes files to student repositories on GitHub (default = False; only copies files to
                local repos)
