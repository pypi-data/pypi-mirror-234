"""
File system helpers
"""

import functools
import os
import pathlib
import re
import time

from .. import __project_name__, constants, errors
from . import LazyModule, os_family, types

import logging  # isort:skip
_log = logging.getLogger(__name__)

natsort = LazyModule(module='natsort', namespace=globals())


OS_SEP_REGEX = re.escape(os.sep)
r"""
:attr:`os.sep` escaped with :func:`re.escape`

On Windows, this should be ``"\\"`` while it should be identical to
:attr:`os.sep` on Unix-likes.
"""


def assert_file_readable(filepath):
    """Raise :exc:`~.ContentError` if `open(filepath)` fails"""
    try:
        open(filepath).close()
    except OSError as e:
        raise errors.ContentError(f'{filepath}: {e.strerror or e}')


def assert_dir_usable(path):
    """Raise :exc:`~.ContentError` if `dirpath` can not be used as a directory"""
    if not os.path.isdir(path):
        raise errors.ContentError(f'{path}: Not a directory')
    elif not os.access(path, os.R_OK):
        raise errors.ContentError(f'{path}: Not readable')
    elif not os.access(path, os.W_OK):
        raise errors.ContentError(f'{path}: Not writable')
    elif not os.access(path, os.X_OK):
        raise errors.ContentError(f'{path}: Not executable')


@functools.lru_cache(maxsize=None)
def projectdir(content_path, base=None):
    """
    Return path to existing directory in which jobs put their files and cache

    :param str content_path: Path to torrent content
    :param str base: Location of the project directory; defaults to
        :attr:`~.constants.DEFAULT_CACHE_DIRECTORY`

    :raise ContentError: if `content_path` exists and is not a directory or has
        insufficient permissions
    """
    if content_path:
        if not base:
            base = constants.DEFAULT_CACHE_DIRECTORY
        path = os.path.join(base, basename(content_path) + f'.{__project_name__}')
        mkdir(path)
    else:
        path = '.'
    _log.debug('Using project directory: %r', path)
    return path


def limit_directory_size(path, max_total_size, min_age=None, max_age=None):
    """
    Delete oldest files (by access time) until maximum size is not exceeded

    Empty files and directories are always deleted.

    :param path: Path to directory
    :param max_total_size: Maximum combined size of all files in `path` and its
        subdirectories
    :param min_age: Preserve files that are younger than this
    :type min_age: Unix timestamp
    :param max_age: Preserve files that are older than this
    :type max_age: Unix timestamp
    """
    @functools.lru_cache(maxsize=None)
    def cached_file_size(f):
        return file_size(f)

    def combined_size(filepaths):
        return sum(cached_file_size(f) for f in filepaths
                   if os.path.exists(f) and not os.path.islink(f))

    # This should return mtime if file system was mounted with noatime.
    def atime(filepath):
        try:
            return os.stat(filepath, follow_symlinks=False).st_atime
        except OSError:
            return 0

    def get_filepaths(dirpath):
        return file_list(dirpath, min_age=min_age, max_age=max_age, follow_dirlinks=False)

    # How much space do we have to free up?
    filepaths = get_filepaths(path)
    total_size = combined_size(filepaths)
    size_diff = total_size - max_total_size
    if size_diff > 0:
        # Collect old files until they free up enough space when removed
        oldest_files = sorted(filepaths, key=atime)
        files_to_remove = [oldest_files.pop(0)]
        while combined_size(files_to_remove) < size_diff:
            files_to_remove.append(oldest_files.pop(0))

        # Actually remove the files
        for file_to_remove in files_to_remove:
            # It's possible another process already unlinked this file while we
            # were still collecting old files.
            try:
                os.unlink(file_to_remove)
            except FileNotFoundError:
                pass


