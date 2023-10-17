import asyncio
import base64
import io
import itertools
import os
import pathlib
import re
import ssl
import time
from unittest.mock import AsyncMock, Mock, call

import httpx
import pytest
from pytest_httpserver.httpserver import Response
from werkzeug.datastructures import Headers, ImmutableMultiDict

from upsies import __project_name__, __version__, errors
from upsies.utils import http, semantic_hash


class RequestHandler:
    def __init__(self):
        self.requests_seen = []

    def __call__(self, request):
        # `request` is a Request object from werkzeug
        # https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#werkzeug.wrappers.BaseRequest
        try:
            return self.handle(request)
        except Exception as e:
            # pytest-httpserver doesn't show the traceback if we call
            # raise_for_status() on the response.
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)
            raise

    def handle(self, request):
        raise NotImplementedError()


@pytest.mark.parametrize(
    argnames=('cache_directory, default_cache_directory, exp_cache_directory'),
    argvalues=(
        ('my/custom/path', 'the/default/path', 'my/custom/path'),
        ('', 'the/default/path', 'the/default/path'),
        (None, 'the/default/path', 'the/default/path'),
    ),
)
@pytest.mark.asyncio
async def test_get_cache_directory(cache_directory, default_cache_directory, exp_cache_directory, mocker):
    mocker.patch('upsies.constants.DEFAULT_CACHE_DIRECTORY', default_cache_directory)
    mocker.patch('upsies.utils.http.cache_directory', cache_directory)
    assert http._get_cache_directory() == exp_cache_directory


@pytest.mark.asyncio
async def test_get(mocker):
    request_mock = mocker.patch('upsies.utils.http._request', new_callable=AsyncMock)
    kwargs = {
        'url': Mock(),
        'headers': Mock(),
        'params': Mock(),
        'auth': Mock(),
        'cache': Mock(),
        'max_cache_age': Mock(),
        'user_agent': Mock(),
        'follow_redirects': Mock(),
        'verify': Mock(),
        'timeout': Mock(),
        'cookies': Mock(),
        'debug_file': Mock(),
    }
    result = await http.get(**kwargs)
    assert request_mock.call_args_list == [
        call(**{**{'method': 'GET'}, **kwargs})
    ]
    assert result is request_mock.return_value


@pytest.mark.asyncio
async def test_post(mocker):
    request_mock = mocker.patch('upsies.utils.http._request', new_callable=AsyncMock)
    kwargs = {
        'url': Mock(),
        'headers': Mock(),
        'data': Mock(),
        'files': Mock(),
        'auth': Mock(),
        'cache': Mock(),
        'max_cache_age': Mock(),
        'user_agent': Mock(),
        'follow_redirects': Mock(),
        'verify': Mock(),
        'timeout': Mock(),
        'cookies': Mock(),
        'debug_file': Mock(),
    }
    result = await http.post(**kwargs)
    assert request_mock.call_args_list == [
        call(**{**{'method': 'POST'}, **kwargs})
    ]
    assert result is request_mock.return_value


def test_Response_is_string():
    r = http.Response('foo', b'foo')
    assert isinstance(r, str)
    assert r == 'foo'

def test_Response_bytes():
    r = http.Response('föö', bytes('föö', 'utf-8'))
    assert r.bytes == bytes('föö', 'utf-8')
    assert str(r.bytes, 'utf-8') == 'föö'

def test_Response_headers():
    r = http.Response('foo', b'foo')
    assert r.headers == {}
    r = http.Response('foo', b'foo', headers={'a': '1', 'b': '2'})
    assert r.headers == {'a': '1', 'b': '2'}

def test_Response_status_code():
    r = http.Response('foo', b'foo')
    assert r.status_code is None
    r = http.Response('foo', b'foo', status_code=304)
    assert r.status_code == 304

def test_Response_json():
    r = http.Response('{"this":"that"}', b'{"this":"that"}')
    assert r.json() == {'this': 'that'}
    r = http.Response('{"this":"that"', b'{"this":"that"')
    assert r == '{"this":"that"'
    with pytest.raises(errors.RequestError, match=r'^Malformed JSON: {"this":"that": '):
        r.json()

@pytest.mark.parametrize(
    argnames='kwargs, exp_kwargs',
    argvalues=(
        ({'text': 'föö', 'bytes': bytes('föö', 'utf-8')}, {'text': 'föö', 'bytes': bytes('föö', 'utf-8')}),
        ({'text': 'foo', 'bytes': b'foo', 'headers': {'bar': 'baz'}}, {'text': 'foo', 'bytes': b'foo', 'headers': {'bar': 'baz'}}),
        ({'text': 'foo', 'bytes': b'foo', 'headers': {}}, {'text': 'foo', 'bytes': b'foo'}),
        ({'text': 'foo', 'bytes': b'foo', 'headers': None}, {'text': 'foo', 'bytes': b'foo'}),
        ({'text': 'foo', 'bytes': b'foo', 'status_code': 123}, {'text': 'foo', 'bytes': b'foo', 'status_code': 123}),
        ({'text': 'foo', 'bytes': b'foo', 'status_code': 0}, {'text': 'foo', 'bytes': b'foo', 'status_code': 0}),
        ({'text': 'foo', 'bytes': b'foo', 'status_code': None}, {'text': 'foo', 'bytes': b'foo'}),
    ),
    ids=lambda v: str(v),
)
def test_Response_repr(kwargs, exp_kwargs):
    r = http.Response(**kwargs)
    exp_kwargs_string = ', '.join(f'{k}={v!r}' for k, v in exp_kwargs.items())
    assert repr(r) == f'Response({exp_kwargs_string})'


@pytest.mark.asyncio
async def test_request_with_invalid_url(mock_cache):
    # The error message keeps changing, so we just make sure RequestError is raised
    url = r'http:///baz'
    with pytest.raises(errors.RequestError, match=(rf"^{re.escape(url)}: ")) as excinfo:
        await http._request('GET', url)
    assert excinfo.value.status_code is None


