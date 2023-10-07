import functools

from .... import __project_name__, errors
from . import JobWidgetBase


class SubmitJobWidget(JobWidgetBase):
    def setup(self):
        self.job.signal.register('error', self._handle_error)

    def _handle_error(self, error):
        if isinstance(error, errors.AnnounceUrlNotSetError):
            cmd = f'{__project_name__} set trackers.{error.tracker.name}.announce_url <URL>'
            self.job.error(f'Set it with this command: {cmd}')

        elif isinstance(error, errors.FoundDupeError):
            self.job.error('You can override the dupe check with --ignore-dupes.')

    @functools.cached_property
    def runtime_widget(self):
        return None
