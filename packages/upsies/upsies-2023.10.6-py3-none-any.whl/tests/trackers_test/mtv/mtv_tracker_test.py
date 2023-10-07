import os
import re
from unittest.mock import Mock, PropertyMock, call

import pytest

from upsies import __project_name__, errors, utils
from upsies.trackers.mtv import MtvTracker, MtvTrackerConfig, MtvTrackerJobs


@pytest.fixture
def make_tracker():
    def make_tracker(**kwargs):
        options = {
            'username': 'bunny',
            'password': 'hunter2',
            'base_url': 'http://mtv.local',
        }
        options.update(kwargs)
        return MtvTracker(options=options)

    return make_tracker


def test_name_attribute():
    assert MtvTracker.name == 'mtv'


def test_label_attribute():
    assert MtvTracker.label == 'MTV'


def test_TrackerConfig_attribute():
    assert MtvTracker.TrackerConfig is MtvTrackerConfig


def test_MtvTracker_attribute():
    assert MtvTracker.TrackerJobs is MtvTrackerJobs


def test_MtvTracker_base_url_attribute(make_tracker):
    tracker = make_tracker(base_url='http://foo.local')
    assert tracker._base_url == 'http://foo.local'


def test_MtvTracker_login_url_attribute(make_tracker):
    tracker = make_tracker(base_url='http://foo.local')
    assert tracker._login_url == 'http://foo.local/login'


def test_MtvTracker_logout_url_attribute(make_tracker):
    tracker = make_tracker(base_url='http://foo.local')
    assert tracker._logout_url == 'http://foo.local/logout'


def test_MtvTracker_upload_url_attribute(make_tracker):
    tracker = make_tracker(base_url='http://foo.local')
    assert tracker._upload_url == 'http://foo.local/upload.php'


def test_MtvTracker_torrents_url_attribute(make_tracker):
    tracker = make_tracker(base_url='http://foo.local')
    assert tracker._torrents_url == 'http://foo.local/torrents.php'


@pytest.fixture
def tracker_for_login(make_tracker, mocker):
    tracker = make_tracker()
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker, '_get_token', return_value='mock token'), '_get_token')
    mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.post'), 'post')
    mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.html.parse'), 'parse')
    mocks.attach_mock(mocker.patch.object(tracker, '_confirm_login'), '_confirm_login')
    return tracker, mocks

@pytest.mark.asyncio
async def test_MtvTracker_login_without_username(tracker_for_login):
    tracker, mocks = tracker_for_login
    del tracker.options['username']
    with pytest.raises(errors.RequestError, match=r'^Login failed: No username configured$'):
        await tracker._login()
    assert mocks.mock_calls == []

@pytest.mark.asyncio
async def test_MtvTracker_login_without_password(tracker_for_login):
    tracker, mocks = tracker_for_login
    del tracker.options['password']
    with pytest.raises(errors.RequestError, match=r'^Login failed: No password configured$'):
        await tracker._login()
    assert mocks.mock_calls == []

@pytest.mark.asyncio
async def test_MtvTracker_login_succeeds(tracker_for_login):
    tracker, mocks = tracker_for_login
    await tracker._login()
    assert mocks.mock_calls == [
        call._get_token(),
        call.post(
            url=tracker._login_url,
            user_agent=True,
            data={
                'token': mocks._get_token.return_value,
                'username': tracker.options['username'],
                'password': tracker.options['password'],
                'cinfo': '1280|720|24|0',
                'iplocked': '1',
                'submit': 'login',
            },
        ),
        call.parse(mocks.post.return_value),
        call._confirm_login(mocks.parse.return_value),
    ]


@pytest.fixture
def make_tracker_for_logout(make_tracker, mocker):
    def make_tracker_for_logout():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.post'), 'post')
        mocks.attach_mock(mocker.patch.object(tracker, '_get_token'), '_get_token')
        return tracker, mocks

    return make_tracker_for_logout

@pytest.mark.asyncio
async def test_MtvTracker_logout_fails(make_tracker_for_logout):
    tracker, mocks = make_tracker_for_logout()
    exception = errors.RequestError('nope')
    mocks.post.side_effect = exception

    with pytest.raises(type(exception), match=rf'^{re.escape(str(exception))}$'):
        await tracker._logout()

    exp_mock_calls = [
        call._get_token(),
        call.post(
            url=tracker._logout_url,
            data={'token': mocks._get_token.return_value},
            user_agent=True,
        ),
    ]
    assert mocks.mock_calls == exp_mock_calls