@pytest.mark.asyncio
async def test_request_with_invalid_method(mock_cache):
    with pytest.raises(ValueError, match=r'^Invalid method: hello$'):
        await http._request('hello', 'asdf')


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_with_caching_disabled(method, mock_cache, httpserver):
    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_data(
        'have this',
    )
    for i in range(3):
        result = await http._request(
            method=method,
            url=httpserver.url_for('/foo'),
            cache=False,
        )
        assert result == 'have this'
        assert isinstance(result, http.Response)
        assert mock_cache.mock_calls == []


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_gets_cached_result(method, mock_cache):
    mock_cache.from_cache.return_value = 'cached result'
    url = 'http://localhost:12345/foo'
    for i in range(1, 4):
        result = await http._request(method=method, url=url, cache=True)
        assert result == 'cached result'
        assert result is mock_cache.from_cache.return_value
        assert mock_cache.mock_calls == [
            call.cache_file(method, url, {}),
            call.from_cache(mock_cache.cache_file.return_value, max_age=float('inf')),
        ] * i


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_caches_result(method, mock_cache, httpserver):
    mock_cache.from_cache.return_value = None
    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_data(
        'have this',
    )
    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        cache=True,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)
    assert mock_cache.mock_calls == [
        call.cache_file(method, httpserver.url_for('/foo'), {}),
        call.from_cache(mock_cache.cache_file.return_value, max_age=float('inf')),
        call.cache_file(method, httpserver.url_for('/foo'), {}),
        call.to_cache(mock_cache.cache_file.return_value, b'have this'),
    ]


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_sends_default_headers(method, mock_cache, httpserver):
    class Handler(RequestHandler):
        def handle(self, request):
            for k, v in http._default_headers.items():
                assert request.headers[k] == v
            return Response('have this')

    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        Handler(),
    )
    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        user_agent=True,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_sends_custom_headers(method, mock_cache, httpserver, mocker):
    mocker.patch.dict(http._default_headers, {'a': '1', 'b': '2'})
    custom_headers = {'foo': 'bar', 'b': '20'}
    combined_headers = {'a': '1', 'b': '20', 'foo': 'bar'}

    class Handler(RequestHandler):
        def handle(self, request):
            for k, v in combined_headers.items():
                assert request.headers[k] == v
            return Response('have this')

    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        Handler(),
    )
    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        headers=custom_headers,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_sends_params(method, mock_cache, httpserver):
    query = {'foo': '1', 'bar': 'baz'}
    httpserver.expect_request(
        uri='/foo',
        method=method,
        query_string=query,
    ).respond_with_data(
        'have this',
    )
    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        params=query,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)


@pytest.mark.parametrize(
    argnames='data, files, exp_data, exp_form',
    argvalues=(
        (b'raw bytes', {}, b'raw bytes', ImmutableMultiDict([])),
        ('string', {}, b'string', ImmutableMultiDict([])),
        (b'raw bytes', {'file_input': {'file': io.BytesIO(b'foo')},}, b'raw bytes', ImmutableMultiDict([])),
        ('string', {'file_input': {'file': io.BytesIO(b'foo')}}, b'string', ImmutableMultiDict([])),
        (
            {'foo': 1, 'bar': None, 'baz': [1, 2, 3],},
            {},
            b'foo=1&baz=1&baz=2&baz=3',
            ImmutableMultiDict([
                ('foo', '1'),
                ('baz', '1'), ('baz', '2'), ('baz', '3'),
            ]),
        ),
        (
            {'foo': 1, 'bar': None, 'baz': [1, 2, 3],},
            {
                'file_input': {
                    'file': io.BytesIO(b'foo'),
                },
            },
            # Encoded multipart/form-data is impossible to predict
            None,
            ImmutableMultiDict([
                ('foo', '1'),
                ('baz', '1'), ('baz', '2'), ('baz', '3'),
                ('file_input', 'foo'),
            ]),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_sends_data(method, data, files, exp_data, exp_form, mock_cache, httpserver):
    class Handler(RequestHandler):
        def handle(self, request):
            if exp_data is not None:
                assert request.data == exp_data
            if exp_form is not None:
                assert request.form == exp_form
            return Response('have this')

    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        Handler()
    )
    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        data=data,
        files=files,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)


@pytest.mark.asyncio
async def test_request_sends_files(mock_cache, httpserver, mocker):
    files = {
        'foo': 'path/to/foo.jpg',
        'bar': ('path/to/bar', 'image/png'),
    }
    mocker.patch('upsies.utils.http._open_files', return_value={
        'foo': ('foo.jpg', io.BytesIO(b'foo image')),
        'bar': ('bar', io.BytesIO(b'bar image'), 'image/png')
    })

    class Handler(RequestHandler):
        def handle(self, request):
            assert request.content_type.startswith('multipart/form-data')
            data = request.data.decode('utf-8')
            assert re.search(
                (
                    r'^'
                    r'--[0-9a-f]{32}\r\n'
                    r'Content-Disposition: form-data; name="foo"; filename="foo.jpg"\r\n'
                    r'Content-Type: image/jpeg\r\n'
                    r'\r\n'
                    r'foo image\r\n'
                    r'--[0-9a-f]{32}\r\n'
                    r'Content-Disposition: form-data; name="bar"; filename="bar"\r\n'
                    r'Content-Type: image/png\r\n'
                    r'\r\n'
                    r'bar image\r\n'
                    r'--[0-9a-f]{32}--\r\n'
                    r'$'
                ),
                data,
            )
            return Response('have this')

    httpserver.expect_request(
        uri='/foo',
        method='POST',
    ).respond_with_handler(
        Handler(),
    )
    result = await http._request(
        method='POST',
        url=httpserver.url_for('/foo'),
        files=files,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_sends_auth(method, mock_cache, httpserver):
    auth = ('AzureDiamond', 'hunter2')
    auth_str = ':'.join(auth)
    auth_encoded = base64.b64encode(auth_str.encode('utf-8')).decode()

    class Handler(RequestHandler):
        def handle(self, request):
            assert request.headers['Authorization'] == f'Basic {auth_encoded}'
            return Response('have this')

    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        Handler(),
    )
    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        auth=auth,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_does_not_send_auth(method, mock_cache, httpserver):
    class Handler(RequestHandler):
        def handle(self, request):
            assert request.headers.get('Authorization') is None
            return Response('have this')

    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        Handler(),
    )
    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        auth=None,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)


