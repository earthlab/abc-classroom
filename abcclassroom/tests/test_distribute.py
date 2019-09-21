import pytest
import os
import abcclassroom.distribute as abcdist


def test_here():
    current_wd = os.getcwd()

    assert current_wd == os.getcwd()
