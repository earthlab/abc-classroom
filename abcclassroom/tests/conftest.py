""" Utility functions for tests. """
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
        "extra_files": {
            "testfile.txt": ["line1", "line2"],
            "README.md": ["line1", "line2"],
        },
    }
    return config
