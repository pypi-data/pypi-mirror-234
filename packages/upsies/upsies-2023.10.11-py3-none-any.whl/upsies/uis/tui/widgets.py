"""
Custom TUI widgets
"""

import collections
import itertools
import textwrap

from prompt_toolkit.application import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension

from ...utils import get_aioloop

import logging  # isort:skip
_log = logging.getLogger(__name__)


hspacer = Window(FormattedTextControl(' '), dont_extend_width=True, dont_extend_height=True)
vspacer = Window(FormattedTextControl(''), dont_extend_width=True, dont_extend_height=True)


class TextField:
    """Single line of non-editable text"""

    def __init__(self, text='', width=None, height=1, extend_width=True, style=''):
        self._text = text
        self._width = width
        self._height = height
        self._activity_indicator = ActivityIndicator(callback=self.set_text)
        self.container = Window(
            content=FormattedTextControl(lambda: self.text),
            width=width,
            height=height,
            dont_extend_height=True,
            dont_extend_width=not extend_width,
            wrap_lines=True,
            style=style,
        )

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self.set_text(text)

    def set_text(self, text):
        if isinstance(self._width, int) and self._width > 1:
            width = self._width
            if isinstance(self._height, int):
                height = self._height
            else:
                height = None

            if height == 1:
                # Remove newlines. Don't do word wrapping to avoid replacing
                # long words with "…" with lots of available free space.
                self._text = text.replace('\n', ' ')
            else:
                # prompt_toolkit has no support for word wrapping.
                paragraphs = text.split('\n')
                self._text = '\n\n'.join(textwrap.fill(
                    paragraph,
                    width=width,
                    max_lines=height,
                    placeholder='…',
                ) for paragraph in paragraphs)

        else:
            self._text = text

        get_app().invalidate()

    @property
    def is_loading(self):
        """Whether an activity indicator is displayed"""
        return self._activity_indicator.active

    @is_loading.setter
    def is_loading(self, is_loading):
        self._activity_indicator.active = is_loading

    def __pt_container__(self):
        return self.container


class InputField:
    """Single line of user-editable text"""

    def __init__(self, text='', width=None, extend_width=True, read_only=False,
                 on_accepted=None, on_changed=None, style=''):
        self._activity_indicator = ActivityIndicator(callback=self.set_text)
        self.read_only = read_only
        self.on_accepted = on_accepted
        self.buffer = Buffer(
            multiline=False,
            accept_handler=self._accept_handler,
            on_text_changed=on_changed,
            read_only=Condition(lambda: self.read_only),
        )
        self.container = Window(
            content=BufferControl(self.buffer),
            always_hide_cursor=Condition(lambda: self.read_only),
            width=width,
            dont_extend_height=True,
            dont_extend_width=not extend_width,
            style=style,
        )
        if text:
            self.set_text(text, ignore_callback=True)

    def _accept_handler(self, buffer):
        if self.on_accepted:
            self.on_accepted(buffer)
        # Do not clear input field on enter
        return True

    @property
    def text(self):
        return self.buffer.text

    @text.setter
    def text(self, text):
        self.set_text(text)

    def set_text(self, text, ignore_callback=False, preserve_cursor_position=False):
        if preserve_cursor_position:
            curpos = self.buffer.cursor_position

        if ignore_callback:
            handlers = self.buffer.on_text_changed._handlers
            self.buffer.on_text_changed._handlers = []

        self.buffer.set_document(Document(text), bypass_readonly=True)

        if ignore_callback:
            self.buffer.on_text_changed._handlers = handlers

        if preserve_cursor_position:
            self.buffer.cursor_position = curpos

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        self._read_only = bool(read_only)

    @property
    def is_loading(self):
        """Whether an activity indicator is displayed"""
        return self._activity_indicator.active

    @is_loading.setter
    def is_loading(self, is_loading):
        self._activity_indicator.active = is_loading

    def __pt_container__(self):
        return self.container


