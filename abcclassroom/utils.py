"""
abc-classroom.utils
===================

"""


import os
import stat
import shutil
import subprocess
import tempfile
import textwrap

import requests


def copy_files(src_dir, dest_dir, files_to_ignore=None):
    """Copies contents of src_dir into dest_dir, creating dest_dir if it
    does not exist. Uses 'files_to_ignore' list to determine what not to
    copy. Copies subdirectories recursively. Overwrites existing files
    with the same path. Implements the python 3.8 version of copytree,
    which allows dest_dir to exits.

    Throws FileNotFoundError if src_dir does not exist.

    Parameters
    ----------
    src_dir: path
        Directory to copy files from. Must exist.
    dest_dir: path
        Directory to copy files to. Must exist.
    files_to_ignore: list
        List of file patterns to ignore.
    """

    if files_to_ignore:
        abccopytree(
            src_dir,
            dest_dir,
            ignore=shutil.ignore_patterns(*files_to_ignore),
            dirs_exist_ok=True,
        )
    else:
        abccopytree(src_dir, dest_dir, dirs_exist_ok=True)


class Error(OSError):
    pass


# implements a simple GET request to the GitHub API url provided,
# optionally using a token in the authentication header
# returns the status code and response
def get_request(url, token=None):
    if token is None:
        header = {
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
        }
    else:
        header = {
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token {}".format(token),
        }
    r = requests.get(url, headers=header)
    return (r.status_code, r.json())


# The following two functions are from python>3.8 where copytree
# has an optional argument that allows the destination directory to exist
# Once we are no longer supporting Python<3.8 we should delete these and
# simply call shutil.copytree
# See https://github.com/python/cpython/blob/3.9/Lib/shutil.py for source
def _abccopytree(
    entries,
    src,
    dst,
    symlinks,
    ignore,
    copy_function,
    ignore_dangling_symlinks,
    dirs_exist_ok=False,
):
    if ignore is not None:
        ignored_names = ignore(os.fspath(src), [x.name for x in entries])
    else:
        ignored_names = set()

    os.makedirs(dst, exist_ok=dirs_exist_ok)
    errors = []
    use_srcentry = (
        copy_function is shutil.copy2 or copy_function is shutil.copy
    )

    for srcentry in entries:
        if srcentry.name in ignored_names:
            continue
        srcname = os.path.join(src, srcentry.name)
        dstname = os.path.join(dst, srcentry.name)
        srcobj = srcentry if use_srcentry else srcname
        try:
            is_symlink = srcentry.is_symlink()
            if is_symlink and os.name == "nt":
                # Special check for directory junctions, which appear as
                # symlinks but we want to recurse.
                lstat = srcentry.stat(follow_symlinks=False)
                if lstat.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT:
                    is_symlink = False
            if is_symlink:
                linkto = os.readlink(srcname)
                if symlinks:
                    # We can't just leave it to `copy_function` because legacy
                    # code with a custom `copy_function` may rely on copytree
                    # doing the right thing.
                    os.symlink(linkto, dstname)
                    shutil.copystat(
                        srcobj, dstname, follow_symlinks=not symlinks
                    )
                else:
                    # ignore dangling symlink if the flag is on
                    if not os.path.exists(linkto) and ignore_dangling_symlinks:
                        continue
                    # otherwise let the copy occur. copy2 will raise an error
                    if srcentry.is_dir():
                        abccopytree(
                            srcobj,
                            dstname,
                            symlinks,
                            ignore,
                            copy_function,
                            dirs_exist_ok=dirs_exist_ok,
                        )
                    else:
                        copy_function(srcobj, dstname)
            elif srcentry.is_dir():
                abccopytree(
                    srcobj,
                    dstname,
                    symlinks,
                    ignore,
                    copy_function,
                    dirs_exist_ok=dirs_exist_ok,
                )
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy_function(srcobj, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        # Copying file access times may fail on Windows
        if getattr(why, "winerror", None) is None:
            errors.append((src, dst, str(why)))
    if errors:
        raise Error(errors)
    return dst


def abccopytree(
    src,
    dst,
    symlinks=False,
    ignore=None,
    copy_function=shutil.copy2,
    ignore_dangling_symlinks=False,
    dirs_exist_ok=False,
):
    """Recursively copy a directory tree and return the destination directory.
    dirs_exist_ok dictates whether to raise an exception in case dst or any
    missing parent directory already exists.
    If exception(s) occur, an Error is raised with a list of reasons.
    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied. If the file pointed by the symlink doesn't
    exist, an exception will be added in the list of errors raised in
    an Error exception at the end of the copy process.
    You can set the optional ignore_dangling_symlinks flag to true if you
    want to silence this exception. Notice that this has no effect on
    platforms that don't support os.symlink.
    The optional ignore argument is a callable. If given, it
    is called with the `src` parameter, which is the directory
    being visited by copytree(), and `names` which is the list of
    `src` contents, as returned by os.listdir():
    callable(src, names) -> ignored_names
    Since copytree() is called recursively, the callable will be
    called once for each directory that is copied. It returns a
    list of names relative to the `src` directory that should
    not be copied.
    The optional copy_function argument is a callable that will be used
    to copy each file. It will be called with the source path and the
    destination path as arguments. By default, copy2() is used, but any
    function that supports the same signature (like copy()) can be used.
    """
    # sys.audit not available until python 3.8
    # sys.audit("shutil.copytree", src, dst)
    with os.scandir(src) as itr:
        entries = list(itr)
    return _abccopytree(
        entries=entries,
        src=src,
        dst=dst,
        symlinks=symlinks,
        ignore=ignore,
        copy_function=copy_function,
        ignore_dangling_symlinks=ignore_dangling_symlinks,
        dirs_exist_ok=dirs_exist_ok,
    )


def input_editor(default_message=None):
    """Ask for user input via a text editor"""
    default_message = textwrap.dedent(default_message)

    with tempfile.NamedTemporaryFile(mode="r+") as tmpfile:
        if default_message is not None:
            tmpfile.write(default_message)
            tmpfile.flush()
        subprocess.check_call([get_editor(), tmpfile.name])
        tmpfile.seek(0)

        with open(tmpfile.name) as f:
            msg = f.read()
            return msg.strip()


def get_editor():
    return os.environ.get("VISUAL") or os.environ.get("EDITOR") or "vi"


def get_abspath(testpath, coursepath):
    """
    Create an absoluate path of testpath inside coursepath if testpath is
    not already absolute.
    """
    if os.path.isabs(testpath):
        return testpath
    else:
        return os.path.join(coursepath, testpath)


def write_file(filepath, contents):
    """Write a new file with the given path.
    Each item in contents is a line in the file.
    """
    # filepath = os.path.join(dir, filename)
    try:
        with open(filepath, "w") as f:
            for line in contents:
                f.write("{}".format(line))

    except OSError as err:
        print("Cannot open file: {0}".format(err))
