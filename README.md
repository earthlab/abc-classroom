# Experimenting with grading workflows

This under development package supports several activities related to developing 
online courses using Jupyter notebooks including:

1. preparing course materials 
2. distributing course materials to learners in a GitHub classroom environment
3. automatic feedback on student assignments using CircleCi and
4. autograding infrastructure for student assignments

## Try it out!

Install locally with `pip install -e.` from the directory of this README.

Then run `nbauthor master/01-lecture.ipynb`. This will take the master notebook,
and create a student and autograder version. The student version will be in
the `student/` subdirectory and the autograder version in `autograder/`.

The student directory can be distributed to students. It includes the questions
and code to run the grading steps that students can execute themselves.

To create a template repository for students use the `nbdistribute` command.
After running `nbauthor` on all the notebooks you want to include run:
`nbdistribute /tmp/student-template` to take the contents of the
`student/` directory and create a template repository from it at `/tmp/student-template`. Push this repository to GitHub and use it as the
template for your GitHub classroom assignment.

In the autograder directory you will find both the public and private tests,
but no notebook. The idea is that at a later stage students submit their
notebook and it is executed in the autograder directory by some server/robot.


## Assumptions

* instructor authors all work in a notebook
* instructor version of materials is published on a private GitHub repository
* student version of materials is published on a public GitHub repository
* answer to an assignment is multiple choice question
* answer to an assignment is code to be executed
* answer to an assignment is free form text
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
