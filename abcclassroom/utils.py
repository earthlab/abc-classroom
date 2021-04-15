"""
abc-classroom.utils
===================

"""


import os
import stat
import shutil
import subprocess
import sys
import tempfile
import textwrap

import requests
from contextlib import contextmanager

from IPython import get_ipython


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


# TODO: this will require grabbing paths to files or creating paths in this
# function so it will require a bit more thought.

#
# def move_files(all_files, src_dir, dest_dir):
#     """Moves files from one location to another.
#
#     Ignores files specified
#     in the ``files_to_ignore`` in the config. Currently does not support
#     moving directories but could in the future.
#
#     Parameters
#     ----------
#     all_files: list or glob generator object?
#         list of file and directory names to move
#     src_dir: path
#         Path to the src directory of files to move
#     dest_dir: path
#         Path to the destination directory of files to move
#
#     """
#     # TODO this could also use the copy files helper - thinking to put it in
#     # the utils module
#     # Get a list of files to ignore - maybe our default config has some
#     # could have some defaults - then remove all files that we want to ignore
#     config = cf.get_config()
#     files_to_ignore = cf.get_config_option(config, "files_to_ignore", True)
#     files_to_move = set(all_files).difference(files_to_ignore)
#
#     for file in files_to_move:
#         fpath = Path(release_dir, file)
#         if fpath.is_dir():
#             # TODO: Note that as written here, moving directories will fail
#             print(
#                 "Oops - looks like {} is a directory. Currently I can't "
#                 "move that for you. Contact the abc-classroom maintainers"
#                 "if this is a feature that you'd "
#                 "like".format(fpath.relative_to(course_dir))
#             )
#         else:
#             print(" {}".format(fpath.relative_to(course_dir)))
#             # Overwrites if fpath exists in template_repo
#             shutil.copy(fpath, template_repo)
#             nfiles += 1
#
#     print("Copied {} files to your assignment directory!".format(nfiles))
#     print("The files copied include: {}".format(files_to_move))


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


# Draft for a function to include only certain patterns instead of ignoring
# patterns when copying folders

# def include_patterns(patterns):
#     """Factory function that can be used with copytree() ignore parameter.
#
#     Arguments define a sequence of glob-style patterns
#     that are used to specify what files to NOT ignore.
#     Creates and returns a function that determines this for each directory
#     in the file hierarchy rooted at the source directory when used with
#     shutil.copytree().
#
#     Parameters
#     -----------
#     patterns: list
#         List of strings file extensions to be copied. Should be a string of
#         what it's expected the file name will end in.
#     """
#
#     # We might want to move this to utils, as it is a helper for copytree
#
#     def _ignore_patterns(path, names):
#         keep = set(
#             name
#             for pattern in patterns
#             for name in names
#             if name.endswith(pattern)
#         )
#         ignore = set(
#             name
#             for name in names
#             if name not in keep and not Path(path, name).is_dir()
#         )
#         return ignore
#
#     return _ignore_patterns

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


def flush_inline_matplotlib_plots():
    """
    Flush matplotlib plots immediately, rather than asynchronously.
    Basically, the inline backend only shows the plot after the entire
    cell executes, which means we can't easily use a contextmanager to
    suppress displaying it.
    See https://github.com/jupyter-widgets/ipywidgets/issues/1181/
    and https://github.com/ipython/ipython/issues/10376 for more details. This
    function displays flushes any pending matplotlib plots if we are using
    the inline backend.

    Stolen from https://github.com/jupyter-widgets/ipywidgets/blob/4cc15e66d5e9e69dac8fc20d1eb1d7db825d7aa2/ipywidgets/widgets/interaction.py#L35 # noqa: E501
    """
    if "matplotlib" not in sys.modules:
        # matplotlib hasn't been imported, nothing to do.
        return

    try:
        import matplotlib as mpl
        from ipykernel.pylab.backend_inline import flush_figures
    except ImportError:
        return

    if mpl.get_backend() == "module://ipykernel.pylab.backend_inline":
        flush_figures()


@contextmanager
def hide_outputs():
    """
    Context manager for hiding outputs from display() calls.

    IPython handles matplotlib outputs specially, so those are supressed too.
    """
    ipy = get_ipython()
    if ipy is None:
        # Not running inside ipython!
        yield
        return
    old_formatters = ipy.display_formatter.formatters
    ipy.display_formatter.formatters = {}
    try:
        yield
    finally:
        ipy.display_formatter.formatters = old_formatters


@contextmanager
def chdir(path):
    """Change working directory to `path` and restore old path on exit.
    `path` can be `None` in which case this is a no-op.
    """
    if path is None:
        yield
    else:
        old_dir = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(old_dir)


#################################################################
# Unused code from before the refactor that is causing the
# linters to fail

# def P(*paths):
#     """Construct absolute path inside the repository from `paths`"""
#     path = os.path.join(*paths)
#     return os.path.join(TOP(), path)

# @lru_cache(1)
# def TOP():
#     """Path to the top level of the repository we are in"""
#     try:
#         ret = _call_git("rev-parse", "--show-toplevel")
#     except RuntimeError as e:
#         print(" ".join(e.args))
#         sys.exit(1)
#
#     return ret.stdout.decode("utf-8").strip()

# def valid_date(s):
#     try:
#         return datetime.datetime.strptime(s, "%Y-%m-%d").date()
#     except ValueError:
#         msg = "Not a valid date: '{0}'.".format(s)
#         raise argparse.ArgumentTypeError(msg)
