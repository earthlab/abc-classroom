.. _abc-clone:

Collecting materials from students
----------------------------------

Once the students have pushed their completed assignments to their GitHub
repositories, the `abc-clone` script retrieves the materials::

  $ abc-clone assignment-name

This does two things - cloning the repos, then copying the files.

**Cloning the repositories**

Using the ``github_username`` column in the student roster, the assignment name
provided as a command line argument, and the GitHub organization set in
``config.yml``, the script clones each student repository using the URL:

    ``git@github.com:github-organization/assignment-student.git``

into the ``clone_dir`` directory as specified in ``config.yml``.

If a git repository with the same name already exists in ``clone_dir``,
**abc-classroom** updates the repo using ``git-pull`` (unless you specify to skip
existing repos, see comand-line arguments, below).

**Copying the assignment files**

Once the repos are cloned, the script copies the files from the local
repository to the course materials directory. For each student, copy all files
from ``clone_dir/assignment-student`` into:

    ``course_materials/submitted/student/assignment``

where ``course_materials`` is defined in ``config.yml``. Will create
subdirectories of ``course_materials`` as needed.

Command-line arguments
======================

Run ``abc-clone -h`` to see details of command line parameters::

  $ abc-clone -h

  usage: abc-clone [-h] [--skip-existing] assignment

  Clone the student repositories for the assignment and (optionall) copies
  notebook files into the course_materials 'submitted' directory. Clones into the
  clone_dir directory, as specified in config.yml. Requires that you have
  filename of student roster defined in config.yml and that the roster file
  exists. By default, if a local directory with the name of the repo already
  exists, pulls from github to update. Use the --skip-existing flag if you don't
  want to update existing repos.

  positional arguments:
    assignment       Name of assignment. Must match assignment name in course_materials directories

  optional arguments:
    -h, --help       show this help message and exit
    --skip-existing  Do not attempt to update repositories that have already been cloned.
