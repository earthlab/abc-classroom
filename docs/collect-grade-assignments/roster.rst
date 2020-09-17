===============================
About The Student Roster
===============================

The student roster is an important way to keep track of students in your
GitHub classroom class. This roster is used to keep track of which repos it
needs to clone and also send feedback to.

There are a few steps associated with setting up GitHub classroom that you may
want to consider.

1. OPTIONAL: Connect GitHub classroom with your Learning Management System

This step is optional. If you connect GitHub classroom to your Learning
Management System (examples: Canvas, Moodle, D2L), it will allow you to
sync a list of the students in your class with the list of students in
your GitHub classroom class. This can be especially helpful given you often
want to align student names from the LMS  with their respective GitHub username
for grading purposes.

You can download the roster from GitHub Classroom directly.

.. note::
  It can be helpful to ask students to add their first and last names to their
  GitHub profile given sometimes the usernames do not clearly link to their
  LMS profile names.

Once you have created your roster, you can add the path to the roster location
in the ``config.yml`` file.

``roster: path-to-roster-here/roster.csv``.


.. note::
  If you are using ``abc-classroom`` with ``nbgrader``, you may want to add this roster
  to the ``nbgrader`` database. More on that to come in the future....
