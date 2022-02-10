.. _assignment_template:

Create A New Assignment Template GitHub Repository
---------------------------------------------------

A template assignment GitHub  repo is what is used to create repositories for
each student in GitHub Classroom. This repo  should have all of the files that
the students need to complete their assignment. These files may include:

* A Jupyter Notebook (or rMarkdown file).
* Any images required to load in the notebook
* any other files that you want to distribute through GitHub

Once you have your assignment ready to share with students on GitHub Classroom,
you can create a template GitHub repository. This is the repository that
GitHub Classroom will use to share the assignment repo with each student in your
class. To create a new assignment template, do the following:

#. Make sure that all required assignment files are in the **course_materials/release/assignment_name** directory.
#. Make sure that all general files such as a **README.md** or a **.gitignore** file are located in the **extra_files** directory.

When you create a template abc-classroom will:

#. Copy specific for this assignment from **course_materials/release/assignment_name** to ``template_repos/assignment_name``.
#. Copy any files that you want to have in all assignment repos to non-specific assignment files from `extra_files` to `template_repos/assignment_name`.
#. Setting up **template_repos/assignment_name** as a git repository.
#. Pushing the template repository to your GitHub Classroom organization.

Then, on GitHub classroom, you link the assignment to the template git repo, which
contains all of the files that a student will need to complete the assignment.

The ``abc-new-template`` and ``abc-update-template`` scripts allow you to create and update template repositories.

How To Create and Update Template Repositories
==============================================

There are two template scripts or commands that you can use

1. ``abc-new-template``: Use this for creating the initial template repository
   When used with the optional --github flag, you can push to GitHub  after files
   are updated.
2. ``abc-update-template``: Quickly update your template repo and push to
   GitHub . No flag is needed to push to GitHub .

.. note::
  ``abc-update-template`` is a convenience function - both
  scripts call the same code, but with different default parameters
  (i.e. you can replicate the behavior of 'update' by choosing the
  parameters of 'new').

Make sure you have updated your **config.yml** before running the template
scripts. See the Configuration section below for details.

.. _abc-new-template:

Create a New Template Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a GitHub Classroom homework assignment template repository:

1. In the terminal, navigate to the course directory that you created using ``abc-quickstart`` (TODO: add link to quickstart page).

2. To create a new git repo containing the assignment template called **assignment1** run::

    abc-new-template assignment1

``abc-new-template`` will then perform the following steps:

* get the name of the **template_dir** directory from the config file
* create a local directory in **template_dir** called **assignment1-template** and initialize as a git repository
* copy files from the **course_materials/release/assignment1** directory
* create any extra files in the directory specified in your **config.yml** file.
* ``git add`` and ``git commit`` the local files

 If you want to push the ``assignment1`` template repo to GitHub, in addition
 to the steps outlined above, run::

  abc-new-template assignment1 --github

If you have already created the template directory, you will need to use the
``--mode merge`` or ``--mode delete`` options to ensure the existing template is
either 1) deleted if you want to start over OR 2) merged or updated to reflect
changes to files. The command to merge would look like::

    abc-new-template assignment1 --mode merge --github

Extra Files: Readme and other Template Files
=============================================
GitHub repos normally have a ``Readme.md`` and a ``.gitignore`` file. The ``readme.md`` file
provides a user with an overview of the repository. The ``.gitignore`` specifies files that
should never be committed to git history. One example of such a file is a Jupyter Notebook
``.ipynb_checkpoints`` file. This is a file that you may never want to be committed
to git but that will always by in a directory where you are working on a
Jupyter Notebook. By default, abc-classroom provides a standard ``readme.md`` and
``.gitignore`` file that can be found in the ``extra_files`` directory that is created
when you create a new class with abc-classroom. You can look at the default
content contained within those files, on GitHub, here:
https://github.com/earthlab/abc-classroom/tree/main/abcclassroom/example-data/extra_files

* To customize the ``readme.md`` file, you can edit the file within the ``extra_files`` directory.
* To customize the ``.gitignore`` file, edit that file within the ``extra_files`` directory.

You can also add any files that you wish to that directory such as images, text
files, etc. Any files within the ``extra_files`` directory will be added to a new
template repository upon creating or updating a new assignment.

A few notes about how this works:

* Extra files will NOT be updated for older assignments when you create or update a new template. Only that new template will have the newest files.
* Abc-classroom will add the assignment name to the top of the readme file.


Text Editors and Git Commit Messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The default commit message used when you run
``abc-new-template <assignment-name>`` is **initial commit**. A text editor
will not open in this case.

When you run ``abc-update-template`` the text editor that is specified in your
system configuration settings will open up. If you do not have a text editor
specified, VIM will open as a default.

If you wish to use nano instead you can run the following in your terminal::

  export EDITOR=nano

.. note::
  Right now if you try to use an editor like atom that launches outside of the
  terminal, abc-classroom will currently fail and return a message saying
  **empty commit message** . This may be fixed in the future but for now we
  suggest that you use a terminal based editor for your default when using
  abc-classroom.



Command Line Options
~~~~~~~~~~~~~~~~~~~~~~

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


.. _abc-update-template:

Updating an Existing Template Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To update an existing template repository (for example, if you change assignment
files and want to push new versions to GitHub), use the ``abc-update-template``
scripts. Assuming that ``template_dir/assignment1-template`` exists::

    abc-update-template assignment1

will:

* copy any files in ``course_materials/release/assignment1`` to ``template_dir/assignment1-template`` (overwriting any existing files with the same name; use the ``-delete`` mode if you want to erase the existing template before starting)
* ``git add`` and ``git commit`` the changes
* ``git push`` the changes to GitHub

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


Configuration Settings
======================

Creating an assignment uses these settings from ``config.yml``:

* ``template_dir`` : the directory where the local git repository will be created.
* ``organization`` : the GitHub organization where the new remote repository will be created
* ``course_materials`` : the path to the local directory where you are storing course materials (the top-level nbgrader dir if you are using nbgrader).
* ``extra_files`` : (optional) Any extra files that you want to add to the repo, such as .gitignore or README
