Configuration
-------------

The settings for abc-classroom are in a configuration file. By default, this
file is called "config.yml" and is located in the course directory. If you
used ```abc-quickstart``, this file is created for you.

roster
======

Enter the path to the classroom roster. If you enter a bare filename,
`abc-classroom` will look in the course directory for the file. If your
roster file is somewhere else, you can enter a full path to the file,
e.g. `/home/user/directory/filename.csv`. 

Default: `roster: classroom_roster.csv`


Files_to_ignore
===============

This is a list of file patterns that you do not want to copy from your
assignment release directory to the github template repo. These may be
system files, checkpoints or other files that are created by various
tools and operating system functions.

Use quoted wildcards, e.g. '\*.csv', to ignore all files that match a
pattern.

.. note::
    You must use quotes around wildcard entries in order to avoid yaml
    parsing errors (in yaml, an unquoted \* is treated as an alias).

Example

.. code-block:: yaml

    files_to_ignore:
    - .DS_Store
    - .ipynb_checkpoints
    - '*.csv'
