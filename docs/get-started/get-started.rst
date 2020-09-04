
Install abc-classroom & Setup GitHub Authentication
---------------------------------------------------

Installation Instructions
==========================

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