def prune_empty(path, files=False, directories=True):
    """
    Remove empty subdirectories recursively

    :param path: Path to directory
    :param bool files: Whether to prune empty files
    :param bool directories: Whether to prune empty directories

    Dead symbolic links are removed after pruning files and directories.

    If `path` is not a directory, do nothing.
    """
    if not os.path.isdir(path):
        return

    def raise_error(e, path):
        raise RuntimeError(f'{path}: Failed to prune: {e.strerror or e}')

    # Prune empty files
    if files:
        for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    if os.path.exists(filepath) and file_size(filepath) <= 0:
                        os.unlink(filepath)
                except OSError as e:
                    raise_error(e, filepath)

    # Prune empty directories
    if directories:
        for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
            for dirname in dirnames:
                subdirpath = os.path.join(dirpath, dirname)
                try:
                    if not os.path.islink(subdirpath) and not os.listdir(subdirpath):
                        os.rmdir(subdirpath)
                except OSError as e:
                    raise_error(e, subdirpath)

    # Prune dead links
    for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.islink(filepath):
                    if not os.path.exists(filepath):
                        os.unlink(filepath)
            except OSError as e:
                raise_error(e, filepath)

    try:
        if directories and not os.listdir(path):
            os.rmdir(path)
    except OSError as e:
        raise_error(e, path)


def mkdir(path):
    """
    Create directory and its parents

    Existing directories are ignored.

    If `path` is empty, no directory is created.

    :raise ContentError: if directory creation fails
    """
    if path:
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as e:
            raise errors.ContentError(f'{path}: {e.strerror or e}')
        else:
            assert_dir_usable(path)


def basename(path, parents=0):
    """
    Return last segment in `path`

    Unlike :func:`os.path.basename`, this removes any trailing directory
    separators first.

    >>> os.path.basename('a/b/c/')
    ''
    >>> upsies.utils.basename('a/b/c/')
    'c'

    :param parents: How many levels of parent directories to include in the
        returned path
    """
    basename = os.path.basename(str(path).rstrip(os.sep))
    parent_parts = list(pathlib.Path(str(path)).parent.parts)
    parents_to_include = []
    for _ in range(parents):
        if parent_parts:
            parents_to_include.insert(0, parent_parts.pop(-1))
    return str(pathlib.Path(*parents_to_include).joinpath(basename))


def dirname(path):
    """
    Remove last segment in `path`

    Unlike :func:`os.path.dirname`, this removes any trailing directory
    separators first.

    >>> os.path.dirname('a/b/c/')
    'a/b/c'
    >>> upsies.utils.dirname('a/b/c/')
    'a/b'
    """
    return os.path.dirname(str(path).rstrip(os.sep))


def file_and_parent(path):
    """Return `path`'s filename and parent directoy name if there is one"""
    if os.sep in path:
        return (
            basename(path),
            basename(dirname(path)),
        )
    else:
        return (path,)


def sanitize_filename(filename):
    """
    Replace illegal characters in `filename` with "_"

    Illegal characters include :attr:`os.sep`.
    """
    if os_family() == 'windows':
        illegal_chars = ('<', '>', ':', '"', '/', '\\', '|', '?', '*')
    else:
        illegal_chars = ('/',)
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    return filename


def sanitize_path(path):
    """
    Replace illegal characters in each `path` segment with "_"

    `path` is split at :attr:`os.sep` and the resulting items are passed to
    :func:`sanitize_filename` and joined.

    On Windows, the drive (e.g. "C:") is not sanitized to keep the ":".
    """
    # Get drive from Windows paths (e.g. "C:") because we don't want to sanitize
    # the ":", which is illegal otherwise
    drive, path = os.path.splitdrive(str(path))
    segments = str(path).split(os.sep)
    sanitized_segments = [sanitize_filename(segment) for segment in segments]
    return drive + os.sep.join(sanitized_segments)


def tildify_path(path):
    """Return `path` with $HOME replaced by ``~``"""
    home = os.path.expanduser('~')
    return re.sub(rf'^{re.escape(home)}', '~', path)


