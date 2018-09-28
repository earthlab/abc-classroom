import os
import sys
import shutil

from nbclean import NotebookCleaner

from .distribute import find_notebooks, render_circleci_template


def distribute():
    """Create a student template repository for use with GitHub classroom"""
    student_repo_template = sys.argv[1]
    output_directory = sys.argv[2]

    print('Using %s to create the student template.' % student_repo_template)
    print('Creating template repository in:', output_directory)

    # always delete and recreate output directory
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    shutil.copytree(student_repo_template, output_directory)

    # the template only needs the basename, not the .ipynb extension
    notebook_paths = [f[:-6] for f in find_notebooks(student_repo_template)]

    circleci = render_circleci_template(notebook_paths)

    os.makedirs(os.path.join(output_directory, '.circleci'))
    circleci_yml = os.path.join(output_directory, '.circleci', 'config.yml')
    with open(circleci_yml, 'w') as f:
        f.write(circleci)


def author():
    notebook = sys.argv[1]
    print('Processing', notebook)

    directory, nb_name = os.path.split(notebook)
    base_name, extension = os.path.splitext(nb_name)

    # create test files and notebook for the student
    nb = NotebookCleaner(notebook)
    nb.create_tests(tag='private',
                    oktest_path=base_name,
                    base_dir='autograder')
    nb.create_tests(tag='public',
                    oktest_path=base_name,
                    base_dir='student')
    text_replace_begin = '### BEGIN SOLUTION'
    text_replace_end = '### END SOLUTION'
    nb.replace_text(text_replace_begin, text_replace_end)

    nb.save(os.path.join('student', nb_name))

    # create test files for the autograder
    nb = NotebookCleaner(notebook)
    nb.create_tests(tag='private',
                    oktest_path=base_name,
                    base_dir='autograder')
    nb.create_tests(tag='public',
                    oktest_path=base_name,
                    base_dir='autograder')
