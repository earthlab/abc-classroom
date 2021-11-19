"""
abc-classroom.config
====================

"""

import pprint
from pathlib import Path
from ruamel.yaml import YAML
import ruamel.yaml.composer


def get_config(configpath=None):
    """Attempts to read a config file at the provided path (or at
    "config.yml" if no path provided). Throws FileNotFoundError if no
    config file found, and RuntimeError if there
    is a problem reading the file.

    Returns
    -------
    ruamel.yaml.comments.CommentedMap
        Yaml object that contains the contents of the config file.
    """
    yaml = YAML()
    try:
        if configpath is None:
            configpath = Path("config.yml")
        else:
            configpath = Path(configpath, "config.yml")
        with open(configpath) as f:
            config = yaml.load(f)
        return config
    except ruamel.yaml.composer.ComposerError:
        raise RuntimeError(
            "Error reading config.yml. This can happen if the config "
            "contains an unquoted *. Try adding quotes around any wildcards "
            "in the config, e.g. '*.csv'. See "
            "https://abc-classroom.readthedocs.io/en/latest/get-started/configuration.html "  # noqa
            "for details."
        )
    except FileNotFoundError:
        c = configpath.resolve()
        raise FileNotFoundError(
            "Oops! I can't seem to find a config.yml file at {}. "
            "Are you in the top-level directory for the course? If you don't "
            "have a course directory and config file "
            "setup yet, you can create one using abc-quickstart"
            ".\n".format(c)
        )


def print_config(config=None, configpath=None):
    """
    Print configuration. Can supply as dictionary parameter, or specify a path
    to look for config.yml. If neither option specified, looks for config.yml
    in current working directory. If both specified, prints dictionary, not
    from file.
    """
    configtoprint = {}
    if config is None:
        configtoprint = get_config(configpath)
    else:
        configtoprint = config
    print("Current configuration:\n")
    pprint.pprint(configtoprint)


def write_config(config, configpath=None):
    yaml = YAML()
    if configpath is None:
        configpath = Path("config.yml")
    else:
        configpath = Path(configpath, "config.yml")
    with open(configpath, "w") as f:
        yaml.dump(config, f)


# TODO: allow for nested gets, e.g. config[a][b]
def get_config_option(config, option, required=True):
    """
    Get an option (value of key) from provided config dictionary. If the key
    does not exist, exit with KeyError (required=True) or return None
    (required=False).
    """
    try:
        value = config[option]
        return value
    except KeyError:
        if required:
            raise KeyError(
                "Oops! I  couldn't find the required option in the "
                "config file. Check your config file to ensure the the {} "
                "option is populated".format(option)
            )
        else:
            return None


def set_config_option(
    config, option, value, append_value=False, configpath=None
):
    """
    Sets a config option. If option already exists and append_value is False,
    replaces existing value. If option exists and append_value is true, adds
    new value to list of existing values. Will not add a duplicate value.

    Writes the new config (overwriting the existing file) and returns new
    config dict.
    """

    existing_value = get_config_option(config, option, required=False)
    if append_value and existing_value is not None:
        if isinstance(existing_value, list):
            existing_value.append(value)
            value = existing_value
        else:
            value = [existing_value, value]
        # eliminate duplicates
        value = list(set(value))
    config[option] = value
    print("Writing modified config at {}".format(configpath))
    write_config(config, configpath)
    return config
