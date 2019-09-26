
Setting Up A Template Repo
--------------------------

To create a new assignment, you need to

1. Create the assignment within your classroom on GitHub and
2. Create a template repository. This repo contains all of the files that the students will need to complete their homework.

Step two can be implemented with abc-classroom by performing the following steps.


1. Authenticate with GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, you need to authenticate with GitHub. This authentication step will
allow you to automagically create the template repo within your chosen organization.

Before you can authenticate, you need a few things already installed on your
computer.

1. Git must be set up locally on your machine.
2. The ``abc-classroom`` package should be installed locally as well. If you don't have
   ``abc-classroom`` installed, you can run the command

   $ pip install git+https://github.com/earthlab/abc-classroom.git

   to install it.
3. The authentication requires a valid GitHub username and password.

To authenticate, run:

    $ abc-init

.. note::
   When you run ``abc-init``, you may get an error saying you have an outdated
   version of a package, or are missing a package all together. This should
   be resolved by installing or upgrading whatever packages the error says
   are missing or out of date.

This step will ask you for your GitHub username and password. It will
then create a token on GitHub which will allow you to create a repo.
This token can even be used to interact with GitHub through ```abc-classroom``.

The token is stored in a yaml file in your home directory, and is named
``.abc-classroom.tokens.yml`` This is the file that ``abc-init`` will look for
when creating your GitHub token.

.. note::
   If there is already a token file present in your home directory,
   ``abc-init`` will inform that the GitHub token is present and valid. If you
   wish to sign in with another username, you will have to delete or move this
   file so ``abc-init`` will know to create a new file with a different token.

You can view the token online by going to https://github.com/settings/tokens
The token will be called `Grading workflow helper`.
