"""
Custom job that provide the result of a coroutine
"""

import collections

from . import JobBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class CustomJob(JobBase):
    """Wrapper around coroutine function or awaitable"""

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    def initialize(self, *, name, label, worker, catch=()):
        """
        Set internal state

        :param name: Name for internal use
        :param label: Name for user-facing use
        :param worker: Coroutine function that takes the job instance as a
            positional argument and returns this job's output

            If `worker` returns any iterable that isn't a string, each item is
            passed to :attr:`send`.

            If `worker` returns `None`, it is interpreted as "no output" and the
            job fails. An empty string is valid output and does not mean the job
            failed.
        :param catch: Sequence of :class:`Exception` classes to catch from
            `worker` and pass to :meth:`~.JobBase.error`

        This job finishes when `worker` returns.

        :class:`~.asyncio.CancelledError` from `worker` is ignored. Any other
        exceptions are passed to :meth:`~.JobBase.exception`.
        """
        self._name = str(name)
        self._label = str(label)
        self._worker = worker
        self._expected_exceptions = tuple(catch)
        self._task = None

    def execute(self):
        self._task = self.attach_task(
            self._catch_errors(self._worker(self)),
            callback=self._handle_worker_done,
        )

    async def _catch_errors(self, coro):
        try:
            return await coro
        except self._expected_exceptions as e:
            self.error(e)

    def _handle_worker_done(self, result):
        if result is not None:
            if (
                    not isinstance(result, str)
                    and isinstance(result, collections.abc.Iterable)
            ):
                for result in result:
                    self.send(result)
            else:
                self.send(result)
        self.finish()
        self.signal.emit('refresh_job_list')

    async def wait(self):
        """Wait for `worker`"""
        if self._task:
            await self._task
        await super().wait()

    def finish(self):
        """Cancel `worker` and finish this job"""
        if self._task:
            self._task.cancel()
        super().finish()
