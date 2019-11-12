
Get Started Using ABC-Classroom & GitHub Classroom: Authenticate With GitHub
----------------------------------------------------------------------------

ABC-Classroom provides tool that make it easier for you to work with GitHub
classroom. To create repositories on GitHub using ABC-Classroom, you will
need to first authenticate with GitHub by creating a token. You only
need to create this token once.

To begin, you can install abc-classroom using:

``pip install abc-classroom``

Please note that because ABC-Classroom is under development, you may need to
install directly from this repository by running:

``$ pip install git+git://github.com/earthlab/abc-classroom``

Setup GitHub Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once abc-classroom is installed, you are ready to setup GitHub Authentication.
Below it is assumed that you have already installed ``abc-classroom`` on your computer.

Follow the steps below to create your GitHub token.

1. SetUp Git on Your Computer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To begin you should have git setup on your computer. If you haven't setup
git before, you can use the instructions below to setup git.

https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-git-bash-conda/#git-setup

Once you have setup git locally, you are ready to authenticate with Github.

2. Authenticate with GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have git setup on your computer, you can use ``abc-init`` to create
a GitHub token. This token is needed to create new repositories in GitHub classroom.

To create a token, run:

    ``$ abc-init``

at the command line. When you run ``abc-init``, you will be asked for your
GitHub username and password. Enter those into the command line prompts. If you
don't already have a token for **abc-classroom**, this command will create a token on
GitHub.

.. _GitHub Tokens: https://github.com/settings/tokens


The token name is: **ABC-classroom workflow helper**.


.. note::
   When you run ``abc-init``, you may get an error saying you have an outdated
   version of a package, or are missing a package all together. This should
   be resolved by installing or upgrading whatever packages the error says
   are missing or out of date.

Where Does Abc-Classroom Store the Token Information?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The token created by abc-classroom is stored in a yaml file called ``.abc-classroom.tokens.yml``
in your home directory called. This is the file that ``abc-init`` will create after it's
created your GitHub token. Once the token is created, ``abc-init`` will simply check to
ensure that the ``.abc-classroom.tokens.yml`` file exists on your computer.

.. note::
   If there is already a token file present in your home directory,
   ``abc-init`` will will provide a message that tells you that the GitHub token is
   present and valid. If you
   wish to use abc-classroom with another account, then you will have to delete or move this
   token file. You can then run ``abc-init`` and re-authenticate with a different username.

Once you have your authentication with GitHub Setup, you are ready to setup
your directory structure.

ABC-Classroom Quickstart
~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
    When you run ``abc-quickstart``, ensure you are not in an existing git repository. The directory created will
    eventually have other git repositories inside of it, and it is best to avoid creating repositories inside of
    existing repositories.

To set up the directory structure needed for abc-classroom, run:

     $ abc-quickstart course-name-here

This will

1. create a course directory for you that is named whatever you called your ``course-name-here`` variable
2. Create several other directories required to store homework assignment folders
   and cloned student repositories.
3. Creates a sample ``config.yml`` file that can be modified to run the program for your classroom. ``abc-quickstart`` has two arguments that can be used to modify its functionality.

Flags
~~~~~
 1. ``--course_name course-directory-custom-name-here`` This argument will allow you to modify the name of the main
 directory ``abc-quickstart`` will create.
 2. ``-f`` This argument will allow you to override an existing output from ``abc-quickstart``. Doing this will
 delete anything currently in your course directory, but will allow you to start over fresh.

 ## Optional but Required for Now
 ``abc-classroom`` does not fully depend upon ``nbgrader`` but does require a ``nbgrader``
 directory structure in it's early stages of development. We suggest that you
 setup an ``nbgrader`` directory within the quickstart directory that you created
 above by:

 1. Installing nbgrader and then running
 2. $ nbgrader quickstart course-name-here

Your final directory will look something like this:

.. code-block:: bash

  course-name-here/
    cloned-files/
    template-files/
    nbgrader/
      release/
    config.yml
