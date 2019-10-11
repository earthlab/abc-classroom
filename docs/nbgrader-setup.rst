Setup nbgrader repository
-------------------------

`nbgrader` requires a specific directory structure in order to work properly.
See the [nbgrader philosophy](https://nbgrader.readthedocs.io/en/stable/user_guide/philosophy.html)
for details. In order to use the autograding workflow, you need to set up your
course using this directory structure. Note that there is **one** nbgrader
directory for each course (not each assignment).

* Create an `nbgrader` directory on your local computer using the command

`nbgrader quickstart course-name-here`

This is the directory that you will use to manage all assignments in your course.
The course name does not have to match the name of the course that you used for
your github classroom setup but we suggest that you do make the names the same
to keep things simple.

In bash, `cd` to your local course directory.
