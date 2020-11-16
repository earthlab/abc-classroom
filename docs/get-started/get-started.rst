
Install abc-classroom & Setup GitHub Authentication
---------------------------------------------------

Installation Instructions
==========================

To install the release version of **abc-classroom**:

``pip install abc-classroom``

If you want the development version, you can install directly from GitHub:

``$ pip install git+git://github.com/earthlab/abc-classroom``

.. _abc-init:

Setup git and GitHub
====================

**abc-classroom** uses git locally, and also interacts with GitHub (to create template repositories or push to
student repositories). For local git actions, **abc-classroom** uses your
local git settings. For GitHub actions, it requires that you authenticate
through GitHub to generate an access token for the GitHub API.

Follow the steps below to set up git and create your GitHub token.

1. Install git and setup ssh keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you aren't already using git, use the instructions below to install and
setup git:

https://help.github.com/en/github/getting-started-with-github/set-up-git

.. note::
  We link to the GitHub documentation for setting up git, but git is not
  limited to GitHub, and there are many other sets of instructions out there.

**abc-classroom** uses git + GitHub via SSH rather than https, so you need to
setup ssh keys for passwordless access. There are three steps to setup ssh on
your computer:

1. Check to see if you already have an ssh key installed on your computer locally https://docs.github.com/en/enterprise/2.14/user/articles/checking-for-existing-ssh-keys
2. Generate a new key - https://docs.github.com/en/enterprise/2.14/user/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
3. Add the key to GitHub - https://docs.github.com/en/enterprise/2.14/user/articles/adding-a-new-ssh-key-to-your-github-account

2. Authenticate to GitHub for abc-classroom
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**abc-classroom** needs to be able to create repositories and push to
student repositories in the course organization. To do this, we need to
setup an access token for the GitHub API.

#. Run ``abc-init`` at the command line. If you don't already have a token,
   **abc-classroom** will prompt you to authenticate through GitHub.

#. Open a web browser, go to https://github.com/device/login, log in to GitHub
   (if you aren't already) and enter the temporary code provided by
   **abc-classroom**:

   .. image:: ../media/temporary_code.png
      :width: 400

   When you git Continue on the web page, you will see the permissions that the **abc-classroom** app requests. Accept the request to authenticate the app.

#. Return to the command line and press <RETURN>. **abc-classroom** will verify
   your access token, print a success message, and save the token locally in a
   file called ``.abc-classroom.tokens.yml`` in your home directory.

If after running ``abc-init``, you instead see the message `Access token is present and valid; successfully authenticated as user <your-username`, then you already have a token.

.. note::
  If you installed and used **abc-classroom** prior to November 2020, you
  probably have both a local tokens file and a personal access token stored
  on GitHub. Due to changes in GitHub authentication, we recommend that you
  delete the local `.abc-classroom.tokens.yml` file and also the
  **ABC-classroom workflow helper** token from GitHub
  (https://github.com/settings/tokens) and run `abc-init` again to generate a
  new, more secure, token.

Un-authenticating abc-classroom
===============================

If you want to remove the **abc-classroom** access to your account, visit
https://github.com/settings/apps/authorizations and revoke authorization to
``abc-classroom-bot``.

If you want to authenticate to **abc-classroom** with a different GitHub
account, remove the local ``.abc-classroom.tokens.yml`` file, re-run
``abc-init`` and log into GitHub with the alternate credentials to grant
access.

Installing the abc-classroom-bot on the organization
====================================================

The ``abc-classroom-bot`` is a GitHub App that must be installed on the
organization(s) where you want to create template and student repositories.
At this time, the app is not yet available on the public GitHub Marketplace.
Please contact the **abc-classroom** developers if you want to install the app.

.. _abc-quickstart:
