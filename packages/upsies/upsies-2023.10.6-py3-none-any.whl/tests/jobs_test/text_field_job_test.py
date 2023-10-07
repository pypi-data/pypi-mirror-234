import re
from unittest.mock import AsyncMock, Mock, call, patch

import pytest

from upsies import errors
from upsies.jobs.dialog import TextFieldJob


@pytest.fixture
def make_TextFieldJob(tmp_path):
    def make_TextFieldJob(**kwargs):
        return TextFieldJob(home_directory=tmp_path, cache_directory=tmp_path, **kwargs)
    return make_TextFieldJob

def test_name_property(make_TextFieldJob):
    job = make_TextFieldJob(name='foo', label='Foo')
    assert job.name == 'foo'


def test_label_property(make_TextFieldJob):
    job = make_TextFieldJob(name='foo', label='Foo')
    assert job.label == 'Foo'


@pytest.mark.parametrize('read_only', (True, False))
def test_text_property(read_only, make_TextFieldJob):
    job = make_TextFieldJob(name='foo', label='Foo', text='0',
                            validator=Mock(side_effect=ValueError('No likey')),
                            normalizer=Mock(side_effect=str.capitalize),
                            read_only=read_only)
    cb = Mock()
    job.signal.register('text', cb.text)
    assert job.text == '0'
    assert cb.text.call_args_list == []
    job.text = 123
    assert job.text == '123'
    assert cb.text.call_args_list == [call('123')]
    job.text = 'foo'
    assert job.text == 'Foo'
    assert cb.text.call_args_list == [call('123'), call('Foo')]


def test_obscured_property(make_TextFieldJob):
    job = make_TextFieldJob(name='foo', label='Foo', obscured=True)
    cb = Mock()
    job.signal.register('obscured', cb.obscured)
    assert job.obscured is True
    assert cb.obscured.call_args_list == []
    job.obscured = 0
    assert job.obscured is False
    assert cb.obscured.call_args_list == [call(False)]
    job.obscured = 'yes'
    assert job.obscured is True
    assert cb.obscured.call_args_list == [call(False), call(True)]


def test_read_only_property(make_TextFieldJob):
    job = make_TextFieldJob(name='foo', label='Foo', read_only=True)
    cb = Mock()
    job.signal.register('read_only', cb.read_only)
    assert job.read_only is True
    assert cb.read_only.call_args_list == []
    job.read_only = ''
    assert job.read_only is False
    assert cb.read_only.call_args_list == [call(False)]
    job.read_only = '1'
    assert job.read_only is True
    assert cb.read_only.call_args_list == [call(False), call(True)]


def test_is_loading_property(make_TextFieldJob):
    job = make_TextFieldJob(name='foo', label='Foo')
    cb = Mock()
    job.signal.register('is_loading', cb.is_loading)
    assert job.is_loading is False
    assert cb.is_loading.call_args_list == []
    job.is_loading = 1
    assert job.is_loading is True
    assert cb.is_loading.call_args_list == [call(True)]
    job.is_loading = ''
    assert job.is_loading is False
    assert cb.is_loading.call_args_list == [call(True), call(False)]


@pytest.mark.asyncio
async def test_execute_gets_awaitable(make_TextFieldJob, mocker):
    async def text():
        return 'my text'

    awaitable = text()
    default = 'my default'
    finish_on_success = 'my finish_on_success'
    nonfatal_exceptions = 'my nonfatal_exceptions'
    try:

        job = make_TextFieldJob(
            name='foo',
            label='Foo',
            text=awaitable,
            default=default,
            finish_on_success=finish_on_success,
            nonfatal_exceptions=nonfatal_exceptions,
        )

        mocks = Mock()
        mocks.attach_mock(mocker.patch.object(job, 'fetch_text', Mock(return_value='fetch_text() coro')), 'fetch_text')
        mocks.attach_mock(mocker.patch.object(job, 'attach_task'), 'attach_task')
        mocks.attach_mock(mocker.patch.object(job, 'set_text'), 'set_text')

        job.execute()

        assert mocks.mock_calls == [
            call.fetch_text(
                coro=awaitable,
                default='my default',
                finish_on_success='my finish_on_success',
                nonfatal_exceptions='my nonfatal_exceptions',
            ),
            call.attach_task(job.fetch_text.return_value),
        ]

    finally:
        # Prevent RuntimeWarning: coroutine 'test_execute_gets_awaitable.<locals>.text' was never awaited
        await awaitable

