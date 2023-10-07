import functools

from . import JobWidgetBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PosterJobWidget(JobWidgetBase):
    def setup(self):
        self.job.signal.register('finding_poster', self.handle_finding_poster)
        self.job.signal.register('downloading_poster', self.handle_downloading_poster)
        self.job.signal.register('resizing_poster', self.handle_resizing_poster)
        self.job.signal.register('uploading_poster', self.handle_uploading_poster)
        self.job.signal.register('uploaded_poster', self.handle_uploaded_poster)

    def handle_finding_poster(self, id):
        self.job.info = f'Searching {id}'

    def handle_downloading_poster(self, url):
        self.job.info = f'Downloading {url}'

    def handle_resizing_poster(self, filepath):
        self.job.info = f'Resizing {filepath}'

    def handle_uploading_poster(self, filepath):
        self.job.info = f'Uploading {filepath}'

    def handle_uploaded_poster(self, url):
        self.invalidate()

    @functools.cached_property
    def runtime_widget(self):
        return None
