Previous functionality
======================

ABC-classroom is going through a significant refactoring starting in October 2019. This documentation pertains to the pre-refactoring functionality.

Links
-----
Some of the documentation about abc-classroom lives outside of this repo.

* `hackmd documentation <https://hackmd.io/0ZbGctpuSdqYK2OdPI51dw?view/>`_ for setting up a new course
* `autograding course starter repo <https://github.com/betatim/autograded-course-starter/>`_ (contains `sample config file <https://github.com/betatim/autograded-course-starter/blob/master/config.yml/>`_)

Console_scripts
---------------

There are five console scripts for using ABC-classroom functions. All assume
that we are sitting in a git repo for the course.

abc-init
~~~~~~~~
Sets up GitHub credentials. Makes sure that there is a valid GitHub authentication yaml file, and if there isn't one, create a valid file
and populate with token (so that we don't need to keep asking for
username and password).

abc-grade
~~~~~~~~~
Grades the work of some or all students, for some or all assignments.

* clones the course repo for each student into a directory called 'graded'
* checks which assignments have a due date today or in the past
* collects notebooks for assignment that are due
* grades the notebooks (using ok.grade_notebook): execute notebook, then iterate through cells collecting points
* prints results

abc-author
~~~~~~~~~~
Creates student repository and autograding tests.

* copy notebooks from master directory to student directory
* copy any extra files listed in config
* set up CircleCI on student directory

abc-distribute
~~~~~~~~~~~~~~
Create or update student repositories.

Create steps:

* creates template directory called `coursename-template`
* copies everything from `student` directory into template dir
* initialize git repo in template dir
* creates repo in GitHub organization specified in config
* adds origin to local repo, pushes to remote

Update steps:

* clones repo for each student
* copies new file over to student repo
* create new branch, add, commit
* push branch to github and create pull request

(Current abc-classroom setup is one repo per student for whole course,
which is why we need to clone, edit, and push for each assignment)

When called with --template flag, only runs the Create steps.
