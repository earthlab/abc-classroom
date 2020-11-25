# Tests for config methods

import pytest

from pathlib import Path

import abcclassroom.config as abcconfig

# def __write_config_file(config,tmp_path):
#     yaml = YAML()
#     cfpath = Path(tmp_path,"config.yml")
#     with open(cfpath, "w") as f:
#         yaml.dump(config, f)


def test_write_config(default_config, tmp_path):
    abcconfig.write_config(default_config, configpath=tmp_path)
    assert Path(tmp_path, "config.yml").exists()


def test_get_config(default_config, tmp_path):
    abcconfig.write_config(default_config, configpath=tmp_path)
    config = abcconfig.get_config(configpath=tmp_path)
    assert config == default_config


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
