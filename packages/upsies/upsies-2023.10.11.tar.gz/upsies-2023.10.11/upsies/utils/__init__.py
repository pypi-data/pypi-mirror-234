"""
Swiss Army knife
"""

import asyncio
import collections
import functools
import hashlib
import importlib
import inspect
import itertools
import os
import re
import types as _types


def get_aioloop():
    """Return :class:`asyncio.AbstractEventLoop` instance"""
    # https://docs.python.org/3.10/library/asyncio-eventloop.html
    try:
        return asyncio.get_running_loop()
    # "no running event loop"
    except RuntimeError:
        # We need a loop before the application has started.
        # This mimics get_event_loop(), but that is going to be an alias for
        # get_running_loop() in future Python releases.
        return asyncio.get_event_loop_policy().get_event_loop()


def os_family():
    """
    Return "windows" or "unix"
    """
    return 'windows' if os.name == 'nt' else 'unix'


# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/util/lazy_loader.py
class LazyModule(_types.ModuleType):
    """
    Lazily import module to decrease execution time

    :param str module: Name of the module
    :param mapping namespace: Usually the return value of `globals()`
    :param str name: Name of the module in `namespace`; defaults to `module`
    """

    def __init__(self, module, namespace, name=None):
        self._module = module
        self._namespace = namespace
        self._name = name or module
        super().__init__(module)

    def _load(self):
        # Import the target module and insert it into the parent's namespace
        module = importlib.import_module(self.__name__)
        self._namespace[self._name] = module

        # Update this object's dict so that if someone keeps a reference to the
        # LazyLoader, lookups are efficient (__getattr__ is only called on
        # lookups that fail).
        self.__dict__.update(module.__dict__)

        return module

    def __getattr__(self, item):
        module = self._load()
        return getattr(module, item)

    def __dir__(self):
        module = self._load()
        return dir(module)


def submodules(package):
    """
    Return list of submodules and subpackages in `package`

    :param str package: Fully qualified name of parent package,
        e.g. "upsies.utils.imghosts"
    """
    # Get absolute path to parent directory of top-level package
    own_path = os.path.dirname(__file__)
    rel_path = __package__.replace('.', os.sep)
    assert own_path.endswith(rel_path), f'{own_path!r}.endswith({rel_path!r})'
    project_path = own_path[:-len(rel_path)]

    # Add relative path within project to given package
    package_path = os.path.join(project_path, package.replace('.', os.sep))

    # Find and import public submodules
    submods = []
    for name in os.listdir(package_path):
        if not name.startswith('_'):
            if name.endswith('.py'):
                name = name[:-3]
            if '.' not in name:
                submods.append(
                    importlib.import_module(name=f'.{name}', package=package)
                )
    return submods


def subclasses(basecls, modules):
    """
    Find subclasses in modules

    :param type basecls: Class that all returned classes are a subclass of
    :param modules: Modules to search
    :type modules: list of module objects
    """
    subclses = set()
    for mod in modules:
        for name, member in inspect.getmembers(mod):
            if (member is not basecls and
                isinstance(member, type) and
                issubclass(member, basecls)):
                subclses.add(member)
    return subclses


def closest_number(n, ns, max=None, default=0):
    """
    Return the number from `ns` that is closest to `n`

    :param n: Given number
    :param ns: Sequence of allowed numbers
    :param max: Remove any item from `ns` that is larger than `max`
    :param default: Return value in case `ns` is empty
    """
    if max is not None:
        ns_ = tuple(n_ for n_ in ns if n_ <= max)
        if not ns_:
            raise ValueError(f'No number equal to or below {max}: {ns}')
    else:
        ns_ = ns
    return min(ns_, key=lambda x: abs(x - n), default=default)


