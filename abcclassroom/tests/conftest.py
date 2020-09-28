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
        "files_to_ignore": [".DS_Store", ".ipynb_checkpoints"],
    }
    return config
