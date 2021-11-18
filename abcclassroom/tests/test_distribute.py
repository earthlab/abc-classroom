# I am not sure what this test file is for? can we just remove it?

import os


def test_here():
    current_wd = os.getcwd()

    assert current_wd == os.getcwd()
