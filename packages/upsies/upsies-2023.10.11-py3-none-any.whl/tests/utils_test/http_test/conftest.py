import contextlib
import ssl
from unittest.mock import Mock

import pytest
import trustme


@pytest.fixture
def mock_cache(mocker):
    parent = Mock(
        cache_file=Mock(return_value='path/to/cache.file'),
        from_cache=Mock(return_value=None),
        to_cache=Mock(return_value=None),
    )
    mocker.patch('upsies.utils.http._cache_file', parent.cache_file)
    mocker.patch('upsies.utils.http._from_cache', parent.from_cache)
    mocker.patch('upsies.utils.http._to_cache', parent.to_cache)
    yield parent


@pytest.fixture
def custom_host(ssl_context):
    @contextlib.contextmanager
    def custom_host(httpserver, host, tls=False, port=None):
        httpserver.stop()
        original_host, original_port = httpserver.host, httpserver.port
        httpserver.host = host
        if port:
            httpserver.port = port
        if tls:
            httpserver.ssl_context = ssl_context

        httpserver.start()

        try:
            yield
        finally:
            httpserver.stop()
            httpserver.host, httpserver.port = original_host, original_port
            httpserver.ssl_context = None
            httpserver.start()

    return custom_host

@pytest.fixture(scope='module')
def ssl_context(ca):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_cert = ca.issue_cert('localhost')
    localhost_cert.configure_cert(context)
    return context

@pytest.fixture(scope='module')
def ca():
    return trustme.CA()
