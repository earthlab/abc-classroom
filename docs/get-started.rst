
Getting started with abc-classroom
----------------------------------

These instructions will lead you through installing **abc-classroom**, setting
up authentication with GitHub, and creating
a new **abc-classroom** course. It is also helpful to read through the :doc:`overview` to understand the **abc-classroom** workflow.

Installing abc-classroom
========================

To install the release version of **abc-classroom**:

``pip install abc-classroom``

If you want the development version, you can install directly from GitHub:

``$ pip install git+git://github.com/earthlab/abc-classroom``

.. _abc-init:

Setup GitHub Authentication
===========================

In order to interact with GitHub (to create template repositories or push to
student repositories), **abc-classroom** uses a `personal access token
<https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line/>`_.
Follow the steps below to create your GitHub token for **abc-classroom**. You
only need to create this token once.

1. Install and setup git
~~~~~~~~~~~~~~~~~~~~~~~~

If you aren't already using git, use the instructions below to install and
setup git:

https://help.github.com/en/github/getting-started-with-github/set-up-git

2. Create your personal access token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run ``abc-init`` at the command line to create your GitHub personal access token:

    ``$ abc-init``

**abc-classroom** will ask for your GitHub username and password. Enter those into the command line prompts. This step does two things:

* creates a token called **ABC-classroom workflow helper** on GitHub. You can
  view your personal access tokens at https://github.com/settings/tokens
* stores the token locally in a file called ``.abc-classroom.tokens.yml``
  in your home directory.


Running ``abc-init`` if you already have a token simply checks that the ``.abc-classroom.tokens.yml`` file exists on your computer and outputs ``GitHub token present and valid``.

.. note::
   If you
   wish to use **abc-classroom** with a different GitHub account, then you will have to delete or move this
   token file. You can then run ``abc-init`` and re-authenticate with a different username.

.. _abc-quickstart:

Creating a new abc-classroom course
===================================

The ``abc-quickstart`` script creates a new **abc-classroom** course, including the necessary directory structure and configuration file.

.. note::
    When you run ``abc-quickstart``, ensure you are not in an existing git repository. The directory created will
    eventually have other git repositories inside of it, and it is best to avoid creating repositories inside of
    existing repositories. To check that you aren't in a git repo, run ``git status`` and look for the message ``fatal: not a git repository (or any of the parent directories): .git``.

To create a new course:

     ``$ abc-quickstart course-name``

This will:

1. Create a course directory named whatever you called your ``course-name`` variable
2. Create two other directories required to store template repositories
   and cloned student repositories.
3. Create a sample ``config.yml`` file that can be modified to run the program for your classroom.
4. Create an `extra_files` directory that contains files (like .gitignore and a readme) that will get added to every assignment template. You can modify the contents as you like. 

If you already have a directory called ``course-name``, then ``abc-quickstart`` will fail. If you want to overwrite this directory, run ``abc-quickstart -f course-name``.

Run ``abc-quickstart -h`` to see options.

Now, you can set up the directory where you manage your course materials: :doc:`course-materials`.
