"""
abc-classroom.config
====================

"""

import os
import sys
from pathlib import Path
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


def get_config(configpath=None):
    yaml = YAML()
    try:
        if configpath is None:
            configpath = Path("config.yml")
        else:
            configpath = Path(configpath, "config.yml")
        with open(configpath) as f:
            config = yaml.load(f)
        return config
    except FileNotFoundError as err:
        configpath.resolve()
        print(
            "Oops! I can't seem to find a config.yml file at {}. "
            "Are you in the top-level directory for the course? If you don't have a course directory and config file "
            "setup yet, you can create one using abc-quickstart"
            ".\n".format(configpath)
        )
        sys.exit(1)


def write_config(config, configpath=None):
    yaml = YAML()
    if configpath is None:
        configpath = Path("config.yml")
    else:
        configpath = Path(configpath, "config.yml")
    print("Writing config to {}".format(configpath))
    with open(configpath, "w") as f:
        yaml.dump(config, f)


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
                "Did not find required option {} in config; exiting".format(
                    option
                )
            )
            sys.exit(1)
        else:
            return None


def set_config_option(
    config, option, value, append_value=False, configpath=None
):
    """
    Sets a config option. If option already exists and append_value is False, replaces existing value. If option exists and append_value is true, adds new value to list of existing values. Writes the new config (overwriting the existing file) and returns new config dict.
    """

    existing_value = get_config_option(config, option, required=False)
    if append_value == True and existing_value is not None:
        if isinstance(existing_value, list):
            existing_value.append(value)
            value = existing_value
        else:
            value = [existing_value, value]
    config[option] = value
    print("Writing new config at {}".format(configpath))
    write_config(config, configpath)
    return config
