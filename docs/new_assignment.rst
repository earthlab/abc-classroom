Create A New Assignment Git Repo
--------------------------------

If you are working in GitHub classroom, you will need to
1. Create a template repository for each student assignment. This is the repo that each student will get a copy of when you release the assignment for them to work on.
2. Push that template repository to your GitHub organization that is setup with a classroom, for distribution.

<<<<<<< HEAD
If you are using nbgrader, then the files needed to distribute and grade each assignment
live in a sub directory of **nbgrader** called **releases**.

The ``abc-assignment-template`` command will pull files from the releases directory
and create a new assignment template directory that is also initialized as a git
repository.

=======
<Somethng about assuming nbgrader>
To create a new assignment git repo,

1. Navigate to the course directory that you created using abc-quickstart (TODO: add link to quickstart page).
the commands below assume that you have a config.yml file with the needed information already added (TODO: Add instructions on customizing yaml file)
>>>>>>> add89a422144d682de1d70436259ecb7970b2b1b

Creating a new assignment template involves getting your local assignment
files into
a new repository on GitHub that you can use as a template for a GitHub
classroom assignment.

<<<<<<< HEAD
How To Create A New Assignment Template repository
==================================================

Creating a new assignment using ``abc-assignment-template`` requires you to first
update your config.yml file. Be sure to read the documentation about updating the config
before followign the steps below <TODO: add link to that documentation>.

To create a new assignment git repo:

1. In the terminal, navigate to the course directory that you created using ``abc-quickstart`` (TODO: add link to quickstart page).

2. To create a new assignment template called **assignment1** run:

  ``$ abc-assignment-template assignment1``

``abc-assignment-template`` will then perform the following steps:

* create a local directory in the xxx/cloned_repos?? called assignment1 and initialize as a git repository
=======
To create a new assignment template called "assignment1" using abc-classroom run ::

  ``$ abc-assignment-template assignment1``

This performs the following steps:

* create a local directory and initialize as a git repository
>>>>>>> add89a422144d682de1d70436259ecb7970b2b1b
* copy files from the ``nbgrader/release/assignment`` directory
* create any additional files as listed in ``config.yml``
* create a new repository on GitHub with the name ``assignment1-template``
* add and commit the local files, and push the contents to GitHub

Command line arguments
======================

Run `abc-assignment_template -h` to see the command line arguments. The output
is reproduced here::

    usage: abc-assignment-template [-h] [--custom-message] [--local-only]
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
* ``course_name`` : (optional) If set, the name of the local git repository and remote github repository will be ``course_name-assignment-template``. If ``short_coursename`` is not set, you must set course_name.
* ``short_coursename`` : (optional) If set, the the name of the local git repository and remote github repository will be ``short_coursename-assignment-template``.
* ``nbgrader_dir`` : the path to the local nbgrader directory.
* ``extra_files`` : (optional) Any extra files that you want to add to the repo, such as .gitignore or README
