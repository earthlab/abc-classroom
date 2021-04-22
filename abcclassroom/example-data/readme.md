# Example data for abc-classroom

This directory contains two files (in addition to this readme) and a
directory.

**Do not modify the files in example-data** - they are used by `abc-classroom`
when setting up a new course.

## config.yml

The template config file. When you run `abc-quickstart`, it copies this config into the new course directory and updates the `course_directory` key. If you aren't using `abc-quickstart` and you want to create your own config, make a copy, place the copy in your course directory, and modify the copy.

## classroom_roster.csv

A sample course roster (matching the format downloaded from [GitHub classroom](https://classroom.github.com/)). This file is copied by
`abc-quickstart` into the course materials directory as a sample of
the roster format.

## extra_files

This directory gets copied to your `course_materials` directory as part of
`abc-quickstart`. After that, any additional files that you place in
`course_materials/extra_files` will be copied into new assignment
template directories. By default, this directory contains a `.gitignore` file and a `readme.md`.
