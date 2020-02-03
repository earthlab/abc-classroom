Overview of abc-classroom
-------------------------

The **abc-classroom** package is designed for course instructors who are developing / marking course material locally but using GitHub Classroom to distribute material to students and collect submitted materials from students.

General Workflow
================

Here is the general workflow for each new course and for each new assignment.
Not all of the steps can be completed using **abc-classroom** - some steps
require that you use the GitHub classroom web interface (due to lack of API
for GitHub classroom).

**For each course:**

* :ref:`create a new local course <quickstart-label>` in **abc-classroom**
* create a new GitHub Classroom course

**For each assignment:**

* develop course materials
* :doc:`create a template repository from the assignment materials </new_assignment>`
* create an assignment on GitHub Classroom and link the template repository to the GitHub Classroom assignment
* give students the assignment link
* students accept assignment, complete work, and submit by pushing to their github repo
* :doc:`clone student repos and copy submitted files </clone>` into course materials directory
* :doc:`copy feedback reports from course materials to student repos </feedback>` and push back to students

abc-classroom scripts
=====================

**abc-classroom** is implemented as a set of command-line scripts. A summary of
each script, with links to more documentation:

* `abc-init` : sets up token-based access to GitHub
* `abc-quickstart` : sets up a new course
* `abc-new-template` : creates a git repository from a directory of course materials and pushes the repo to your GitHub organization to be used as an assignment template
* `abc-update-template` : updates an existing template repository based on local changes to course materials
* `abc-clone` : clones each of the student repositories and copies submitted assignments into your course materials directory
* `abc-feedback` : copies feedback reports from your course materials directory into local student repositories and then pushes to GitHub

Directory structure
===================

Each **abc-classroom** course is a separate directory, with a specific structure:

.. code-block:: bash

  course_directory/ (created by quickstart)
  |-- config.yml
  |-- roster.csv (student list)
  |-- course_materials (where you develop / mark your course files)
  |    |--- release (materials to be given to students)
  |        |--- assignment1
  |        |--- assignment2
  |    |--- submitted (collected from students)
  |        |--- student1
  |        |--- student2
  |    |--- feedback (reports to be given to students)
  |-- template_repos (location of GitHub Classroom template repositories)
  |-- clone_dir (destination for cloned student repositories)


Running ``abc-quickstart`` sets up the basics, and
other **abc-classroom** scripts create directories as needed. The only directory you need to create and manage yourself is the course_materials, and there are more details about that in :doc:`course-materials`. The names of
directories are configurable in ``config.yml`` - see :doc:`configuration`.
