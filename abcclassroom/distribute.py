"""
abc-classroom.distribute
========================

Take a template directory and distribute it
"""
import os
import subprocess

import jinja2


# current directory
HERE = os.path.dirname(os.path.abspath(__file__))


def find_notebooks(base_path):
    """Find all notebooks below base_path and return path to them"""
    notebook_paths = []
    for path, _, files in os.walk(base_path):
        # remove leading directory
        path = os.path.relpath(path, base_path)
        for f in files:
            if f.endswith(".ipynb"):
                notebook_paths.append(os.path.join(path, f))

    return notebook_paths


def render_circleci_template(notebook_paths):
    """Load the CircleCI template"""
    template = open(os.path.join(HERE, "circleci.yml")).read()

    t = jinja2.Template(template)

    return t.render(
        notebook_dirs=[os.path.dirname(p) for p in notebook_paths],
        notebook_names=[os.path.split(p)[1] for p in notebook_paths],
        notebooks=notebook_paths,
    )


def git_init(directory):
    """Initialise and populate a git repository in `directory`

    Add all files in `directory` to a newly create git repository in that
    directory.
    """
    subprocess.run(
        ["git", "init"], cwd=directory, check=True, stdout=subprocess.PIPE
    )

    subprocess.run(
        ["git", "add", "*"], cwd=directory, check=True, stdout=subprocess.PIPE
    )

    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=directory,
        check=True,
        stdout=subprocess.PIPE,
    )
