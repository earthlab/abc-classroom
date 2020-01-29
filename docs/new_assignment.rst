.. _new_assignment:

Creating a new assignment template repo
---------------------------------------

Once you have your course materials ready, you can create a template repository
for distributing the materials to students. Creating a new assignment template
in **abc-classroom** involves:

1. Ensuring that the materials to be distributed to students are in the `course_materials/release/assignment_name` directory.
1. Copying files from `course_materials/release/assignment_name` to `template_repos/assignment_name`.
1. Setting up `template_repos/assignment_name` as a git repository.
1. Pushing the template repository to your GitHub Classroom organization.

Then, on GitHub classroom, you link the assignment to the template git repo, which
contains all of the files that a student will need to complete the assignment.

The ``abc-new-template`` and ``abc-update-template`` scripts allow you to create and update template repositories.

How To Create and Update Template Repositories
==============================================

There are two template scripts : `abc-new-template` and `abc-update-template`. The 'new' script is for first-time creation of a new assignment template repository from a directory of assignment files. The 'update' script allows you to quickly update the local and remote repositories after making changes to assignment files.

Make sure you have updated your ``config.yml`` before running the template scripts. See the Configuration section below for details.

Creating a New Template repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a GitHub classroom homework assignment template repo:

1. In the terminal, navigate to the course directory that you created using ``abc-quickstart`` (TODO: add link to quickstart page).

2. To create a new assignment template called `assignment1` run:

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


Configuration settings
======================

Creating an assignment uses these settings from ``config.yml``:

* ``template_dir`` : the directory where the local git repository will be created.
* ``organization`` : the GitHub organization where the new remote repository will be created
* ``course_materials`` : the path to the local directory where you are storing course materials (the top-level nbgrader dir if you are using nbgrader).
* ``extra_files`` : (optional) Any extra files that you want to add to the repo, such as .gitignore or README
