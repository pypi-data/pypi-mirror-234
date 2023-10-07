import re
from unittest.mock import Mock, PropertyMock, call

import pytest

from upsies import errors
from upsies.trackers import ptp


@pytest.fixture
def make_tracker():
    def make_tracker(**kwargs):
        options = {
            'username': 'bunny',
            'password': 'hunter2',
            'base_url': 'http://ptp.local',
        }
        options.update(kwargs)
        return ptp.PtpTracker(options=options)

    return make_tracker

@pytest.fixture
def tracker(make_tracker):
    return make_tracker()


class MockResponse(str):
    def __new__(cls, html='<html>nothing</html>', headers={}, json={}):
        self = super().__new__(cls, html)
        self.headers = headers
        self.json = Mock(return_value=json)
        return self


def test_name_attribute():
    assert ptp.PtpTracker.name == 'ptp'


def test_label_attribute():
    assert ptp.PtpTracker.label == 'PTP'


def test_PtpTracker_TrackerConfig_attribute():
    assert ptp.PtpTracker.TrackerConfig is ptp.PtpTrackerConfig


def test_PtpTracker_TrackerJobs_attribute():
    assert ptp.PtpTracker.TrackerJobs is ptp.PtpTrackerJobs


def test_PtpTracker_base_url_property(tracker, mocker):
    mocker.patch.object(type(tracker), '_base_url', PropertyMock(return_value='http://foo.local'))
    assert tracker._base_url == 'http://foo.local'


def test_PtpTracker_ajax_url_property(tracker, mocker):
    mocker.patch.object(type(tracker), '_base_url', PropertyMock(return_value='http://foo.local'))
    assert tracker._ajax_url == 'http://foo.local/ajax.php'


def test_PtpTracker_logout_url_property(tracker, mocker):
    mocker.patch.object(type(tracker), '_base_url', PropertyMock(return_value='http://foo.local'))
    assert tracker._logout_url == 'http://foo.local/logout.php'


def test_PtpTracker_upload_url_property(tracker, mocker):
    mocker.patch.object(type(tracker), '_base_url', PropertyMock(return_value='http://foo.local'))
    assert tracker._upload_url == 'http://foo.local/upload.php'


def test_PtpTracker_torrents_url_property(tracker, mocker):
    mocker.patch.object(type(tracker), '_base_url', PropertyMock(return_value='http://foo.local'))
    assert tracker._torrents_url == 'http://foo.local/torrents.php'


@pytest.mark.parametrize(
    argnames='announce_url, exp_result',
    argvalues=(
        ('', errors.AnnounceUrlNotSetError(tracker='mock tracker instance')),
        ('http://mock.announce.url', 'http://mock.announce.url'),
    ),
)
def test_PtpTracker_announce_url_property(announce_url, exp_result, tracker, mocker):
    mocker.patch.dict(tracker.options, {'announce_url': announce_url})

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker._announce_url
    else:
        assert tracker._announce_url == exp_result


@pytest.mark.parametrize(
    argnames='announce_url, exp_result',
    argvalues=(
        ('http://mock.url:1234/d34db33f/announce', 'd34db33f'),
        ('http://mock.url:1234/announce', RuntimeError('Failed to find passkey in announce URL: http://mock.url:1234/announce')),
    ),
)
def test_PtpTracker_passkey_property(announce_url, exp_result, tracker, mocker):
    mocker.patch.object(type(tracker), '_announce_url', PropertyMock(return_value=announce_url))

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker._passkey
    else:
        assert tracker._passkey == exp_result