class CaseInsensitiveString(str):
    """String that ignores case when compared or sorted"""

    def __hash__(self):
        return hash(self.casefold())

    def __eq__(self, other):
        if not isinstance(other, str):
            return NotImplemented
        else:
            return self.casefold() == other.casefold()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.casefold() < other.casefold()

    def __le__(self, other):
        return self.casefold() <= other.casefold()

    def __gt__(self, other):
        return self.casefold() > other.casefold()

    def __ge__(self, other):
        return self.casefold() >= other.casefold()


class MonitoredList(collections.abc.MutableSequence):
    """
    :class:`list` that calls `callback` after every change

    :param callback: Callable that gets the instance as a positional argument
    """

    def __init__(self, *args, callback, **kwargs):
        self._list = list(*args, **kwargs)
        self._callback = callback

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        self._list[index] = value
        self._callback(self)

    def __delitem__(self, index):
        del self._list[index]
        self._callback(self)

    def insert(self, index, value):
        self._list.insert(index, value)
        self._callback(self)

    def __len__(self):
        return len(self._list)

    def __eq__(self, other):
        return self._list == other

    def __repr__(self):
        return f'{type(self).__name__}({repr(self._list)}, callback={self._callback!r})'


class ImmutableMapping(collections.abc.Mapping):
    """
    :class:`dict`-like that can't be changed after initialization

    All values are also made immutable recursively. Keys should already be
    immutable because the must be hashable.
    """

    def __init__(self, *args, **kwargs):
        self._dct = {
            k: self._make_immutable(v)
            for k, v in dict(*args, **kwargs).items()
        }

    def _make_immutable(self, obj):
        if isinstance(obj, str):
            # Catch strings early because they are also sequences
            return obj

        elif isinstance(obj, collections.abc.Sequence):
            return tuple(self._make_immutable(item) for item in obj)

        elif isinstance(obj, collections.abc.Mapping):
            return ImmutableMapping(obj)

        else:
            return obj

    def __getitem__(self, key):
        return self._dct[key]

    def __iter__(self):
        return iter(self._dct)

    def __len__(self):
        return len(self._dct)

    def __hash__(self):
        return hash(tuple(frozenset(self._dct.items())))

    def __eq__(self, other):
        if isinstance(other, collections.abc.Mapping):
            return hash(self) == hash(tuple(frozenset(self._dct.items())))
        else:
            return NotImplemented

    def __repr__(self):
        return f'{type(self).__name__}({repr(self._dct)})'


def is_sequence(obj):
    """Return whether `obj` is a sequence and not a string"""
    return (
        isinstance(obj, collections.abc.Sequence)
        and not isinstance(obj, str)
    )


def merge_dicts(a, b, path=()):
    """
    Merge nested dictionaries `a` and `b` into new dictionary with same
    structure
    """
    keys = itertools.chain(a, b)
    merged = {}
    for key in keys:
        if (isinstance(a.get(key), collections.abc.Mapping) and
            isinstance(b.get(key), collections.abc.Mapping)):
            merged[key] = merge_dicts(a[key], b[key], path + (key,))
        elif key in b:
            # Value from b takes precedence
            merged[key] = b[key]
        elif key in a:
            # Value from a is default
            merged[key] = a[key]
    return merged


def deduplicate(seq, key=None):
    """
    Return sequence `seq` with all duplicate items removed while maintaining
    the original order

    :param key: Callable that gets each item and returns a hashable identifier
        for that item
    """
    if key is None:
        def key(k):
            return k

    seen_keys = set()
    deduped = []
    for item in seq:
        k = key(item)
        if k not in seen_keys:
            seen_keys.add(k)
            deduped.append(item)
    return deduped


