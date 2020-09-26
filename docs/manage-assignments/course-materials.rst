Organize Assignments
--------------------

The ``course_materials`` directory is the only course subdirectory that you need to
manage yourself. We have been developing ``abc-classroom`` while
using `nbgrader <https://nbgrader.readthedocs.io/en/stable/>`_
for autograding Jupyter notebooks, so some of the necessary structure of
```course_materials`` follows from the ``nbgrader`` requirements. It is not
necessary to use nbgrader with **abc-classroom**, but it might be helpful to
read about how `nbgrader structures course
files <https://nbgrader.readthedocs.io/en/stable/user_guide/philosophy.html>`_ to
better understand **abc-classroom**. We provide instructions below for both cases.

Manage Assignments Using nbgrader
========================================

Assuming you have `installed nbgrader <https://nbgrader.readthedocs.io/en/stable/user_guide/installation.html>`_ ::

    cd my-abc-classroom-course
    nbgrader quickstart my-nbgrader-course : this will create a nbgrader course directory called ``nbgrader``

Make sure the "course_materials" setting in `config.yml` matches the name of what you used for `my-nbgrader-course` (see below for config instructions).

Develop your notebooks in the `my-nbgrader-course/source` directory, then to
generate the student versions for an assignment called `assignment1`::

    cd my-abc-classroom-course
    cd my-nbgrader-course
    nbgrader generate_assignment assignment1`

This will generate the student versions of the assignment notebooks in `my-nbgrader-course/release`. You are now ready to :doc:`create the template repository <new_assignment>` for GitHub classroom.

Manage Assignments Manually
==================================

Create a directory for course materials inside your **abc-classroom** course
directory::

    cd my-abc-classroom-course
    mkdir course_materials

You can call this directory anything you want. Modify the value of
"course_materials" in `config.yml` (as described below) to match your chosen
directory name. Then, create a `release` directory in your course materials
dir (this _must_ be called `release`)::

    mkdir course_materials/release

Put the files that you want to distribute to students in the `release` directory before :doc:`creating a new template repository <new_assignment>`.

Add Files To Every Assignment Repository
==========================================

There are probably some files that you want to add to each assignment
repository. Any files that you wish to add to every new template repo can be
added to the ``extra_files`` directory which is created when you run
``abc-quickstart`` to set things up. By default, abc-quickstart will generate
an extra_files directory containing:

1. a generic ``README.md`` file for the repository and
2. a ``.gitignore`` file.

You can add any additional files that want in each repo to this directory.
File that you may want could include things like:

1. a customized .gitignore file
2. logos and graphics that you want to display on every student assignment
3. custom modules needed to complete assignments for the course

Any files in the extra_files directory will be addeded by defaul to each
template repository.

Ignore Some Files
~~~~~~~~~~~~~~~~~~
In many cases there may be system and tool based files that you do not wish to
move. if that is the case, you can populate the ``files_to_ignore`` section
of your ``config.yml`` file with anything that you want to skip.

. code-block:: yaml
    # Add any system files that you wish to ignore when copying files to your
    # template here
    files_to_ignore:
    - .DS_Store
    - .ipynb_checkpoints


.. note::
    Currently abc-classroom does not support moving entire directories over to
    new template repos. We will consider adding that functionality in the
    future if it is of community interest AND/OR are open to community PR's to
    add that functionality.


Update config.yml
===================

To tell **abc-classroom** where the directory containing your course materials
is located, update the ``config.yml`` file. Change the ``course_materials``
parameter in that file to the location on your computer that contains your
assignments (if you used the nbgrader quickstart, above, then use the directory
created by nbgrader).

.. code-block:: yaml

  # Path to the course_materials directory. Assumed to be relative to course_dir unless
  # you enter an absolute path (i.e. starting with '/' on Linux or OS X or with
  # 'C:' on Windows).
  course_materials: course_materials
