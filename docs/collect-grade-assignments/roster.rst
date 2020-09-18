===============================
About The Student Roster
===============================

The student roster allows you to to keep track of students in your
GitHub classroom class. This roster is used to keep track of which repos
``abc-classroom`` needs to clone and also which repos it will send feedback to
when you are done grading.

There are a few steps associated with setting up GitHub classroom that you may
want to consider.

1. If you didn't explicitly invite students to GitHub classroom, you
may want to wait until all students have accepted the first assignment to
create your roster. This will ensure that all of the students in your class are
listed in the roster.
2. Once you think all of your students have accepted the first assignment, go
   to the classroom interface and click on the ``download roster`` button.
   This will return a list of students with their names as they have entered them
   in GitHub and their github usernames. The format will look like::

   identifier github_username github_id name

   .. note::
     It can be helpful to ask students to add their first and last names to their
     GitHub profile given sometimes the usernames do not clearly link to their
     LMS profile names.

3. Once you have your roster, you can add the path to the roster location
   in the anc-classroom ``config.yml`` file.

   ``roster: path-to-roster-here/roster.csv``


Optional: Link GitHub Classroom to Your Learning Management System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you connect GitHub classroom to your Learning Management System (examples:
Canvas, Moodle, D2L), it will allow you to
sync a list of the students in your class with the list of students in
your GitHub classroom class. This can be especially helpful given you often
want to align student names from the LMS  with their respective GitHub username
for grading purposes. Or if there is a school identifier that you need to
associate with your roster.

Once you have created that link, you may need to manually associated some of
your student's names with their GitHub usernames.


Optional: Add Roster to Nbgrader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using nbgrader, you may also want to upload the roster to the nbgrader
database. You can add a .csv file to nbgrader using::

    nbgrader db student import class-roster-file.csv

If you generated your roster using github classroom there are a few changes that
you may want to make to your roster before uploading it. Nbgrader requires an id
field for this to work. As suchh you may want to

  1. Add a new id column containing the ``github`` usernames for each students
  2. Divide the Name column into a  ``first_name`` and ``last_name`` columns which
     ``nbgrader`` will recognize

Once you have made this changes, ``nbgrader`` will be able to associated each
``github`` username with a first and last name. This may make grading easier.
