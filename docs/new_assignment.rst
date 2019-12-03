Create A New Assignment Template Repo For GitHub Classroom
----------------------------------------------------------

If you are working in GitHub classroom there are several steps that will need to
be done before creating a new assignment.

1. You need to setup a class in GitHub Classroom
2. Once you have a class you can create an assignment within the class

The GitHub classroom assignment can be linked to a template git repo that is on GitHub.
This repo should have all of the files that a student will need to complete the assignment.

Abc-classroom makes it easier for you to create this template repo by collecting
the files that you want to add to the template repo, adding a readme and
initializing it as a git repo and then finally adding a .gitignore file.

The steps below assume that you have already setup a class and an assignment in
GitHub Classroom.

.. note::
  If you are using nbgrader, then the files needed to distribute and grade each assignment
  live in a sub directory of **nbgrader** called **releases**.

  The ``abc-assignment-template`` command will pull files from the releases directory
  and create a new assignment template directory that is also initialized as a git
  repository.

  If you are using nbgrader you will want to

  1. run ``$ nbgrader quickstart nbgrader``
  to setup the nbgrader directory structure within your new course created with
  ``abc-classroom quickstart course-name-here``. Note that we suggest that you name
  your nbgrader course ``nbgrader-coursename`` to make the directory structure
  a bit cleaner. Once that is setup:
  2. Change your directory to the newly created nbgrader directory ``$ cd nbgrader``
  3. Create and release an nbgrader assignment using.
  ``nbgrader generate_assignment assignment1`` generates assignment1 from the
  nbgrader source directory. This step will move the
  assignments created in the **source/** nbgrader directory over to a **release/**
  directory. abc-classroom will look for that release/ directory to find
  assignment files each time you run ``abc-assignment-template``. Once you have
  created and released the assignment with nbgrader, you can then
  create the assignment template using abc-classroom which will generate a new
  template GitHub repo that you can use with GitHub classroom.


How To Create A New Assignment Template Repository
==================================================

Creating a new assignment using abc-classroom requires you to first
update your config.yml file. Be sure to read the documentation about updating the config
before following the steps below <TODO: add link to that documentation>.

To create a GitHub classroom homework assignment template repo:

1. In the terminal, navigate to the course directory that you created using ``abc-quickstart`` (TODO: add link to quickstart page).

2. To create a new assignment template called **assignment1** run:

  ``$ abc-new-template assignment1``

``abc-new-template`` will then perform the following steps:

* create a local directory in the xxx/cloned_repos?? called assignment1 and initialize as a git repository
* copy files from the ``nbgrader/release/assignment`` directory
* create any additional files as listed in ``config.yml``

To push that repo to github as a template use:

* ``abc-update-template`` : this will both update the template repo with any files that you updated in the release/assignment directory.
* create a new repository on GitHub with the name ``assignment1-template``
* add and commit the local files, and push the contents to GitHub

TODO: initialize this repo as a template repo!! issue opened on this.

Command line arguments
======================

Run `abc-new-template -h` to see the command line arguments. The output
is reproduced here::

    usage: abc-new-template [-h] [--custom-message] [--local-only]
                                   [--mode {delete,fail,merge}]
                                   assignment

    Create a new assignment template repository: creates local directory, copy /
    create required files, intialize as git repo, create remote repo on GitHub,
    and push local repo to GitHub. Will open git editor to ask for commit message.

    positional arguments:
      assignment            Name of assignment. Must match name in nbgrader
                            release directory

    optional arguments:
      -h, --help            show this help message and exit
      --custom-message      Use a custom commit message for git. Will open the
                            default git text editor for entry. If not set, will
                            use message 'Initial commit'.
      --local-only          Create local template repository only; do not create
                            GitHub repo or push to GitHub (default: False)
      --mode {delete,fail,merge}
                            Action if template directory already exists. Choices
                            are: delete = delete the directory and contents; fail
                            = exit and let user delete or rename; merge = keep
                            existing dir, overwrite existing files, add new files.
                            Default is fail.


Configuration settings
======================

Creating an assignment uses these settings from ``config.yml``:

* ``template_dir`` : the directory where the local git repository will be created.
* ``organization`` : the GitHub organization where the new remote repository will be created
* ``course_name`` : (optional) If set, the name of the local git repository and remote GitHub repository will be ``course_name-assignment-template``. If ``short_coursename`` is not set, you must set course_name.
* ``short_coursename`` : (optional) If set, the the name of the local git repository and remote GitHub repository will be ``short_coursename-assignment-template``.
* ``nbgrader_dir`` : the path to the local nbgrader directory.
* ``extra_files`` : (optional) Any extra files that you want to add to the repo, such as .gitignore or README
