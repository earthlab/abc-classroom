"""
abc-classroom.config
====================

"""

import os
import sys

import os.path as op

from ruamel.yaml import YAML


def get_github_auth():
    """
    Check to see if there is an existing github authentication
    and load the authentication.

    Returns
    -------
    ruamel.yaml.comments.CommentedMap
        Yaml object that contains the token and id for a github session.
        If yaml doesn't exists, return an empty dictionary.
    """
    yaml = YAML()
    try:
        with open(op.expanduser("~/.abc-classroom.tokens.yml")) as f:
            config = yaml.load(f)
        return config["github"]

    except FileNotFoundError:
        return {}


def set_github_auth(auth_info):
    """
    Set the github authentication information. Put the token and id authentication
    information into a yaml file if it doesn't already exist.

    Parameters
    ----------
    auth_info : dictionary
        The token and id authentication information from github stored in a
        dictionary object.
    """
    yaml = YAML()
    config = {}
    if get_github_auth():
        with open(op.expanduser("~/.abc-classroom.tokens.yml")) as f:
            config = yaml.load(f)

    config["github"] = auth_info

    with open(op.expanduser("~/.abc-classroom.tokens.yml"), "w") as f:
        yaml.dump(config, f)


def get_config():
    yaml = YAML()
    try:
        with open("config.yml") as f:
            config = yaml.load(f)
        return config
    except FileNotFoundError as err:
        print(
            "Error: config file (config.yml) not found in current directory\n"
        )
        sys.exit(1)


# TODO: allow for nested gets, e.g. config[a][b]
def get_config_option(config, option, required=True):
    """
    Get an option (value of key) from provided config dictionary. If the key
    does not exist, exit with KeyError (required=True) or return None  (required=False).
    """
    try:
        value = config[option]
        return value
    except KeyError as err:
        if required == True:
            print(
                "Did not find required option {} in config; exciting".format(
                    option
                )
            )
            sys.exit(1)
        else:
            return None


def set_config(config):
    yaml = YAML()
    with open(P("config.yml"), "w") as f:
        yaml.dump(config, f)
