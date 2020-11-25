.. _abc-clone:

Collect Student Assignments
----------------------------------

The ``abc-clone`` function retrieves or clones each student repo with all of
the commits that they've made to date.::

    abc-clone assignment-name

In order for this command to work properly, you will need to setup a ssh key
both locally and on GitHub (discussed at the end of this page).

``abc-clone`` does two things:

1. It clones each repository using ``git clone``
2. It then copies each student's notebook files into ``course_materials/submitted/student/assignment-name``

ABC-Clone - How Clone Works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``abc-clone`` uses
1. the ``github_username`` column in the student roster,  and
2. the assignment name provided as a command line argument,
3. the GitHub organization set in the config file ``config.yml``.

The function clones each student repository using the SSH URL:

    ``git@github.com:github-organization/assignment-student.git``

into the ``clone_dir`` directory path as specified in ``config.yml``.

If a git repository with the same name already exists in ``clone_dir``,
**abc-classroom** updates the repo using ``git-pull`` unless you specify to skip
existing repos using the ``--skip-existing`` flag.::

    abc-clone assignment-name --skip-existing

Copy Assignment Files For Grading
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the student repos are cloned, the script copies the files to be graded
from the local repository to the course materials directory which you specified
in the ``config.yml`` file. If you are using ``nbgrader``, it will copy the
files into the nbgrader ``submitted`` directory using the structure:
``course_materials/submitted/student/assignment``.::

    course_materials/
      submitted/
        student-name-1/
          assignment-name-1/
            notebook-file.ipynb
        student-name-2/
          assignment-name-1/
            notebook-file.ipynb

The path to ``course_materials`` is defined in ``config.yml`` file. ``abc-clone``
will create subdirectories within ``course_materials`` for each student as needed.

Cone and Do Not Move to Submitted
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sometimes you need to update student repos however  you may not with to update
the submitted directory which contains the version oof the assignment that you
graded. In this case, you can run ``abc-clone assignment-name --no-submitted``.
The ``no-submitted`` flag / parameter will make abc-clone only clone or pull down
repo updates. It will NOT update your submitted directory.

Setup SSH to Ensure abc-clone Runs Properly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are three steps to setup ssh on your computer. You can follow the GitHub
documentation carefully to set this up. ``abc-clone`` will fail if this
authentication is not setup!

* Step one: Check to see if you already have an ssh key installed on your computer locally https://docs.github.com/en/enterprise/2.14/user/articles/checking-for-existing-ssh-keys
* Step two: Generate a new key - https://docs.github.com/en/enterprise/2.14/user/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
* Step three: Add the key to GitHub - https://docs.github.com/en/enterprise/2.14/user/articles/adding-a-new-ssh-key-to-your-github-account


Command-line Arguments
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
