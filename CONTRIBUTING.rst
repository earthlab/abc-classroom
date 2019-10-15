Get Started!
============

Ready to contribute? Here's how to set up EarthPy for local development.

1. Fork the repository on GitHub
--------------------------------

To create your own copy of the repository on GitHub, navigate to the
`earthlab/abc-classroom <https://github.com/earthlab/abc-classroom>`_ repository
and click the **Fork** button in the top-right corner of the page.

2. Clone your fork locally
--------------------------

Use ``git clone`` to get a local copy of your EarthPy repository on your
local filesystem::

    $ git clone git@github.com:your_name_here/abc-classroom.git
    $ cd abc-classroom/

3. Set up your fork for local development
-----------------------------------------

Setup the ABC-Classroom Dev Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using conda, there are two options.

1. The easiest option is to create an environment from the
``environment.yml`` file.
Note that this will only allow you to test against one version of python
locally, but this is the recommended option on Windows and MacOS::

    $ conda env create -f environment.yml
    $ conda activate abc-dev

Install the package & The Precommit Hook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once your abc-dev environment is activated, install EarthPy in editable
mode, along with the development requirements and pre-commit hooks::

    $ pip install -e .
    $ pip install -r dev-requirements.txt

We are using black to enforce PEP 8 styles. Install the pre-commit once and black
will run every time you make a commit. Note that you will need to commit any changes
that black makes to your code after those changes are applied.

    $ pre-commit install

Running tests
^^^^^^^^^^^^^
To run all of the tests (from the root directory of the repo):

    $ pytest

To run only the subset of the tests in (for example) `singlefile.py`, use:

    $ pytest abcclassroom/tests/single_file.py


Install nbgrader Extensions into the Active Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One the environment is activated and the package is installed, it is helpful
to add useful extensions to Jupyter notebook. The recommended extensions can
be installed by running::

    $ bash nbgrader-ext-installs.txt

This will install all of the extensions to your current active environment.