@pytest.mark.asyncio
async def test_MtvTracker_logout_succeeds(make_tracker_for_logout):
    tracker, mocks = make_tracker_for_logout()

    await tracker._logout()

    exp_mock_calls = [
        call._get_token(),
        call.post(
            url=tracker._logout_url,
            data={'token': mocks._get_token.return_value},
            user_agent=True,
        ),
    ]
    assert mocks.mock_calls == exp_mock_calls


@pytest.fixture
def make_tracker_for_get_announce_url(make_tracker, mocker):
    def make_tracker_for_get_announce_url():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.get'), 'get')
        mocks.attach_mock(mocker.patch.object(tracker, 'login'), 'login')
        mocks.attach_mock(mocker.patch.object(tracker, 'logout'), 'logout')
        return tracker, mocks

    return make_tracker_for_get_announce_url

@pytest.mark.parametrize(
    argnames='config_url, website_url, exp_url',
    argvalues=(
        ('http://config.url/announce', 'http://website.url/announce', 'http://config.url/announce'),
        ('', 'http://website.url/announce', 'http://website.url/announce'),
        (None, 'http://website.url/announce', 'http://website.url/announce'),
    ),
)
@pytest.mark.asyncio
async def test_MtvTracker_get_announce_url_from_config(config_url, website_url, exp_url, make_tracker_for_get_announce_url, mocker):
    tracker, mocks = make_tracker_for_get_announce_url()
    mocks.get.return_value = f'<html><input value="{website_url}" /></html>'
    if config_url is not None:
        tracker.options['announce_url'] = config_url
    announce_url = await tracker.get_announce_url()
    assert announce_url == exp_url

@pytest.mark.parametrize(
    argnames='html, exp_result',
    argvalues=(
        (
            '<html><input value="http://foo.local:123/announce" /></html>',
            'http://foo.local:123/announce',
        ),
        (
            '<html><input value="https://foo.local:123/announce?d34db33f" /></html>',
            'https://foo.local:123/announce?d34db33f',
        ),
        (
            '<html><input value="https://foo.local:123/announce/d34db33f" /></html>',
            'https://foo.local:123/announce/d34db33f',
        ),
        (
            '<html><input value="https://foo.local:123/d34db33f/announce" /></html>',
            'https://foo.local:123/d34db33f/announce',
        ),
        (
            '<html><input value="https://foo.local:123/anon" /></html>',
            errors.RequestError(
                'Failed to find announce URL - set it manually: '
                f'{__project_name__} set trackers.mtv.announce_url <YOUR URL>',
            ),
        ),
        (
            '<html><input value="" /></html>',
            errors.RequestError(
                'Failed to find announce URL - set it manually: '
                f'{__project_name__} set trackers.mtv.announce_url <YOUR URL>',
            ),
        ),
        (
            '<html><input /></html>',
            errors.RequestError(
                'Failed to find announce URL - set it manually: '
                f'{__project_name__} set trackers.mtv.announce_url <YOUR URL>',
            ),
        ),
        (
            '<html><div>hello</div></html>',
            errors.RequestError(
                'Failed to find announce URL - set it manually: '
                f'{__project_name__} set trackers.mtv.announce_url <YOUR URL>',
            ),
        ),
    ),
)
@pytest.mark.asyncio
async def test_MtvTracker_get_announce_url_from_website(html, exp_result, make_tracker_for_get_announce_url, mocker):
    tracker, mocks = make_tracker_for_get_announce_url()
    tracker.options['announce_url'] = None
    mocks.get.return_value = html

    if isinstance(exp_result, BaseException):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await tracker.get_announce_url()
    else:
        return_value = await tracker.get_announce_url()
        assert return_value == exp_result

    assert mocks.mock_calls == [
        call.login(),
        call.get(tracker._upload_url, user_agent=True),
        # call.logout(),
    ]


def test_MtvTracker_calculate_piece_size_min_max():
    piece_size_min, piece_size_max = MtvTracker.calculate_piece_size_min_max(123456)
    assert piece_size_min == 32 * 1024
    assert piece_size_max == 8 * 1024 * 1024