@pytest.fixture
def tracker_for_request(tracker, mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.get'), 'get')
    mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.post'), 'post')
    mocks.attach_mock(mocker.patch.object(tracker, '_maybe_raise_error'), '_maybe_raise_error')
    return tracker, mocks

@pytest.mark.parametrize('method', ('GET', 'get', 'POST', 'post'))
@pytest.mark.asyncio
async def test_PtpTracker_request_catches_RequestError_from_method(method, tracker_for_request):
    tracker, mocks = tracker_for_request
    get_exception = errors.RequestError('Your GET request sucks')
    post_exception = errors.RequestError('Your POST request sucks')
    mocks.get.side_effect = get_exception
    mocks.post.side_effect = post_exception

    args = ('foo', 'bar')
    kwargs = {'baz': 123}

    await tracker._request(method, *args, **kwargs)

    assert mocks.mock_calls == [
        getattr(call, method.lower())(
            *args,
            user_agent=True,
            follow_redirects=False,
            **kwargs,
        ),
        call._maybe_raise_error(
            get_exception if method.lower() == 'get' else post_exception
        ),
    ]

@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.parametrize(
    argnames='error_prefix, exception, exp_result',
    argvalues=(
        (None, errors.RequestError('Raised error'), errors.RequestError('Raised error')),
        ('', errors.RequestError('Raised error'), errors.RequestError('Raised error')),
        ('YO', errors.RequestError('Raised error'), errors.RequestError('YO: Raised error')),
        ('YO', None, '<method return value>'),
    ),
)
@pytest.mark.asyncio
async def test_PtpTracker_request_catches_RequestError_from_maybe_raise_error(method, error_prefix, exception,
                                                                              exp_result,
                                                                              tracker_for_request):
    tracker, mocks = tracker_for_request
    mocks._maybe_raise_error.side_effect = exception

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await tracker._request(method, error_prefix=error_prefix)
    else:
        return_value = await tracker._request(method, error_prefix=error_prefix)
        assert return_value is getattr(mocks, method.lower()).return_value

    assert mocks.mock_calls == [
        getattr(call, method.lower())(
            user_agent=True,
            follow_redirects=False,
        ),
        call._maybe_raise_error(getattr(mocks, method.lower()).return_value),
    ]


@pytest.mark.parametrize(
    argnames='response_or_request_error, exp_exception',
    argvalues=(
        ('normal response', None),
        (errors.RequestError('Raised error'), errors.RequestError('Raised error')),
    ),
    ids=lambda v: repr(v),
)
def test_PtpTracker_maybe_raise_error(response_or_request_error, exp_exception, tracker, mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker, '_maybe_raise_error_from_json'), '_maybe_raise_error_from_json')
    mocks.attach_mock(mocker.patch.object(tracker, '_maybe_raise_error_from_html'), '_maybe_raise_error_from_html')

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            tracker._maybe_raise_error(response_or_request_error)
    else:
        return_value = tracker._maybe_raise_error(response_or_request_error)
        assert return_value is None

    assert mocks.mock_calls == [
        call._maybe_raise_error_from_json(response_or_request_error),
        call._maybe_raise_error_from_html(response_or_request_error),
    ]


@pytest.mark.parametrize(
    argnames='json, exp_exception',
    argvalues=(
        (Mock(side_effect=errors.RequestError('Malformed JSON')), None),
        (Mock(return_value={}), None),
        (Mock(return_value={'Result': 'Success'}), None),
        (Mock(return_value={'Result': 'Error'}), None),
        (Mock(return_value={'Result': 'Error', 'Message': ''}), None),
        (
            Mock(return_value={'Result': 'Error', 'Message': 'Oh no!'}),
            errors.RequestError('Oh no!'),
        ),
        (
            Mock(return_value={'Result': 'Error', 'Message': 'Oh no!\n<br />\n<br>This is not good.<br>\n<br/>'}),
            errors.RequestError('Oh no!\nThis is not good.'),
        ),
    ),
    ids=lambda v: repr(v),
)
def test_PtpTracker_maybe_raise_error_from_json(json, exp_exception, tracker):
    response_or_request_error = Mock(json=json)

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            tracker._maybe_raise_error_from_json(response_or_request_error)
    else:
        return_value = tracker._maybe_raise_error_from_json(response_or_request_error)
        assert return_value is None


