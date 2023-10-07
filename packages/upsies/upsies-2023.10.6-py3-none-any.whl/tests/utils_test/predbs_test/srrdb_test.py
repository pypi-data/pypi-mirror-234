import json
import re
import types
from unittest.mock import AsyncMock, Mock, call, patch

import pytest

from upsies import errors, utils
from upsies.utils.predbs import srrdb


@pytest.fixture
def api():
    return srrdb.SrrdbApi()


def test_name():
    assert srrdb.SrrdbApi.name == 'srrdb'


def test_label():
    assert srrdb.SrrdbApi.label == 'srrDB'


def test_default_config():
    assert srrdb.SrrdbApi.default_config == {}


def test__make_release_name_from_path(mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch('upsies.utils.fs.basename'), 'basename')
    mocks.attach_mock(mocker.patch('upsies.utils.fs.strip_extension'), 'strip_extension')
    release_name = srrdb.SrrdbApi._make_release_name_from_path('path/to/My.Release.Name')
    assert release_name is mocks.strip_extension.return_value
    assert mocks.mock_calls == [
        call.basename('path/to/My.Release.Name'),
        call.strip_extension(mocks.basename.return_value),
    ]


@pytest.mark.parametrize(
    argnames=(
        'query,'
        'exact_movie_or_episode_results, exact_season_results,'
        'page_size, max_skip, pages, exp_results, exp_mock_calls'
    ),
    argvalues=(
        pytest.param(
            types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group'),
            ['The.Exact.Release.Name.720p.BluRay.x264-ASDF'],
            ['The.Exact.Release.Name.S03.720p.BluRay.x264-ASDF'],
            -1, -2, [['pages', 'are'], ['irrelevant', 'here']],
            ['The.Exact.Release.Name.720p.BluRay.x264-ASDF'],
            [
                call._search_for_exact_movie_or_episode(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
            ],
            id='Exact movie or episode name is found',
        ),
        pytest.param(
            types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group'),
            [],
            ['The.Exact.Release.Name.S03.720p.BluRay.x264-ASDF'],
            -1, -2, [['pages', 'are'], ['irrelevant', 'here']],
            ['The.Exact.Release.Name.S03.720p.BluRay.x264-ASDF'],
            [
                call._search_for_exact_movie_or_episode(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
                call._search_for_exact_season(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
            ],
            id='Exact season name is found',
        ),
        pytest.param(
            types.SimpleNamespace(release_info=None, keywords='mock keywords', group='mock group'),
            [],
            [],
            3, 99, [['a', 'b', 'c'], []],
            ['a', 'b', 'c'],
            [
                call._get_keywords_path('mock keywords', 'mock group', 0),
                call._request_search_page('keywords/for/page/1'),
                call._get_keywords_path('mock keywords', 'mock group', 3),
                call._request_search_page('keywords/for/page/2'),
            ],
            id='Query does not provide release_info',
        ),
        pytest.param(
            types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group'),
            [],
            [],
            3, 99, [['a', 'b', 'c'], []],
            ['a', 'b', 'c'],
            [
                call._search_for_exact_movie_or_episode(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
                call._search_for_exact_season(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
                call._get_keywords_path('mock keywords', 'mock group', 0),
                call._request_search_page('keywords/for/page/1'),
                call._get_keywords_path('mock keywords', 'mock group', 3),
                call._request_search_page('keywords/for/page/2'),
            ],
            id='No exact search results found',
        ),
        pytest.param(
            types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group'),
            [],
            [],
            4, 99, [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i']],
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
            [
                call._search_for_exact_movie_or_episode(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
                call._search_for_exact_season(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
                call._get_keywords_path('mock keywords', 'mock group', 0),
                call._request_search_page('keywords/for/page/1'),
                call._get_keywords_path('mock keywords', 'mock group', 4),
                call._request_search_page('keywords/for/page/2'),
                call._get_keywords_path('mock keywords', 'mock group', 8),
                call._request_search_page('keywords/for/page/3'),
            ],
            id='Stop requesting pages if page is not full',
        ),
        pytest.param(
            types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group'),
            [],
            [],
            2, 10, [['a', 'b'], ['c', 'd'], ['e', 'f'], ['g', 'h'], ['i', 'j'], ['k', 'l'], ['m', 'n'], ['o', 'p']],
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'],
            [
                call._search_for_exact_movie_or_episode(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
                call._search_for_exact_season(
                    types.SimpleNamespace(release_info='mock release info', keywords='mock keywords', group='mock group')
                ),
                call._get_keywords_path('mock keywords', 'mock group', 0),
                call._request_search_page('keywords/for/page/1'),
                call._get_keywords_path('mock keywords', 'mock group', 2),
                call._request_search_page('keywords/for/page/2'),
                call._get_keywords_path('mock keywords', 'mock group', 4),
                call._request_search_page('keywords/for/page/3'),
                call._get_keywords_path('mock keywords', 'mock group', 6),
                call._request_search_page('keywords/for/page/4'),
                call._get_keywords_path('mock keywords', 'mock group', 8),
                call._request_search_page('keywords/for/page/5'),
                call._get_keywords_path('mock keywords', 'mock group', 10),
                call._request_search_page('keywords/for/page/6'),
            ],
            id='Stop requesting pages if maximum page requests are reached',
        ),
    ),
)
@pytest.mark.asyncio
async def test__search(query,
                       exact_movie_or_episode_results, exact_season_results,
                       page_size, max_skip, pages,
                       exp_results, exp_mock_calls, api, mocker):
    mocker.patch.object(api, '_page_size', page_size)
    mocker.patch.object(api, '_max_skip', max_skip)

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(api, '_search_for_exact_movie_or_episode', return_value=exact_movie_or_episode_results),
        '_search_for_exact_movie_or_episode',
    )
    mocks.attach_mock(
        mocker.patch.object(api, '_search_for_exact_season', return_value=exact_season_results),
        '_search_for_exact_season',
    )
    mocks.attach_mock(
        mocker.patch.object(api, '_get_keywords_path', side_effect=(
            f'keywords/for/page/{i + 1}'
            for i in range(len(pages))
        )),
        '_get_keywords_path',
    )
    mocks.attach_mock(
        mocker.patch.object(api, '_request_search_page', side_effect=pages),
        '_request_search_page',
    )

    response = await api._search(query)
    assert list(response) == exp_results
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames='release_type, exp_search_requested',
    argvalues=(
        (utils.release.ReleaseType.movie, True),
        (utils.release.ReleaseType.episode, True),
        (utils.release.ReleaseType.season, False),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize(
    argnames='release_path, results, exp_results, exp_mock_calls',
    argvalues=(
        pytest.param(
            'path/to/Exact.Release.Name.720p.BluRay.x264-ASDF.mkv',
            ('Exact.Release.Name.720p.BluRay.x264-ASDF',),
            ('Exact.Release.Name.720p.BluRay.x264-ASDF',),
            [
                call._make_release_name_from_path('path/to/Exact.Release.Name.720p.BluRay.x264-ASDF.mkv'),
                call._search_for_exact_release_name('RELEASE_NAME:path/to/Exact.Release.Name.720p.BluRay.x264-ASDF.mkv'),
            ],
            id='Results are found',
        ),
        pytest.param(
            'path/to/Exact.Release.Name.720p.BluRay.x264-ASDF.mkv',
            (),
            (),
            [
                call._make_release_name_from_path('path/to/Exact.Release.Name.720p.BluRay.x264-ASDF.mkv'),
                call._search_for_exact_release_name('RELEASE_NAME:path/to/Exact.Release.Name.720p.BluRay.x264-ASDF.mkv'),
            ],
            id='No results are found',
        ),
    ),
)
@pytest.mark.asyncio
async def test__search_for_exact_movie_or_episode(release_path, release_type, results,
                                                  exp_search_requested, exp_results, exp_mock_calls,
                                                  api, mocker):
    release_name = f'RELEASE_NAME:{release_path}'
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(api, '_make_release_name_from_path', return_value=release_name),
        '_make_release_name_from_path',
    )
    mocks.attach_mock(
        mocker.patch.object(api, '_search_for_exact_release_name', return_value=results),
        '_search_for_exact_release_name',
    )

    query = Mock(release_info=Mock(
        __getitem__=Mock(return_value=release_type),
        path=release_path,
    ))

    results = await api._search_for_exact_movie_or_episode(query)

    if exp_search_requested:
        assert results == exp_results
        assert mocks.mock_calls == exp_mock_calls
    else:
        assert results is None
        assert mocks.mock_calls == []


@pytest.mark.parametrize(
    argnames='is_dir, release_type, exp_search_requested',
    argvalues=(
        pytest.param(False, utils.release.ReleaseType.movie, False, id='nondirectory, movie'),
        pytest.param(False, utils.release.ReleaseType.episode, False, id='nondirectory, episode'),
        pytest.param(False, utils.release.ReleaseType.season, False, id='nondirectory, season'),
        pytest.param(True, utils.release.ReleaseType.movie, False, id='directory, movie'),
        pytest.param(True, utils.release.ReleaseType.episode, False, id='directory, episode'),
        pytest.param(True, utils.release.ReleaseType.season, True, id='directory, season'),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize(
    argnames='release_path, found_videos, results, exp_results, exp_mock_calls',
    argvalues=(
        pytest.param(
            'path/to/Exact.Release.Name.S03.720p.BluRay.x264-ASDF',
            (
                'path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv',
                'path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv',
                'path/to/Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF.mkv',
            ),
            {
                'path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv': ['Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF'],
                'path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv': ['Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF'],
                'path/to/Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF.mkv': ['Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF'],
            },
            [
                'Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF',
                'Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF',
                'Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF',
            ],
            [
                call.find_videos('path/to/Exact.Release.Name.S03.720p.BluRay.x264-ASDF'),
                call._make_release_name_from_path('path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv'),
                call._search_for_exact_release_name('RELEASE_NAME:path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv'),
                call._make_release_name_from_path('path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv'),
                call._search_for_exact_release_name('RELEASE_NAME:path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv'),
                call._make_release_name_from_path('path/to/Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF.mkv'),
                call._search_for_exact_release_name('RELEASE_NAME:path/to/Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF.mkv'),
            ],
            id='Results are found',
        ),
        pytest.param(
            'path/to/Exact.Release.Name.S03.720p.BluRay.x264-ASDF',
            (
                'path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv',
                'path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv',
                'path/to/Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF.mkv',
            ),
            {
                'path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv': [],
                'path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv': [],
                'path/to/Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF.mkv': [],
            },
            [],
            [
                call.find_videos('path/to/Exact.Release.Name.S03.720p.BluRay.x264-ASDF'),
                call._make_release_name_from_path('path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv'),
                call._search_for_exact_release_name('RELEASE_NAME:path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv'),
            ],
            id='No results are found',
        ),
        pytest.param(
            'path/to/Exact.Release.Name.S03.720p.BluRay.x264-ASDF',
            (
                'path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv',
                'path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv',
                'path/to/Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF.mkv',
            ),
            {
                'path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv': ['Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF'],
                'path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv': [],
                'path/to/Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF.mkv': ['Exact.Release.Name.S03E03.720p.BluRay.x264-ASDF'],
            },
            [],
            [
                call.find_videos('path/to/Exact.Release.Name.S03.720p.BluRay.x264-ASDF'),
                call._make_release_name_from_path('path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv'),
                call._search_for_exact_release_name('RELEASE_NAME:path/to/Exact.Release.Name.S03E01.720p.BluRay.x264-ASDF.mkv'),
                call._make_release_name_from_path('path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv'),
                call._search_for_exact_release_name('RELEASE_NAME:path/to/Exact.Release.Name.S03E02.720p.BluRay.x264-ASDF.mkv'),
            ],
            id='No results are found for one episode',
        ),
    ),
)
@pytest.mark.asyncio
async def test__search_for_exact_season(release_path, release_type, is_dir, found_videos, results,
                                        exp_search_requested, exp_results, exp_mock_calls,
                                        api, mocker):
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.find_videos', return_value=found_videos),
        'find_videos',
    )
    mocks.attach_mock(
        mocker.patch.object(api, '_make_release_name_from_path', side_effect=(
            f'RELEASE_NAME:{found_video}'
            for found_video in found_videos
        )),
        '_make_release_name_from_path',
    )
    mocks.attach_mock(
        mocker.patch.object(api, '_search_for_exact_release_name', side_effect=results.values()),
        '_search_for_exact_release_name',
    )

    query = Mock(release_info=Mock(
        __getitem__=Mock(return_value=release_type),
        path=release_path,
    ))

    with patch('os.path.isdir', return_value=is_dir):
        results = await api._search_for_exact_season(query)

    if exp_search_requested:
        assert results == exp_results
        assert mocks.mock_calls == exp_mock_calls
    else:
        assert results is None
        assert mocks.mock_calls == []


@pytest.mark.parametrize(
    argnames='release_name, response, exp_results, exp_mock_calls',
    argvalues=(
        pytest.param(
            'Exact.Release.Name.720p.BluRay.x264-ASDF',
            {'results': [{'release': 'Exact.Release.Name.720p.BluRay.x264-ASDF'}]},
            ('Exact.Release.Name.720p.BluRay.x264-ASDF',),
            [
                call.get(f'{srrdb.SrrdbApi._search_url}/r:Exact.Release.Name.720p.BluRay.x264-ASDF', cache=True),
            ],
            id='Exact release name is found',
        ),
        pytest.param(
            'Exact.Release.Name.720p.BluRay.x264-ASDF',
            {'foo': 'bar'},
            (),
            [
                call.get(f'{srrdb.SrrdbApi._search_url}/r:Exact.Release.Name.720p.BluRay.x264-ASDF', cache=True),
            ],
            id='Nothing is found',
        ),
        pytest.param(
            'Exact.Release.Name.720p.BluRay.x264-ASDF',
            errors.RequestError('What a stupid request.'),
            (),
            [
                call.get(f'{srrdb.SrrdbApi._search_url}/r:Exact.Release.Name.720p.BluRay.x264-ASDF', cache=True),
            ],
            id='Request raises error',
        ),
    ),
)
@pytest.mark.asyncio
async def test__search_for_exact_release_name(release_name, response, exp_results, exp_mock_calls, api, mocker):

    mocks = Mock()
    if isinstance(response, Exception):
        get_mock = AsyncMock(side_effect=response)
    else:
        get_mock = AsyncMock(return_value=Mock(json=Mock(return_value=response)))
    mocks.attach_mock(
        mocker.patch('upsies.utils.http.get', get_mock),
        'get',
    )
    results = await api._search_for_exact_release_name(release_name)
    assert results == exp_results
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.asyncio
async def test_request_page(api, mocker):
    http_mock = mocker.patch('upsies.utils.http', Mock(
        get=AsyncMock(return_value=Mock(json=Mock(return_value={
            'results': [
                {'release': 'Foo-ASDF'},
                {'release': 'Bar-ASDF'},
                {'release': 'Baz-FDSA'},
            ],
        }))),
    ))

    response = await api._request_search_page('mock/keywords/path')
    assert list(response) == [
        'Foo-ASDF',
        'Bar-ASDF',
        'Baz-FDSA',
    ]

    assert http_mock.get.call_args_list == [
        call(
            f'{api._search_url}/mock/keywords/path',
            cache=True,
        ),
    ]


@pytest.mark.parametrize('skip', (0, 100))
@pytest.mark.parametrize('group', (None, '', 'ASDF'), ids=lambda v: str(v))
@pytest.mark.parametrize(
    argnames='keywords, exp_return_value',
    argvalues=(
        (['10,000', 'BC'], "10/000/bc"),
        (["Lot's", 'of', 'Riff-Raff'], 'lot/s/of/riff/raff'),
    ),
)
def test_get_keywords_path(keywords, group, skip, exp_return_value, api, mocker):
    return_value = api._get_keywords_path(keywords, group=group, skip=skip)

    if group:
        exp_return_value += f'/group:{group.lower()}'
    exp_return_value += '/order:date-desc'
    exp_return_value += f'/skipr:{skip}.{api._page_size}'
    assert return_value == exp_return_value


class MockResponse(str):
    def json(self):
        return json.loads(self)

@pytest.mark.parametrize(
    argnames='release_name, response, exp_result',
    argvalues=(
        pytest.param(
            'Foo.2000-ASDF',
            MockResponse(
                '{'
                '  "name":"Foo.2000-ASDF",'
                '  "archived-files": ['
                '    {"name":"Foo.mkv", "size": 123,"crc": "abc"},'
                '    {"name":"bar.txt", "size": 234,"crc": "def"},'
                '    {"name":"baz.nfo", "size": 456,"crc": "efg"}'
                '  ]'
                '}'
            ),
            {
                'bar.txt': {'release_name': 'Foo.2000-ASDF', 'file_name': 'bar.txt', 'size': 234, 'crc': 'def'},
                'baz.nfo': {'release_name': 'Foo.2000-ASDF', 'file_name': 'baz.nfo', 'size': 456, 'crc': 'efg'},
                'Foo.mkv': {'release_name': 'Foo.2000-ASDF', 'file_name': 'Foo.mkv', 'size': 123, 'crc': 'abc'},
            },
            id='All information is available',
        ),

        pytest.param(
            'Foo.2000-ASDF',
            MockResponse('[]'),
            {},
            id='Response is empty list',
        ),

        pytest.param(
            'Mock.Release.Name',
            MockResponse(''),
            {},
            id='Response is empty string',
        ),
    ),
)
@pytest.mark.asyncio
async def test_release_files(release_name, response, exp_result, api, mocker):
    http_get_mock = mocker.patch('upsies.utils.http.get', return_value=response)

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await api._release_files(release_name)
    else:
        return_value = await api._release_files(release_name)
        assert return_value == exp_result

    assert http_get_mock.call_args_list == [call(
        f'{api._details_url}/{release_name}',
        cache=True,
    )]
