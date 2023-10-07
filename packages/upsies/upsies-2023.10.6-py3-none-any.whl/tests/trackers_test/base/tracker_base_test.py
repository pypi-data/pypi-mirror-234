import asyncio
import re
from unittest.mock import AsyncMock, Mock, PropertyMock, call

import pytest

from upsies import errors
from upsies.trackers import base


def make_MockTracker(**kwargs):
    class MockTracker(base.TrackerBase):
        name = 'asdf'
        label = 'AsdF'
        TrackerJobs = PropertyMock()
        TrackerConfig = PropertyMock()
        _login = AsyncMock()
        _logout = AsyncMock()
        get_announce_url = AsyncMock()
        upload = AsyncMock()

    return MockTracker(**kwargs)


def test_options():
    options = {'username': 'foo', 'password': 'bar'}
    tracker = make_MockTracker(options=options)
    assert tracker.options is options


def test_tasks():
    tracker = make_MockTracker()
    assert tracker._tasks == []
    assert tracker._tasks is tracker._tasks


@pytest.mark.parametrize('callback', (None, Mock()))
def test_attach_task(callback, mocker):
    tracker = make_MockTracker()
    run_task_mock = mocker.patch('upsies.utils.run_task')
    coro = Mock()
    if callback is None:
        return_value = tracker.attach_task(coro, callback=callback)
        assert run_task_mock.call_args_list == [call(coro, callback=callback)]
    else:
        return_value = tracker.attach_task(coro)
        assert run_task_mock.call_args_list == [call(coro, callback=None)]
    assert return_value is run_task_mock.return_value


@pytest.mark.asyncio
async def test_await_tasks(mocker):
    tracker = make_MockTracker()
    tasks = (
        asyncio.ensure_future(AsyncMock()()),
        asyncio.ensure_future(AsyncMock()()),
        asyncio.ensure_future(AsyncMock()()),
    )
    tracker._tasks.extend(tasks)

    for task in tasks:
        assert not task.done()

    await tracker.await_tasks()

    for task in tasks:
        assert task.done()


@pytest.mark.asyncio
async def test_login_when_already_logged_in(mocker):
    tracker = make_MockTracker()
    mocker.patch.object(tracker, '_login')
    mocker.patch.object(tracker, '_is_logged_in', True, create=True)

    assert tracker.is_logged_in

    # Login multiple times concurrently
    await asyncio.gather(
        tracker.login(),
        tracker.login(),
        tracker.login(),
    )

    assert tracker.is_logged_in
    assert tracker._login.call_args_list == []

@pytest.mark.asyncio
async def test_login_succeeds(mocker):
    tracker = make_MockTracker()
    mocker.patch.object(tracker, '_login')

    assert not tracker.is_logged_in

    # Login multiple times concurrently
    await asyncio.gather(
        tracker.login(),
        tracker.login(),
        tracker.login(),
    )

    assert tracker.is_logged_in
    assert tracker._login.call_args_list == [call()]

@pytest.mark.asyncio
async def test_login_fails(mocker):
    tracker = make_MockTracker()
    exception = errors.RequestError('nope')
    mocker.patch.object(tracker, '_login', side_effect=exception)

    assert not tracker.is_logged_in

    # Login multiple times concurrently
    with pytest.raises(type(exception), match=rf'^{re.escape(str(exception))}$'):
        await asyncio.gather(
            tracker.login(),
            tracker.login(),
            tracker.login(),
        )

    assert not tracker.is_logged_in
    assert tracker._login.call_args_list == [call(), call(), call()]

@pytest.mark.asyncio
async def test_logout_when_already_logged_out(mocker):
    tracker = make_MockTracker()
    mocker.patch.object(tracker, '_logout')
    mocker.patch.object(tracker, '_is_logged_in', False, create=True)

    assert not tracker.is_logged_in

    # Logout multiple times concurrently
    await asyncio.gather(
        tracker.logout(),
        tracker.logout(),
        tracker.logout(),
    )

    assert not tracker.is_logged_in
    assert tracker._logout.call_args_list == []

async def test_logout_succeeds(mocker):
    tracker = make_MockTracker()
    mocker.patch.object(tracker, '_logout')
    mocker.patch.object(tracker, '_is_logged_in', True, create=True)

    assert tracker.is_logged_in

    # Logout multiple times concurrently
    await asyncio.gather(
        tracker.logout(),
        tracker.logout(),
        tracker.logout(),
    )

    assert not tracker.is_logged_in
    assert tracker._logout.call_args_list == [call()]

@pytest.mark.asyncio
async def test_logout_fails(mocker):
    tracker = make_MockTracker()
    exception = errors.RequestError('nope')
    mocker.patch.object(tracker, '_logout', side_effect=exception)
    mocker.patch.object(tracker, '_is_logged_in', True, create=True)

    assert tracker.is_logged_in

    # Logout multiple times concurrently
    with pytest.raises(type(exception), match=rf'^{re.escape(str(exception))}$'):
        await asyncio.gather(
            tracker.logout(),
            tracker.logout(),
            tracker.logout(),
        )

    assert not tracker.is_logged_in
    assert tracker._logout.call_args_list == [call()]


def test_calculate_piece_size():
    tracker = make_MockTracker()
    assert type(tracker).calculate_piece_size is None


def test_calculate_piece_size_min_max():
    tracker = make_MockTracker()
    assert type(tracker).calculate_piece_size_min_max is None


def test_signals():
    tracker = make_MockTracker()
    cb = Mock()
    tracker.signal.register('warning', cb.warn)
    tracker.signal.register('error', cb.error)
    tracker.signal.register('exception', cb.exception)
    tracker.warn('foo')
    assert cb.mock_calls == [call.warn('foo')]
    tracker.error('bar')
    assert cb.mock_calls == [call.warn('foo'), call.error('bar')]
    tracker.exception('baz')
    assert cb.mock_calls == [call.warn('foo'), call.error('bar'), call.exception('baz')]


def test_generate_setup_howto_makes_expected_calls(mocker):
    Howto_mock = mocker.patch('upsies.trackers.base.tracker.Howto')
    evaluate_fstring_mock = mocker.patch('upsies.utils.string.evaluate_fstring')
    tracker = make_MockTracker()
    return_value = type(tracker).generate_setup_howto()
    assert return_value is evaluate_fstring_mock.return_value
    assert Howto_mock.call_args_list == [call(tracker_cls=type(tracker))]

def test_generate_setup_howto_populates_namespace_expectedly(mocker):
    tracker = make_MockTracker()
    type(tracker).setup_howto_template = '{isinstance(howto, Howto)}'
    assert type(tracker).generate_setup_howto() == 'True'