@pytest.fixture
def make_tracker_for_upload(make_tracker, mocker, tmp_path):
    def make_tracker_for_upload():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch.object(tracker, '_make_autofill_request'), '_make_autofill_request')
        mocks.attach_mock(mocker.patch.object(tracker, '_make_upload_request'), '_make_upload_request')
        return tracker, mocks

    return make_tracker_for_upload

@pytest.mark.asyncio
async def test_MtvTracker_upload(make_tracker_for_upload, mocker):
    tracker, mocks = make_tracker_for_upload()
    tracker_jobs = Mock()

    tracker_page_url = await tracker.upload(tracker_jobs)
    assert tracker_page_url is tracker._make_upload_request.return_value

    assert mocks.mock_calls == [
        call._make_autofill_request(tracker_jobs),
        call._make_upload_request(tracker_jobs, mocks._make_autofill_request.return_value),
    ]


@pytest.fixture
def make_tracker_for_make_autofill_request(make_tracker, mocker, tmp_path):
    def make_tracker_for_make_autofill_request():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch.object(tracker, '_prepare_post_data', return_value={'prepared': 'data'}), '_prepare_post_data')
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.post'), 'post')
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.html.parse'), 'parse')
        mocks.attach_mock(mocker.patch.object(tracker, '_raise_error_dupes'), '_raise_error_dupes')
        mocks.attach_mock(mocker.patch.object(tracker, '_raise_error'), '_raise_error')
        mocks.attach_mock(mocker.patch.object(tracker, '_get_form_value'), '_get_form_value')
        return tracker, mocks

    return make_tracker_for_make_autofill_request

@pytest.mark.asyncio
async def test_MtvTracker_make_autofill_request_succeeds(make_tracker_for_make_autofill_request, mocker):
    tracker, mocks = make_tracker_for_make_autofill_request()
    tracker_jobs = Mock(
        post_data_autofill={'autofill': 'data'},
        torrent_filepath='mock/path/to.torrent',
    )
    mocks.post.return_value = '<html><form>autofilled values</form></html>'
    mocks._get_form_value.side_effect = (
        'mock tempfileid',
        'mock tempfilename',
        'mock taglist',
    )

    autofill_post_data = await tracker._make_autofill_request(tracker_jobs)
    assert autofill_post_data == {
        'tempfileid': 'mock tempfileid',
        'tempfilename': 'mock tempfilename',
        'taglist': 'mock taglist',
    }

    assert mocks.mock_calls == [
        call._prepare_post_data(tracker_jobs.post_data_autofill),
        call.post(
            url=tracker._upload_url,
            cache=False,
            user_agent=True,
            follow_redirects=False,
            data={'prepared': 'data'},
            files={
                'file_input': {
                    'file': tracker_jobs.torrent_filepath,
                    'mimetype': 'application/x-bittorrent',
                },
            },
        ),
        call.parse(mocks.post.return_value),
        call._get_form_value(mocks.parse.return_value, 'input', attrs={'name': 'tempfileid'}),
        call._get_form_value(mocks.parse.return_value, 'input', attrs={'name': 'tempfilename'}),
        call._get_form_value(mocks.parse.return_value, 'textarea', attrs={'name': 'taglist'}),
    ]