@pytest.mark.parametrize('wrapper_class', (str, errors.RequestError))
@pytest.mark.parametrize(
    argnames='text, exp_exception',
    argvalues=(
        ('This is not HTML', None),
        ('<html>\nThis is HTML\n</html>', None),
        ('<html>\n<div id="content"><div>This is not an error</div></div>\n</html>', None),
        ('<html>\n<div id="content"><div class="page__title">Good News!</div></div>\n</html>', None),
        ('<html>\n<div id="content"><div class="page__title">Error</div></div>\n</html>', None),
        (
            (
                '<html>\n<div id="content">'
                '<div class="page__title">Error</div>'
                '<div>Everything is great</div>'
                '</div>\n</html>'
            ),
            None,
        ),
        (
            (
                '<html>\n<div id="content">'
                '<div class="page__title">Error</div>'
                '<div class="panel__body"></div>'
                '</div>\n</html>'
            ),
            None,
        ),
        (
            (
                '<html>\n<div id="content">'
                '<div class="page__title">Error</div>'
                '<div class="panel__body">  Something went wrong<br/>  Badly!  </div>'
                '</div>\n</html>'
            ),
            errors.RequestError('Something went wrong  Badly!'),
        ),
    ),
    ids=lambda v: repr(v),
)
def test_PtpTracker_maybe_raise_error_from_html(text, wrapper_class, exp_exception, tracker):
    response_or_request_error = wrapper_class(text)

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            tracker._maybe_raise_error_from_html(response_or_request_error)
    else:
        return_value = tracker._maybe_raise_error_from_html(response_or_request_error)
        assert return_value is None


@pytest.mark.parametrize(
    argnames='json, exp_result',
    argvalues=(
        (
            {'AntiCsrfToken': 'd34db33f'},
            'd34db33f',
        ),
        (
            {'wat': 'huh?'},
            KeyError('AntiCsrfToken'),
        ),
    ),
    ids=lambda v: repr(v),
)
def test_PtpTracker_get_anti_csrf_token(json, exp_result, tracker):
    response = Mock(json=Mock(return_value=json))
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker._get_anti_csrf_token(response)
    else:
        return_value = tracker._get_anti_csrf_token(response)
        assert return_value == exp_result


@pytest.mark.parametrize(
    argnames='response, exp_result',
    argvalues=(
        (
            '<html><a href="http://host/logout.php?auth=d34db33f&foo=bar">logout</a></html>',
            'd34db33f'
        ),
        (
            '<html><a href="http://host/logout.php?foo=bar&auth=d34db33f">logout</a></html>',
            'd34db33f'
        ),
        (
            '<html><a href="http://host/foo.php?foo=bar&auth=d34db33f">logout</a></html>',
            RuntimeError('Could not find auth'),
        ),
        (
            '<html><a>logout</a></html>',
            RuntimeError('Could not find auth'),
        ),
        (
            '<html></html>',
            RuntimeError('Could not find auth'),
        ),
        (
            errors.RequestError('Connection refused'),
            errors.RequestError('Connection refused'),
        ),
    ),
)
@pytest.mark.asyncio
async def test_PtpTracker_get_auth(response, exp_result, tracker, mocker):
    mocker.patch.object(type(tracker), 'is_logged_in', PropertyMock(return_value=True))
    mocker.patch.object(type(tracker), '_base_url', PropertyMock(return_value='http://host/'))

    mocks = Mock()
    if isinstance(response, Exception):
        mocks.attach_mock(
            mocker.patch.object(tracker, '_request', side_effect=response),
            '_request',
        )
    else:
        mocks.attach_mock(
            mocker.patch.object(tracker, '_request', return_value=response),
            '_request',
        )
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await tracker._get_auth()
    else:
        return_value = await tracker._get_auth()
        assert return_value == exp_result

    assert mocks.mock_calls == [
        call._request('GET', tracker._base_url),
    ]


