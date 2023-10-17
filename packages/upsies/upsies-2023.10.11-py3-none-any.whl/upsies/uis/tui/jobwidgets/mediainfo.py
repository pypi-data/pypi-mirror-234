import functools

from . import JobWidgetBase


class MediainfoJobWidget(JobWidgetBase):
    def setup(self):
        pass

    @functools.cached_property
    def runtime_widget(self):
        return None