@pytest.mark.parametrize(
    argnames='user_agent, exp_user_agent',
    argvalues=(
        (True, f'{__project_name__}/{__version__}'),
        (False, None),
        ('Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)',
         'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'),
    ),
)
@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_sends_user_agent(method, user_agent, exp_user_agent, mock_cache, httpserver):
    class Handler(RequestHandler):
        def handle(self, request):
            assert request.headers.get('User-Agent') == exp_user_agent
            return Response('have this')

    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        Handler(),
    )
    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        user_agent=user_agent,
    )
    assert result == 'have this'
    assert isinstance(result, http.Response)


@pytest.mark.parametrize(
    argnames='timeout, response_delay, exp_exception',
    argvalues=(
        (1, 0.5, None),
        (1, 1.5, errors.RequestError('timeout')),
    ),
)
@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_with_timeout_argument(method, timeout, response_delay, exp_exception, mock_cache, httpserver):
    class Handler(RequestHandler):
        def handle(self, request):
            import time
            time.sleep(response_delay)
            return Response('have this')

    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        Handler(),
    )
    request_url = httpserver.url_for('/foo')
    if exp_exception:
        with pytest.raises(errors.RequestError, match=rf'^{request_url}: Timeout$'):
            await http._request(
                method=method,
                url=request_url,
                timeout=timeout,
            )
    else:
        result = await http._request(
            method=method,
            url=request_url,
            timeout=timeout,
        )
        assert result == 'have this'
        assert isinstance(result, http.Response)