@pytest.mark.parametrize(
    argnames='options, exp_result',
    argvalues=(
        pytest.param(
            {'password': 'hunter2'},
            errors.RequestError('Login failed: No username configured'),
            id='No username configured',
        ),
        pytest.param(
            {'username': 'AzureDiamond'},
            errors.RequestError('Login failed: No password configured'),
            id='No password configured',
        ),
        pytest.param(
            {'username': 'AzureDiamond', 'password': 'hunter2'},
            None,
            id='Login succeeds',
        ),
    ),
)
@pytest.mark.asyncio
async def test_PtpTracker_login(options, exp_result, tracker, mocker):
    mocker.patch.object(type(tracker), 'options', PropertyMock(return_value=options))
    mocker.patch.object(type(tracker), '_ajax_url', PropertyMock(return_value='http://host/ajax.php'))
    mocker.patch.object(type(tracker), '_passkey', PropertyMock(return_value='mypasskey'))

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker, '_request'), '_request')
    mocks.attach_mock(
        mocker.patch.object(tracker, '_get_anti_csrf_token', return_value='MOCK_ANTI_CSRF_TOKEN'),
        '_get_anti_csrf_token',
    )

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await tracker._login()

        assert mocks.mock_calls == []
        assert not hasattr(tracker, '_anti_csrf_token')

    else:
        return_value = await tracker._login()
        assert return_value is None

        assert mocks.mock_calls == [
            call._request(
                method='POST',
                url=f'{tracker._ajax_url}?action=login',
                data={
                    'username': options['username'],
                    'password': options['password'],
                    'passkey': tracker._passkey,
                },
                error_prefix='Login failed',
            ),
            call._get_anti_csrf_token(mocks._request.return_value),
        ]
        assert tracker._anti_csrf_token == 'MOCK_ANTI_CSRF_TOKEN'


@pytest.mark.parametrize('anti_csrf_token', (None, 'MOCK_ANTI_CSRF_TOKEN'))
@pytest.mark.parametrize(
    argnames='response',
    argvalues=(
        pytest.param(
            'ignored mock response',
            id='Logout succeeds',
        ),
        pytest.param(
            errors.RequestError('YOU CANNOT LEAVE'),
            id='Logout raises',
        ),
    ),
)
@pytest.mark.asyncio
async def test_PtpTracker_logout(response, anti_csrf_token, tracker, mocker):
    mocks = Mock()
    mocker.patch.object(type(tracker), 'name', PropertyMock(return_value='mytracker'))
    mocker.patch.object(type(tracker), '_logout_url', PropertyMock(return_value='http://host/logout.php'))
    if anti_csrf_token is not None:
        tracker._anti_csrf_token = anti_csrf_token
    mocks.attach_mock(
        mocker.patch.object(tracker, '_get_auth', return_value='mock auth'),
        '_get_auth',
    )
    if isinstance(response, Exception):
        mocks.attach_mock(
            mocker.patch.object(tracker, '_request', side_effect=response),
            '_request',
        )
    else:
        mocks.attach_mock(
            mocker.patch.object(tracker, '_request', return_value=response),
            '_request',
        )

    if isinstance(response, Exception):
        with pytest.raises(type(response), match=rf'^{re.escape(str(response))}$'):
            await tracker._logout()
    else:
        return_value = await tracker._logout()
        assert return_value is None

    assert mocks.mock_calls == [
        call._get_auth(),
        call._request(
            method='GET',
            url=tracker._logout_url,
            params={'auth': mocks._get_auth.return_value},
            error_prefix='Logout failed',
        ),
    ]
    assert not hasattr(tracker, '_anti_csrf_token')


@pytest.mark.asyncio
async def test_PtpTracker_get_announce_url(tracker, mocker):
    mocker.patch.object(type(tracker), '_announce_url', PropertyMock(return_value='http://mock.announce.url'))
    announce_url = await tracker.get_announce_url()
    assert announce_url == 'http://mock.announce.url'


