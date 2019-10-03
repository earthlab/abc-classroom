"""
abc-classroom.dir-setup
===================

"""

import os
import shutil
import argparse


def directory_setup():
    cloned = "cloned_repos"
    template = "template_repos"
    main_dir = os.path.join(os.getcwd(), "course_dir")
    if os.path.isdir(main_dir):
        raise ValueError("Direcoty setup has already been run in this directory.")
    parser = argparse.ArgumentParser(description="Name subdirectories in the course directory.")
    parser.add_argument(
        "--cloned_repo",
        help="Name of the repository to hold the cloned files"
    )
    parser.add_argument(
        "--template_repo",
        help="Name of the repository to hold the template files"
    )
    args = parser.parse_args()
    if args.cloned_repo:
        cloned = args.cloned_repo
    if args.template_repo:
        template = args.template_repo
    os.mkdir(main_dir)
    cloned_dir = os.path.join(main_dir, cloned)
    template_dir = os.path.join(main_dir, template)
    os.mkdir(cloned_dir)
    os.mkdir(template_dir)
    config = os.path.join(os.getcwd(), "setup-config.yml")
    if os.path.exists(config):
        shutil.copyfile(config, main_dir)
    else:
        raise ValueError("Configuration file can't be located, please run this in the same folder abc-classroom")
