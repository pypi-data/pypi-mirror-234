import functools

from .. import widgets
from . import JobWidgetBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class ChoiceJobWidget(JobWidgetBase):
    def setup(self):
        self._radiolist = widgets.RadioList(
            choices=self.job.choices,
            focused=self.job.focused,
            autodetected=self.job.autodetected,
            on_accepted=self._handle_accepted,
        )
        self.job.signal.register('dialog_updated', self._handle_dialog_updated)

    def _handle_dialog_updated(self, job):
        self._radiolist.choices = job.choices
        self._radiolist.autodetected_index = job.autodetected_index
        self._radiolist.focused_index = job.focused_index
        self.invalidate()

    def _handle_accepted(self, choice):
        self.job.make_choice(choice)

    @functools.cached_property
    def runtime_widget(self):
        return self._radiolist


class TextFieldJobWidget(JobWidgetBase):
    def setup(self):
        self._input_field = widgets.InputField(
            text=self.job.text,
            read_only=self.job.read_only,
            style='class:dialog.text',
            on_accepted=self._on_accepted,
        )
        self.job.signal.register('is_loading', self._handle_is_loading)
        self.job.signal.register('read_only', self._handle_read_only)
        self.job.signal.register('text', self._handle_text)

    def _handle_is_loading(self, is_loading):
        self._input_field.is_loading = is_loading
        self.invalidate()

    def _handle_read_only(self, read_only):
        self._input_field.read_only = read_only
        self.invalidate()

    def _handle_text(self, text):
        self._input_field.text = text
        self.invalidate()

    def _on_accepted(self, buffer):
        self.job.send(buffer.text)

    @functools.cached_property
    def runtime_widget(self):
        return self._input_field
