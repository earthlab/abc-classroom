"""
abc-classroom.dir-setup
===================

"""

import os
import shutil


def directory_setup(cloned="cloned_repos", template="template_repos"):
    home = os.getcwd()
    main_dir = os.path.join(home, "course_dir")
    if os.path.isdir(main_dir):
        raise ValueError("Direcoty setup has already been run in this directory.")
    os.mkdir(main_dir)
    cloned_dir, template_dir = os.path.join(main_dir, cloned), os.path.join(main_dir, template)
    os.mkdir(cloned_dir), os.mkdir(template_dir)
    config = os.path.join(home, "setup-config.yml")
    if os.path.exists(config):
        shutil.copyfile(config, main_dir)
    else:
        raise ValueError("Configuration file can't be located, please run this in the same folder abc-classroom")
