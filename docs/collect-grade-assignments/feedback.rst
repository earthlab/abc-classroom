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

By default ``abc-feedback`` only copies the files to each cloned student repo,
and commits the changes in your local directory. It only pushes to github if
you use the ``--github`` flag.

Remove Hidden Tests in Html Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you are using ``nbgrader`` to create your feedback reports, all of the hidden tests
(which will likely include the assignment answers) will be included in the default
feedback report. ``Nbgrader`` relies on a database where all comments and grades are
stored. If you wish to remove the hidden tests from your output html files, you
can use the ``--scrub`` argument. Scrub will remove all code as follows::

    ### BEGIN HIDDEN TESTS
    # code here will be removed
    a = "this code will be scrubbed"
    ### END HIDDEN TESTS

You can use the scrub comment as follows::

    abc-feedback assignment-name --scrub

Command-line Arguments
======================

Run ``abc-feedback -h`` to see details of command line parameters::

  $ abc-feedback -h
  usage: abc-feedback [-h] [--github] [--scrub] assignment-name

  Copies feedback reports to local student repositories and (optionally) pushes to github. Assumes files
  are in the directory course_materials/feedback/student/assignment. Copies all files in the source
  directory.

  positional arguments:
    assignment  Name of assignment. Must match name in course_materials feedback directory

  optional arguments:
    -h, --help  show this help message and exit
    --github    Also pushes files to student repositories on GitHub (default = False; only copies files to
                local repos)
    --scrub     Cleans out hidden tests from notebooks when used.
