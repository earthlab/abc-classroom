# Tests for config methods

import pytest

from pathlib import Path

import abcclassroom.config as abcconfig


@pytest.fixture
def broken_config(tmp_path):
    """
    Writes a improperly formatted config.yml file into the directory
    broken_config.
    """

    # Create directory for the config (to avoid messing up the config
    # in tmp_path used by other tests)
    dir = Path(tmp_path, "broken_config")
    dir.mkdir()
    configpath = Path(dir, "config.yml")

    # write broken file (we can't use yaml / ruamel for this, because
    # it would throw an error writing the file)
    # The broken line is the *.csv without quotes
    with open(configpath, "w") as f:
        f.write("files_to_ignore:\n")
        f.write("- .DS_Store\n")
        f.write("- .ipynb_checkpoints\n")
        f.write("- *.csv\n")

    return dir


def test_get_config(default_config, tmp_path):
    """Test basic getting of config"""
    abcconfig.write_config(default_config, configpath=tmp_path)
    config = abcconfig.get_config(configpath=tmp_path)
    assert config == default_config


def test_get_config_does_not_exist():
    """Test that get_config throws a FileNotFoundError when the
    given path does not exist.
    """
    with pytest.raises(
        FileNotFoundError, match="Oops! I can't seem to find a config.yml"
    ):
        abcconfig.get_config("dirthatdoesntexist")


def test_broken_config(broken_config):
    """Test that we throw the right exception when the config contains
    an unquoted wildcard (interpreted as a yaml alias)."""
    with pytest.raises(RuntimeError, match="Error reading config.yml"):
        abcconfig.get_config(broken_config)


def test_write_config(default_config, tmp_path):
    """Test that we can write the config to a custom path"""
    testpath = Path(tmp_path, "write_config")
    testpath.mkdir()
    abcconfig.write_config(default_config, configpath=testpath)
    assert Path(testpath, "config.yml").exists()


def test_get_config_option(default_config):
    # test that works in basic get existing option cases
    assert (
        abcconfig.get_config_option(default_config, "template_dir")
        == "test_template"
    )
    assert (
        abcconfig.get_config_option(default_config, "template_dir", True)
        == "test_template"
    )
    assert (
        abcconfig.get_config_option(default_config, "template_dir", False)
        == "test_template"
    )

    # test we're ok when option not required and missing
    assert (
        abcconfig.get_config_option(default_config, "floofykitten", False)
        is None
    )

    # Test that fails when required but absent
    with pytest.raises(
        KeyError, match="Oops! I  couldn't find the required option"
    ):
        abcconfig.get_config_option(default_config, "floofykitten", True)


def test_set_config_option(default_config, tmp_path):
    abcconfig.write_config(default_config, configpath=tmp_path)

    # test writing new value
    config = abcconfig.set_config_option(
        default_config, "pie", "apple", configpath=tmp_path
    )
    assert abcconfig.get_config_option(config, "pie") == "apple"

    # test replacing existing value
    config = abcconfig.set_config_option(
        default_config, "pie", "peach", configpath=tmp_path
    )
    assert abcconfig.get_config_option(config, "pie") == "peach"

    # test adding values to existing single value
    config = abcconfig.set_config_option(
        default_config,
        "pie",
        "pumpkin",
        append_value=True,
        configpath=tmp_path,
    )
    assert "peach" in abcconfig.get_config_option(config, "pie")
    assert "pumpkin" in abcconfig.get_config_option(config, "pie")

    # test adding values to existing list
    config = abcconfig.set_config_option(
        default_config, "pie", "pecan", append_value=True, configpath=tmp_path
    )
    assert "pecan" in abcconfig.get_config_option(config, "pie")

    # test that we don't add duplicates
    config = abcconfig.set_config_option(
        default_config, "pie", "pecan", append_value=True, configpath=tmp_path
    )
    assert abcconfig.get_config_option(config, "pie").count("pecan") == 1

    # test replacing existing list
    pie_list = ["pecan", "sugar"]
    config = abcconfig.set_config_option(
        default_config,
        "pie",
        pie_list,
        append_value=False,
        configpath=tmp_path,
    )
    assert len(abcconfig.get_config_option(config, "pie")) == 2
    assert "sugar" in abcconfig.get_config_option(config, "pie")