@pytest.mark.asyncio
async def test_execute_gets_coroutine_function(make_TextFieldJob, mocker):
    text = Mock()
    default = 'my default'
    finish_on_success = 'my finish_on_success'
    nonfatal_exceptions = 'my nonfatal_exceptions'

    job = make_TextFieldJob(
        name='foo',
        label='Foo',
        text=text,
        default=default,
        finish_on_success=finish_on_success,
        nonfatal_exceptions=nonfatal_exceptions,
    )

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'fetch_text', Mock(return_value='fetch_text() coro')), 'fetch_text')
    mocks.attach_mock(mocker.patch.object(job, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(job, 'set_text'), 'set_text')

    with patch('inspect.iscoroutinefunction', return_value=True):
        job.execute()

    assert mocks.mock_calls == [
        call.fetch_text(
            coro=text.return_value,
            default=default,
            finish_on_success=finish_on_success,
            nonfatal_exceptions=nonfatal_exceptions,
        ),
        call.attach_task(job.fetch_text.return_value),
    ]

@pytest.mark.asyncio
async def test_execute_gets_text(make_TextFieldJob, mocker):
    text = 'my text'

    job = make_TextFieldJob(
        name='foo',
        label='Foo',
        text=text,
    )

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'fetch_text', Mock(return_value='fetch_text() coro')), 'fetch_text')
    mocks.attach_mock(mocker.patch.object(job, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(job, 'set_text'), 'set_text')

    job.execute()

    assert mocks.mock_calls == [
        call.set_text(
            text=text,
            default=None,
            finish_on_success=False,
            nonfatal_exceptions=(),
        ),
    ]

@pytest.mark.asyncio
async def test_execute_gets_anything_else(make_TextFieldJob, mocker):
    text = Mock()
    default = 'my default'
    finish_on_success = 'my finish_on_success'
    nonfatal_exceptions = 'my nonfatal_exceptions'

    job = make_TextFieldJob(
        name='foo',
        label='Foo',
        text=text,
        default=default,
        finish_on_success=finish_on_success,
        nonfatal_exceptions=nonfatal_exceptions,
    )

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'fetch_text', Mock(return_value='fetch_text() coro')), 'fetch_text')
    mocks.attach_mock(mocker.patch.object(job, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(job, 'set_text'), 'set_text')

    job.execute()

    assert mocks.mock_calls == [
        call.set_text(
            text=text,
            default=default,
            finish_on_success=finish_on_success,
            nonfatal_exceptions=nonfatal_exceptions,
        ),
    ]


@pytest.mark.parametrize(
    argnames='text, default, finish_on_success, nonfatal_exceptions, exp_mock_calls',
    argvalues=(
        (
            'my text', 'my default', 'my finish_on_success', 'my nonfatal_exceptions',
            [
                call._set_text('my text', default='my default', finish='my finish_on_success'),
            ],
        ),
        (
            Mock(return_value='my text'), 'my default', 'my finish_on_success', 'my nonfatal_exceptions',
            [
                call._set_text('my text', default='my default', finish='my finish_on_success'),
            ],
        ),
        (
            Mock(side_effect=errors.RequestError('foo')), 'my default', 'my finish_on_success', 'my nonfatal_exceptions',
            [
                call._set_text('my default'),
                call._handle_exception(errors.RequestError('foo'), nonfatal='my nonfatal_exceptions'),
            ],
        ),
        (
            None, 'my default', 'my finish_on_success', 'my nonfatal_exceptions',
            [
                call._set_text(None, default='my default', finish='my finish_on_success'),
            ],
        ),
    ),
    ids=lambda v: repr(v),
)
def test_set_text(text, default, finish_on_success, nonfatal_exceptions,
                  exp_mock_calls,
                  make_TextFieldJob, mocker):
    job = make_TextFieldJob(name='foo', label='Foo')

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, 'send'), 'send')
    mocks.attach_mock(mocker.patch.object(job, '_set_text'), '_set_text')
    mocks.attach_mock(mocker.patch.object(job, '_handle_exception'), '_handle_exception')

    def check_states(*args, **kwargs):
        assert job.is_loading is True
        assert job.read_only is True

    mocks._set_text.side_effect = check_states
    mocks._handle_exception.side_effect = check_states

    job.set_text(
        text,
        default=default,
        finish_on_success=finish_on_success,
        nonfatal_exceptions=nonfatal_exceptions,
    )
    assert mocks.mock_calls == exp_mock_calls
    assert job.is_loading is False
    assert job.read_only is False


