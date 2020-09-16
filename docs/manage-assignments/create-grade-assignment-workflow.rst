Nbgrader Create and Grade Assignment Workflow
-------------------------------------------------

If you are using ``nbgrader`` as a part of your workflow, these cliff notes may
help you get started setting things up. This workflow represents that of the
Earth Analytics Education group's workflow. Be sure to refer back to the
``nbgrader`` documentation for the most recent and more robust ``nbgrader`` docs.

The documentation below assumes that you have already setup your nbgrader directory.
TODO -- add link to our documentation where that is overviewed.

Nbgrader Configuration - The Exchange Directory
================================================

``Nbgrader`` needs a location where you can read and write files in order for the
GUI based ``formgrader`` to work properly. These are simply directories that
``nbgrader`` uses to read and write files.  The location of this directory can be
specified in the ``nbgrader_config.py`` script which is ideally located within
your ``nbgrader`` directory.

Do the following:

#. in your ``nbgrader`` directory, create a subdirectory called ``tmp/exchange``. The
   name of this directory if  up to you but this name is what we use at Earth Lab.
#. Next, find the ``nbgrader_config.py`` - it should be in your ``nbgrader`` directory
   already. Add the location of your exchange directory as a parameter, TODO: add example
#. Once you have done this, launch ``Jupyter Notebook`` from your ``nbgrader`` directory. ``Nbgrader`` assumes that you are doing th is and will look for the e xchange directory and the  config files accordingly.

Once you have done this, the ``formgrader`` interface within ``Jupyter`` should work properly.
You will only need to set up the above once. After  it's setup you can simply launch
Jupyter Notebook from your ``nbgrader`` directory and everything should work.

TODO -- this is probably a step surrounding adding students as well but i haven't gotten here yet.

Create & Release Your Assignment
=================================

Next, create your assignment in the source directory of your ``nbgrader`` directory.
For the purposes of ``abc-classroom``, this directory is referred to as ``course_materials``.

Then, add the assignment to the nbgrader database using::

    nbgrader assignment add assignment-name-here

This step adds the assignment to the nbgrader database. This may be an optional
step. TODO -- more testing is needed.

At this point you are ready to work on your assignment. Test that it validates correctly.
When you are happy with the assignment you can release it. We often release the
assignment several times to look at the output and ensure that it looks correct.

TODO - make this below a note~

Important: if you are testing your assignment wi th a dummy submission prior to
releasing it to students be careful. Once an assignment is "graded" nbgrader
will not allow you to release it again. Thus a work around is to delete the
assignment from the database using::

    nbgrader db assignment remove assignment-name-here --force

IMPORTANT: Danger zone - you are removing an assignment using --force that may
have grades in your ``nbgrader`` database. Proceed with caution if you have already
graded this assignment!

TODO: BELOW CAN BE A NOTE

.. note::
  The command line to release an assignment with a header nbgrader::

        nbgrader generate_assignment assignment-name --IncludeHeaderFooter.header=source/header.ipynb --create -f

  If you add the ``--IncludeFooter.header=source/header.ipynb`` it will automagically
  add a custom  header located in the source dir called ``header.ipynb``


Collect Student Assignments
===========================

More here on collecting

When assignments are collected they are stored in a directory structure::

    student-id-1/
       assignment-1/
       assignment-2/
    student-id-2/
       assignment-1/
       assignment-2/




* if you happen to test a grading workflow and need to recreate the assignment but have already graded some
* you will have to remove the assignment using nbgrader db assignment remove assignment-name-here

Once you have released the assignment ou can share it with the students using
GitHub Classroom


TODO: add workflow here about the github classroom piece


****

3. next collect the assignments from github classroom

TODO: link here to that page

Finally grade
=======================

Once you have collected your assignments you can begin grading. To do this
go into the ``formgrader`` and select the ``autograde`` button.

.. rst-class:: fa fa-bolt

   <- The thunderbolt icon

If all goes well points will be assigned to each cell. You can go back into the
manual grader then to add comments and manually grade any items.



Notebook Design
===================
a cell with autograded answer is completely wiped clean and replace with a ``notimplemented()``.
* thus any imports or things that you need in the notebook need to be within the test cells

it appears as if anything in the test cells is available to the autograder. we
need to do more testing on this!!