@pytest.mark.asyncio
async def test_PtpTracker_upload(tracker, mocker):
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.http.post'),
        'post',
    )
    mocks.attach_mock(
        mocker.patch.object(tracker, '_handle_upload_response', return_value='mock response'),
        '_handle_upload_response',
    )
    mocker.patch.object(tracker, '_anti_csrf_token', 'MOCK_ANTI_CSRF_TOKEN', create=True)
    mocker.patch.object(type(tracker), '_upload_url', PropertyMock(return_value='http://host/upload.php'))

    tracker_jobs = Mock(
        post_data={'mock': 'post', 'data': 'for you'},
        torrent_filepath='path/to/content.torrent',
    )

    return_value = await tracker.upload(tracker_jobs)
    assert return_value == mocks._handle_upload_response.return_value

    assert mocks.mock_calls == [
        call.post(
            url=tracker._upload_url,
            cache=False,
            user_agent=True,
            data={'mock': 'post', 'data': 'for you', 'AntiCsrfToken': 'MOCK_ANTI_CSRF_TOKEN'},
            files={
                'file_input': {
                    'file': tracker_jobs.torrent_filepath,
                    'mimetype': 'application/x-bittorrent',
                },
            },
            follow_redirects=False,
        ),
        call._handle_upload_response(mocks.post.return_value),
    ]


@pytest.mark.parametrize(
    argnames='response, exp_result, exp_calls',
    argvalues=(
        pytest.param(
            MockResponse(headers={'Location': 'torrents.php?id=123'}),
            '{base_url}/torrents.php?id=123',
            [],
            id='Redirect to torrent page URL',
        ),
        pytest.param(
            MockResponse(headers={'Location': 'foo.php?id=123'}),
            errors.RequestError('Failed to interpret response (see ptp_upload_failed.html)'),
            [
                call.html_dump(str(MockResponse()), 'ptp_upload_failed.html'),
            ],
            id='Redirect to other URL',
        ),
        pytest.param(
            MockResponse(),
            errors.RequestError('Failed to interpret response (see ptp_upload_failed.html)'),
            [
                call.html_dump(str(MockResponse()), 'ptp_upload_failed.html'),
            ],
            id='No redirect',
        ),
        pytest.param(
            MockResponse(html='<html><div class="alert">  Your upload is <b>no good</b>!\n</html>'),
            errors.RequestError('Upload failed: Your upload is no good!'),
            [],
            id='Error message is found',
        ),
    ),
)
def test_PtpTracker_handle_upload_response(response, exp_result, exp_calls, tracker, mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker, 'error'), 'error')
    mocks.attach_mock(mocker.patch('upsies.utils.html.dump'), 'html_dump')

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker._handle_upload_response(response)
    else:
        return_value = tracker._handle_upload_response(response)
        assert return_value == exp_result.format(base_url=tracker._base_url)

    assert mocks.mock_calls == exp_calls


