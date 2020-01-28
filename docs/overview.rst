Overview of abc-classroom
-------------------------

The **abc-classroom** package is designed for course instructors who are developing / marking course material locally but using GitHub Classroom to distribute material to students and collect submitted materials from students.

abc-classroom is implemented as a set of command-line scripts

General Workflow
================

**For each course:**

* create a new local course in **abc-classroom**
* create a new GitHub Classroom course

**For each assignment:**

* develop course materials
* :doc:`create a template repository from the assignment materials </new_assignment>`
* create an assignment on GitHub Classroom and link the template repository to the GitHub Classroom assignment
* give students the assignment link
* students accept assignment, complete work, and submit by pushing to their github repo
* :doc:`clone student repos and copy submitted files </clone>` into course materials directory
* :doc:`copy feedback reports from course materials to student repos </feedback>` and push back to students

Directory structure
===================

**abc-classroom** expects a specific directory structure. You don't need to create
any of these directories yourself. ``abc-quickstart`` sets up the basics, and
other **abc-classroom** scripts create directories as needed. The names of these
directories are configurable in ``config.yml``:

::

  course_directory/ (created by quickstart)
  |-- config.yml
  |-- roster.csv (student list)
  |-- course_materials/ (where you develop / mark your course files)
  |-- template_repos/ (location of GitHub Classroom template repositories)
  |-- clone_dir/ (destination for cloned student repositories)
