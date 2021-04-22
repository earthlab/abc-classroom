Managing the classroom roster
-----------------------------

The classroom roster is a csv file that contains information about the students
in your class. `abc-classroom` uses the roster file when:

* cloning student assignment repositories with `abc-clone`
* pushing feedback to student repositories with `abc-feedback`

Location of the roster
======================
The location of the classroom roster is defined in the configuration file,
`config.yml`. By default, this is `classroom_roster.csv` in the course directory. See :doc:`Configuration <configuration>` for information on setting the name and location of the roster.

Roster formats
==============

The roster formats for GitHub Classroom and nbgrader are slightly different
and you cannot directly use a GitHub Classroom roster as input for nbgrader.

The nbgrader roster requires an "id" column with a unique identifier for
each student. It is also helpful to have the first name and last name
of each student in the nbgrader roster. Then, you can identify students
in the web interface based on real names rather than GitHub usernames.

The GitHub Classroom roster contains an "identifier" column,
but this can contain a name, email address, or github username (depending
on the student profile, whether they have accepted an assignment, etc).

If you aren't using nbgrader, you can use the GitHub Classroom roster
with `abc-classroom`. The only piece of information that `abc-classroom`
requires is a single column for each
student, labelled `github_username`, that contains the
GitHub username for each student.

Converting a roster to nbgrader format
======================================

To convert a Classroom roster to nbgrader format, we want to copy the
"github_username" column in the former to an "id" column in the latter. We
can also split the "name" column into first_name and last_name.

Download the GitHub Classroom roster using the download link on the
Students tab on your Classroom course page. This file will contain the
following columns::

  identifier, github_username, github_id, name

Make sure you have a course_materials directory defined in ``config.yml``
and that the directory exists.

Run ``abc-roster``::

  $ abc-roster classroom_roster.csv

Which will create a new file, ``course_materials/nbgrader_roster.csv`` with
the following columns::

  identifier,github_username,github_id,name,id,first_name,last_name

You can specify a different output filename with the ``-o`` option.

``abc-roster`` creates the first and last name columns by splitting
the "name" column on the last whitespace (i.e. "Kermit the Frog" becomes
"Kermit the", "Frog"). You can specify a different
column to split using the ``-n`` option.

Run ``abc-roster -h`` for details.
