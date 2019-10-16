ABC-Classroom Quickstart
------------------------

.. note::
   When you run ``abc-quickstart``, ensure you are not in an existing git repository. The directory created will
   eventually have other git repositories inside of it, and it is best to avoid creating repositories inside of
   existing repositories.

To set up a template directory to run abc-classroom in, run:

    $ abc-quickstart

This will create a directory for you that contains pre-made directories for templates and cloned files, as well as
a sample ``config.yml`` file that can be modified to run the program for your classroom. ``abc-quickstart`` has
two arguments that can be used to modify its functionality.

1. ``--course_name course-directory-custom-name-here`` This argument will allow you to modify the name of the main
directory ``abc-quickstart`` will create.
2. ``-f`` This argument will allow you to override an existing output from ``abc-quickstart``. Doing this will
delete anything currently in your course directory, but will allow you to start over fresh.