def as_groups(sequence, group_sizes, default=None):
    """
    Iterate over items from `sequence` in equally sized groups

    :params sequence: List of items to group
    :params group_sizes: Sequence of acceptable items in a group

        Determine the group size with the lowest number of `default` items in
        the last group. That group size is then used for all groups.
    :param default: Value to pad last group with if
        ``len(sequence) % group_size != 0``

    Example:

    >>> sequence = range(1, 10)
    >>> for group in as_groups(sequence, [4, 5], default='_'):
    ...     print(group)
    (1, 2, 3, 4, 5)
    (6, 7, 8, 9, '_')
    >>> for group in as_groups(sequence, [3, 4], default='_'):
    ...     print(group)
    (1, 2, 3)
    (4, 5, 6)
    (7, 8, 9)
    """
    # Calculate group size that results in the least number of `default` values
    # in the final group
    gs_map = collections.defaultdict(lambda: [])
    for gs in group_sizes:
        # How many items from `sequence` are in the last group
        overhang = len(sequence) % gs
        # How many `default` values are in the last group
        default_count = 0 if overhang == 0 else gs - overhang
        gs_map[default_count].append(gs)

    lowest_default_count = sorted(gs_map)[0]
    group_size = max(gs_map[lowest_default_count])
    args = [iter(sequence)] * group_size
    yield from itertools.zip_longest(*args, fillvalue=default)


def is_regex_pattern(object):
    """
    Whether `object` is a regular expression object

    A regular expression object is usually obtained from :func:`re.compile`.
    """
    return isinstance(object, re.Pattern)


_unsupported_semantic_hash_types = (
    collections.abc.Iterator,
    collections.abc.Iterable,
    collections.abc.Generator,
)

def semantic_hash(obj):
    """
    Return SHA256 hash for `obj` that stays the same between Python interpreter
    sessions

    https://github.com/schollii/sandals/blob/master/json_sem_hash.py
    """
    def as_str(obj):
        if isinstance(obj, str):
            return obj

        elif isinstance(obj, collections.abc.Mapping):
            stringified = ((as_str(k), as_str(v)) for k, v in obj.items())
            return as_str(sorted(stringified))

        elif isinstance(obj, (collections.abc.Sequence, collections.abc.Set)):
            stringified = (as_str(item) for item in obj)
            return ''.join(sorted(stringified))

        elif isinstance(obj, _unsupported_semantic_hash_types):
            raise RuntimeError(f'Unsupported type: {type(obj)}: {obj!r}')

        else:
            return str(obj)

    return hashlib.sha256(bytes(as_str(obj), 'utf-8')).hexdigest()


def run_task(coro, callback):
    """
    Run awaitable in background task and return immediately

    This method should be used to call coroutine functions and other awaitables
    in a synchronous context.

    The returned task must be collected (e.g. in a :class:`list`) and awaited or
    cancelled eventually.

    If the returned task is cancelled, the :class:`asyncio.CancelledError` is
    silently ignored and `callback` is called with `None`.

    :param coro: Any awaitable object
    :param callback: Callable that is called with exception or return value of
        `coro`

    :return: :class:`asyncio.Task` instance
    """

    @functools.wraps(coro)
    async def wrap_coro(coro):
        try:
            return await asyncio.ensure_future(coro)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            raise e

    def handle_task_done(task):
        try:
            result = task.result()
        except asyncio.CancelledError:
            # I don't know how to reliably reproduce or unittest this, but
            # CancelledError was raised here.
            pass
        except Exception as e:
            if callback:
                callback(e)
            else:
                raise
        else:
            if callback:
                callback(result)

    task = asyncio.ensure_future(wrap_coro(coro))
    task.add_done_callback(handle_task_done)
    return task


async def run_async(function, *args, **kwargs):
    """
    Run synchronous `function` asynchronously in a thread

    See :meth:`asyncio.BaseEventLoop.run_in_executor`.
    """
    loop = get_aioloop()
    wrapped = functools.partial(function, *args, **kwargs)
    return await loop.run_in_executor(None, wrapped)


# We must import these here to prevent circular imports
from . import (  # noqa: E402 isort:skip
    argtypes,
    browser,
    btclient,
    configfiles,
    country,
    daemon,
    fs,
    html,
    http,
    image,
    imghosts,
    predbs,
    release,
    signal,
    string,
    subproc,
    subtitle,
    timestamp,
    torrent,
    types,
    update,
    video,
    webdbs,
)
