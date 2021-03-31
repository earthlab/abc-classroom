Create a New abc-classroom Course
----------------------------------

The ``abc-quickstart`` script creates a new **abc-classroom** course, including
the necessary directory structure and configuration file. The abc-classroom
course directory structure will allow you to manage your GitHub classroom course
from the command line supporting the following tasks

1. Creating GitHub classroom template repos that contains course assignment materials
2. Collecting completed GitHub repos for each assignment and for each student
3. Providing feedback to students after grading is complete.

.. note::
    Do not run ``abc-quickstart`` in an existing ``git``
    repository. The directory created will eventually have other git
    repositories inside of it, and it is best to avoid creating repositories
    inside of existing repositories. To check that you aren't in a git repo,
    run ``git status`` and look for the message ``fatal: not a git repository
    (or any of the parent directories): .git``.

To create a new course using ``abc-classroom`` run::

    abc-quickstart course-name

This will:

1. Create a course directory named whatever you called your ``course-name`` variable
2. Create two other directories required to store template repositories
   and cloned student repositories.
3. Create a sample ``config.yml`` file that can be modified to run the program for your classroom. See :doc:`configuration <configuration>` for information on configuring ``abc-classroom``.
4. Create an ``extra_files`` directory that contains files (like .gitignore and a readme) that will get added to every assignment template. You can modify the contents as you like.

If you already have a directory called ``course-name``, then ``abc-quickstart``
will fail. If you want to overwrite this directory, run
``abc-quickstart -f course-name``.

Run::

    abc-quickstart -h

to see options.

Now, you can set up the directory where you manage your
assignments: :doc:`../manage-assignments/course-materials`.
