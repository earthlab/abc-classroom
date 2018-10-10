import argparse
import datetime
import glob
import os
import shutil
import subprocess
import sys
import yaml

from .distribute import find_notebooks, render_circleci_template, git_init
from .notebook import split_notebook


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
    """Create or update student repositories"""
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


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def author():
    """Create student repository and autograding tests"""
    parser = argparse.ArgumentParser(description='Author student repository.')
    parser.add_argument('--date',
                        default=datetime.datetime.today().date(),
                        type=valid_date,
                        help='Assumed date when preparing assignments (default: today)')
    args = parser.parse_args()

    config = get_config()
    now = args.date

    if os.path.exists('student'):
        shutil.rmtree('student')
    os.makedirs('student')

    if os.path.exists('autograder'):
        shutil.rmtree('autograder')

    for assignment in os.listdir('master'):
        release_date = config['assignments'][assignment]['release']
        if release_date > now:
            continue

        student_path = os.path.join('student', assignment)
        master_path = os.path.join('master', assignment)

        # copy over everything, including master notebooks. They will be
        # overwritten by split_notebook() below
        shutil.copytree(master_path, student_path)

        for notebook in glob.glob('master/%s/*.ipynb' % assignment):
            split_notebook(notebook,
                           student_path,
                           os.path.join('autograder', assignment))

    # Create additional files
    for target, source in config['extra_files'].items():
        shutil.copyfile(source,
                        os.path.join('student', target))
