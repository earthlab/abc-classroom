

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3539582.svg)](https://doi.org/10.5281/zenodo.3539582)


![PyPI](https://img.shields.io/pypi/v/abc-classroom.svg?color=purple&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/abc-classroom.svg?color=purple&label=pypi%20downloads&style=plastic)
[![codecov](https://codecov.io/gh/earthlab/abc-classroom/branch/master/graph/badge.svg)](https://codecov.io/gh/earthlab/abc-classroom)

[![Documentation Status](https://readthedocs.org/projects/abc-classroom/badge/?version=latest)](https://abc-classroom.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://img.shields.io/badge/code%20style-black-000000.svg)

# Why ABC Classroom

Many of us teaching data science are using GitHub Classroom as a way to teach students
both git and GitHub skills and also potentially collaboration skills that align
with open source software development best practices. However there are many steps
associated with using GitHub classroom to manage a class.

Abc-Classroom contains a suite of command-line utilities that make it easier to
manage a class of students using GitHub classroom by:

1. Making it easier to create template assignment directories that are directly connected to your classroom organization
2. Making it easier to update those assignments and
3. (still under development) making it easier to clone all student assignments for grading.

We are currently using nbgrader in our workflow and are thus building this tool
out to support the use of nbgrader as well.

## Install abc-classroom

abc-classroom is under significant development currently. We are occasionally
pushing updates to pypi and plan to push it to conda-forge in the near future.

For now, install from PyPi using:

`$ pip install abc-classroom`

Or to get the most current updates, clone this repo and run:

`$ pip install -e . `

to install the development version.

## Use Abc-classroom
Because this is a command line set of tools, you will need to ensure that abc-classroom
is installed in the active environment that you are using for your class.

## Active Maintainers / Developers

<a title="Karen Cranston" href="https://www.github.com/kcranston"><img width="60" height="60" alt="Leah Wasser" class="pull-left" src="https://avatars.githubusercontent.com/u/312034?size=120" /></a>
<a title="Leah Wasser" href="https://www.github.com/lwasser"><img width="60" height="60" alt="Leah Wasser" class="pull-left" src="https://avatars.githubusercontent.com/u/7649194?size=120" /></a>

## How to Contribute

We welcome contributions to abc-classroom as we are developing it and beyond! Please be sure to check out our
[contributing guidelines](https://abc-classroom.readthedocs.io/en/latest/contributing.html)
for more information about submitting pull requests or changes to abc-classroom.

## License & Citation

[BSD-3](https://github.com/earthlab/abc-classroom/blob/master/LICENSE)
