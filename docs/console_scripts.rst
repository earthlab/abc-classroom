Console_scripts
---------------
Description of methods before the refactoring in Oct 2019.

There are five console scripts for using abc-classroom functions. All assume
that we are sitting in a git repo for the course.

abc-init
~~~~~~~~
Sets up GitHub credentials. Makes sure that there is a valid GitHub authentication yaml file, and if there isn't one, create a valid file
and populate with token (so that we don't need to keep asking for
username and password).

abc-grade
~~~~~~~~~

abc-author
~~~~~~~~~~

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
