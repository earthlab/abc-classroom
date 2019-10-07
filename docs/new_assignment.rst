Creating a new assignment template
----------------------------------

Creating a new assignment template involves getting your local assignment
files into
a new repository on GitHub that you can use as a template for a GitHub
classroom assignment.

To create a new assignment template called "assignment1" using abc-classroom::

  $ abc-assignment_template -a assignment1

This performs the following steps:

* create a local directory and initialize as a git repository
* copy files from the ``nbgrader/release/assignment`` directory
* create any additional files as listed in ``config.yml``
* create a new repository on GitHub with the name ``assignment1-template``
* add and commit the local files, and push the contents to GitHub

Command line arguments
======================

Run `abc-assignment_template -h` to see the command line arguments. The output
is reproduced here::

  usage: abc-assignment-template [-h] [--custom-message] [--local-only]
                                 assignment

  Create a new assignment template repository: creates local directory, copy /
  create required files, intialize as git repo, create remote repo on GitHub,
  and push local repo to GitHub. Will open git editor to ask for commit message.

  positional arguments:
    assignment        Name of assignment. Must match name in nbgrader release
                      directory

  optional arguments:
    -h, --help        show this help message and exit
    --custom-message  Use a custom commit message for git. Will open the default
                      git text editor for entry. If not set, will use message
                      'Initial commit of template repository'.
    --local-only      Create local template repository only; do not create
                      GitHub repo or push to GitHub (default: False)


Configuration settings
======================

Creating an assignment uses these settings from ``config.yml``:

* ``template_dir`` : the directory where the local git repository will be created.
* ``organization`` : the GitHub organization where the new remote repository will be created
* ``course_name`` : (optional) If set, the name of the local git repository and remote github repository will be ``course_name-assignment-template``. If ``short_coursename`` is not set, you must set course_name.
* ``short_coursename`` : (optional) If set, the the name of the local git repository and remote github repository will be ``short_coursename-assignment-template``.
* ``nbgrader_dir`` : the path to the local nbgrader directory.
* ``extra_files`` : (optional) Any extra files that you want to add to the repo, such as .gitignore or README
