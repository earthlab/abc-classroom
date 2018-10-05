import os
import sys
import shutil
import subprocess
import yaml

from nbclean import NotebookCleaner

from .distribute import find_notebooks, render_circleci_template, git_init


def get_config():
    with open('config.yml') as f:
        config = yaml.load(f)
    return config


def grade():
    """Grade student's work"""
    config = get_config()
    assignment = config['assignment']

    for student in config['students']:
        print("Fetching work for %s..." % student)
        cwd = os.path.join('graded', student)

        # always delete and recreate students directories
        if os.path.exists(cwd):
            shutil.rmtree(cwd)
        os.makedirs(cwd)

        # use ssh in the hope that this takes care of auth problems more often
        fetch_command = ['git', 'clone',
                         'git@github.com:{}/{}-{}.git'.format(
                             assignment['organisation'],
                             assignment['name'],
                             student
                             )
                         ]
        try:
            subprocess.run(fetch_command,
                           cwd=cwd,
                           check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as err:
            print("Fetching work with '%s' failed:" % ' '.join(fetch_command))
            print()
            print(err.stderr.decode('utf-8'))
            print()
            print('Skipping this student.')
            continue

        print("Grading work...")
        print("🎉 Top marks all around because grading isn't implemented yet.")
        print()


def distribute():
    """Create a student template repository for use with GitHub classroom"""
    student_repo_template = 'student'
    output_directory = sys.argv[1]

    print('Using %s to create the student template.' % student_repo_template)
    print('Creating template repository in:', output_directory)
    print('Loading configuration from config.yml')

    config = get_config()

    # always delete and recreate output directory
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    # Copy assignment related files to the template repository
    shutil.copytree(student_repo_template, output_directory)

    # Create the grading token file which is used by the notebook bot
    # to access the CircleCI build artefacts
    grading_token = os.path.join(output_directory, '.grading.token')
    with open(grading_token, 'w') as f:
        f.write(config['tokens']['circleci'])

    # Create the required CircleCI configuration
    # the template only needs the basename, not the .ipynb extension
    notebook_paths = [f[:-6] for f in find_notebooks(student_repo_template)]

    circleci = render_circleci_template(notebook_paths)

    os.makedirs(os.path.join(output_directory, '.circleci'))
    circleci_yml = os.path.join(output_directory, '.circleci', 'config.yml')
    with open(circleci_yml, 'w') as f:
        f.write(circleci)

    # Create additional files
    for target, source in config['extra_files'].items():
        shutil.copyfile(source,
                        os.path.join(output_directory, target))

    # Final step: create git repo and commit everything
    git_init(output_directory)


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
