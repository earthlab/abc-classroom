Create A New Assignment Template Repo For GitHub Classroom
----------------------------------------------------------

Creating a new assignment involves:

1. Creating a template repository for each student assignment. This is the repo containing assignment files that each student will get a copy of when you release the assignment for them to work on.
2. Pushing that template repository to your GitHub organization that is setup with a classroom, for distribution.

The GitHub classroom assignment can be linked to a template git repo that is on GitHub.
This repo should have all of the files that a student will need to complete the assignment.

The ``abc-new-template`` and ``abc-update-template`` commands allow you to create and update template repositories.

.. note::
   The current version abc-classroom assumes that you have the student version of assignment files in the ``course_materials/release/assignment_name`` directory (where ``course_materials`` is defined in the abc-classroom ``config.yml``). This mirrors the structure of an nbgrader course. See :doc:`get-started` for more details about abc-classroom and nbgrader setup.

How To Create and Update Template Repositories
==============================================

There are two template scripts : `abc-new-template` and `abc-update-template`. The 'new' script is for first-time creation of a new assignment template repository from a directory of assignment files. The 'update' script allows you to quickly update the local and remote repositories after making changes to assignment files.

Make sure you have updated your ``config.yml`` before running the template scripts. See the Configuration section below for details.

Creating a New Template repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a GitHub classroom homework assignment template repo:

1. In the terminal, navigate to the course directory that you created using ``abc-quickstart`` (TODO: add link to quickstart page).

2. To create a new assignment template called **assignment1** run:

  ``$ abc-new-template assignment1``

``abc-new-template`` will then perform the following steps:

* get the name of the `template_dir` directory from the config file
* create a local directory in ``template_dir`` called ``assignment1-template`` and initialize as a git repository
* copy files from the ``course_materials/release/assignment1`` directory
* create any extra files as listed in ``config.yml``
* git add and git commit the local files
* (optionally, if using ``--github`` flag) create a new repository on GitHub with the name ``assignment1-template`` and push the contents of the local repo to GitHub

**Command line options**

Run ``abc-new-template -h`` to see the options. The output is reproduced below::

    usage: abc-new-template [-h] [--custom-message] [--github]
                            [--mode {delete,fail,merge}]
                            assignment

    Create a new assignment template repository: creates local directory, copy /
    create required files, intialize as git repo, and (optionally) create remote
    repo on GitHub and push local repo to GitHub. Will open git editor to ask for
    commit message if custom message requested.

    positional arguments:
      assignment            Name of assignment. Must match name in course_materials
                            release directory

    optional arguments:
      -h, --help            show this help message and exit
      --custom-message      Use a custom commit message for git. Will open the
                            default git text editor for entry (if not set, uses
                            default message 'Initial commit').
      --github              Also perform the GitHub operations (create remote repo
                            on GitHub and push to remote (by default, only does
                            local repository setup).
      --mode {delete,fail,merge}
                            Action if template directory already exists. Choices
                            are: delete = delete contents before proceeding
                            (except .git directory); merge = keep existing dir,
                            overwrite existing files, add new files (Default =
                            fail).

Updating an existing template repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To update an existing template repository (for example, if you change assignment files and want to push new versions to GitHub), use the ``abc-update-template`` scripts. Assuming that ``template_dir/assignment1-template`` exists:

```abc-update-template assignment1``

will:

* copy any files in ``course_materials/release/assignment1`` to ``template_dir/assignment1-template`` (overwriting any existing files with the same name; use the ``-delete`` mode if you want to erase the existing template before starting)
* git add and git commit the changes
* push the changes to GitHub

**Command line arguments**

Run `abc-update_template -h` to see the command line arguments. The output
is reproduced here::

    usage: abc-update-template [-h] [--mode {delete,merge}] assignment

    Updates an existing assignment template repository: update / add new and
    changed files, then push local changes to GitHub. Will open git editor to ask
    for commit message.

    positional arguments:
      assignment            Name of assignment. Must match name in course_materials
                            release directory

    optional arguments:
      -h, --help            show this help message and exit
      --mode {delete,merge}
                            What to do with existing contents of template
                            directory. Choices are: delete = remove contents
                            before proceeding (leaving .git directory); merge =
                            overwrite existing files add new files (Default =
                            merge).


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

Configuration settings
======================

Creating an assignment uses these settings from ``config.yml``:

* ``template_dir`` : the directory where the local git repository will be created.
* ``organization`` : the GitHub organization where the new remote repository will be created
* ``materials_dir`` : the path to the local directory where you are storing course materials (the top-level nbgrader dir if you are using nbgrader).
* ``extra_files`` : (optional) Any extra files that you want to add to the repo, such as .gitignore or README
