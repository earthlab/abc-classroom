Setting Up a Template Directory
-------------------------------

To set up a template directory to run abc-classroom in, run:

    $ abc-dir-setup

This will create a directory for you that contains pre-made directories for templates and cloned files, as well as
a sample ``config.yml`` file that can be modified to run the program for your classroom. ``abc-dir-setup`` has
four arguments that can be used to modify its functionality.

1. ``--course_repo course-repo-custom-name-here`` This argument will allow you to modify the name of the main
repository ``abc-dir-setup`` will create.
1. ``--cloned_repo cloned-repo-custom-name-here`` This argument will allow you to modify the name of the cloned
repository that ``abc-dir-setup`` will create inside the main repository.
2. ``--template_repo template-repo-custom-name-here`` This argument will allow you to modify the name of the template
repository that ``abc-dir-setup`` will create inside the main repository.
3. ``--override_existing True/False`` This argument will allow you to override an existing output from
``abc-dir-setup``. Doing this will delete anything currently in your course directory, but will allow you to modify
names of folders or start over fresh.

