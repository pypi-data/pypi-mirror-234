"""
Get information from the user
"""

import collections
import inspect
import re

from .. import utils
from . import JobBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class ChoiceJob(JobBase):
    """
    Ask the user to choose from a set of values

    This job adds the following signals to the :attr:`~.JobBase.signal`
    attribute:

        ``dialog_updated``
            Emitted when the :attr:`choices`, :attr:`focused` or
            :attr:`autodetected` properties are set or when :attr:`choices` is
            modified. Registered callbacks get the job instance as a positional
            argument.
    """

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def choices(self):
        """
        Sequence of choices the user can make

        A choice is a :class:`tuple` with 2 items. The first item is a
        human-readable :class:`str` and the second item is any object that is
        available as :attr:`choice` when the job is finished.

        Choices may also be passed as a flat iterable of :class:`str`, in which
        case both items in the tuple are identical.

        When setting this property, focus is preserved if the value of the
        focused choice exists in the new choices. Otherwise, the first choice is
        focused.
        """
        return getattr(self, '_choices', ())

    @choices.setter
    def choices(self, choices):
        # Build new list of choices
        valid_choices = []
        for choice in choices:
            if isinstance(choice, str):
                valid_choices.append((choice, choice))
            elif isinstance(choice, collections.abc.Sequence):
                if len(choice) != 2:
                    raise ValueError(f'Choice must be 2-tuple, not {choice!r}')
                else:
                    valid_choices.append((str(choice[0]), choice[1]))
            else:
                raise ValueError(f'Choice must be 2-tuple, not {choice!r}')

        if len(valid_choices) < 2:
            raise ValueError(f'There must be at least 2 choices: {choices!r}')

        # Remember current focus
        prev_focused = self.focused

        # Set new choices
        self._choices = utils.MonitoredList(
            valid_choices,
            callback=lambda _: self.signal.emit('dialog_updated', self),
        )

        # Try to restore focus if the previously focused item still exists,
        # default to first choice
        self._focused_index = 0
        if prev_focused:
            prev_label, prev_value = prev_focused
            for index, (label, value) in enumerate(valid_choices):
                if value == prev_value:
                    self._focused_index = index
                    break

        self.signal.emit('dialog_updated', self)

    def get_index(self, thing):
        """
        Return index in :attr:`choices`

        :param thing: Identifier of a choice in :attr:`choices`

            This can be:

            `None`
                Return `None`

            an index (:class:`int`)
               Return `thing`, but limited to the minimum/maximum valid index.

            one of the 2-tuples in :attr:`choices`
                Return the index of `thing` in :attr:`choices`.

            an item of one of the 2-tuples in :attr:`choices`
                Return the index of the first 2-tuple in :attr:`choices` that
                contains `thing`.

            a :func:`regular expression <re.compile>`
                Return the index of the first 2-tuple in :attr:`choices` that
                contains something that matches `thing`. Non-string values are
                converted to :class:`str` for matching against the regular
                expression.

        :raise ValueError: if `thing` is not found in :attr:`choices`
        """
        if thing is None:
            return None

        elif isinstance(thing, int):
            return max(0, min(thing, len(self.choices) - 1))

        elif thing in self.choices:
            return self.choices.index(thing)

        else:
            for i, (label, value) in enumerate(self.choices):
                # Focus by human-readable text or value
                if thing == label or thing == value:
                    return i

                # Focus by matching regex against human-readable text or value
                elif isinstance(thing, re.Pattern):
                    value_str = str(value)
                    if thing.search(label) or thing.search(value_str):
                        return i

        raise ValueError(f'No such choice: {thing!r}')

    def get_choice(self, thing):
        """
        Return item in :attr:`choices`

        :param thing: See :meth:`get_index`

        If `thing` is `None`, return the currently focused choice, which is
        indicated by :attr:`focused_index`.
        """
        choice_index = self.get_index(thing)
        if choice_index is None:
            choice_index = self.focused_index
        return self.choices[choice_index]

    @property
    def focused_index(self):
        """Index of currently focused choice in :attr:`choices`"""
        return getattr(self, '_focused_index', None)

    @property
    def focused(self):
        """
        Currently focused choice (2-tuple)

        This property can be set to anything that is a valid value for
        :meth:`get_index`.
        """
        focused_index = self.focused_index
        if focused_index is not None:
            return self.choices[focused_index]

    @focused.setter
    def focused(self, focused):
        # focused_index can't be set to None, so we default to first choice
        self._focused_index = self.get_index(focused)
        if self._focused_index is None:
            self._focused_index = 0
        self.signal.emit('dialog_updated', self)

    @property
    def autodetected_index(self):
        """Index of autodetected choice in :attr:`choices` or `None`"""
        return getattr(self, '_autodetected_index', None)

    @property
    def autodetected(self):
        """
        Autodetected choice (2-tuple) or `None`

        This property can be set to anything that is a valid value for
        :meth:`get_index`.
        """
        autodetected_index = self.autodetected_index
        if autodetected_index is not None:
            return self.choices[autodetected_index]

    @autodetected.setter
    def autodetected(self, autodetected):
        self._autodetected_index = self.get_index(autodetected)
        self.signal.emit('dialog_updated', self)

    @property
    def choice(self):
        """
        User-chosen value if job is finished, `None` otherwise

        While :attr:`~.base.JobBase.output` contains the user-readable string
        (first item of the chosen 2-tuple in :attr:`choices`), this is the
        object attached to it (second item).
        """
        choice = getattr(self, '_choice', None)
        if choice is not None:
            return choice

    def _set_choice(self, choice):
        # This method is called via `output` signal (see initialize()), which is
        # emitted by send(), so make_choice() doesn't need to call _set_choice().
        if hasattr(self, '_choice'):
            raise RuntimeError(f'{self.name}: Choice was already made: {self.choice}')
        else:
            label, value = self.get_choice(choice)
            self._choice = value

    def make_choice(self, thing):
        """
        Make a choice and :meth:`~.JobBase.finish` this job

        :param thing: See :meth:`get_choice`

        After this method is called, this job :attr:`~.JobBase.is_finished`,
        :attr:`~.JobBase.output` contains the human-readable label of the choice
        and :attr:`choice` is the machine-readable value of the choice.
        """
        label, value = self.get_choice(thing)
        self.send(label)
        self.finish()

    def set_label(self, identifier, new_label):
        """
        Assign new label to choice

        :param identifier: Choice (2-tuple of (<current label>, <value>) or the
            current label or value of a choice
        :param new_label: New label for the choice defined by `identifier`

        Do nothing if `identifier` doesn't match any choice.
        """
        new_choices = []
        for label, value in tuple(self.choices):
            if identifier == label or identifier == value or identifier == (label, value):
                new_choices.append((str(new_label), value))
            else:
                new_choices.append((label, value))
        if self.choices != new_choices:
            self.choices = new_choices

    def initialize(self, *, name, label, choices, focused=None, autodetected=None,
                   autodetect=None, autodetect_and_finish=None):
        """
        Set internal state

        :param name: Name for internal use
        :param label: Name for user-facing use
        :param choices: Iterable of choices the user can make
        :param focused: See :attr:`focused`
        :param autodetected: See :attr:`autodetected`
        :param autodetect: Callable that sets :attr:`autodetected` in
            :meth:`.JobBase.start`

            `autodetect` gets the job instance (``self``) as a positional
            argument.
        :param autodetect_and_finish: Same as `autodetect`, but :meth:`finish`
            this job if the returned value is not `None`

        :raise ValueError: if `choices` is shorter than 2 or `focused` is
            invalid
        """
        self._name = str(name)
        self._label = str(label)
        self._autodetect = autodetect
        self._autodetect_and_finish = autodetect_and_finish

        self.signal.add('dialog_updated')
        self.signal.register('output', self._set_choice)

        self.choices = choices
        self.autodetected = autodetected

        if focused is not None:
            self.focused = focused
        else:
            self.focused = autodetected

    def start(self):
        super().start()

        # Job is not started if it is disabled.
        # Job is finished right away if output was cached previously.
        if self.is_started and not self.is_finished:
            if self._autodetect:
                autodetected = self._autodetect(self)
                if autodetected is not None:
                    self.autodetected = self.focused = autodetected

            if self._autodetect_and_finish:
                autodetected = self._autodetect_and_finish(self)
                if autodetected is not None:
                    self.autodetected = self.focused = autodetected
                    self.make_choice(self.focused)


