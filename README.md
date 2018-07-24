# Experimenting with grading workflows

This repository is the wild wild west playground for experimenting with workflows
that allow a course instructor to prepare material, distribute it to learners,
and for them to then turn in their homework.


## Assumptions

* instructor authors all work in a notebook
* instructor version of materials is published on a private GitHub repository
* student version of materials is published on a public GitHub repository
* answer to an assignment is multiple choice question
* answer to an assignment is code to be executed
* answer to an assigment is free form text
* partial answers to assignments receive partial credit
* assignments contain public parts
* assignments contain private parts
* public assignments can be executed by students on their notebook server
* solutions to public assignments can be seen by students
* solutions to private assignments can not be seen by students
* private assignments are executed by the "autograder" after students submit
  their work


## Questions

### How to check for "good style"?

Check for general programming style of the notebook. Variable names that are
sensible. All packages are imported at the top.

Run flake8 or pep8 on notebook converted to a `.py`?


### Is there a spellcheck extension for notebooks?


### How to check for "extra" stuff in the notebook?

We don't want a bunch of extra stuff. Can we test that there aren't extra
plots in the notebook?
