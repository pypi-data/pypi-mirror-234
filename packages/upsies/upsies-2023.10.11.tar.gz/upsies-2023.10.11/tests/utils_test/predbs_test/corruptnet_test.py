from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies.utils.predbs import corruptnet


@pytest.fixture
def api():
    return corruptnet.CorruptnetApi()


def test_name():
    assert corruptnet.CorruptnetApi.name == 'corruptnet'


def test_label():
    assert corruptnet.CorruptnetApi.label == 'pre.corrupt-net.org'


def test_default_config():
    assert corruptnet.CorruptnetApi.default_config == {}


@pytest.mark.parametrize(
    argnames='keywords, group, exp_return_value',
    argvalues=(
        (['foo ', ' bar', 'b az'], None, 'foo bar b az'),
        (['foo', 'bar', 'baz'], ' NOGROUP  ', 'foo bar baz group:NOGROUP'),
        (['foo', 'bar', 'baz', '  s03E06 '], 'NOGROUP', 'foo bar baz s03E06 group:NOGROUP'),
    ),
)
def test_join_keywords(keywords, group, exp_return_value, api):
    return_value = api._join_keywords(keywords, group)
    assert return_value == exp_return_value


@pytest.mark.parametrize(
    argnames='query, results_per_page, max_pages, pages, exp_return_value, exp_mock_calls',
    argvalues=(
        pytest.param(
            Mock(keywords=['my', 'keywords'], group='MYGROUP'),
            3, 4,
            [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'], ['j', 'k', 'l'], ['m', 'n', 'o'], ['p', 'q', 'r'], []],
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'],
            [
                call._request_page(['my', 'keywords'], 'MYGROUP', 0),
                call._request_page(['my', 'keywords'], 'MYGROUP', 3),
                call._request_page(['my', 'keywords'], 'MYGROUP', 6),
                call._request_page(['my', 'keywords'], 'MYGROUP', 9),
            ],
            id='Maximum number of pages',
        ),

        pytest.param(
            Mock(keywords=['my', 'keywords'], group='MYGROUP'),
            3, 4,
            [['a', 'b', 'c'], ['d', 'e', 'f'], []],
            ['a', 'b', 'c', 'd', 'e', 'f'],
            [
                call._request_page(['my', 'keywords'], 'MYGROUP', 0),
                call._request_page(['my', 'keywords'], 'MYGROUP', 3),
                call._request_page(['my', 'keywords'], 'MYGROUP', 6),
            ],
            id='Results count divisible by page count',
        ),

        pytest.param(
            Mock(keywords=['my', 'keywords'], group='MYGROUP'),
            3, 4,
            [['a', 'b', 'c'], ['d', 'e', 'f'], ['g']],
            ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
            [
                call._request_page(['my', 'keywords'], 'MYGROUP', 0),
                call._request_page(['my', 'keywords'], 'MYGROUP', 3),
                call._request_page(['my', 'keywords'], 'MYGROUP', 6),
            ],
            id='Results count not divisible by page count',
        ),
    ),
)
@pytest.mark.asyncio
async def test_search(query, results_per_page, max_pages, pages, exp_return_value, exp_mock_calls, api, mocker):
    mocks = Mock()
    mocker.patch.object(api, '_max_pages', max_pages)
    mocker.patch.object(api, '_results_per_page', results_per_page)
    mocks.attach_mock(
        mocker.patch.object(api, '_request_page', side_effect=pages),
        '_request_page',
    )

    return_value = await api._search(query)
    assert return_value == exp_return_value
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='keywords, group, page, exp_params',
    argvalues=(
        pytest.param(
            ['my', 'keywords'], 'MYGROUP', 0,
            {'search': 'my keywords group:MYGROUP', 'ts': 0, 'pretimezone': 0, 'timezone': 0},
            id='First page',
        ),
        pytest.param(
            ['my', 'keywords'], 'MYGROUP', 123,
            {'search': 'my keywords group:MYGROUP', 'ts': 0, 'pretimezone': 0, 'timezone': 0, 'page': 123},
            id='Not first page',
        ),
    ),
)
@pytest.mark.asyncio
async def test_request_page(keywords, group, page, exp_params, api, mocker):
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.predbs.corruptnet.http.get', AsyncMock()),
        'get',
    )
    mocks.attach_mock(
        mocker.patch.object(api, '_yield_release_names', Mock()),
        '_yield_release_names',
    )

    return_value = await api._request_page(keywords, group, page)
    assert return_value == mocks._yield_release_names.return_value
    assert mocks.mock_calls == [
        call.get(api._search_url, params=exp_params, cache=True, verify=False),
        call._yield_release_names(mocks.get.return_value),
    ]


@pytest.mark.parametrize(
    argnames='response, exp_return_value',
    argvalues=(
        pytest.param(
            (
                '<tr>'
                '<td>X264</td>'
                '<td>&nbsp;This.2003.1080p.BluRay.x264-<span><font>TEHGRP</font></span></td>'
                '<td>foo</td>'
                '</tr>'
                '<tr>'
                '<td>X264</td>'
                '<td>&nbsp;That.2004.720p.DVDRip.x264-<span><font>ASDF</font></span></td>'
                '<td>foo</td>'
                '</tr>'
                '<tr>'
                '<td>X264</td>'
                '<td>&nbsp;Some.Of.These.1999.720p.WEB.x264-<span><font>ARF</font></span></td>'
                '<td>foo</td>'
                '</tr>'
            ),
            [
                'This.2003.1080p.BluRay.x264-TEHGRP',
                'That.2004.720p.DVDRip.x264-ASDF',
                'Some.Of.These.1999.720p.WEB.x264-ARF',
            ],
            id='Results found',
        ),
        pytest.param(
            (
                '<td>X264</td>'
                '<td>&nbsp;This.2003.1080p.BluRay.x264-<span><font>TEHGRP</font></span></td>'
                '<td>foo</td>'
            ),
            [],
            id='No results found: No <tr> tag',
        ),
        pytest.param(
            (
                '<tr>'
                '<p>X264</p>'
                '<div>&nbsp;This.2003.1080p.BluRay.x264-<span><font>TEHGRP</font></span></div>'
                '</tr>'
            ),
            [],
            id='No results found: No <td> tag',
        ),
    ),
)
def test_yield_release_name(response, exp_return_value, api):
    return_value = list(api._yield_release_names(response))
    assert return_value == exp_return_value


@pytest.mark.asyncio
async def test_release_files(api):
    with pytest.raises(NotImplementedError):
        await api._release_files('foo')
