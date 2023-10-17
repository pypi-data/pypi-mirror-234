import re
import types
from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies import constants, errors, utils
from upsies.utils.predbs import SceneQuery, base


def make_TestDb(default_config=None, **kwargs):
    default_config_ = default_config

    class TestDb(base.PredbApiBase):
        name = 'scn'
        label = 'SCN'
        default_config = default_config_ or {}
        _search = AsyncMock()
        _release_files = AsyncMock()

    return TestDb(**kwargs)


def test_config_property():
    db = make_TestDb()
    assert db.config == {}
    db = make_TestDb(default_config={'foo': 1, 'bar': 2})
    assert db.config == {'foo': 1, 'bar': 2}
    db = make_TestDb(default_config={'foo': 1, 'bar': 2}, config={'bar': 99})
    assert db.config == {'foo': 1, 'bar': 99}


@pytest.mark.parametrize(
    argnames='query, only_existing_releases, results, exp_mock_calls, exp_return_value_from',
    argvalues=(
        pytest.param(
            'path/to/My.Release.2000.Bluray, x264-ASDF',
            'mock_only_existing_releases',
            ['Foo', 'Bar', 'Baz'],
            [
                call._search(SceneQuery('My', 'Release', '2000', 'BluRay', 'x264', group='ASDF')),
                call._postprocess_search_results(
                    ['Foo', 'Bar', 'Baz'],
                    SceneQuery('My', 'Release', '2000', 'BluRay', 'x264', group='ASDF'),
                    'mock_only_existing_releases',
                ),
            ],
            '_postprocess_search_results',
            id='[non-season-pack] Query is path',
        ),
        pytest.param(
            {
                'type': utils.release.ReleaseType.movie,
                'title': 'My Release',
                'source': 'BluRay',
                'group': 'ASDF',
            },
            'mock_only_existing_releases',
            ['Foo', 'Bar', 'Baz'],
            [
                call._search(SceneQuery('My', 'Release', 'BluRay', group='ASDF')),
                call._postprocess_search_results(
                    ['Foo', 'Bar', 'Baz'],
                    SceneQuery('My', 'Release', 'BluRay', group='ASDF'),
                    'mock_only_existing_releases',
                ),
            ],
            '_postprocess_search_results',
            id='[non-season-pack] Query is mapping',
        ),
        pytest.param(
            utils.predbs.SceneQuery('My', 'Release', 'BluRay', group='ASDF'),
            'mock_only_existing_releases',
            ['Foo', 'Bar', 'Baz'],
            [
                call._search(SceneQuery('My', 'Release', 'BluRay', group='ASDF')),
                call._postprocess_search_results(
                    ['Foo', 'Bar', 'Baz'],
                    SceneQuery('My', 'Release', 'BluRay', group='ASDF'),
                    'mock_only_existing_releases',
                ),
            ],
            '_postprocess_search_results',
            id='[non-season-pack] Query is SceneQuery',
        ),
        pytest.param(
            'path/to/My.Release.S03.Bluray.x264-ASDF',
            'mock_only_existing_releases',
            [],
            [
                call._search(SceneQuery('My', 'Release', 'BluRay', 'x264', group='ASDF', episodes={'3': []})),
                call._search_for_episodes(
                    'path/to/My.Release.S03.Bluray.x264-ASDF',
                    'mock_only_existing_releases',
                ),
            ],
            '_search_for_episodes',
            id='[season-pack] Query is path',
        ),
        pytest.param(
            {
                'type': utils.release.ReleaseType.movie,
                'title': 'My Release',
                'episodes': {'3': []},
                'source': 'BluRay',
                'group': 'ASDF',
            },
            'mock_only_existing_releases',
            [],
            [
                call._search(SceneQuery('My', 'Release', 'BluRay', group='ASDF', episodes={'3': []})),
                call._postprocess_search_results(
                    [],
                    SceneQuery('My', 'Release', 'BluRay', group='ASDF', episodes={'3': []}),
                    'mock_only_existing_releases',
                ),
            ],
            '_postprocess_search_results',
            id='[season-pack] Query is mapping',
        ),
    ),
)
@pytest.mark.asyncio
async def test_search(query, results, only_existing_releases, exp_mock_calls, exp_return_value_from, mocker):
    db = make_TestDb()
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(db, '_search', AsyncMock(return_value=results)),
        '_search',
    )
    mocks.attach_mock(
        mocker.patch.object(db, '_postprocess_search_results'),
        '_postprocess_search_results',
    )
    mocks.attach_mock(
        mocker.patch.object(db, '_search_for_episodes'),
        '_search_for_episodes',
    )

    return_value = await db.search(
        query=query,
        only_existing_releases=only_existing_releases,
    )
    exp_return_value = getattr(mocks, exp_return_value_from).return_value
    assert return_value is exp_return_value
    assert mocks.mock_calls == exp_mock_calls

