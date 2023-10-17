"""
Abstract base class for all tracker-specific stuff
"""

import abc
import asyncio
import functools

from ... import errors, utils
from ._howto import Howto

import logging  # isort:skip
_log = logging.getLogger(__name__)


class TrackerBase(abc.ABC):
    """
    Base class for tracker-specific operations, e.g. uploading

    :param options: User configuration options for this tracker,
        e.g. authentication details, announce URL, etc
    :type options: :class:`dict`-like
    """

    @property
    @abc.abstractmethod
    def TrackerJobs(self):
        """Subclass of :class:`TrackerJobsBase`"""

    @property
    @abc.abstractmethod
    def TrackerConfig(self):
        """Subclass of :class:`TrackerConfigBase`"""

    def __init__(self, options=None):
        self._options = options or {}
        self._signal = utils.signal.Signal('warning', 'error', 'exception')

    @property
    @abc.abstractmethod
    def name(self):
        """Lower-case tracker name abbreviation for internal use"""

    @property
    @abc.abstractmethod
    def label(self):
        """User-facing tracker name abbreviation"""

    setup_howto_template = 'Nobody has written a setup howto yet.'
    """
    Step-by-step guide that explains how to make your first upload

    .. note:: This MUST be a class attribute and not a property.
    """

    @classmethod
    def generate_setup_howto(cls):
        # `howto` is now in the local namespace (see `locals()`) and
        # `evalute_fstring()` can access its properties to replace, for example,
        # "{howto.current}" in `setup_howto_template` with the current section
        # number.
        howto = Howto(tracker_cls=cls)  # noqa: F841 local variable 'howto' is assigned to but never used
        return utils.string.evaluate_fstring(cls.setup_howto_template)

    @property
    def options(self):
        """
        Configuration options provided by the user

        This is the :class:`dict`-like object from the initialization argument
        of the same name.
        """
        return self._options

    @functools.cached_property
    def _tasks(self):
        return []

    def attach_task(self, coro, callback=None):
        """
        Run awaitable `coro` in background task

        :param coro: Any awaitable

        :param callback: Callable that is called with the return value or
            exception from `coro`
        """
        task = utils.run_task(coro, callback=callback)
        self._tasks.append(task)
        return task

    async def await_tasks(self):
        """Wait for all awaitables passed to :meth:`attach_task`"""
        for task in self._tasks:
            await task

    async def login(self):
        """
        Start user session

        Set :attr:`is_logged_in` to `True` or `False`.

        :raise errors.RequestError: on failure
        """
        async with self._session_lock:
            if not self.is_logged_in:
                try:
                    await self._login()
                except errors.RequestError:
                    self._is_logged_in = False
                    raise
                else:
                    self._is_logged_in = True

    async def logout(self):
        """
        End user session

        Always set :attr:`is_logged_in` to `False`, even on failure.

        :raise errors.RequestError: on failure
        """
        async with self._session_lock:
            if self.is_logged_in:
                try:
                    await self._logout()
                finally:
                    self._is_logged_in = False

    @abc.abstractmethod
    async def _login(self):
        """
        Start user session

        :raise errors.RequestError: on any kind of failure
        """

    @abc.abstractmethod
    async def _logout(self):
        """
        End user session

        :raise errors.RequestError: on any kind of failure
        """

    @functools.cached_property
    def _session_lock(self):
        # Prevent multiple simultaneous login/logout attempts
        return asyncio.Lock()

    @property
    def is_logged_in(self):
        """Whether a user session is active"""
        return getattr(self, '_is_logged_in', False)

    @abc.abstractmethod
    async def get_announce_url(self):
        """Get announce URL from tracker website"""

    calculate_piece_size = None
    """
    :class:`staticmethod` that takes a torrent's content size and returns
    the corresponding piece size

    If this is `None`, the default implementation is used.
    """

    calculate_piece_size_min_max = None
    """
    :class:`staticmethod` that takes a torrent's content size and returns
    the corresponding allowed minimum and maximum piece sizes

    If this is `None`, the default implementation is used.
    """

    @abc.abstractmethod
    async def upload(self, tracker_jobs):
        """
        Upload torrent and other metadata from jobs

        :param TrackerJobsBase tracker_jobs: :attr:`TrackerJobs` instance
        """

    @property
    def signal(self):
        """
        :class:`~.signal.Signal` instance with the signals ``warning``, ``error``
        and ``exception``
        """
        return self._signal

    def warn(self, warning):
        """
        Emit ``warning`` signal (see :attr:`signal`)

        Emit a warning for any non-critical issue that the user can choose to
        ignore or fix.
        """
        self.signal.emit('warning', warning)

    def error(self, error):
        """
        Emit ``error`` signal (see :attr:`signal`)

        Emit an error for any critical but expected issue that can't be
        recovered from (e.g. I/O error).
        """
        self.signal.emit('error', error)

    def exception(self, exception):
        """
        Emit ``exception`` signal (see :attr:`signal`)

        Emit an exception for any critical and unexpected issue that should be
        reported as a bug.
        """
        self.signal.emit('exception', exception)
