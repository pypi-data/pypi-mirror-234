import functools

from . import JobWidgetBase

# This job is hidden so we only need a dummy widget.

class SetJobWidget(JobWidgetBase):
    def setup(self):
        pass

    @functools.cached_property
    def runtime_widget(self):
        return None