@pytest.mark.parametrize(
    argnames='coro, default, finish_on_success, nonfatal_exceptions, exp_mock_calls',
    argvalues=(
        (
            AsyncMock(return_value='my text'), 'my default', 'my finish_on_success', 'my nonfatal_exceptions',
            [
                call.coro(),
                call._set_text('my text', default='my default', finish='my finish_on_success'),
            ],
        ),
        (
            AsyncMock(side_effect=errors.RequestError('foo')), 'my default', 'my finish_on_success', 'my nonfatal_exceptions',
            [
                call.coro(),
                call._set_text('my default'),
                call._handle_exception(errors.RequestError('foo'), nonfatal='my nonfatal_exceptions'),
            ],
        ),

    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_fetch_text(coro, default, finish_on_success, nonfatal_exceptions,
                          exp_mock_calls,
                          make_TextFieldJob, mocker):
    job = make_TextFieldJob(name='foo', label='Foo')

    mocks = Mock()
    mocks.attach_mock(coro, 'coro')
    mocks.attach_mock(mocker.patch.object(job, 'send'), 'send')
    mocks.attach_mock(mocker.patch.object(job, '_set_text'), '_set_text')
    mocks.attach_mock(mocker.patch.object(job, '_handle_exception'), '_handle_exception')

    async def wrapped_coro():
        assert job.is_loading is True
        assert job.read_only is True
        return await coro()

    await job.fetch_text(
        wrapped_coro(),
        default=default,
        finish_on_success=finish_on_success,
        nonfatal_exceptions=nonfatal_exceptions,
    )
    assert mocks.mock_calls == exp_mock_calls
    assert job.is_loading is False
    assert job.read_only is False


@pytest.mark.parametrize(
    argnames='text, default, finish, exp_text, exp_send_calls',
    argvalues=(
        (None, None, False, 'original', []),
        (None, None, True, 'original', []),
        (None, 'mydefault', False, 'mydefault', []),
        (None, 'mydefault', True, 'mydefault', []),
        ('mytext', None, False, 'mytext', []),
        ('mytext', None, True, 'mytext', [call('mytext')]),
        ('mytext', 'mydefault', False, 'mytext', []),
        ('mytext', 'mydefault', True, 'mytext', [call('mytext')]),
    ),
    ids=lambda v: repr(v),
)
def test__set_text(text, default, finish, exp_text, exp_send_calls, make_TextFieldJob, mocker):
    job = make_TextFieldJob(name='foo', label='Foo')
    job.text = 'original'
    mocker.patch.object(job, 'send')

    job._set_text(text, default=default, finish=finish)
    assert job.text == exp_text

    assert job.send.call_args_list == exp_send_calls


@pytest.mark.parametrize(
    argnames='exception, nonfatal, exp_warn, exp_raised',
    argvalues=(
        (errors.RequestError('foo'), (), None, errors.RequestError('foo')),
        (errors.RequestError('foo'), (errors.RequestError,), errors.RequestError('foo'), None),
        (errors.ConfigError('foo'), (errors.RequestError,), None, errors.ConfigError('foo')),
    ),
    ids=lambda v: repr(v),
)
def test__handle_exception(exception, nonfatal, exp_warn, exp_raised, make_TextFieldJob, mocker):
    job = make_TextFieldJob(name='foo', label='Foo')
    mocker.patch.object(job, 'warn')

    if exp_raised:
        with pytest.raises(type(exp_raised), match=rf'^{re.escape(str(exp_raised))}$'):
            job._handle_exception(exception, nonfatal=nonfatal)
    else:
        job._handle_exception(exception, nonfatal=nonfatal)
        assert job.warn.call_args_list == [call(exp_warn)]


def test_send_valid_text(make_TextFieldJob):
    callables = Mock()
    callables.normalizer = Mock(side_effect=str.upper)
    job = make_TextFieldJob(
        name='foo',
        label='Foo',
        text='bar',
        validator=callables.validator,
        normalizer=callables.normalizer,
    )
    assert callables.mock_calls == [
        call.normalizer('bar'),
    ]
    assert job.text == 'BAR'
    assert job.output == ()

    callables.reset_mock()
    job.send('baz')

    assert callables.mock_calls == [
        call.normalizer('baz'),
        call.validator('BAZ'),
    ]
    assert job.warnings == ()
    assert job.is_finished
    assert job.exit_code == 0
    assert job.output == ('BAZ',)

def test_send_invalid_text(make_TextFieldJob):
    callables = Mock()
    callables.validator = Mock(side_effect=ValueError('Nope'))
    callables.normalizer = Mock(side_effect=str.upper)
    job = make_TextFieldJob(
        name='foo',
        label='Foo',
        text='bar',
        validator=callables.validator,
        normalizer=callables.normalizer,
    )
    assert callables.mock_calls == [
        call.normalizer('bar'),
    ]

    callables.reset_mock()
    job.send('baz')

    assert callables.mock_calls == [
        call.normalizer('baz'),
        call.validator('BAZ'),
    ]
    assert job.warnings == ('Nope',)
    assert not job.is_finished
    assert job.exit_code is None
    assert job.output == ()
