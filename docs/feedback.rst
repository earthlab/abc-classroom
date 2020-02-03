.. _abc-feedback:

Pushing feedback reports back to students
-----------------------------------------

The the final step in the **abc-classroom** workflow is pushing any feedback
from the instructor to the students through their GitHub repositories for the
assignment. Running::

  $ abc-feedback assignment-name

iterates through students in the
roster and copies any files from ``course_materials/feedback/student/assignment``
into the respository at ``cloned_dir/assignment-student``.

If you want to also push the feedback reports to the student repository on GitHub (using ``git push``) use the ``--github`` option (see below). By default,
``abc-feedback`` only copies the files locally.

Command-line arguments
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