@pytest.mark.parametrize(
    argnames='unfound_form_field',
    argvalues=(
        (('input',), {'attrs': {'name': 'tempfileid'}}),
        (('input',), {'attrs': {'name': 'tempfilename'}}),
        (('textarea',), {'attrs': {'name': 'taglist'}}),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_MtvTracker_make_autofill_request_fails(unfound_form_field, make_tracker_for_make_autofill_request, mocker):
    tracker, mocks = make_tracker_for_make_autofill_request()
    tracker_jobs = Mock(
        post_data_autofill={'autofill': 'data'},
        torrent_filepath='mock/path/to.torrent',
    )
    mocks.post.return_value = '<html><form>autofilled values</form></html>'

    def get_form_value_side_effect(doc, *args, **kwargs):
        if (args, kwargs) == unfound_form_field:
            raise ValueError(f'No such form field: ({args}, {kwargs})')

    mocks._get_form_value.side_effect = get_form_value_side_effect

    mocks._raise_error.side_effect = errors.RequestError('Autofilling failed')

    exp_exception = mocks._raise_error.side_effect
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
        await tracker._make_autofill_request(tracker_jobs)

    exp_mock_calls = [
        call._prepare_post_data(tracker_jobs.post_data_autofill),
        call.post(
            url=tracker._upload_url,
            cache=False,
            user_agent=True,
            follow_redirects=False,
            data={'prepared': 'data'},
            files={
                'file_input': {
                    'file': tracker_jobs.torrent_filepath,
                    'mimetype': 'application/x-bittorrent',
                },
            },
        ),
        call.parse(mocks.post.return_value),
    ]

    # We don't care about the order of _get_form_value() calls
    assert mocks.mock_calls[:len(exp_mock_calls)] == exp_mock_calls
    # TODO: Figure out how to assert that every mocks.mock_calls[len(exp_mock_calls):-1]
    #       is call._get_from_value() without specifying the exact arguments.
    assert mocks.mock_calls[-1] == call._raise_error(mocks.parse.return_value, msg_prefix='Upload failed')


@pytest.fixture
def make_tracker_for_make_upload_request(make_tracker, mocker, tmp_path):
    def make_tracker_for_make_upload_request():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch.object(tracker, '_prepare_post_data', return_value={'prepared': 'data'}), '_prepare_post_data')
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.post'), 'post')
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.html.parse'), 'parse')
        mocks.attach_mock(mocker.patch.object(tracker, '_raise_error_dupes'), '_raise_error_dupes')
        mocks.attach_mock(mocker.patch.object(tracker, '_raise_error'), '_raise_error')
        return tracker, mocks

    cwd_orig = os.getcwd()
    os.chdir(tmp_path)
    try:
        yield make_tracker_for_make_upload_request
    finally:
        os.chdir(cwd_orig)

@pytest.mark.asyncio
async def test_MtvTracker_make_upload_request_succeeds(make_tracker_for_make_upload_request, mocker):
    tracker, mocks = make_tracker_for_make_upload_request()
    tracker_jobs = Mock(post_data_upload={'upload': 'data'})
    autofill_post_data = {'autofill': 'data'}
    exp_post_data = {
        'prepared': 'data',
        'autofill': 'data',
    }
    mocks.post.return_value = Mock(headers={'location': '/torrents.php?id=123'})

    torrent_page_url = await tracker._make_upload_request(tracker_jobs, autofill_post_data)
    assert torrent_page_url == f'{tracker._base_url}/torrents.php?id=123'

    assert mocks.mock_calls == [
        call._prepare_post_data(tracker_jobs.post_data_upload),
        call.post(
            url=tracker._upload_url,
            cache=False,
            user_agent=True,
            follow_redirects=False,
            data=exp_post_data,
        ),
    ]

@pytest.mark.asyncio
async def test_MtvTracker_make_upload_request_finds_dupes(make_tracker_for_make_upload_request, mocker):
    tracker, mocks = make_tracker_for_make_upload_request()
    tracker_jobs = Mock(post_data_upload={'upload': 'data'})
    autofill_post_data = {'autofill': 'data'}
    exp_post_data = {
        'prepared': 'data',
        'autofill': 'data',
    }
    mocks._raise_error_dupes.side_effect = errors.FoundDupeError(['dupe file'])
    mocks.post.return_value = Mock(headers={})

    exp_exception = mocks._raise_error_dupes.side_effect
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
        await tracker._make_upload_request(tracker_jobs, autofill_post_data)

    assert mocks.mock_calls == [
        call._prepare_post_data(tracker_jobs.post_data_upload),
        call.post(
            url=tracker._upload_url,
            cache=False,
            user_agent=True,
            follow_redirects=False,
            data=exp_post_data,
        ),
        call.parse(mocks.post.return_value),
        call._raise_error_dupes(mocks.parse.return_value),
    ]

@pytest.mark.asyncio
async def test_MtvTracker_make_upload_request_finds_error_message(make_tracker_for_make_upload_request, mocker):
    tracker, mocks = make_tracker_for_make_upload_request()
    tracker_jobs = Mock(post_data_upload={'upload': 'data'})
    autofill_post_data = {'autofill': 'data'}
    exp_post_data = {
        'prepared': 'data',
        'autofill': 'data',
    }
    mocks._raise_error.side_effect = errors.RequestError('Your upload sucks monkey balls.')
    mocks.post.return_value = Mock(headers={})

    exp_exception = mocks._raise_error.side_effect
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
        await tracker._make_upload_request(tracker_jobs, autofill_post_data)

    assert mocks.mock_calls == [
        call._prepare_post_data(tracker_jobs.post_data_upload),
        call.post(
            url=tracker._upload_url,
            cache=False,
            user_agent=True,
            follow_redirects=False,
            data=exp_post_data,
        ),
        call.parse(mocks.post.return_value),
        call._raise_error_dupes(mocks.parse.return_value),
        call._raise_error(mocks.parse.return_value, msg_prefix='Upload failed'),
    ]

@pytest.mark.asyncio
async def test_MtvTracker_make_upload_request_cannot_find_error_message(make_tracker_for_make_upload_request, mocker, tmp_path):
    tracker, mocks = make_tracker_for_make_upload_request()
    tracker_jobs = Mock(
        post_data_upload={'upload': 'data'},
        content_path='path/to/Foo.2012-HEYHO/',
    )
    autofill_post_data = {'autofill': 'data'}
    exp_post_data = {
        'prepared': 'data',
        'autofill': 'data',
    }
    mocks._raise_error.side_effect = RuntimeError('My error discovery sucks monkey balls.')
    mocks.post.return_value = Mock(headers={
        'mock': 'header',
        'fali': 'fala',
    })

    exp_exception = mocks._raise_error.side_effect
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
        await tracker._make_upload_request(tracker_jobs, autofill_post_data)

    assert mocks.mock_calls == [
        call._prepare_post_data(tracker_jobs.post_data_upload),
        call.post(
            url=tracker._upload_url,
            cache=False,
            user_agent=True,
            follow_redirects=False,
            data=exp_post_data,
        ),
        call.parse(mocks.post.return_value),
        call._raise_error_dupes(mocks.parse.return_value),
        call._raise_error(mocks.parse.return_value, msg_prefix='Upload failed'),
    ]

    dumped_headers_file = 'Foo.2012-HEYHO.headers'
    dumped_headers = (tmp_path / dumped_headers_file).read_text()
    assert dumped_headers == 'mock: header\nfali: fala\n'


@pytest.fixture
def make_tracker_for_prepare_post_data(make_tracker, mocker):
    def make_tracker_for_prepare_post_data():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch.object(tracker, '_get_auth', return_value='myauth'), '_get_auth')
        return tracker, mocks

    return make_tracker_for_prepare_post_data

