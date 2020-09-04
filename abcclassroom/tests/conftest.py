"""
Fixtures to set up basic directory structure, including config and
extra files, for tests.
"""
import pytest


@pytest.fixture
def default_config():
    """
    A config dictionary with default values.
    """
    config = {
        "template_dir": "test_template",
        "course_materials": "nbgrader",
        "clone_dir": "cloned-repos",
    }
    return config
