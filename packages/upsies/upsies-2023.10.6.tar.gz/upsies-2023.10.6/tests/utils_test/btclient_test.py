import re
import types
from unittest.mock import AsyncMock, Mock, call

import aiobtclientapi
import aiobtclientrpc
import pytest

from upsies import errors, utils
from upsies.utils import btclient


def test_client_names(mocker):
    client_names_mock = mocker.patch('aiobtclientapi.client_names')
    return_value = btclient.client_names()
    assert return_value is client_names_mock.return_value
    client_names_mock.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='client_name, exp_config',
    argvalues=(
        ('foo', None),
        (
            'deluge', {
                'url': aiobtclientapi.api_class('deluge').URL.default,
                'username': '',
                'password': '',
                'check_after_add': utils.types.Bool('no'),
            },
        ),
        (
            'qbittorrent', {
                'url': aiobtclientapi.api_class('qbittorrent').URL.default,
                'username': '',
                'password': '',
                'check_after_add': utils.types.Bool('no'),
                'category': '',
            },
        ),
        (
            'rtorrent', {
                'url': aiobtclientapi.api_class('rtorrent').URL.default,
                'username': '',
                'password': '',
                'check_after_add': utils.types.Bool('no'),
            },
        ),
        (
            'transmission', {
                'url': aiobtclientapi.api_class('transmission').URL.default,
                'username': '',
                'password': '',
                'check_after_add': utils.types.Bool('no'),
            },
        ),
    ),
    ids=lambda v: repr(v),
)
def test_client_defaults(client_name, exp_config, mocker):
    return_value = btclient.client_defaults(client_name)
    assert return_value == exp_config


@pytest.mark.parametrize(
    argnames='client_name, kwargs, exp_calls',
    argvalues=(
        (
            'foo',
            {
                'url': 'http://foo',
                'username': 'bar',
                'password': 'baz',
                'download_path': 'some/path',
                'check_after_add': 'maybe',
            },
            [
                call.api(
                    name='foo',
                    url='http://foo',
                    username='bar',
                    password='baz',
                ),
            ],
        ),
        (
            'foo',
            {
                'url': 'http://foo',
                'username': 'bar',
                'password': 'baz',
                'download_path': 'some/path',
                'check_after_add': 'maybe',
                'category': 'my_category',
            },
            [
                call.api(
                    name='foo',
                    url='http://foo',
                    username='bar',
                    password='baz',
                ),
            ],
        ),
    ),
    ids=lambda v: repr(v),
)
def test_BtClient_api(client_name, kwargs, exp_calls, mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch('aiobtclientapi.api', return_value='mock api'), 'api')
    client = btclient.BtClient(client_name, **kwargs)
    assert client._api == 'mock api'
    assert client._download_path == kwargs['download_path']
    assert client._check_after_add == kwargs['check_after_add']
    assert client._category == kwargs.get('category', '')
    assert mocks.mock_calls == exp_calls


def test_BtClient_name(mocker):
    api = Mock()
    api.configure_mock(name='myclient')
    mocker.patch('aiobtclientapi.api', return_value=api)

    client = btclient.BtClient(
        name='foo',
        url='http://foo',
        username='bar',
        password='baz',
        download_path='some/path',
        check_after_add='maybe',
    )

    assert client.name == 'myclient'

    # Property is immutable
    with pytest.raises(AttributeError):
        client.name = 'notmyclient'


def test_BtClient_label(mocker):
    api = Mock()
    api.configure_mock(label='MyClient')
    mocker.patch('aiobtclientapi.api', return_value=api)

    client = btclient.BtClient(
        name='irrelevant',
        url='http://foo',
        username='bar',
        password='baz',
        download_path='some/path',
        check_after_add='maybe',
    )

    assert client.label == 'MyClient'

    # Property is immutable
    with pytest.raises(AttributeError):
        client.label = 'NoyMyClient'


@pytest.mark.parametrize('category', ('', 'my_category'))
@pytest.mark.parametrize(
    argnames=(
        'torrent, download_path, check_after_add, '
        'response_errors, response_added, response_already_added, '
        'exp_result, exp_calls'
    ),
    argvalues=(
        pytest.param(
            'my.torrent', 'download/path', 'maybe verify',
            [Exception('whatever')], [], [],
            errors.TorrentAddError('whatever'),
            [
                call.add(
                    'my.torrent',
                    location='download/path',
                    verify='maybe verify',
                ),
            ],
            id='Adding torrent fails',
        ),
        pytest.param(
            'my.torrent', 'download/path', 'maybe verify',
            [], ['d34db33f'], [],
            'd34db33f',
            [
                call.add(
                    'my.torrent',
                    location='download/path',
                    verify='maybe verify',
                ),
            ],
            id='Adding torrent succeeds',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_BtClient_add_torrent(torrent, download_path, check_after_add, category,
                                    response_errors, response_added, response_already_added,
                                    exp_result, exp_calls,
                                    mocker):
    mocker.patch('aiobtclientapi.api', return_value=Mock(
        add=AsyncMock(
            return_value=Mock(
                errors=response_errors,
                added=response_added,
                already_added=response_already_added,
            ),
        ),
    ))

    client = btclient.BtClient(
        name='irrelevant',
        url='http://foo',
        username='bar',
        password='baz',
        download_path=download_path,
        check_after_add=check_after_add,
        category=category,
    )

    mocks = Mock()
    mocks.attach_mock(client._api.add, 'add')
    mocks.attach_mock(mocker.patch.object(client, '_set_category'), '_set_category')

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await client.add_torrent(torrent)
    else:
        return_value = await client.add_torrent(torrent)
        assert return_value == exp_result

        if category:
            exp_calls.append(call._set_category(exp_result, category))

    assert mocks.mock_calls == exp_calls


@pytest.mark.parametrize(
    argnames='infohash, category, api, exp_exception, exp_calls',
    argvalues=(
        pytest.param(
            'd34db33f',
            'my_category',
            types.SimpleNamespace(
                name='notqbittorrent',
                label='NotqBittorrent',
                call=AsyncMock(),
            ),
            RuntimeError('Categories are not supported for NotqBittorrent'),
            [],
            id='Client is not qBittorrent',
        ),
        pytest.param(
            'd34db33f',
            'my_category',
            types.SimpleNamespace(
                name='qbittorrent',
                label='qBittorrent',
                call=AsyncMock(side_effect=aiobtclientrpc.RPCError('Incorrect category name')),
            ),
            errors.TorrentAddError('Unknown category: my_category'),
            [],
            id='Setting unknown category',
        ),
        pytest.param(
            'd34db33f',
            'my_category',
            types.SimpleNamespace(
                name='qbittorrent',
                label='qBittorrent',
                call=AsyncMock(side_effect=aiobtclientrpc.RPCError('WAT')),
            ),
            aiobtclientrpc.RPCError('WAT'),
            [],
            id='Unexpected exception',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_BtClient__set_category(infohash, category, api, exp_exception, exp_calls, mocker):
    mocker.patch('aiobtclientapi.api', return_value=api)

    client = btclient.BtClient(
        name='irrelevant',
        url='http://foo',
        username='bar',
        password='baz',
        download_path='download/path',
        check_after_add='maybe',
        category=category,
    )

    mocks = Mock()
    mocks.attach_mock(client._api, 'api')

    if isinstance(exp_exception, Exception):
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            await client._set_category(infohash, category)
    else:
        return_value = await client._set_category(infohash, category)
        assert return_value is None

    assert mocks.mock_calls == exp_calls
