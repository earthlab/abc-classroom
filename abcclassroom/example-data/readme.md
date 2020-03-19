# Example data for abc-classroom

This directory contains two files and a directory.

## config.yml

**Do not modify this file in this location**

The template config file. When you run `abc-quickstart`, it copies this config into the new course directory and updates the `course_directory` key. Because this file is used by **abc-classroom**, do not modify this file directly. If you aren't using `abc-quickstart` and you want to create your own config, make a copy, place the copy in your course directory, and modify the copy.

## sample_roster.csv

A sample course roster (matching the format downloaded from [GitHub classroom](https://classroom.github.com/)). This file is not used by **abc-classroom** directly. It is only provided here for reference.

## extra_files

This directory gets copied to your `course_materials` directory. Then, any files
placed in `course_materials/extra_files` will be copied into new assignment
template directories. By default, this directory contains a `.gitignore` file and
a `readme.md`.
