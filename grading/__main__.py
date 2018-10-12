import argparse
import datetime
import glob
import os
import shutil
import subprocess
import tempfile

from getpass import getpass

from ruamel.yaml import YAML

from github3 import authorize

from .distribute import find_notebooks, render_circleci_template
from .notebook import split_notebook
from . import github as GH
from .utils import copytree


def get_config():
    yaml = YAML()
    with open('config.yml') as f:
        config = yaml.load(f)
    return config


def set_config(config):
    yaml = YAML()
    with open('config.yml', 'w') as f:
        yaml.dump(config, f)


def init():
    """Setup GitHub credentials for later"""
    user = input('GitHub username: ')
    password = ''

    while not password:
        password = getpass('Password for {0}: '.format(user))

    note = 'grading workflow helper'
    note_url = 'http://example.com'
    scopes = ['repo']

    def two_factor():
        code = ''
        while not code:
            # The user could accidentally press Enter before being ready,
            # let's protect them from doing that.
            code = input('Enter 2FA code: ')
        return code

    auth = authorize(user, password, scopes, note, note_url,
                     two_factor_callback=two_factor)

    config = get_config()
    config['github'] = {'token': auth.token, 'id': auth.id}
    set_config(config)


def grade():
    """Grade student's work"""
    config = get_config()
    course = config['courseName']

    for student in config['students']:
        print("Fetching work for %s..." % student)
        cwd = os.path.join('graded', student)

        # always delete and recreate students directories
        if os.path.exists(cwd):
            shutil.rmtree(cwd)
        os.makedirs(cwd)

        # Use HTTPS and tokens to avoid access problems
        # `git clone https://<token>@github.com/owner/repo.git`
        fetch_command = ['git', 'clone',
                         'https://{}@github.com/{}/{}-{}.git'.format(
                             config['github']['token'],
                             config['organisation'],
                             course,
                             student,
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
    parser = argparse.ArgumentParser(description='Distribute work to students')
    parser.add_argument('--template',
                        action='store_true',
                        help='Create template repository only (default: False)'
                        )
    args = parser.parse_args()

    student_repo_template = 'student'

    print('Using %s to create the student template.' % student_repo_template)
    print('Loading configuration from config.yml')

    config = get_config()

    if args.template:
        print("Creating template repository.")
        repo_name = "{}-{}".format(config['courseName'], 'template')
        with tempfile.TemporaryDirectory() as d:
            copytree('student', d)
            GH.git_init(d)
            GH.commit_all_changes(d, "Initial commit")
            GH.create_repo(config['organisation'],
                           repo_name,
                           d,
                           config['github']['token'])

        print('Visit https://github.com/{}/{}'.format(config['organisation'],
                                                     repo_name))

    else:
        for student in config['students']:
            print("Fetching work for %s..." % student)
            with tempfile.TemporaryDirectory() as d:
                student_dir = GH.fetch_student(config['organisation'],
                                               config['courseName'],
                                               student,
                                               directory=d)
                # Copy assignment related files to the template repository
                copytree('student', student_dir)

                if GH.repo_changed(student_dir):
                    repo = "{}-{}".format(config['courseName'], student)
                    message = 'New material for next week.'
                    branch = GH.new_branch(student_dir)

                    GH.commit_all_changes(student_dir, message)
                    GH.push_to_github(student_dir, branch)
                    GH.create_pr(config['organisation'],
                                 repo,
                                 branch,
                                 message,
                                 config['github']['token'])

                else:
                    print("Everything up to date.")


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
                        help=('Assumed date when preparing assignments '
                              '(default: today)'))
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

    # Create the grading token file which is used by the notebook bot
    # to access the CircleCI build artefacts
    grading_token = os.path.join('student', '.grading.token')
    with open(grading_token, 'w') as f:
        f.write(config['tokens']['circleci'])

    # Create the required CircleCI configuration
    # the template only needs the basename, not the .ipynb extension
    notebook_paths = [f[:-6] for f in find_notebooks('student')]
    circleci = render_circleci_template(notebook_paths)

    os.makedirs(os.path.join('student', '.circleci'))
    circleci_yml = os.path.join('student', '.circleci', 'config.yml')
    with open(circleci_yml, 'w') as f:
        f.write(circleci)

    print("Inspect `student/` to check it looks as you expect.")