@pytest.mark.asyncio
async def test_search_is_not_supported(mocker):
    db = make_TestDb()
    db._search.side_effect = NotImplementedError()
    with pytest.raises(errors.RequestError, match=fr'{re.escape(str(db.name))} does not support searching'):
        await db.search('foo')


@pytest.mark.asyncio
async def test_search_for_episodes(mocker):
    db = make_TestDb()
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(db, '_generate_episode_queries', Mock(return_value=iter((
            'mock episode_query 1',
            'mock episode_query 2',
            'mock episode_query 3',
        )))),
        '_generate_episode_queries',
    )
    mocks.attach_mock(
        mocker.patch.object(db, 'search', side_effect=(
            ['results 1 for episode_query 1', 'results 2 for episode_query 1', 'results 1 for episode_query 1'],
            [],
            ['results 1 for episode_query 3', 'results 2 for episode_query 3'],
        )),
        'search',
    )
    mock_only_existing_releases = 'mock only_existing_releases'
    path = 'path/to/season.pack'

    return_value = await db._search_for_episodes(path, mock_only_existing_releases)
    assert return_value == [
        'results 1 for episode_query 1', 'results 2 for episode_query 1', 'results 1 for episode_query 1',
        'results 1 for episode_query 3', 'results 2 for episode_query 3',
    ]
    assert mocks.mock_calls == [
        call._generate_episode_queries(path),
        call.search('mock episode_query 1', mock_only_existing_releases),
        call.search('mock episode_query 2', mock_only_existing_releases),
        call.search('mock episode_query 3', mock_only_existing_releases),
    ]

@pytest.mark.parametrize(
    argnames='path, exp_queries_generated',
    argvalues=(
        ('path/to/Foo.2000.x264-ASDF', False),
        ('path/to/Foo.S03E06.x264-ASDF.mkv', False),
        ('path/to/Foo.S03.x264-MiXED/', True),
    ),
)
def test_generate_episode_queries(path, exp_queries_generated, mocker):
    db = make_TestDb()

    file_list = [
        'Foo.S01E01.x264-ASDF.mkv',
        'arf-foo-s01e02.mkv',
        'Foo.S01E03.x264-FDSA.mkv',
    ]

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.fs.file_list', Mock(return_value=file_list)),
        'file_list',
    )

    return_value = db._generate_episode_queries(path)
    assert isinstance(return_value, types.GeneratorType)

    if not exp_queries_generated:
        assert list(return_value) == []
    else:
        assert list(return_value) == [
            utils.predbs.SceneQuery.from_string(file_list[0]),
            utils.predbs.SceneQuery.from_string(file_list[2]),
        ]
        assert mocks.mock_calls == [
            call.file_list(path, extensions=constants.VIDEO_FILE_EXTENSIONS),
        ]


@pytest.mark.asyncio
async def test_release_files_is_not_supported(mocker):
    db = make_TestDb()
    db._release_files.side_effect = NotImplementedError()
    with pytest.raises(errors.RequestError, match=fr'{re.escape(str(db.name))} does not provide file information'):
        await db.release_files('foo')