@pytest.mark.parametrize(
    argnames='imdb_id_digits, exp_return_value',
    argvalues=(
        ('1234567890', '1234567890'),
        ('123456789', '123456789'),
        ('12345678', '12345678'),
        ('1234567', '1234567'),
        ('123456', '0123456'),
        ('12345', '0012345'),
        ('1234', '0001234'),
        ('123', '0000123'),
        ('12', '0000012'),
        ('1', '0000001'),
        ('0', '0'),
        (1234567890, '1234567890'),
        (123456789, '123456789'),
        (12345678, '12345678'),
        (1234567, '1234567'),
        (123456, '0123456'),
        (12345, '0012345'),
        (1234, '0001234'),
        (123, '0000123'),
        (12, '0000012'),
        (1, '0000001'),
        (0, '0'),
        ('', '0'),
        (None, '0'),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize('prefix', ('tt', ''))
@pytest.mark.asyncio
async def test_PtpTracker_normalize_imdb_id(prefix, imdb_id_digits, exp_return_value, tracker):
    if isinstance(imdb_id_digits, str):
        imdb_id = prefix + imdb_id_digits
    else:
        imdb_id = imdb_id_digits

    return_value = tracker.normalize_imdb_id(imdb_id)
    assert return_value == exp_return_value


@pytest.mark.parametrize(
    argnames='imdb_id, exceptions, response, exp_return_value, exp_mock_calls',
    argvalues=(
        pytest.param(
            'tt0123',
            {},
            MockResponse(headers={'location': 'foo.php?id=123456'}),
            '123456',
            [
                call.login(),
                call.normalize_imdb_id('tt0123'),
                call._request,
            ],
            id='Group ID is found',
        ),
        pytest.param(
            'tt0123',
            {},
            MockResponse(headers={'location': 'foo.php?this=that'}),
            None,
            [
                call.login(),
                call.normalize_imdb_id('tt0123'),
                call._request,
            ],
            id='No group ID in location header',
        ),
        pytest.param(
            'tt0123',
            {},
            MockResponse(headers={'foo': 'bar'}),
            None,
            [
                call.login(),
                call.normalize_imdb_id('tt0123'),
                call._request,
            ],
            id='No location header in response',
        ),
        pytest.param(
            'tt0123',
            {
                'login': errors.RequestError('Wrong password'),
            },
            None,
            None,
            [
                call.login(),
                call.error(errors.RequestError('Wrong password')),
            ],
            id='Login failed',
        ),
        pytest.param(
            'tt0123',
            {
                '_request': errors.RequestError('No response'),
            },
            None,
            None,
            [
                call.login(),
                call.normalize_imdb_id('tt0123'),
                call._request,
                call.error(errors.RequestError('No response')),
            ],
            id='Request failed',
        ),
    ),
)
@pytest.mark.asyncio
async def test_PtpTracker_get_ptp_group_id_by_imdb_id(imdb_id, exceptions, response,
                                                      exp_return_value, exp_mock_calls,
                                                      tracker, mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker, 'login'), 'login')
    mocks.attach_mock(mocker.patch.object(tracker, '_request', return_value=response), '_request')
    mocker.patch.object(type(tracker), '_torrents_url', PropertyMock(return_value='http://host/torrents.php'))
    mocks.attach_mock(mocker.patch.object(tracker, 'normalize_imdb_id'), 'normalize_imdb_id')
    mocks.attach_mock(mocker.patch.object(tracker, 'error'), 'error')

    for method, exception in exceptions.items():
        getattr(mocks, method).side_effect = exception

    return_value = await tracker.get_ptp_group_id_by_imdb_id(imdb_id)
    assert return_value == exp_return_value

    # Add call._request() arguments
    if call._request in exp_mock_calls:
        exp_mock_calls[exp_mock_calls.index(call._request)] = call._request(
            method='GET',
            url=tracker._torrents_url,
            params={
                'imdb': tracker.normalize_imdb_id.return_value,
                'json': '1',
            },
            cache=True,
        )
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='imdb_id, key, exceptions, response, exp_return_value, exp_mock_calls',
    argvalues=(
        pytest.param(
            'tt0123', None,
            {},
            MockResponse(json=[{'all': 'metadata'}]),
            {'all': 'metadata'},
            [
                call.login(),
                call.normalize_imdb_id('tt0123'),
                call._request,
            ],
            id='Get all metadata',
        ),
        pytest.param(
            'tt0123', 'bar',
            {},
            MockResponse(json=[{'foo': 1, 'bar': 2, 'baz': 3}]),
            2,
            [
                call.login(),
                call.normalize_imdb_id('tt0123'),
                call._request,
            ],
            id='Get single metadata field',
        ),
        pytest.param(
            'tt0123', 'bar',
            {
                'login': errors.RequestError('Wrong password'),
            },
            None,
            None,
            [
                call.login(),
                call.error(errors.RequestError('Wrong password')),
            ],
            id='Login failed',
        ),
        pytest.param(
            'tt0123', 'bar',
            {
                '_request': errors.RequestError('No response'),
            },
            None,
            None,
            [
                call.login(),
                call.normalize_imdb_id('tt0123'),
                call._request,
                call.error(errors.RequestError('No response')),
            ],
            id='Request failed',
        ),
    ),
)
@pytest.mark.asyncio
async def test_PtpTracker_get_ptp_metadata(imdb_id, key, exceptions, response,
                                           exp_return_value, exp_mock_calls,
                                           tracker, mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker, 'login'), 'login')
    mocks.attach_mock(mocker.patch.object(tracker, '_request', return_value=response), '_request')
    mocker.patch.object(type(tracker), '_ajax_url', PropertyMock(return_value='http://host/ajax.php'))
    mocks.attach_mock(mocker.patch.object(tracker, 'normalize_imdb_id'), 'normalize_imdb_id')
    mocks.attach_mock(mocker.patch.object(tracker, 'error'), 'error')

    for method, exception in exceptions.items():
        getattr(mocks, method).side_effect = exception

    return_value = await tracker.get_ptp_metadata(imdb_id, key=key)
    assert return_value == exp_return_value

    # Add call._request() arguments
    if call._request in exp_mock_calls:
        exp_mock_calls[exp_mock_calls.index(call._request)] = call._request(
            method='GET',
            url='http://host/ajax.php',
            params={
                'action': 'torrent_info',
                'imdb': mocks.normalize_imdb_id.return_value,
            },
            cache=True,
        )
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='bytes, exp_piece_size',
    argvalues=(
        # Numbers are copied from PTP piece size chart
        (1 * 1024 * 1024, 2**15),
        (6 * 1024 * 1024, 2**15),
        (10 * 1024 * 1024, 2**15),
        (12 * 1024 * 1024, 2**15),
        (15 * 1024 * 1024, 2**15),
        (18 * 1024 * 1024, 2**15),
        (22 * 1024 * 1024, 2**15),
        (27 * 1024 * 1024, 2**15),

        (33 * 1024 * 1024, 2**16),
        (40 * 1024 * 1024, 2**16),
        (48 * 1024 * 1024, 2**16),
        (58 * 1024 * 1024, 2**16),

        (70 * 1024 * 1024, 2**17),
        (84 * 1024 * 1024, 2**17),
        (101 * 1024 * 1024, 2**17),
        (122 * 1024 * 1024, 2**17),

        (147 * 1024 * 1024, 2**18),
        (177 * 1024 * 1024, 2**18),
        (213 * 1024 * 1024, 2**18),
        (256 * 1024 * 1024, 2**18),

        (308 * 1024 * 1024, 2**19),
        (370 * 1024 * 1024, 2**19),
        (444 * 1024 * 1024, 2**19),

        (533 * 1024 * 1024, 2**20),
        (640 * 1024 * 1024, 2**20),
        (768 * 1024 * 1024, 2**20),
        (922 * 1024 * 1024, 2**20),

        (1.08 * 1024 * 1024 * 1024, 2**21),
        (1.30 * 1024 * 1024 * 1024, 2**21),
        (1.56 * 1024 * 1024 * 1024, 2**21),
        (1.87 * 1024 * 1024 * 1024, 2**21),

        (2.24 * 1024 * 1024 * 1024, 2**22),
        (2.69 * 1024 * 1024 * 1024, 2**22),
        (3.23 * 1024 * 1024 * 1024, 2**22),
        (3.88 * 1024 * 1024 * 1024, 2**22),

        (4.65 * 1024 * 1024 * 1024, 2**23),
        (5.59 * 1024 * 1024 * 1024, 2**23),
        (6.70 * 1024 * 1024 * 1024, 2**23),
        (8.04 * 1024 * 1024 * 1024, 2**23),

        (9.65 * 1024 * 1024 * 1024, 2**24),
        (11.58 * 1024 * 1024 * 1024, 2**24),
        (13.90 * 1024 * 1024 * 1024, 2**24),
        (16.68 * 1024 * 1024 * 1024, 2**24),
        (20.02 * 1024 * 1024 * 1024, 2**24),
        (24.02 * 1024 * 1024 * 1024, 2**24),
        (28.83 * 1024 * 1024 * 1024, 2**24),
        (34.59 * 1024 * 1024 * 1024, 2**24),
        (41.51 * 1024 * 1024 * 1024, 2**24),
        (49.81 * 1024 * 1024 * 1024, 2**24),
        (59.78 * 1024 * 1024 * 1024, 2**24),
        (71.73 * 1024 * 1024 * 1024, 2**24),
        (86.08 * 1024 * 1024 * 1024, 2**24),
        (103.30 * 1024 * 1024 * 1024, 2**24),
        (123.96 * 1024 * 1024 * 1024, 2**24),
        (148.75 * 1024 * 1024 * 1024, 2**24),
        (178.50 * 1024 * 1024 * 1024, 2**24),
        (214.20 * 1024 * 1024 * 1024, 2**24),
        (257.04 * 1024 * 1024 * 1024, 2**24),
        (308.45 * 1024 * 1024 * 1024, 2**24),
        (370.14 * 1024 * 1024 * 1024, 2**24),
        (444.16 * 1024 * 1024 * 1024, 2**24),
        (533.00 * 1024 * 1024 * 1024, 2**24),
        (639.60 * 1024 * 1024 * 1024, 2**24),
        (767.52 * 1024 * 1024 * 1024, 2**24),
        (921.02 * 1024 * 1024 * 1024, 2**24),
    ),
)
def test_PtpTracker_calculate_piece_size(bytes, exp_piece_size):
    piece_size = ptp.PtpTracker.calculate_piece_size(bytes)
    assert piece_size == exp_piece_size