@pytest.mark.parametrize('follow_redirects', (True, False))
@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.parametrize('status_code', (301, 302, 303, 307, 308))
@pytest.mark.asyncio
async def test_request_with_follow_redirects(status_code, method, follow_redirects, mock_cache, httpserver):
    class Handler(RequestHandler):
        def handle(self, request):
            if request.path == '/foo':
                return Response(
                    response='not redirected',
                    status=status_code,
                    headers={'Location': httpserver.url_for('/bar')},
                )
            else:
                return Response('redirected')

    handler = Handler()
    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        handler,
    )
    httpserver.expect_request(
        uri='/bar',
        method='GET' if status_code in (301, 302, 303) else method,
    ).respond_with_handler(
        handler,
    )

    result = await http._request(
        method=method,
        url=httpserver.url_for('/foo'),
        follow_redirects=follow_redirects,
    )
    if follow_redirects:
        assert result == 'redirected'
    else:
        assert result == 'not redirected'
    assert isinstance(result, http.Response)


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_preserves_session_cookies_between_requests(method, mock_cache, httpserver):
    class Handler(RequestHandler):
        expected_cookies = ImmutableMultiDict({})

        def handle(self, request):
            print('SERVER: Got cookies:', request.cookies)
            assert request.cookies == self.expected_cookies

            bar = int(request.cookies.get('bar', 0))
            self.expected_cookies = ImmutableMultiDict({'bar': str(bar + 1), 'baz': 'asdf'})

            if not request.cookies:
                # First request
                headers = Headers((
                    ('Set-Cookie', f'bar={bar + 1}'),
                    ('Set-Cookie', 'baz=asdf'),
                ))
            else:
                headers = Headers((
                    ('Set-Cookie', f'bar={bar + 1}'),
                ))
            print('SERVER: Sending cookies:', headers)

            return Response(response=f'bar is currently {bar}', headers=headers)

    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        Handler(),
    )

    try:
        for i in range(3):
            response = await http._request(
                method=method,
                url=httpserver.url_for('/foo'),
                cache=False,
            )
            assert response == f'bar is currently {i}'
    finally:
        http.clear_session_cookies()


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_uses_separate_cookie_jar_per_domain(method, mock_cache, httpserver):
    class Handler(RequestHandler):
        def handle(self, request):
            if getattr(self, 'set_cookie'):
                domain = request.url.split('/')[2]
                headers = {'Set-Cookie': f'cookie_domain={domain}'}
            else:
                headers = {}
            return Response(
                response='current cookies: ' + ', '.join(f'{k}={v}' for k, v in request.cookies.items()),
                headers=headers,
            )

    handler = Handler()
    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        handler,
    )

    hosts = ('foo.localhost', 'bar.localhost', 'baz.localhost')

    try:
        # Fill cookie jar with some subdomain-specific cookies
        handler.set_cookie = True
        for host in hosts:
            httpserver.host = host
            response = await http._request(
                method=method,
                url=httpserver.url_for('/foo'),
                cache=False,
            )
            assert response == 'current cookies: '

        # Check if we get the same cookies back for each subdomain
        handler.set_cookie = False
        for host in hosts:
            httpserver.host = host
            response = await http._request(
                method=method,
                url=httpserver.url_for('/foo'),
                cache=False,
            )
            assert response == f'current cookies: cookie_domain={host}:{httpserver.port}'

    finally:
        http.clear_session_cookies()


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_with_custom_cookies(method, mock_cache, httpserver):
    custom_cookies = {'foo': 'bar'}
    server_cookies = {'server': 'cookie'}

    class Handler(RequestHandler):
        def handle(self, request):
            if getattr(self, 'cookies_already_set', False):
                headers = {}
                exp_request_cookies = ImmutableMultiDict({**custom_cookies, **server_cookies})
            else:
                headers = {'Set-Cookie': ', '.join(f'{k}={v}' for k, v in server_cookies.items())}
                self.cookies_already_set = True
                exp_request_cookies = ImmutableMultiDict(custom_cookies)

            assert request.cookies == exp_request_cookies

            return Response(
                response='got cookies: ' + ', '.join(f'{k}={v}' for k, v in request.cookies.items()),
                headers=headers,
            )

    handler = Handler()
    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        handler,
    )

    try:
        response = await http._request(
            method=method,
            url=httpserver.url_for('/foo'),
            cache=False,
            cookies=custom_cookies,
        )
        assert response == 'got cookies: ' + ', '.join(f'{k}={v}' for k, v in custom_cookies.items())

        response = await http._request(
            method=method,
            url=httpserver.url_for('/foo'),
            cache=False,
            cookies=custom_cookies,
        )
        assert response == 'got cookies: ' + ', '.join(f'{k}={v}' for k, v in {**custom_cookies, **server_cookies}.items())

    finally:
        http.clear_session_cookies()


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_with_cookies_file(method, mock_cache, httpserver, custom_host, tmp_path):
    cookies_filepath = str(tmp_path / 'path' / 'to' / 'my.cookies')

    class Handler(RequestHandler):
        def handle(self, request):
            assert request.cookies == ImmutableMultiDict(self.expected_cookies)

            domain = request.url.split('/')[2].split(':')[0]
            if getattr(self, 'set_cookie'):
                headers = {'Set-Cookie': f'your_domain={domain}; max-age=500000'}
            else:
                headers = {}
            domain = request.url.split('/')[2]
            return Response(
                response=f'got cookies on {domain}: ' + ', '.join(f'{k}={v}' for k, v in request.cookies.items()),
                headers=headers,
            )

    handler = Handler()
    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        handler,
    )

    # We are only interested in cookies sourced from file
    http.clear_session_cookies()

    # Set cookies
    for domain in ('foo.localhost', 'bar.localhost'):
        with custom_host(httpserver, domain):
            handler.set_cookie = True
            handler.expected_cookies = {}
            response = await http._request(
                method=method,
                url=httpserver.url_for('/foo'),
                cache=False,
                cookies=cookies_filepath + f'.{domain}',
            )
            assert response == f'got cookies on {domain}:{httpserver.port}: '

    # We are only interested in cookies sourced from file
    http.clear_session_cookies()

    # Check if we only send the cookies for each domain
    for domain in ('foo.localhost', 'bar.localhost'):
        with custom_host(httpserver, domain):
            handler.set_cookie = False
            handler.expected_cookies = {'your_domain': domain}
            response = await http._request(
                method=method,
                url=httpserver.url_for('/foo'),
                cache=False,
                cookies=cookies_filepath + f'.{domain}',
            )
            assert response == f'got cookies on {domain}:{httpserver.port}: your_domain={domain}'


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_with_unsavable_cookies_file(method, mock_cache, httpserver, tmp_path, mocker):
    class Handler(RequestHandler):
        def handle(self, request):
            headers = {'Set-Cookie': 'your_cookie=foo; max-age=500000'}
            return Response(
                response='setting cookie',
                headers=headers,
            )

    handler = Handler()
    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_handler(
        handler,
    )

    httpserver.host = 'foo.localhost'
    cookies_filepath = tmp_path / 'unwritable' / 'my.cookies'
    cookies_filepath.parent.mkdir()

    def mkdir(path):
        pathlib.Path(path).chmod(0o000)

    mocker.patch('upsies.utils.fs.mkdir', Mock(side_effect=mkdir))

    try:
        with pytest.raises(errors.RequestError, match=rf'^Failed to write {cookies_filepath}: Permission denied$'):
            await http._request(
                method=method,
                url=httpserver.url_for('/foo'),
                cache=False,
                cookies=cookies_filepath,
            )
    finally:
        cookies_filepath.parent.chmod(0o600)


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_with_unloadable_cookies_file(method, mock_cache, tmp_path):
    cookies_filepath = tmp_path / 'my.cookies'
    cookies_filepath.write_text('mock cookies')
    cookies_filepath.chmod(0o000)
    try:
        with pytest.raises(errors.RequestError, match=rf'^Failed to read {cookies_filepath}: Permission denied$'):
            await http._request(
                method=method,
                url='http://localhost:123/foo',
                cache=False,
                cookies=cookies_filepath,
            )
    finally:
        cookies_filepath.chmod(0o600)


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_with_unsupported_cookies_type(method, mock_cache):
    with pytest.raises(RuntimeError, match=r'^Unsupported cookies type: \(1, 2, 3\)$'):
        await http._request(
            method=method,
            url='http://localhost:123/foo',
            cache=False,
            cookies=(1, 2, 3),
        )


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_catches_HTTP_error_status(method, mock_cache, httpserver):
    url = httpserver.url_for('/foo')
    httpserver.expect_request(
        uri='/foo',
        method=method,
    ).respond_with_data(
        '<html>  Dave is not   here\n</html> ',
        status=404,
        headers={'foo': 'bar'},
    )
    with pytest.raises(errors.RequestError, match=rf'^{url}: Dave is not here$') as excinfo:
        await http._request(method=method, url=url)
    assert excinfo.value.status_code == 404
    assert excinfo.value.headers['foo'] == 'bar'
    assert excinfo.value.url == url
    assert excinfo.value.text == '<html>  Dave is not   here\n</html> '


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_catches_NetworkError(method, mock_cache):
    url = 'http://localhost:12345/foo/bar/baz'
    with pytest.raises(errors.RequestError, match=rf'^{url}: All connection attempts failed$') as excinfo:
        await http._request(method=method, url=url)
    assert excinfo.value.status_code is None
    assert excinfo.value.headers == {}


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_catches_TimeoutException(method, mock_cache, mocker):
    exc = httpx.TimeoutException(
        message='Some error',
        request='mock request',
    )
    mocker.patch('httpx.AsyncClient.send', AsyncMock(side_effect=exc))
    url = 'http://localhost:12345/foo/bar/baz'
    with pytest.raises(errors.RequestError, match=rf'^{url}: Timeout$') as excinfo:
        await http._request(method=method, url=url)
    assert excinfo.value.status_code is None
    assert excinfo.value.headers == {}


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.asyncio
async def test_request_catches_HTTPError(method, mock_cache, mocker):
    exc = httpx.HTTPError('Some error')
    mocker.patch('httpx.AsyncClient.send', AsyncMock(side_effect=exc))
    url = 'http://localhost:12345/foo/bar/baz'
    with pytest.raises(errors.RequestError, match=rf'^{url}: Some error$') as excinfo:
        await http._request(method=method, url=url)
    assert excinfo.value.status_code is None
    assert excinfo.value.headers == {}


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.parametrize(
    argnames='exception, exception_attrs, exp_exception',
    argvalues=(
        (
            ssl.SSLError('Default message'),
            {'verify_message': 'Verification failed'},
            errors.RequestError('TLS: Verification failed'),
        ),
        (
            ssl.SSLError('Default message'),
            {'reason': 'Verification failed'},
            errors.RequestError('TLS: Verification failed'),
        ),
        (
            ssl.SSLError('Default message'),
            {'strerror': 'Verification failed'},
            errors.RequestError('TLS: Verification failed'),
        ),
        (
            ssl.SSLError('Default message'),
            {},
            errors.RequestError("TLS: ('Default message',)"),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_request_catches_SSLError(exception, exception_attrs, exp_exception, method, mock_cache, mocker):
    # It seems to be impossible to normally specify `verify_message` and it is
    # not documented how to instantiate SSLCertVerificationError anywhere.
    for attr, value in exception_attrs.items():
        setattr(exception, attr, value)
    mocker.patch('httpx.AsyncClient.send', AsyncMock(side_effect=exception))
    url = 'https://localhost:12345/foo/bar/baz'
    with pytest.raises(type(exp_exception), match=rf'^{url}: {re.escape(str(exp_exception))}$') as excinfo:
        await http._request(method=method, url=url)
    assert excinfo.value.status_code is None
    assert excinfo.value.headers == {}


@pytest.mark.parametrize('debug_file', ('', None, 'path/to/debug.file'))
@pytest.mark.asyncio
async def test_request_with_debug_file_argument(debug_file, mocker):
    mock_request = Mock(
        headers={'User-Agent': 'asdf'},
        aread=AsyncMock(),
    )
    mocker.patch('httpx.AsyncClient.build_request', Mock(return_value=mock_request))
    mock_response = Mock()
    mocker.patch('httpx.AsyncClient.send', AsyncMock(return_value=mock_response))

    dump_req_res_mock = mocker.patch('upsies.utils.http._dump_req_res', AsyncMock())
    await http._request('GET', 'http://foo.bar', debug_file=debug_file)
    if debug_file:
        assert dump_req_res_mock.call_args_list == [
            call(mock_request, f'{debug_file}.request'),
            call(mock_response, f'{debug_file}.response'),
        ]
    else:
        assert dump_req_res_mock.call_args_list == []


@pytest.mark.asyncio
async def test_get_performs_only_one_identical_request_at_the_same_time(httpserver, mocker, tmp_path):
    mocker.patch.object(http, 'cache_directory', str(tmp_path))

    class Handler(RequestHandler):
        def handle(self, request):
            self.requests_seen.append(request.full_path)
            return Response(request.full_path)

    handler = Handler()
    for path in ('/a', '/b', '/c', '/d'):
        httpserver.expect_request(
            uri=path,
            method='GET',
        ).respond_with_handler(
            handler,
        )

    coros = tuple(itertools.chain(
        (http.get(httpserver.url_for('/a'), cache=True) for _ in range(10)),
        (http.get(httpserver.url_for('/b'), cache=True) for _ in range(5)),
        (http.get(httpserver.url_for('/c'), params={'foo': '1'}, cache=True) for _ in range(3)),
        (http.get(httpserver.url_for('/c'), params={'foo': '2'}, cache=True) for _ in range(6)),
    ))
    results = await asyncio.gather(*coros)

    assert set(results) == set(
        ['/a?'] * 10
        + ['/b?'] * 5
        + ['/c?foo=1'] * 3
        + ['/c?foo=2'] * 6
    )
    assert set(handler.requests_seen) == {
        '/a?',
        '/b?',
        '/c?foo=1',
        '/c?foo=2',
    }

@pytest.mark.asyncio
async def test_post_request_performs_only_one_identical_request_at_the_same_time(httpserver, mocker, tmp_path):
    mocker.patch.object(http, 'cache_directory', str(tmp_path))

    class Handler(RequestHandler):
        def handle(self, request):
            s = f'{request.full_path} data:{request.data.decode("utf-8")}'
            self.requests_seen.append(s)
            return Response(s)

    handler = Handler()
    for path in ('/a', '/b', '/c', '/d'):
        httpserver.expect_request(
            uri=path,
            method='POST',
        ).respond_with_handler(
            handler,
        )

    coros = tuple(itertools.chain(
        (http.post(httpserver.url_for('/a'), cache=True) for _ in range(10)),
        (http.post(httpserver.url_for('/b'), cache=True) for _ in range(5)),
        (http.post(httpserver.url_for('/c'), data={'foo': '1'}, cache=True) for _ in range(3)),
        (http.post(httpserver.url_for('/c'), data={'foo': '2'}, cache=True) for _ in range(6)),
    ))
    results = await asyncio.gather(*coros)

    assert set(results) == set(
        ["/a? data:"] * 10
        + ['/b? data:'] * 5
        + ['/c? data:foo=1'] * 3
        + ['/c? data:foo=2'] * 6
    )
    assert len(results) == 10 + 5 + 3 + 6
    assert set(handler.requests_seen) == {
        '/a? data:',
        '/b? data:',
        '/c? data:foo=1',
        '/c? data:foo=2',
    }
    assert len(handler.requests_seen) == 4


@pytest.mark.asyncio
async def test_download_forwards_args_and_kwargs_to_get(mocker, tmp_path):
    mocker.patch('upsies.utils.http.get', AsyncMock(
        return_value=Mock(bytes=b'downloaded data'),
    ))
    filepath = tmp_path / 'downloaded'
    return_value = await http.download('mock url', filepath, 'foo', bar='baz')
    assert return_value == filepath
    assert http.get.call_args_list == [call('mock url', 'foo', bar='baz', cache=False)]

@pytest.mark.parametrize(
    argnames='cache, file_exists, exp_download',
    argvalues=(
        (False, False, True),
        (False, True, True),
        (True, False, True),
        (True, True, False),
    ),
)
@pytest.mark.asyncio
async def test_download_with_cache_argument(cache, file_exists, exp_download, mocker, tmp_path):
    mocker.patch('upsies.utils.http.get', AsyncMock(
        return_value=Mock(bytes=b'downloaded data'),
    ))
    filepath = tmp_path / 'downloaded'
    if file_exists:
        filepath.write_bytes(b'downloaded data')
    return_value = await http.download('mock url', filepath, cache=cache)
    assert return_value == filepath
    if exp_download:
        assert http.get.call_args_list == [call('mock url', cache=False)]
    else:
        assert http.get.call_args_list == []

@pytest.mark.asyncio
async def test_download_writes_filepath(mocker, tmp_path):
    mocker.patch('upsies.utils.http.get', AsyncMock(
        side_effect=errors.RequestError('no response'),
    ))
    filepath = tmp_path / 'downloaded'
    with pytest.raises(errors.RequestError, match=r'^no response$'):
        await http.download('mock url', filepath)
    assert not filepath.exists()

@pytest.mark.asyncio
async def test_download_does_not_write_filepath_if_request_fails(mocker, tmp_path):
    mocker.patch('upsies.utils.http.get', AsyncMock(
        return_value=Mock(bytes=b'downloaded data'),
    ))
    filepath = tmp_path / 'downloaded'
    return_value = await http.download('mock url', filepath)
    assert return_value == filepath
    assert filepath.read_bytes() == b'downloaded data'

@pytest.mark.asyncio
async def test_download_catches_OSError_when_opening_filepath(mocker, tmp_path):
    mocker.patch('upsies.utils.http.get', AsyncMock(
        return_value=Mock(bytes=b'downloaded data'),
    ))
    filepath = tmp_path / 'downloaded'
    mocker.patch('builtins.open', side_effect=OSError('Ouch'))
    with pytest.raises(errors.RequestError, match=rf'^Unable to write {filepath}: Ouch$'):
        await http.download('mock url', filepath)


@pytest.mark.parametrize('domain', (None, 'example.org'))
def test_clear_session_cookies(domain, mocker):
    mocker.patch.object(http, '_session_cookies', {
        'foo.net': {'cookie1': 'bar', 'cookie2': 'baz'},
        'example.org': {'cookie2': 'this', 'cookie3': 'that'},
    })
    http.clear_session_cookies(domain)
    if domain:
        assert http._session_cookies == {
            'foo.net': {'cookie1': 'bar', 'cookie2': 'baz'},
            'example.org': {},
        }
    else:
        assert http._session_cookies == {
            'foo.net': {},
            'example.org': {},
        }


def test_open_files_opens_files(mocker):
    mocker.patch(
        'upsies.utils.http._get_file_object',
        side_effect=(
            io.BytesIO(b'foo image'),
            io.BytesIO(b'bar text1'),
            io.BytesIO(b'bar text2'),
            io.BytesIO(b'bar text3'),
            io.BytesIO(b'bar text4'),
        ),
    )
    opened_files = http._open_files({
        'a': 'path/to/foo.jpg',
        'b': {'file': 'path/to/bar.txt'},
        'c': {'file': 'path/to/bar.txt', 'filename': 'baz'},
        'd': {'file': 'path/to/bar.txt', 'mimetype': 'text/plain'},
        'e': {'file': 'path/to/bar.txt', 'mimetype': None},
        'f': io.BytesIO(b'in-memory data1'),
        'g': {'file': io.BytesIO(b'in-memory data2'), 'mimetype': 'weird/type'},
        'h': {'file': io.BytesIO(b'in-memory data3'), 'mimetype': 'weird/type', 'filename': 'kangaroo'},
        'i': {'file': io.BytesIO(b'in-memory data4'), 'mimetype': None, 'filename': 'kangaroo'},
        'j': {'file': io.BytesIO(b'in-memory data5'), 'filename': 'kangaroo'},
    })
    assert tuple(opened_files) == ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')

    def assert_opened(fieldname, filename, data, mimetype=False):
        assert opened_files[fieldname][0] == filename
        assert opened_files[fieldname][1].read() == data
        if mimetype is False:
            assert len(opened_files[fieldname]) == 2
        else:
            assert opened_files[fieldname][2] == mimetype
            assert len(opened_files[fieldname]) == 3

    assert_opened('a', 'foo.jpg', b'foo image')
    assert_opened('b', 'bar.txt', b'bar text1')
    assert_opened('c', 'baz', b'bar text2')
    assert_opened('d', 'bar.txt', b'bar text3', 'text/plain')
    assert_opened('e', 'bar.txt', b'bar text4', None)
    assert_opened('f', None, b'in-memory data1')
    assert_opened('g', None, b'in-memory data2', 'weird/type')
    assert_opened('h', 'kangaroo', b'in-memory data3', 'weird/type')
    assert_opened('i', 'kangaroo', b'in-memory data4', None)
    assert_opened('j', 'kangaroo', b'in-memory data5')

def test_open_files_catches_invalid_file_value(mocker):
    mocker.patch('upsies.utils.http._get_file_object', return_value='mock file object')
    with pytest.raises(RuntimeError, match=r'^Invalid "file" value in fileinfo: \[1, 2, 3\]$'):
        http._open_files({
            'document': {'file': [1, 2, 3]},
        })

def test_open_files_catches_invalid_fileinfo(mocker):
    mocker.patch('upsies.utils.http._get_file_object', return_value='mock file object')
    with pytest.raises(RuntimeError, match=r'^Invalid fileinfo: \[1, 2, 3\]$'):
        http._open_files({
            'document': [1, 2, 3],
        })

def test_open_files_raises_exception_from_get_file_object(mocker):
    mocker.patch('upsies.utils.http._get_file_object',
                 side_effect=errors.RequestError('bad io'))
    with pytest.raises(errors.RequestError, match=r'^bad io$'):
        http._open_files({
            'image': 'path/to/foo.jpg',
            'document': ('path/to/bar', 'text/plain'),
        })


def test_get_file_object_catches_OSError():
    filepath = 'path/to/foo'
    with pytest.raises(errors.RequestError, match=rf'^{filepath}: No such file or directory$'):
        http._get_file_object(filepath)

def test_get_file_object_returns_fileobj(tmp_path):
    filepath = tmp_path / 'foo'
    filepath.write_bytes(b'hello')
    fileobj = http._get_file_object(filepath)
    assert fileobj.read() == b'hello'


@pytest.mark.parametrize('method', ('GET', 'POST'))
def test_cache_file_without_params(method, mocker):
    def sanitize_filename(filename):
        return filename.replace('a', '#')

    mocker.patch('upsies.utils.fs.sanitize_filename', side_effect=sanitize_filename)
    mocker.patch.object(http, '_get_cache_directory', return_value='/tmp/foo')
    url = 'http://localhost:123/foo/bar'
    exp_cache_file = f'/tmp/foo/{method.upper()}.http://loc#lhost:123/foo/b#r'
    assert http._cache_file(method, url) == exp_cache_file

@pytest.mark.parametrize('method', ('GET', 'POST'))
def test_cache_file_with_params(method, mocker):
    def sanitize_filename(filename):
        return filename.replace('a', '#')

    mocker.patch('upsies.utils.fs.sanitize_filename', side_effect=sanitize_filename)
    mocker.patch.object(http, '_get_cache_directory', return_value='/tmp/foo')
    url = 'http://localhost:123'
    params = {'foo': 'a b c', 'bar': 12}
    exp_cache_file = f'/tmp/foo/{method.upper()}.http://loc#lhost:123?foo=#+b+c&b#r=12'
    assert http._cache_file(method, url, params=params) == exp_cache_file

@pytest.mark.parametrize('method', ('GET', 'POST'))
def test_cache_file_with_very_long_params(method, mocker):
    def sanitize_filename(filename):
        return filename.replace('a', '#')

    mocker.patch('upsies.utils.fs.sanitize_filename', side_effect=sanitize_filename)
    mocker.patch.object(http, '_get_cache_directory', return_value='/tmp/foo')
    url = 'http://localhost:123'
    params = {'foo': 'a b c ' * 100, 'bar': 12}
    exp_cache_file = (
        f'/tmp/foo/{method.upper()}.http://loc#lhost:123?'
        f'[HASH:{sanitize_filename(semantic_hash(params))}]'
    )
    assert http._cache_file(method, url, params=params) == exp_cache_file


def test_from_cache_with_nonexisting_cache_file():
    assert http._from_cache('/no/such/path') is None

def test_from_cache_with_unreadable_cache_file(tmp_path):
    cache_filepath = tmp_path / 'cache_file'
    cache_filepath.write_text('mock data')
    cache_filepath.chmod(0o000)
    try:
        assert http._from_cache(cache_filepath) is None
    finally:
        cache_filepath.chmod(0o600)

@pytest.mark.parametrize(
    argnames='cached_data, max_age, cache_file_age, exp_return_value',
    argvalues=(
        ('föö', 100, 99, http.Response('föö', b'f\xc3\xb6\xc3\xb6')),
        ('föö', 100, 101, None),
    ),
)
def test_from_cache_refuses_to_read_old_cache_file(cached_data, max_age, cache_file_age, exp_return_value, tmp_path):
    cache_filepath = tmp_path / 'cache/file'
    cache_filepath.parent.mkdir(parents=True)
    cache_filepath.write_text(cached_data, encoding='UTF-8')
    mtime = time.time() - cache_file_age
    os.utime(cache_filepath, times=(mtime, mtime))
    cached_result = http._from_cache(cache_filepath, max_age=max_age)
    assert cached_result == exp_return_value


def test_to_cache_requires_bytes_object(tmp_path):
    cache_file = str(tmp_path / 'cachefile')
    with pytest.raises(TypeError, match=r"^Not a bytes object: 'foo'$"):
        http._to_cache(cache_file, 'foo')
    assert not os.path.exists(cache_file)

@pytest.mark.parametrize(
    argnames='bytes, exp_cached_bytes',
    argvalues=(
        (b'foo <script>bar</script> baz', b'foo  baz'),
        (b'foo <script with="attribute">bar</script> baz', b'foo  baz'),
        (b'a < b && b > c', b'a < b && b > c'),
        (b'\xc3\x28 <script', b'\xc3\x28 <script'),
    ),
)
def test_to_cache_removes_javascript_if_possible(bytes, exp_cached_bytes, mocker, tmp_path):
    cache_file = str(tmp_path / 'cached')
    http._to_cache(cache_file, bytes)
    assert open(cache_file, 'rb').read() == exp_cached_bytes

def test_to_cache_cannot_create_cache_directory(mocker):
    mocker.patch('builtins.open')
    mkdir_mock = mocker.patch('upsies.utils.fs.mkdir', side_effect=OSError('No'))
    with pytest.raises(RuntimeError, match=r'^Unable to write cache file mock/path: No$'):
        http._to_cache('mock/path', b'data')
    assert mkdir_mock.call_args_list == [call('mock')]

def test_to_cache_cannot_write_cache_file(mocker):
    open_mock = mocker.patch('builtins.open')
    mkdir_mock = mocker.patch('upsies.utils.fs.mkdir')
    filehandle = open_mock.return_value.__enter__.return_value
    filehandle.write.side_effect = OSError('No')
    with pytest.raises(RuntimeError, match=r'^Unable to write cache file mock/path: No$'):
        http._to_cache('mock/path', b'data')
    assert mkdir_mock.call_args_list == [call('mock')]

def test_to_cache_writes_cache_file(mocker):
    open_mock = mocker.patch('builtins.open')
    mkdir_mock = mocker.patch('upsies.utils.fs.mkdir')
    filehandle = open_mock.return_value.__enter__.return_value
    assert http._to_cache('mock/path', b'data') is None
    assert open_mock.call_args_list == [call('mock/path', 'wb')]
    assert filehandle.write.call_args_list == [call(b'data')]
    assert mkdir_mock.call_args_list == [call('mock')]


USER_AGENT_SOURCE_URLS_MOCKED = [
    'http://get-me-some-user-agents.com',
    'http://info.org/user-agents',
    'http://thereyougo.net/have-some-user-agents.txt',
]

@pytest.mark.parametrize(
    argnames='cached_user_agent, downloaded_user_agents, exp_return_value, exp_mock_calls',
    argvalues=(
        # Get user agent from cache
        (
            'Cached (x86)', ['Downloaded (x86)'], 'Cached (x86)',
            [
                call._get_user_agent_from_cache(),
            ],
        ),
        # Get user agent from first source URL
        (
            None, ['Downloaded (x86)', None, None], 'Downloaded (x86)',
            [call._get_user_agent_from_cache()]
            + [
                call._get_user_agent_from_url(url)
                for url in USER_AGENT_SOURCE_URLS_MOCKED
            ][:1]
            + [call._cache_user_agent('Downloaded (x86)')],
        ),
        # Get user agent from second source URL
        (
            None, [None, 'Downloaded (x86)', None], 'Downloaded (x86)',
            [call._get_user_agent_from_cache()]
            + [
                call._get_user_agent_from_url(url)
                for url in USER_AGENT_SOURCE_URLS_MOCKED
            ][:2]
            + [call._cache_user_agent('Downloaded (x86)')],
        ),
        # Get user agent from DEFAULT_USER_AGENT
        (
            None, [None] * len(USER_AGENT_SOURCE_URLS_MOCKED), http.DEFAULT_USER_AGENT,
            [call._get_user_agent_from_cache()]
            + [
                call._get_user_agent_from_url(url)
                for url in USER_AGENT_SOURCE_URLS_MOCKED
            ],
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_popular_user_agent(cached_user_agent, downloaded_user_agents,
                                      exp_return_value, exp_mock_calls,
                                      mocker):
    mocker.patch('upsies.utils.http.USER_AGENT_SOURCE_URLS', USER_AGENT_SOURCE_URLS_MOCKED)
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.http._get_user_agent_from_cache', return_value=cached_user_agent),
        '_get_user_agent_from_cache',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.http._get_user_agent_from_url', side_effect=downloaded_user_agents),
        '_get_user_agent_from_url',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.http._cache_user_agent'),
        '_cache_user_agent',
    )
    return_value = await http.get_popular_user_agent()
    assert return_value == exp_return_value
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='cached_user_agent, mtime_adjustment, mode, exp_return_value',
    argvalues=(
        (None, None, None, None),
        ('Cached (x86)', 0, 0o400, 'Cached (x86)'),
        ('Cached (x86)', http.USER_AGENT_CACHE_MAX_AGE - 1, 0o400, 'Cached (x86)'),
        ('Cached (x86)', http.USER_AGENT_CACHE_MAX_AGE + 1, 0o400, None),
        ('Cached (x86)', 0, 0o300, None),
    ),
)
def test_get_user_agent_from_cache(cached_user_agent, mtime_adjustment, mode, exp_return_value, mocker, tmp_path):
    if cached_user_agent is not None:
        cache_filepath = tmp_path / 'user-agent'
        cache_filepath.write_text(cached_user_agent)
        cache_filepath.chmod(mode)
        mtime = int(time.time()) - mtime_adjustment
        os.utime(cache_filepath, (time.time(), mtime))
        mocker.patch('upsies.utils.http._get_user_agent_cache_filepath', return_value=cache_filepath)

    return_value = http._get_user_agent_from_cache()
    assert return_value == exp_return_value


@pytest.mark.parametrize(
    argnames='response, acceptable_return_values',
    argvalues=(
        (
            (
                '<td> Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:123.0) like Gecko \n  </td>'
                '<td> Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36 \n  </td>'
                '<td> Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0 \n  </td>'
                '<td> Mozilla/5.0 (Macintosh; Intel Mac OS X 13.1; rv:123.0) Gecko/20100101 Firefox/123.0 \n  </td>'
                '<td> Mozilla/5.0 (X11; Linux i686; rv:123.0) Gecko/20100101 Firefox/123.0 \n  </td>'
                '<td> Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0 \n  </td>'
                '<td> Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:123.0) Gecko/20100101 Firefox/123.0  \n </td>'
                '<td> Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0  \n </td>'
                '<td> Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0  \n </td>'
            ),
            [
                'Mozilla/5.0 (X11; Linux i686; rv:123.0) Gecko/20100101 Firefox/123.0',
                'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
                'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:123.0) Gecko/20100101 Firefox/123.0',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
                'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
            ],
        ),
        (
            errors.RequestError('404 or something'),
            [None],
        ),
        (
            '<td>no user agents to be found here</td>',
            [None],
        ),
    ),
)
@pytest.mark.asyncio
async def test_get_user_agent_from_url(response, acceptable_return_values, mocker, tmp_path):
    if isinstance(response, Exception):
        get_mock = mocker.patch('upsies.utils.http.get', side_effect=response)
    else:
        get_mock = mocker.patch('upsies.utils.http.get', return_value=response)

    url = 'http://list-of-user-agents.com'

    return_value = await http._get_user_agent_from_url(url)
    assert return_value in acceptable_return_values

    assert get_mock.call_args_list == [call(url, cache=False, user_agent=False)]


@pytest.mark.parametrize(
    argnames='user_agent, success, exp_cached_user_agent',
    argvalues=(
        ('Fresh (x86)', True, 'Fresh (x86)'),
        ('Fresh (x86)', False, None),
    ),
)
def test_cache_user_agent(user_agent, success, exp_cached_user_agent, mocker, tmp_path):
    cache_filepath = tmp_path / 'user-agent'
    try:
        if not success:
            cache_filepath.parent.chmod(0o000)
        _get_user_agent_cache_filepath_mock = mocker.patch(
            'upsies.utils.http._get_user_agent_cache_filepath',
            return_value=cache_filepath,
        )

        http._cache_user_agent(user_agent)
    finally:
        cache_filepath.parent.chmod(0o700)

    assert _get_user_agent_cache_filepath_mock.call_args_list == [call()]
    if success:
        assert cache_filepath.exists()
        assert cache_filepath.read_text() == user_agent
    else:
        assert not cache_filepath.exists()

def test_get_user_agent_cache_filepth(mocker):
    cache_directory = '/path/to/cache'
    _get_cache_directory_mock = mocker.patch('upsies.utils.http._get_cache_directory', return_value=cache_directory)
    return_value = http._get_user_agent_cache_filepath()
    assert return_value == os.path.join(cache_directory, 'user-agent')
    assert _get_cache_directory_mock.call_args_list == [call()]
