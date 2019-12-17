""" Utility functions for tests. """
import pytest


@pytest.fixture
def default_config():
    """
    A config dictionary with default values.
    """
    config = {
        "template_dir": "test_template",
        "nbgrader_dir": "nbgrader",
        "extra_files": {
            "testfile.txt": ["line1", "line2"],
            "README.md": ["line1", "line2"],
        },
    }
    return config
