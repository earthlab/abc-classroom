# Tests for config methods

import pytest
import os
from ruamel.yaml import YAML
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
        == None
    )

    # test that fails when required but absent
    with pytest.raises(SystemExit):
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
        default_config, "template_dir", "templates", configpath=tmp_path
    )
    assert abcconfig.get_config_option(config, "template_dir") == "templates"
    config = abcconfig.get_config(configpath=tmp_path)
    assert abcconfig.get_config_option(config, "template_dir") == "templates"

    # test adding values to existing single value
    config = abcconfig.set_config_option(
        default_config,
        "pie",
        "pumpkin",
        append_value=True,
        configpath=tmp_path,
    )
    assert abcconfig.get_config_option(config, "pie") == ["apple", "pumpkin"]
    print(config)
    # test adding values to existing list
    config = abcconfig.set_config_option(
        default_config, "pie", "peach", append_value=True, configpath=tmp_path
    )
    print(config)
    assert abcconfig.get_config_option(config, "pie") == [
        "apple",
        "pumpkin",
        "peach",
    ]

    # test replacing existing list
    pie_list = ["pecan", "sugar"]
    config = abcconfig.set_config_option(
        default_config,
        "pie",
        pie_list,
        append_value=False,
        configpath=tmp_path,
    )
    assert abcconfig.get_config_option(config, "pie") == ["pecan", "sugar"]