class RadioList:
    """
    List of choices the user can select from

    :param choices: Sequence of choices the user can make
    :param focused: Focused index or `None` to focus the first choice
    :param on_accepted: Callback that gets the user-picked choice

    Each choice item must be a :class:`str` or a sequence with one or more
    items. The first item is presented to the user. `on_accept` gets the
    complete choice item.
    """

    def __init__(self, choices=(), focused=None, autodetected=None, on_accepted=None):
        self.choices = choices
        self.on_accepted = on_accepted

        if focused:
            self.focused_index = choices.index(focused)
        else:
            self.focused_index = 0

        if autodetected:
            self.autodetected_index = choices.index(autodetected)
        else:
            self.autodetected_index = None

        kb = KeyBindings()

        @kb.add('up')
        @kb.add('c-p')
        @kb.add('k')
        @kb.add('s-tab')
        def _(event):
            self.focused_index = max(0, self.focused_index - 1)

        @kb.add('down')
        @kb.add('c-n')
        @kb.add('j')
        @kb.add('tab')
        def _(event):
            self.focused_index = min(len(self.choices) - 1, self.focused_index + 1)

        @kb.add('enter')
        @kb.add('c-j')
        @kb.add(' ')
        def _(event):
            if self.on_accepted is not None:
                try:
                    self.on_accepted(self.choices[self.focused_index])
                except IndexError:
                    raise RuntimeError(f'No choice at index {self.focused_index}: {self.choices}')

        self.control = FormattedTextControl(
            self._get_text_fragments,
            key_bindings=kb,
            focusable=True,
        )
        self.window = Window(
            content=self.control,
            style='class:dialog.choice',
            dont_extend_height=True,
            always_hide_cursor=True,
        )

    @property
    def focused_choice(self):
        """Currently focused item in :attr:`choices`"""
        return self.choices[self.focused_index]

    @focused_choice.setter
    def focused_choice(self, choice):
        if choice not in self.choices:
            raise ValueError(f'No such choice: {choice!r}')
        else:
            self.focused_index = self.choices.index(choice)

    def _get_text_fragments(self):
        fragments = []
        if not self.choices:
            return fragments

        def choice_as_string(choice):
            if isinstance(choice, str):
                return choice
            elif isinstance(choice, collections.abc.Sequence):
                return str(choice[0])
            else:
                raise RuntimeError(f'Invalid choice value: {choice!r}')

        width = max(len(choice_as_string(choice)) for choice in self.choices)
        for i, choice in enumerate(self.choices):
            choice_string = choice_as_string(choice)
            if i == self.focused_index:
                style = 'class:dialog.choice.focused'
                fragments.append(('[SetCursorPosition]', ''))
                fragments.append((style, ' *'))
            else:
                style = 'class:dialog.choice'
                fragments.append((style, '  '))
            fragments.append((style, ' '))
            fragments.extend(to_formatted_text(choice_string.ljust(width) + ' ', style=style))
            if i == self.autodetected_index:
                fragments.append(('class:dialog.choice', '(autodetected)'))
            fragments.append(('', '\n'))

        fragments.pop()  # Remove last newline

        return fragments

    def __pt_container__(self):
        return self.window


class HLabel:
    _groups = collections.defaultdict(lambda: [])

    def __init__(self, text, content, group=None, style=''):
        self.label = Window(
            content=FormattedTextControl(text),
            dont_extend_width=True,
            dont_extend_height=True,
            style=style,
            align=WindowAlign.RIGHT,
        )
        self.container = VSplit([
            # The HSplit makes the label non-greedy, i.e. the label itself takes
            # only one line and the space below is empty with default background
            # color.
            HSplit([self.label]),
            hspacer,
            content,
        ])

        self._group = group
        if group is not None:
            self._groups[group].append(self)
            texts = [label.label.content.text for label in self._groups[group]]
            max_width = max(len(text) for text in texts)
            for label in self._groups[group]:
                label.label.width = max_width + 1

    def __pt_container__(self):
        return self.container


class VLabel:
    def __init__(self, text, content, style=''):
        self.container = HSplit([
            Window(
                FormattedTextControl(text=text),
                dont_extend_width=False,
                dont_extend_height=True,
                style=style,
            ),
            content,
        ])

    def __pt_container__(self):
        return self.container


class ProgressBar:
    def __init__(self, text='', style=''):
        self.percent = 0
        self.container = VSplit(
            children=[
                Window(
                    style='class:info.progressbar.progress',
                    width=lambda: Dimension(weight=int(self.percent)),
                    height=1,
                ),
                Window(
                    style='class:info.progressbar',
                    width=lambda: Dimension(weight=int(100 - self.percent)),
                    height=1,
                ),
            ],
            style=style,
        )

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        self._percent = float(value)

    def __pt_container__(self):
        return self.container


class ActivityIndicator:
    """
    Activity indicator that cycles through a sequence of strings

    :param callable callback: Callable that receives a single string from
        `states` as a positional argument
    :param states: Sequence of strings that are cycled through and passed to
        `callback` individually
    :param float interval: Delay between calls to `callback`
    :param bool active: Whether `callback` is called right away
    :param str format: See :attr:`format`
    :param str style: prompt-toolkit style
    :param bool extend_width: Whether to maximize horizontally
    """

    def __init__(self, *, callback=None, states=('⠷', '⠯', '⠟', '⠻', '⠽', '⠾'),
                 interval=0.3, active=False, format='{indicator}', style='',
                 extend_width=False):
        self._iterator = itertools.cycle(states)
        self._interval = float(interval)
        self._callback = callback or None
        self._format = format
        self._text = self._format.format(indicator=states[0])
        self.active = active

        self.container = Window(
            content=FormattedTextControl(lambda: self.text),
            dont_extend_height=True,
            dont_extend_width=not extend_width,
            style=style,
        )

    @property
    def active(self):
        """Whether `callback` is being called continuously"""
        return getattr(self, '_active', False)

    @active.setter
    def active(self, active):
        if active:
            if not getattr(self, '_active', None):
                self._active = True
                self._iterate()
        else:
            self._active = False

    def enable(self):
        """Calling this method sets :attr:`active` to `True`"""
        self.active = True

    def disable(self):
        """Calling this method sets :attr:`active` to `False`"""
        self.active = False

    @property
    def format(self):
        """
        Format string

        ``{indicator}`` is replaced with the current state in `states`.
        """
        return self._format

    @format.setter
    def format(self, format):
        self._format = format

    @property
    def text(self):
        """Formatted :attr:`format` string"""
        return self._text

    def _iterate(self):
        if self.active:
            self._text = self._format.format(indicator=next(self._iterator))
            if self._callback:
                self._callback(self._text)

            get_aioloop().call_later(self._interval, self._iterate)
            get_app().invalidate()

    def __pt_container__(self):
        return self.container
