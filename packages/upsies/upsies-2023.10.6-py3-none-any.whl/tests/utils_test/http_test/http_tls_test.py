import re

import pytest

from upsies import errors
from upsies.utils import http


@pytest.mark.parametrize('method', ('GET', 'POST'))
@pytest.mark.parametrize(
    argnames='use_tls, verify, exp_exception',
    argvalues=(
        (False, False, None),
        (True, False, None),
        (True, True, errors.RequestError('TLS: Unable to get local issuer certificate')),
        (True, False, None),
    ),
)
@pytest.mark.asyncio
async def test_request_with_tls(method, use_tls, verify, exp_exception, mock_cache, httpserver, custom_host):
    with custom_host(httpserver, 'localhost', tls=use_tls):
        httpserver.expect_request(
            uri='/',
            method=method,
        ).respond_with_data('Your response, my lord.')

        url = httpserver.url_for('/')
        if use_tls:
            assert url.startswith('https://')
        else:
            assert url.startswith('http://')

        coro = http._request(method=method, url=url, verify=verify)
        if exp_exception:
            with pytest.raises(type(exp_exception), match=rf'^{url}: {re.escape(str(exp_exception))}$'):
                await coro
        else:
            result = await coro
            assert result == 'Your response, my lord.'