@pytest.mark.parametrize(
    argnames='bytes, exp_result',
    argvalues=(
        (                            -12, ValueError('Unexpected size: -12')),  # noqa E201, E221
        (                             -1, ValueError('Unexpected size: -1')),   # noqa E201, E221
        (                              0, ValueError('Unexpected size: 0')),    # noqa E201

        # Values below were copied from piece size chart on the website

        (            1 * 1024 * 1024, (2**15, 2**18)),  # noqa E201
        (          122 * 1024 * 1024, (2**15, 2**18)),  # noqa E201

        (          147 * 1024 * 1024, (2**16, 2**19)),  # noqa E201
        (          213 * 1024 * 1024, (2**16, 2**19)),  # noqa E201

        (          256 * 1024 * 1024, (2**17, 2**20)),  # noqa E201
        (          444 * 1024 * 1024, (2**17, 2**20)),  # noqa E201

        (          533 * 1024 * 1024, (2**18, 2**21)),  # noqa E201
        (          922 * 1024 * 1024, (2**18, 2**21)),  # noqa E201

        (  1.08 * 1024 * 1024 * 1024, (2**19, 2**22)),  # noqa E201
        (  1.87 * 1024 * 1024 * 1024, (2**19, 2**22)),  # noqa E201

        (  2.24 * 1024 * 1024 * 1024, (2**20, 2**23)),  # noqa E201
        (  3.88 * 1024 * 1024 * 1024, (2**20, 2**23)),  # noqa E201

        (  4.65 * 1024 * 1024 * 1024, (2**21, 2**24)),  # noqa E201
        (  6.70 * 1024 * 1024 * 1024, (2**21, 2**24)),  # noqa E201

        (  8.04 * 1024 * 1024 * 1024, (2**22, 2**24)),  # noqa E201
        (123.96 * 1024 * 1024 * 1024, (2**22, 2**24)),  # noqa E201

        (148.75 * 1024 * 1024 * 1024, (2**23, 2**24)),  # noqa E201
        (214.20 * 1024 * 1024 * 1024, (2**23, 2**24)),  # noqa E201

        (257.04 * 1024 * 1024 * 1024, (2**24, 2**24)),  # noqa E201
        (921.02 * 1024 * 1024 * 1024, (2**24, 2**24)),  # noqa E201
    ),
    ids=lambda v: repr(v),
)
def test_PtpTracker_calculate_piece_size_min_max(bytes, exp_result):
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            ptp.PtpTracker.calculate_piece_size_min_max(bytes)
    else:
        piece_size_min, piece_size_max = ptp.PtpTracker.calculate_piece_size_min_max(bytes)
        assert (piece_size_min, piece_size_max) == exp_result