@pytest.mark.parametrize(
    argnames='post_data, exp_post_data',
    argvalues=(
        (
            {'foo': 'bar', 1: 2, 'nothing': None},
            {'foo': 'bar', '1': '2', 'auth': 'myauth'},
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_MtvTracker_prepare_post_data(post_data, exp_post_data, make_tracker_for_prepare_post_data, mocker):
    tracker, mocks = make_tracker_for_prepare_post_data()
    return_value = await tracker._prepare_post_data(post_data)
    assert return_value == exp_post_data
    assert mocks.mock_calls == [
        call._get_auth(),
    ]


@pytest.fixture
def make_tracker_for_get_token(make_tracker, mocker):
    def make_tracker_for_get_token():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.get'), 'get')
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.html.parse'), 'parse')
        mocks.attach_mock(mocker.patch.object(tracker, '_get_form_value'), '_get_form_value')
        return tracker, mocks

    return make_tracker_for_get_token

@pytest.mark.parametrize(
    argnames='is_logged_in, exp_url_attribute',
    argvalues=(
        (True, '_base_url'),
        (False, '_login_url'),
    ),
)
@pytest.mark.asyncio
async def test_MtvTracker_get_token(is_logged_in, exp_url_attribute, make_tracker_for_get_token, mocker):
    tracker, mocks = make_tracker_for_get_token()
    mocker.patch.object(type(tracker), 'is_logged_in', PropertyMock(return_value=is_logged_in))
    return_value = await tracker._get_token()
    assert return_value is mocks._get_form_value.return_value
    exp_url = getattr(tracker, exp_url_attribute)
    assert mocks.mock_calls == [
        call.get(exp_url, user_agent=True),
        call.parse(mocks.get.return_value),
        call._get_form_value(mocks.parse.return_value, 'input', attrs={'name': 'token'}),
    ]


@pytest.fixture
def make_tracker_for_get_auth(make_tracker, mocker):
    def make_tracker_for_get_auth():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch.object(tracker, 'login'), 'login')
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.http.get'), 'get')
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.html.parse'), 'parse')
        mocks.attach_mock(mocker.patch.object(tracker, '_get_form_value'), '_get_form_value')
        return tracker, mocks

    return make_tracker_for_get_auth

@pytest.mark.asyncio
async def test_MtvTracker_get_auth_with_previously_gotten_auth(make_tracker_for_get_auth, mocker):
    tracker, mocks = make_tracker_for_get_auth()
    tracker._auth = 'my auth'
    auth = await tracker._get_auth()
    assert auth == 'my auth'
    assert mocks.mock_calls == []

@pytest.mark.asyncio
async def test_MtvTracker_get_auth_without_previously_gotten_auth(make_tracker_for_get_auth, mocker):
    tracker, mocks = make_tracker_for_get_auth()
    auth = await tracker._get_auth()
    assert auth is mocks._get_form_value.return_value
    assert mocks.mock_calls == [
        call.login(),
        call.get(tracker._upload_url, user_agent=True),
        call.parse(mocks.get.return_value),
        call._get_form_value(mocks.parse.return_value, 'input', attrs={'name': 'auth'}),
    ]


@pytest.fixture
def make_tracker_for_get_form_value(make_tracker, mocker):
    def make_tracker_for_get_form_value():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch.object(tracker, '_raise_error'), '_raise_error')
        return tracker, mocks

    return make_tracker_for_get_form_value

@pytest.mark.parametrize(
    argnames='html, tag_name, kwargs, exp_result',
    argvalues=(
        # Get value from tag: <... value="..."/>
        (
            '<input class="foo" value="asdf"/>',
            'input',
            {'attrs': {'class': 'foo'}},
            'asdf',
        ),

        # Get value from between tags: <textarea>...</textarea>
        (
            '<textarea class="bar">asdf <b>bold</b></textarea>',
            'textarea',
            {'attrs': {'class': 'bar'}},
            'asdf bold',
        ),

        # Empty value: <... value=""/>
        (
            '<input class="foo" value=""/>',
            'input',
            {'attrs': {'class': 'foo'}},
            ValueError('Tag has no value: <input class="foo" value=""/>'),
        ),

        # Empty value: <textarea></textarea>
        (
            '<textarea class="bar"></textarea>',
            'textarea',
            {'attrs': {'class': 'bar'}},
            ValueError('Tag has no value: <textarea class="bar"></textarea>'),
        ),

        # Tag not found
        (
            '<sometag>asdf</sometag>',
            'mytag',
            {},
            ValueError('Could not find tag: mytag'),
        ),

        # Tag class not found
        (
            '<input class="foo" value="asdf"/>',
            'input',
            {'attrs': {'class': 'bar'}},
            ValueError('Could not find tag: input'),
        ),
    ),
)
def test_MtvTracker_get_form_value(html, tag_name, kwargs, exp_result, make_tracker_for_get_form_value):
    tracker, mocks = make_tracker_for_get_form_value()
    doc = utils.html.parse(html)
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker._get_form_value(doc, tag_name, **kwargs)
    else:
        return_value = tracker._get_form_value(doc, tag_name, **kwargs)
        assert return_value == exp_result


@pytest.fixture
def make_tracker_for_confirm_login(make_tracker, mocker):
    def make_tracker_for_confirm_login():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch.object(tracker, '_raise_error'), '_raise_error')
        return tracker, mocks

    return make_tracker_for_confirm_login

