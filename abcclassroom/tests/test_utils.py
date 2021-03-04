"""
abc-classroom.utils
======================

"""

from pathlib import Path

import pytest

import abcclassroom.utils as abcutils


@pytest.fixture
def test_files(tmp_path):
    """Create some test files and directories"""
    source_path = Path(tmp_path, "source")
    source_path.mkdir()
    Path(source_path, "file1.txt").touch()
    Path(source_path, "data.csv").touch()
    Path(source_path, ".hidden").touch()
    # a subdirectory
    Path(source_path, "subdir").mkdir()
    Path(source_path, "subdir", "file3.txt").touch()
    # a subdirectory that we are going to ignore
    Path(source_path, "ignored").mkdir()
    Path(source_path, "ignored", "file4.txt").touch()
    return source_path


def test_copy_files(default_config, tmp_path, test_files):
    """
    Test that we copy all files and dirs recursively when no ignore
    filter specified.
    """
    source_dir = test_files
    dest_dir = Path(tmp_path, "destination")
    abcutils.copy_files(source_dir, dest_dir)
    src_files = list(source_dir.rglob("*"))
    dest_files = list(dest_dir.rglob("*"))

    # did we copy some stuff?
    assert len(dest_files) > 0

    # are they the same?
    # need to make all paths relative to src and dest
    src_files = [str(Path(x).relative_to(source_dir)) for x in src_files]
    dest_files = [str(Path(x).relative_to(dest_dir)) for x in dest_files]
    assert src_files == dest_files


def test_copy_files_with_ignored(default_config, tmp_path, test_files):
    """
    Test that we ignore files and directories that match filter patterns.
    """
    source_dir = test_files
    ignore_patterns = [".hidden", "*.csv", "ignored"]
    dest_dir = Path(tmp_path, "destination")
    abcutils.copy_files(source_dir, dest_dir, ignore_patterns)
    # check a file that we expect
    assert Path(dest_dir, "subdir", "file3.txt").exists()

    # check files that we do not expect
    assert Path(dest_dir, "data.csv").exists() is False
    assert Path(dest_dir, "ignored").exists() is False
