"""
Interactive text user interface and job manager
"""

import collections
import types

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window, to_container
from prompt_toolkit.output import create_output

from ... import utils
from . import jobwidgets, style

import logging  # isort:skip
_log = logging.getLogger(__name__)


class TUI:
    def __init__(self):
        # Map JobBase.name to SimpleNamespace with attributes:
        #   job       - JobBase instance
        #   widget    - JobWidgetBase instance
        #   container - Container instance
        self._jobs = collections.defaultdict(lambda: types.SimpleNamespace())
        self._app = self._make_app()
        self._app_terminated = False
        self._exception = None
        utils.get_aioloop().set_exception_handler(self._handle_exception)

    def _handle_exception(self, loop, context):
        exception = context.get('exception')
        if exception:
            _log.debug('Caught unhandled exception: %r', exception)
            _log.debug('Unhandled exception context: %r', context)
            if not self._exception:
                self._exception = exception
            self._exit()

    def _make_app(self):
        self._jobs_container = HSplit(
            # FIXME: Layout does not accept an empty list of children, so we add
            #        an empty Window that doesn't display anything.
            #        https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1257
            children=[Window()],
            style='class:default',
        )
        self._layout = Layout(self._jobs_container)

        kb = KeyBindings()

        @kb.add('escape')
        @kb.add('c-g')
        @kb.add('c-q')
        @kb.add('c-c')
        def _(event, self=self):
            if self._app.is_running:
                self._exit()

        app = Application(
            # Write TUI to stderr if stdout is redirected. This is useful for
            # allowing the user to make decisions in the TUI (e.g. selecting an
            # item from search results) while redirecting the final output
            # (e.g. an IMDb ID).
            output=create_output(always_prefer_tty=True),
            layout=self._layout,
            key_bindings=kb,
            style=style.style,
            full_screen=False,
            erase_when_done=False,
            mouse_support=False,
            on_invalidate=self._update_jobs_container,
        )
        return app

    def add_jobs(self, *jobs):
        """Add :class:`~.jobs.base.JobBase` instances"""
        for job in jobs:
            self._add_job(job)

        # Add job widgets to the main container widget (no side effects)
        self._update_jobs_container()

        # Register signal callbacks (no side effects)
        self._connect_jobs(*jobs)

        # Start all enabled jobs. This has side effects because it can trigger
        # more calls to _start_jobs() and _update_jobs_container() via
        # "finished" signal when a job is getting its output from cache.
        self._start_jobs(*jobs)

    def _add_job(self, job):
        if job.name in self._jobs:
            if job is not self._jobs[job.name].job:
                raise RuntimeError(f'Conflicting job name: {job.name}')
        else:
            self._jobs[job.name].job = job
            self._jobs[job.name].widget = jobwidgets.JobWidget(job, self._app)
            self._jobs[job.name].container = to_container(self._jobs[job.name].widget)

    # We accept one argument because the on_invalidate callback passes the
    # Application instance
    def _update_jobs_container(self, _=None):
        enabled_jobs = self._enabled_jobs

        # List interactive jobs first
        jobs_container = []
        for jobinfo in enabled_jobs:
            if jobinfo.widget.is_interactive and jobinfo.job.is_started:
                jobs_container.append(jobinfo.container)

                # Focus the first unfinished job
                if not jobinfo.job.is_finished:
                    self._update_focus(jobinfo)

                    # Don't display more than one unfinished interactive job
                    # unless any job has errors, in which case we are
                    # terminating the application and display all jobs.
                    if not any(jobinfo.job.errors for jobinfo in self._jobs.values()):
                        break

        # Add background jobs below interactive jobs so the interactive widgets
        # don't change position when non-interactive widgets change size.
        for jobinfo in enabled_jobs:
            if not jobinfo.widget.is_interactive and jobinfo.job.is_started:
                jobs_container.append(jobinfo.container)

        self._jobs_container.children[:] = jobs_container

    def _update_focus(self, to_jobinfo):
        try:
            self._layout.focus(to_jobinfo.container)
        except ValueError:
            pass
            # _log.debug('Unfocusable job: %r', to_jobinfo.job.name)

    def _connect_jobs(self, *jobs):
        for job in jobs:
            # Every time a job finishes, other jobs can become enabled due to
            # the dependencies on other jobs or other conditions. We also want
            # to display the next interactive job when an interactive job is
            # done.
            job.signal.register('finished', self._handle_job_finished)

            # A job can also signal explicitly that we should start previously
            # disabled jobs.
            job.signal.register('refresh_job_list', self._refresh_jobs)

    def _handle_job_finished(self, finished_job):
        assert finished_job.is_finished

        # Terminate application if any job finished with non-zero exit code
        if finished_job.exit_code != 0:
            if not self._app_terminated:
                _log.debug('Terminating application because of failed job: %r', finished_job.name)
            self._exit()

        else:
            enabled_jobs = [jobinfo.job for jobinfo in self._enabled_jobs]

            if all(job.is_finished for job in enabled_jobs):
                # Terminate application if all jobs finished
                _log.debug('All jobs finished')
                self._exit()
            else:
                # Start and/or display the next interactive jobs
                self._refresh_jobs()

    def _refresh_jobs(self):
        # Update jobs unless its pointless because _exit() was called
        if not self._app_terminated:
            self._start_jobs(*[jobinfo.job for jobinfo in self._enabled_jobs])
            self._update_jobs_container()
            self._app.invalidate()

    def _start_jobs(self, *jobs):
        for job in jobs:
            if not job.is_started and job.autostart:
                job.start()

    @property
    def _enabled_jobs(self):
        return tuple(jobinfo for jobinfo in self._jobs.values()
                     if jobinfo.job.is_enabled)

    def run(self, jobs):
        """
        Block while running `jobs`

        :param jobs: Iterable of :class:`~.jobs.base.JobBase` instances

        :raise: Any exception that occured while running jobs

        :return: :attr:`~.JobBase.exit_code` from the first failed job or 0 for
            success
        """
        self.add_jobs(*jobs)

        # Block until _exit() is called
        self._app.run(set_exception_handler=False)

        exception = self._get_exception()
        if exception:
            _log.debug('Application exception: %r', exception)
            raise exception
        else:
            # First non-zero exit_code is the application exit_code
            for jobinfo in self._enabled_jobs:
                _log.debug('Checking exit_code of %r: %r', jobinfo.job.name, jobinfo.job.exit_code)
                if jobinfo.job.exit_code != 0:
                    return jobinfo.job.exit_code
            return 0

    def _exit(self):
        if not self._app_terminated:
            if not self._app.is_running and not self._app.is_done:
                utils.get_aioloop().call_soon(self._exit)
            else:
                def handle_jobs_terminated(task):
                    try:
                        task.result()
                    except BaseException as e:
                        _log.debug('Handling exception from %r', task)
                        self._exception = e
                    finally:
                        self._app.exit()
                        self._update_jobs_container()

                self._app_terminated = True
                task = self._app.create_background_task(self._terminate_jobs())
                task.add_done_callback(handle_jobs_terminated)

    async def _terminate_jobs(self):
        jobs = [jobinfo.job for jobinfo in self._jobs.values()]

        self._finish_jobs(jobs)

        _log.debug('Waiting for finished jobs before exiting: %s', [j.name for j in jobs])
        for job in jobs:
            if job.is_started and not job.is_finished:
                _log.debug('Waiting for %r', job.name)
                await job.wait()
                _log.debug('Done waiting for %r', job.name)

    def _finish_jobs(self, jobs):
        for job in jobs:
            if not job.is_finished:
                _log.debug('Finishing %s', job.name)
                job.finish()

    def _get_exception(self):
        if self._exception:
            # Exception from _handle_exception()
            return self._exception
        else:
            # First exception from jobs
            for jobinfo in self._enabled_jobs:
                if jobinfo.job.raised:
                    _log.debug('Exception from %s: %r', jobinfo.job.name, jobinfo.job.raised)
                    return jobinfo.job.raised