@pytest.mark.parametrize(
    argnames='html, exp_user_id, exp_exception',
    argvalues=(
        (
            '<html><a href="/user.php?id=123">superuser</a></html>',
            '123',
            None,
        ),
        (
            '<html><div class="flash error">The <b>ERROR</b> message!</div></html>',
            None,
            errors.RequestError('Login failed: The ERROR message!'),
        ),
        (
            '<html><div>Not the error message</div></html>',
            None,
            RuntimeError('Login failed: No error message found'),
        ),
    ),
)
def test_MtvTracker_confirm_login(html, exp_user_id, exp_exception, make_tracker_for_confirm_login):
    tracker, mocks = make_tracker_for_confirm_login()
    doc = utils.html.parse(html)
    return_value = tracker._confirm_login(doc)
    assert return_value is None
    assert tracker._user_id == exp_user_id

    if exp_exception:
        assert mocks.mock_calls == [
            call._raise_error(doc, msg_prefix='Login failed')
        ]
    else:
        assert mocks.mock_calls == []


@pytest.fixture
def make_tracker_for_raise_error(make_tracker, mocker):
    def make_tracker_for_raise_error():
        tracker = make_tracker()
        mocks = Mock()
        mocks.attach_mock(mocker.patch('upsies.trackers.mtv.tracker.utils.html.dump'), 'dump')
        return tracker, mocks

    return make_tracker_for_raise_error