def file_extension(path, minlen=1, maxlen=None, only=()):
    """
    Return file extension

    Unlike :func:`os.path.splitext`, this function expects the extension to
    consist only of alphanumeric ASCII characters.

    :param str path: Path to file or directory
    :param str minlen: Minimum number of characters in file extension or `None`
        for no limit
    :param str maxlen: Maximum number of characters in file extension or `None`
        for no limit
    :param only: Only strip extension if it exists in this sequence
    :type only: sequence of :class:`str`

    :return: file extension
    :rtype: str
    """
    filename = os.path.basename(path)
    match = re.search(rf'\.([a-zA-Z0-9]{_make_minmax(minlen, maxlen)})$', filename)
    if match:
        ext = match.group(1).lower()
        if not only or ext in (str(e).lower() for e in only):
            return ext
    return ''

def strip_extension(path, minlen=1, maxlen=None, only=()):
    """
    Return `path` without file extension

    If `path` doesn't have a file extension, return it as is.

    A file extension consists only of alphanumeric ASCII characters.

    :param str path: Path to file or directory
    :param str minlen: Minimum number of characters in file extension or `None`
        for no limit
    :param str maxlen: Maximum number of characters in file extension or `None`
        for no limit
    :param only: Only strip extension if it exists in this sequence
    :type only: sequence of :class:`str`

    :return: file name without extension
    :rtype: str
    """
    path = str(path)
    match = re.search(rf'^(.*)\.([a-zA-Z0-9]{_make_minmax(minlen, maxlen)})$', path)
    if match:
        name = match.group(1)
        ext = match.group(2).lower()
        if not only or ext in (str(e).lower() for e in only):
            return name
    return path

def _make_minmax(minlen, maxlen):
    if minlen is not None and maxlen is not None:
        return '{' + f'{minlen},{maxlen}' + '}'
    elif minlen is not None:
        return '{' + f'{minlen},' + '}'
    elif maxlen is not None:
        return '{' + f',{maxlen}' + '}'
    else:
        return '*'


def file_size(path):
    """Return file size in bytes or `None`"""
    if not os.path.isdir(path):
        try:
            return os.path.getsize(path)
        except OSError:
            pass
    return None


def path_size(path):
    """
    Combined size of all files beneath `path`

    Returns the same value as :func:`file_size` if `path` is not a directory.

    Symbolic links are ignored.
    """
    filepaths = file_list(path, follow_dirlinks=False)
    return sum(
        file_size(f) or 0
        for f in filepaths
        if not os.path.islink(f)
    )


def file_list(path, extensions=(), min_age=None, max_age=None, follow_dirlinks=False):
    """
    List naturally sorted files in `path` and any subdirectories

    If `path` is not a directory, it is returned as a single item in a list
    unless `extensions` are given and they don't match.

    If `path` is any falsy value (e.g. ``""`` or `None`), return an empty
    sequence.

    Unreadable directories are excluded.

    :param str path: Path to a directory
    :param str extensions: Only include files with one of these extensions
        (matched case-insensitively)
    :param min_age: Exclude files that are younger than this
    :type min_age: int or float
    :param max_age: Exclude files that are older than this
    :type max_age: int or float
    :param follow_dirlinks: Whether to include the contents of symbolic links to
        directories or the links themselves

    :return: Tuple of file paths
    """
    extensions = tuple(str(e).casefold() for e in extensions)

    def ext_ok(filename):
        return not extensions or file_extension(filename).casefold() in extensions

    def age_ok(filepath, now=time.time()):
        try:
            statinfo = os.stat(filepath, follow_symlinks=False)
        except OSError:
            return False
        else:
            age = round(now - statinfo.st_atime)
            return (min_age or age) <= age <= (max_age or age)

    if not path:
        # Handle any false value, e.g. "" or `None`
        return ()
    elif not os.path.isdir(path):
        if ext_ok(path):
            return (str(path),)
        else:
            return ()

    files = []
    for root, dirnames, filenames in os.walk(path, topdown=True, followlinks=follow_dirlinks):
        for filename in sorted(filenames):
            filepath = os.path.join(root, filename)
            if ext_ok(filename) and age_ok(filepath):
                files.append(filepath)

        # Symbolic links to directories are in `dirnames`
        if not follow_dirlinks:
            # For symbolic links that point to a directory, os.walk() can only
            # include the contents (followlinks=True) or completely ignore the
            # link. Here we look for links to directories and a) include them in
            # the returned list and b), remove them from `dirnames` so os.walk()
            # doesn't recurse into them. It is important to pass topdown=True
            # for b) to work.
            for dirname in tuple(dirnames):
                # Contrary to what the docs say, this returns `True` for dead
                # and living symbolic links
                dirpath = os.path.join(root, dirname)
                if os.path.islink(dirpath):
                    del dirnames[dirnames.index(dirname)]
                    files.append(dirpath)

    return tuple(natsort.natsorted(files, key=str.casefold))