class TextFieldJob(JobBase):
    """
    Ask the user for text input

    This job adds the following signals to the :attr:`~.JobBase.signal`
    attribute:

        ``text``
            Emitted when :attr:`text` was changed without user input. Registered
            callbacks get the new text as a positional argument.

        ``is_loading``
            Emitted when :attr:`is_loading` was changed. Registered callbacks
            get the new :attr:`is_loading` value as a positional argument.

        ``read_only``
            Emitted when :attr:`read_only` was changed. Registered callbacks get
            the new :attr:`read_only` value as a positional argument.

        ``obscured``
            Emitted when :attr:`obscured` was changed. Registered callbacks get
            the new :attr:`obscured` value as a positional argument.
    """

    @property
    def name(self):
        return self._name

    @property
    def label(self):
        return self._label

    @property
    def text(self):
        """Current text"""
        return getattr(self, '_text', '')

    @text.setter
    def text(self, text):
        # Don't call validator here because it should be possible to set invalid
        # texts and let the user fix it manually. We only validate when we
        # commit to `text` (see send()).
        self._text = self._normalizer(str(text))
        self.signal.emit('text', self.text)

    @property
    def obscured(self):
        """
        Whether the text is unreadable, e.g. when entering passwords

        This is currently not fully implemented.
        """
        return getattr(self, '_obscured', False)

    @obscured.setter
    def obscured(self, obscured):
        self._obscured = bool(obscured)
        self.signal.emit('obscured', self.obscured)

    @property
    def read_only(self):
        """Whether the user can change the text"""
        return getattr(self, '_read_only', False)

    @read_only.setter
    def read_only(self, read_only):
        self._read_only = bool(read_only)
        self.signal.emit('read_only', self.read_only)

    @property
    def is_loading(self):
        """Whether :attr:`text` is currently being changed automatically"""
        return getattr(self, '_is_loading', False)

    @is_loading.setter
    def is_loading(self, is_loading):
        self._is_loading = bool(is_loading)
        self.signal.emit('is_loading', self.is_loading)

    def initialize(self, *, name, label,
                   text='', default=None, finish_on_success=False, nonfatal_exceptions=(),
                   validator=None, normalizer=None, obscured=False, read_only=False):
        """
        Set internal state

        :param name: Name for internal use
        :param label: Name for user-facing use
        :param text: Initial text or callable (synchronous or asynchronous)
            which will be called when the job is :meth:`executed
            <upsies.jobs.base.JobBase.execute>`. The return value is used as the
            initial text.
        :param default: Text to use if `text` is `None`, returns `None` or
            raises `nonfatal_exceptions`
        :param finish_on_success: Whether to call :meth:`finish` after setting
            :attr:`text` to `text`

            .. note:: :meth:`finish` is not called when :attr:`text` is set to
                      `default`.
        :param nonfatal_exceptions: Sequence of exception classes that may be
            raised by `text` without crashing

            Fatal exceptions are raised immediately while non-fatal exceptions
            are passed to :meth:`warn`, and the user can fix the situation
            manually.
        :param validator: Callable that gets text before job is finished. If
            `ValueError` is raised, it is displayed as a warning instead of
            finishing the job.
        :type validator: callable or None
        :param normalizer: Callable that gets text and returns the new text. It
            is called before `validator`. It should not raise any exceptions.
        :type normalizer: callable or None
        :param bool obscured: Whether :attr:`obscured` is set to `True`
            initially (currently fully implemented)
        :param bool read_only: Whether :attr:`read_only` is set to `True`
            initially
        """
        self._name = str(name)
        self._label = str(label)
        self._validator = validator or (lambda _: None)
        self._normalizer = normalizer or (lambda text: text)
        self.signal.add('text')
        self.signal.add('is_loading')
        self.signal.add('read_only')
        self.signal.add('obscured')
        self.obscured = obscured
        self.read_only = read_only

        if isinstance(text, str):
            # Set text attribute immediately
            self.text = text

        # Get text from callable when job is executed
        self._execute_arguments = (text, default, finish_on_success, nonfatal_exceptions)

    def execute(self):
        text, default, finish_on_success, nonfatal_exceptions = self._execute_arguments

        if inspect.isawaitable(text):
            self.attach_task(
                self.fetch_text(
                    coro=text,
                    default=default,
                    finish_on_success=finish_on_success,
                    nonfatal_exceptions=nonfatal_exceptions,
                )
            )

        elif inspect.iscoroutinefunction(text):
            self.attach_task(
                self.fetch_text(
                    coro=text(),
                    default=default,
                    finish_on_success=finish_on_success,
                    nonfatal_exceptions=nonfatal_exceptions,
                )
            )

        else:
            self.set_text(
                text=text,
                default=default,
                finish_on_success=finish_on_success,
                nonfatal_exceptions=nonfatal_exceptions,
            )

    def set_text(self, text, default=None, finish_on_success=False, nonfatal_exceptions=()):
        """
        Change :attr:`text` value

        :param text: New text value

            If this is callable, it must return the new :attr:`text` or `None`
            to use `default`

        :param default: Text to use if `text` is `None`, returns `None` or
            raises `nonfatal_exceptions`

        :param finish_on_success: Whether to call :meth:`finish` after setting
            :attr:`text` to `text`

            .. note:: :meth:`finish` is not called when :attr:`text` is set to
                      `default`.

        :param nonfatal_exceptions: Sequence of exception classes that may be
            raised by `text` without crashing

            Fatal exceptions are raised immediately while non-fatal exceptions
            are passed to :meth:`warn`, and the user can fix the situation
            manually.
        """
        self.is_loading = self.read_only = True
        try:
            if callable(text):
                new_text = text()
            elif text is not None:
                new_text = str(text)
            else:
                new_text = None
        except Exception as e:
            self._set_text(default)
            self._handle_exception(e, nonfatal=nonfatal_exceptions)
        else:
            self._set_text(new_text, default=default, finish=finish_on_success)
        finally:
            # Always re-enable text field after we're done messing with it
            self.is_loading = self.read_only = False

    async def fetch_text(self, coro, default=None, finish_on_success=False, nonfatal_exceptions=()):
        """
        Get :attr:`text` from coroutine

        :param coro: Coroutine that returns the new :attr:`text` or `None` to
            use `default`

        :param default: Text to use if `text` is `None`, returns `None` or
            raises `nonfatal_exceptions`

        :param finish_on_success: Whether to call :meth:`finish` after setting
            :attr:`text` to `coro` return value

            .. note:: :meth:`finish` is not called when :attr:`text` is set to
                      `default`.

        :param nonfatal_exceptions: Sequence of exception classes that may be
            raised by `coro` without crashing

            Fatal exceptions are raised immediately while non-fatal exceptions
            are passed to :meth:`warn`, and the user can fix the situation
            manually.
        """
        self.is_loading = self.read_only = True
        try:
            new_text = await coro
        except Exception as e:
            _log.debug('CAUGHT EXCEPTION: %r', e)
            self._set_text(default)
            self._handle_exception(e, nonfatal=nonfatal_exceptions)
        else:
            self._set_text(new_text, default=default, finish=finish_on_success)
        finally:
            # Always re-enable text field after we're done messing with it
            self.is_loading = self.read_only = False

    def _set_text(self, text, default=None, finish=False):
        # Fill in text
        if text is not None:
            self.text = text
            # Only finish if the intended text was set
            if finish:
                # We must call send() because it handles output caching, and it also
                # finishes the job.
                self.send(text)

        elif default is not None:
            self.text = default

    def _handle_exception(self, exception, nonfatal=()):
        # Display error and allow user to manually fix the situation
        if isinstance(exception, nonfatal):
            self.warn(exception)

        # An exception we didn't expect
        else:
            raise exception

    def send(self, output):
        """
        Validate `output` before actually sending it

        Pass `output` to `validator`. If :class:`ValueError` is raised, pass it
        to :meth:`warn` and do not finish. Otherwise, pass `output` to
        :meth:`~.base.JobBase.send` and :meth:`~.base.JobBase.finish` this job.
        """
        output = self._normalizer(output)
        try:
            self._validator(output)
        except ValueError as e:
            self.warn(e)
        else:
            super().send(output)
            super().finish()