@pytest.mark.parametrize(
    argnames='html, exp_exception',
    argvalues=(
        (
            '<html><div class="error">Something went wrong</div></html>',
            errors.RequestError('Something went wrong'),
        ),
        (
            '<html><div class="messagebar alert">Something went wrong</div></html>',
            errors.RequestError('Something went wrong'),
        ),
        (
            '<html><div>Something went wrong unexpectedly!</div></html>',
            RuntimeError('No error message found (dumped HTML response to {filepath})'),
        ),
        (
            '',
            errors.RequestError(
                'Zero bytes response bug encountered.\n'
                'You can try again or pray for someone to fix it.\n'
                'Or gain fame and glory by fixing it yourself!'
            ),
        ),
    ),
    ids=lambda v: repr(v),
)
def test_MtvTracker_raise_error(html, exp_exception, make_tracker_for_raise_error):
    tracker, mocks = make_tracker_for_raise_error()
    doc = utils.html.parse(html)
    if exp_exception:
        exp_msg = f'HEADS UP: {exp_exception}'.format(filepath='HEADS UP.html')
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_msg)}$'):
            tracker._raise_error(doc, msg_prefix='HEADS UP')

        if isinstance(exp_exception, RuntimeError):
            assert mocks.mock_calls == [call.dump(doc, 'HEADS UP.html')]
        else:
            assert mocks.mock_calls == []

    else:
        return_value = tracker._raise_error(doc, msg_prefix='HEADS UP')
        assert return_value is None
        assert mocks.mock_calls == []


@pytest.fixture
def make_tracker_for_raise_error_dupes(make_tracker, mocker):
    def make_tracker_for_raise_error_dupes():
        tracker = make_tracker()
        mocks = Mock()
        return tracker, mocks

    return make_tracker_for_raise_error_dupes

@pytest.mark.parametrize(
    argnames='html, exp_exception',
    argvalues=(
        (
            (
                '<div id="messagebar">Hedgehogs found</div>'
                '<table id="not_torrent_table">'
                '<tr class="torrent"><td class="torrent"><a href="torrent.php?123">file1.mkv</a></td></tr>'
                '</table>'
            ),
            None,
        ),
        (
            (
                '<div id="messagebar">Duplicates found</div>'
                '<table id="torrent_table">'
                '</table>'
            ),
            None,
        ),
        (
            (
                '<div id="messagebar">Duplicates found</div>'
                '<table id="not_torrent_table">'
                '<tr class="torrent"><td class="torrent"><a href="torrent.php?123">file1.mkv</a></td></tr>'
                '</table>'
            ),
            None,
        ),
        (
            (
                '<div id="messagebar">Duplicates found</div>'
                '<table id="torrent_table">'
                '<tr class="torrent"><td class="torrent"><a href="torrent.php?123">file1.mkv</a></td></tr>'
                '<tr class="torrent"><td class="torrent"><a href="torrent.php?234">file2.mkv</a></td></tr>'
                '<tr class="torrent"><td class="torrent"><a href="torrent.php?234">file3.mkv</a></td></tr>'
                '</table>'
            ),
            errors.FoundDupeError(['file1.mkv', 'file2.mkv', 'file3.mkv']),
        ),
    ),
)
def test_MtvTracker_raise_error_dupes(html, exp_exception, make_tracker_for_raise_error_dupes):
    tracker, mocks = make_tracker_for_raise_error_dupes()
    doc = utils.html.parse(html)
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            tracker._raise_error_dupes(doc)
    else:
        return_value = tracker._raise_error_dupes(doc)
        assert return_value is None
