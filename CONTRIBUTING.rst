Contributing
------------

Ready to contribute? Here's how to set up abc-classroom for local development.

Fork and clone the GitHub repository
====================================

To create your own copy of the repository on GitHub, navigate to the
`earthlab/abc-classroom <https://github.com/earthlab/abc-classroom>`_ repository
and click the **Fork** button in the top-right corner of the page.

Then, use ``git clone`` to get a copy of your abc-classroom repository on your
local filesystem::

    $ git clone git@github.com:your_name_here/abc-classroom.git
    $ cd abc-classroom/

Set up your local development environment
=========================================

Create python environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

We use conda to manage the python environment needed for abc-classroom. Once you
`install conda or miniconda <https://docs.conda.io/projects/conda/en/latest/user-guide/install/>`_, create an environment from the
``environment.yml`` file.
Note that this will only allow you to test against one version of python
locally, but this is the recommended option on Windows and MacOS::

    $ conda env create -f environment.yml
    $ conda activate abc-dev

Install abc-classroom
~~~~~~~~~~~~~~~~~~~~~

Once your abc-dev environment is activated, install abc-classroom in editable
mode, along with the development requirements and pre-commit hooks::

    $ pip install -e .
    $ pip install -r dev-requirements.txt

Install black pre-commit hook
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We are using `black <https://black.readthedocs.io/en/stable/>`_ to enforce PEP 8 styles. Install the pre-commit once and black
will run every time you make a commit::

    $ pre-commit install

Note that if black makes changes to your code, you will need to run `git commit` again to complete the commit.

Running tests
=============

To run all of the tests (from the root directory of the repo)::

    $ pytest

To run only the subset of the tests in (for example) `singlefile.py`, use:

    $ pytest abcclassroom/tests/singlefile.py

Building the docs
=================

To build the docs locally (from the root directory of the repo)::

    $ make docs -B

You can view the local docs in your browser by opening the file
`docs/_build/html/index.html`.

Deploying
=========

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed, then run::

    $ bumpversion patch # possible: major / minor / patch

This will increment the version according to a major release (e.g., 0.1.0 to
1.0.0), a minor release (e.g., 0.1.0 to 0.2.0), or a patch (e.g., 0.1.0 to
0.1.1), following the guidelines for semantic versioning: https://semver.org/.


Bumpversion updates the version number throughout the
package, and generates a git commit along with an associated git tag for the
new version.
For more on bumpversion, see: https://github.com/peritus/bumpversion

To deploy abc-classroom, push the commit and the version tags::

    $ git push
    $ git push --tags

Travis will then deploy to PyPI if the build succeeds.
Travis will only deploy to PyPI on tagged commits, so remember to push the tags.
Once that is done, create a release on GitHub for the new version.

Optional: Install nbgrader
==========================

While not required, abc-classroom can be integrated with `nbgrader <https://github.com/jupyter/nbgrader>`_  for managing and autograding notebooks. You can install nbgrader using pip or conda (see the `nbgrader installation documentation <https://nbgrader.readthedocs.io/en/stable/user_guide/installation.html>`_ for details). Using conda::

    $ conda install jupyter
    $ conda install -c conda-forge nbgrader

One nbgrader is installed, it is helpful
to add the nbgrader extensions to Jupyter notebook. We've provided a bash script to install the recommended extensions, which you can use by running::

    $ bash nbgrader-ext-installs.txt

This will install all of the extensions to your current active environment.
