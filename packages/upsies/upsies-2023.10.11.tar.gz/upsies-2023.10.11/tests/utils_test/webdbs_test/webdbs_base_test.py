import re
from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies.utils.webdbs.base import WebDbApiBase
from upsies.utils.webdbs.common import Query


def make_TestWebDbApi(default_config=None, **kwargs):
    # Avoid NameError bug (https://github.com/python/cpython/issues/87546)
    default_config_ = default_config

    class TestWebDbApi(WebDbApiBase):
        name = 'foo'
        label = 'Foo'
        default_config = default_config_ or {}
        search = AsyncMock()
        get_id_from_text = Mock(return_value=None)

        directors = AsyncMock()
        creators = AsyncMock()
        cast = AsyncMock()
        _countries = AsyncMock()
        genres = AsyncMock()
        poster_url = AsyncMock()
        rating_min = 0.0
        rating_max = 10.0
        rating = AsyncMock()
        _runtimes = AsyncMock()
        summary = AsyncMock()
        _titles_english = AsyncMock()
        _title_original = AsyncMock()
        type = AsyncMock()
        url = AsyncMock()
        year = AsyncMock()

    return TestWebDbApi(**kwargs)

@pytest.fixture
def webdb():
    return make_TestWebDbApi()


def test_name_property(webdb):
    assert webdb.name == 'foo'


def test_label_property(webdb):
    assert webdb.label == 'Foo'


def test_no_results_info_property(webdb):
    assert webdb.no_results_info == ''


def test_config_property():
    webdb = make_TestWebDbApi()
    assert webdb.config == {}
    webdb = make_TestWebDbApi(default_config={'foo': 1, 'bar': 2})
    assert webdb.config == {'foo': 1, 'bar': 2}
    webdb = make_TestWebDbApi(default_config={'foo': 1, 'bar': 2}, config={'bar': 99})
    assert webdb.config == {'foo': 1, 'bar': 99}


@pytest.mark.parametrize(
    argnames='query, found_id, exp_result',
    argvalues=(
        pytest.param(
            123,
            None,
            TypeError('Not a Query instance: 123'),
            id='Bad query object',
        ),
        pytest.param(
            Query('The Foo', type='movie', year='2000'),
            None,
            Query('The Foo', type='movie', year='2000'),
            id='No ID found in query title',
        ),
        pytest.param(
            Query('The Foo', type='movie', year='2000'),
            'abc.123',
            Query('The Foo', type='movie', year='2000', id='abc.123'),
            id='ID is found in query title',
        ),
    ),
    ids=lambda v: repr(v),
)
def test_sanitize_query(query, found_id, exp_result, webdb, mocker):
    mocker.patch.object(webdb, 'get_id_from_text', return_value=found_id)
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            webdb.sanitize_query(query)
    else:
        return_value = webdb.sanitize_query(query)
        assert return_value == exp_result
        assert webdb.get_id_from_text.call_args_list == [call(query.title)]


@pytest.mark.parametrize(
    argnames='countries, exp_countries',
    argvalues=(
        (('usa', 'Peoples Republic of China'), ('United States', 'China')),
    ),
)
@pytest.mark.asyncio
async def test_countries(countries, exp_countries, webdb, mocker):
    mocker.patch.object(webdb, '_countries', AsyncMock(return_value=countries))
    return_value = await webdb.countries('mock id')
    assert return_value == exp_countries
    assert webdb._countries.call_args_list == [call('mock id')]


@pytest.mark.parametrize(
    argnames='runtimes, exp_runtimes',
    argvalues=(
        ({'usa': '123', 'Peoples Republic of China': '456', 'default': '789'},
         {'United States': '123', 'China': '456', 'default': '789'}),
        ({'usa': '123', 'Peoples Republic of China': '456', 'default': '123'},
         {'United States': '123', 'China': '456'}),
    ),
)
@pytest.mark.asyncio
async def test_runtimes(runtimes, exp_runtimes, webdb, mocker):
    mocker.patch.object(webdb, '_runtimes', AsyncMock(return_value=runtimes))
    return_value = await webdb.runtimes('mock id')
    assert return_value == exp_runtimes
    assert webdb._runtimes.call_args_list == [call('mock id')]


@pytest.mark.asyncio
async def test_gather(webdb):
    webdb.cast.return_value = 'mock cast'
    webdb.genres.return_value = ['mock genre one', 'mock genre two']
    webdb.summary.return_value = 'mock summary'
    webdb.type.return_value = 'mock type'
    webdb.year.return_value = 'mock year'
    assert await webdb.gather('mock id', 'type', 'year', 'cast', 'genres') == {
        'cast': 'mock cast',
        'id': 'mock id',
        'genres': ['mock genre one', 'mock genre two'],
        'type': 'mock type',
        'year': 'mock year',
    }
    assert webdb.cast.call_args_list == [call('mock id')]
    assert webdb._countries.call_args_list == []
    assert webdb.summary.call_args_list == []
    assert webdb.type.call_args_list == [call('mock id')]
    assert webdb.year.call_args_list == [call('mock id')]