def find_name(name, path, validator=None):
    """
    Return first path (in human sort order) to `name` anywhere beneath
    `path` or `None`

    :param str name: Exact name of the file or directory
    :param str path: Base path to search for `name`

    :param validator: Callable that gets a path that ends with `name` and
        returns whether it is a match or not

        For example, you can use :func:`os.path.isfile` or :func:`os.path.isdir`
        to only find files or directories.
    """
    for root_, dirnames_, filenames_ in natsort.natsorted(
            os.walk(path, topdown=True, followlinks=False),
    ):
        names_ = natsort.natsorted(filenames_ + dirnames_)
        for name_ in names_:
            path_ = os.path.join(root_, name_)
            if name_ == name and (
                    not validator or validator(path_)
            ):
                return path_


# Stolen from torf-cli
# https://github.com/rndusr/torf-cli/blob/master/torfcli/_utils.py

_DOWN       = '\u2502'  # noqa: E221  # │
_DOWN_RIGHT = '\u251C'  # noqa: E221  # ├
_RIGHT      = '\u2500'  # noqa: E221  # ─
_CORNER     = '\u2514'  # noqa: E221  # └

def format_file_tree(tree, _parents_is_last=()):
    """
    Format nested file tree sequence as indented multi-line string

    :param tree: Nested 2-tuples: The first item is the file or directory name,
        the second item is the file size for files or a tuple for directories
    """
    lines = []
    max_i = len(tree) - 1
    for i,(name,node) in enumerate(tree):
        is_last = i >= max_i

        # Assemble indentation string (`_parents_is_last` being empty means
        # this is the top node)
        indent = ''
        if _parents_is_last:
            # `_parents_is_last` holds the `is_last` values of our ancestors.
            # This lets us construct the correct indentation string: For
            # each parent, if it has any siblings below it in the directory,
            # print a vertical bar ('|') that leads to the siblings.
            # Otherwise the indentation string for that parent is empty.
            # We ignore the first/top/root node because it isn't indented.
            for parent_is_last in _parents_is_last[1:]:
                if parent_is_last:
                    indent += '  '
                else:
                    indent += f'{_DOWN} '

            # If this is the last node, use '└' to stop the line, otherwise
            # branch off with '├'.
            if is_last:
                indent += f'{_CORNER}{_RIGHT}'
            else:
                indent += f'{_DOWN_RIGHT}{_RIGHT}'

        if isinstance(node, int):
            lines.append(f'{indent}{name} ({types.Bytes(node)})')
        else:
            def sum_node_size(nodelist):
                size = 0
                for node in nodelist:
                    if isinstance(node, tuple):
                        if len(node) >= 2 and isinstance(node[1], int):
                            size += node[1]
                        else:
                            size += sum_node_size(node)
                return size

            lines.append(f'{indent}{name} ({types.Bytes(sum_node_size(node))})')
            # Descend into child node
            sub_parents_is_last = _parents_is_last + (is_last,)
            lines.append(format_file_tree(node, _parents_is_last=sub_parents_is_last))

    return '\n'.join(lines)
