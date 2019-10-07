Creating a new assignment
-------------------------

Creating a new assignment involves getting your local assignment files into
a new repository on GitHub that you can use as a template for a GitHub
classroom assignment.

To create a new assignment called "assignment1" using abc-classroom::

  $ abc-classroom -a assignment1

This performs the following steps:

* create a local directory and initialize as a git repository
* copy files from the ``nbgrader/release/assignment`` directory
* create any additional files as listed in ``config.yml``
* create a new repository on GitHub with the name ``assignment1-template``
* add and commit the local files, and push the contents to GitHub

Configuration settings
======================

Creating an assignment uses these settings from ``config.yml``:

* ``template_dir`` : the directory where the local git repository will be created.
* ``organization`` : the GitHub organization where the new remote repository will be created
* ``course_name`` : (optional) If set, the name of the local git repository and remote github repository will be ``course_name-assignment-template``. If ``short_coursename`` is not set, you must set course_name.
* ``short_coursename`` : (optional) If set, the the name of the local git repository and remote github repository will be ``short_coursename-assignment-template``.
* ``nbgrader_dir`` : the path to the local nbgrader directory.
* ``extra_files`` : (optional) Any extra files that you want to add to the repo, such as .gitignore or README 
