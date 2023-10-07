from unittest.mock import Mock, call

import pytest

from upsies.uis.tui import widgets


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_ActivityIndicator_active_argument():
    ai = widgets.ActivityIndicator(active=1)
    assert ai.active is True
    ai = widgets.ActivityIndicator(active=0)
    assert ai.active is False

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_ActivityIndicator_active_property(mocker):
    mocker.patch('upsies.uis.tui.widgets.ActivityIndicator._iterate')
    ai = widgets.ActivityIndicator()
    assert ai.active is False
    assert ai._iterate.call_args_list == []
    ai.active = 1
    assert ai.active is True
    assert ai._iterate.call_args_list == [call()]
    ai.active = 0
    assert ai.active is False
    assert ai._iterate.call_args_list == [call()]
    ai.active = 'yes'
    assert ai.active is True
    assert ai._iterate.call_args_list == [call(), call()]

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_ActivityIndicator_active_property_calls_iterate(mocker):
    ai = widgets.ActivityIndicator(interval=0)
    mocker.patch.object(ai, '_iterate')
    assert ai._iterate.call_args_list == []
    ai.active = True
    assert ai._iterate.call_args_list == [call()]


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_ActivityIndicator_enable_disable(mocker):
    ai = widgets.ActivityIndicator(interval=0)
    mocker.patch.object(ai, '_iterate')
    assert ai.active is False
    ai.enable()
    assert ai.active is True
    ai.disable()
    assert ai.active is False


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_ActivityIndicator_format_property(mocker):
    mocker.patch('upsies.uis.tui.widgets.ActivityIndicator._iterate')
    ai = widgets.ActivityIndicator()
    assert ai.format == '{indicator}'
    ai.format = '[{indicator}]'
    assert ai.format == '[{indicator}]'


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_ActivityIndicator_text_property(mocker, event_loop):
    ai = widgets.ActivityIndicator(states=('a', 'b', 'c'), format=':{indicator}:', active=True)
    call_later_mock = mocker.patch.object(event_loop, 'call_later')
    assert ai.text == ':a:'
    ai._iterate()
    assert ai.text == ':b:'
    assert call_later_mock.call_args_list == [
        call(ai._interval, ai._iterate),
    ]

    ai._iterate()
    assert ai.text == ':c:'
    assert call_later_mock.call_args_list == [
        call(ai._interval, ai._iterate), call(ai._interval, ai._iterate),
    ]

    ai._iterate()
    assert ai.text == ':a:'
    assert call_later_mock.call_args_list == [
        call(ai._interval, ai._iterate), call(ai._interval, ai._iterate), call(ai._interval, ai._iterate),
    ]


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_ActivityIndicator_iterate_while_not_active(mocker, event_loop):
    cb = Mock()
    ai = widgets.ActivityIndicator(callback=cb, interval=123, states=('a', 'b', 'c'))
    call_later_mock = mocker.patch.object(event_loop, 'call_later')
    ai._iterate()
    assert cb.call_args_list == []
    assert call_later_mock.call_args_list == []
    ai._iterate()
    assert cb.call_args_list == []
    assert call_later_mock.call_args_list == []
    ai._iterate()
    assert cb.call_args_list == []
    assert call_later_mock.call_args_list == []


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_ActivityIndicator_iterate_while_active(mocker, event_loop):
    cb = Mock()
    ai = widgets.ActivityIndicator(callback=cb, interval=123, states=('a', 'b', 'c'),
                                   active=False, format='<{indicator}>')
    call_later_mock = mocker.patch.object(event_loop, 'call_later')
    assert cb.call_args_list == []
    assert call_later_mock.call_args_list == []
    ai.active = True
    assert cb.call_args_list == [
        call('<a>'),
    ]
    assert call_later_mock.call_args_list == [
        call(123.0, ai._iterate),
    ]
    ai._iterate()
    assert cb.call_args_list == [
        call('<a>'),
        call('<b>'),
    ]
    assert call_later_mock.call_args_list == [
        call(123.0, ai._iterate),
        call(123.0, ai._iterate),
    ]
    ai._iterate()
    assert cb.call_args_list == [
        call('<a>'),
        call('<b>'),
        call('<c>'),
    ]
    assert call_later_mock.call_args_list == [
        call(123.0, ai._iterate),
        call(123.0, ai._iterate),
        call(123.0, ai._iterate),
    ]
