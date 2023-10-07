import os
import re
from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies.utils import release, webdbs
from upsies.utils.types import ReleaseType


def test_Query_title():
    q = webdbs.Query()
    cb = Mock()
    q.signal.register('changed', cb)

    for _ in range(3):
        assert q.title == ''
        assert q.title_normalized == ''
        assert cb.mock_calls == []

    for _ in range(3):
        q.title = 'The Title '
        assert q.title_normalized == 'the title'
        assert cb.mock_calls == [call(q)]

    for _ in range(3):
        q.title = '  The\n OTHER  Title! '
        assert q.title_normalized == 'the other title!'
        assert cb.mock_calls == [call(q), call(q)]


def test_Query_year():
    q = webdbs.Query('The Title', year='2000')
    cb = Mock()
    q.signal.register('changed', cb)
    assert q.year == '2000'
    assert cb.mock_calls == []

    for _ in range(3):
        q.year = 2001
        assert q.year == '2001'
        assert cb.mock_calls == [call(q)]

    for _ in range(3):
        q.year = 2001.5
        assert q.year == '2001'
        assert cb.mock_calls == [call(q)]

    with pytest.raises(ValueError, match=r'^Invalid year: 1000$'):
        q.year = 1000
    assert cb.mock_calls == [call(q)]
    with pytest.raises(ValueError, match=r'^Invalid year: 3000$'):
        q.year = '3000'
    assert cb.mock_calls == [call(q)]
    with pytest.raises(ValueError, match=r'^Invalid year: foo$'):
        q.year = 'foo'
    assert cb.mock_calls == [call(q)]

    q.year = ''
    assert q.year is None
    assert cb.mock_calls == [call(q), call(q)]


@pytest.mark.parametrize('typ', list(ReleaseType) + [str(t) for t in ReleaseType], ids=lambda v: repr(v))
def test_Query_valid_type(typ):
    q = webdbs.Query('The Title', type=typ)
    cb = Mock()
    q.signal.register('changed', cb)
    assert q.type is ReleaseType(typ)

    all_types = list(ReleaseType)
    if all_types.index(ReleaseType(typ)) < len(all_types) - 1:
        next_type_index = all_types.index(ReleaseType(typ)) + 1
    else:
        next_type_index = 0
    print(typ, all_types, next_type_index)
    next_type = all_types[next_type_index]

    for _ in range(3):
        q.type = next_type
        assert q.type is ReleaseType(next_type)
        assert cb.mock_calls == [call(q)]

    for _ in range(3):
        q.type = typ
        assert q.type is ReleaseType(typ)
        assert cb.mock_calls == [call(q), call(q)]

def test_Query_invalid_type():
    q = webdbs.Query('The Title')
    cb = Mock()
    q.signal.register('changed', cb)
    with pytest.raises(ValueError, match=r"^'foo' is not a valid ReleaseType$"):
        q.type = 'foo'
    assert cb.mock_calls == []


def test_Query_id():
    q = webdbs.Query('The Title', id='12345')
    cb = Mock()
    q.signal.register('changed', cb)
    assert q.id == '12345'
    assert cb.mock_calls == []

    for _ in range(3):
        q.id = 123
        assert q.id == '123'
        assert cb.mock_calls == [call(q)]

    for _ in range(3):
        q.id = 'tt12345'
        assert q.id == 'tt12345'
        assert cb.mock_calls == [call(q), call(q)]


@pytest.mark.parametrize('silent', (False, True))
def test_Query_update(silent):
    q = webdbs.Query('The Title', type=ReleaseType.series)
    cb = Mock()
    q.signal.register('changed', cb)
    assert cb.call_args_list == []

    for _ in range(3):
        q.update(webdbs.Query('The Title', type=ReleaseType.movie), silent=silent)
        assert str(q) == 'The Title type:movie'
        assert cb.call_args_list == [] if silent else [call(q)]

    for _ in range(3):
        q.update(webdbs.Query('The Title', type=ReleaseType.season), silent=silent)
        assert str(q) == 'The Title type:season'
        assert cb.call_args_list == [] if silent else [call(q), call(q)]

    for _ in range(3):
        q.update(webdbs.Query('The Other Title', type=ReleaseType.episode, year='2015'), silent=silent)
        assert str(q) == 'The Other Title type:episode year:2015'
        assert cb.call_args_list == [] if silent else [call(q), call(q), call(q)]

    for _ in range(3):
        q.update(webdbs.Query('The Title', id='123', year='2015', type=ReleaseType.episode), silent=silent)
        assert str(q) == 'id:123'
        assert cb.call_args_list == [] if silent else [call(q), call(q), call(q), call(q)]


def test_Query_copy():
    q = webdbs.Query('The Title', year='2010', type=ReleaseType.series, id='1234')
    cb = Mock()
    q.signal.register('changed', cb)
    assert cb.call_args_list == []

    assert q.copy() == webdbs.Query(
        title='The Title',
        year='2010',
        type=ReleaseType.series,
        id='1234',
    )

    assert q.copy(title='Foo') == webdbs.Query(
        title='Foo',
        year='2010',
        type=ReleaseType.series,
        id='1234',
    )

    assert q.copy(year='2020') == webdbs.Query(
        title='The Title',
        year='2020',
        type=ReleaseType.series,
        id='1234',
    )

    assert q.copy(type=ReleaseType.movie) == webdbs.Query(
        title='The Title',
        year='2010',
        type=ReleaseType.movie,
        id='1234',
    )

    assert q.copy(id='4321') == webdbs.Query(
        title='The Title',
        year='2010',
        type=ReleaseType.series,
        id='4321',
    )

    assert cb.call_args_list == []

@pytest.mark.parametrize(
    argnames=('a', 'b'),
    argvalues=(
        (webdbs.Query('The Title'), webdbs.Query('The Title')),
        (webdbs.Query('The Title'), webdbs.Query('the title')),
        (webdbs.Query('The Title'), webdbs.Query('the title ')),
        (webdbs.Query('The Title'), webdbs.Query(' the title')),
        (webdbs.Query('The Title'), webdbs.Query(' the title ')),
        (webdbs.Query('The Title'), webdbs.Query('the  title')),
        (webdbs.Query('The Title'), webdbs.Query('the  title ')),
        (webdbs.Query('The Title'), webdbs.Query(' the title')),
        (webdbs.Query('The Title', year='2000'), webdbs.Query('The Title', year='2000')),
        (webdbs.Query('The Title', type=ReleaseType.movie), webdbs.Query('The Title', type=ReleaseType.movie)),
        (webdbs.Query('The Title', type=ReleaseType.series), webdbs.Query('The Title', type=ReleaseType.series)),
        (webdbs.Query('The Title', type=ReleaseType.episode, year=2000), webdbs.Query('The Title', type=ReleaseType.episode, year=2000)),
    ),
    ids=lambda value: str(value),
)
def test_Query_equality(a, b):
    assert a == b
    assert b == a

@pytest.mark.parametrize(
    argnames=('a', 'b'),
    argvalues=(
        (webdbs.Query('The Title'), webdbs.Query('The Title 2')),
        (webdbs.Query(id=123), webdbs.Query(id=124)),
        (webdbs.Query('The Title', year='2000'), webdbs.Query('The Title', year='2001')),
        (webdbs.Query('The Title', type=ReleaseType.movie), webdbs.Query('The Title', type=ReleaseType.series)),
        (webdbs.Query('The Title', type=ReleaseType.series, year=2000), webdbs.Query('The Title', type=ReleaseType.movie, year=2000)),
        (webdbs.Query('The Title', type=ReleaseType.series, year=2000), webdbs.Query('The Title', type=ReleaseType.series, year=2001)),
        (webdbs.Query('The Title', type=ReleaseType.series, year=2000), webdbs.Query('The Title', type=ReleaseType.movie, year=2001)),
    ),
    ids=lambda value: str(value),
)
def test_Query_inequality(a, b):
    assert a != b
    assert b != a

@pytest.mark.parametrize(
    argnames=('query', 'exp_string'),
    argvalues=(
        (webdbs.Query('The Title'), 'The Title'),
        (webdbs.Query('The Title', type=ReleaseType.movie), 'The Title type:movie'),
        (webdbs.Query('The Title', type=ReleaseType.series), 'The Title type:season'),
        (webdbs.Query('The Title', type=ReleaseType.movie, year='2010'), 'The Title type:movie year:2010'),
        (webdbs.Query('The Title', id='123', year='2010', type=ReleaseType.movie), 'id:123'),
    ),
    ids=lambda value: str(value),
)
def test_Query_as_string(query, exp_string):
    assert str(query) == exp_string

@pytest.mark.parametrize(
    argnames=('string', 'exp_query'),
    argvalues=(
        ('The Title', webdbs.Query('The Title')),
        ('The Title type:movie', webdbs.Query('The Title', type=ReleaseType.movie)),
        ('The Title type:season', webdbs.Query('The Title', type=ReleaseType.season)),
        ('The Title type:episode', webdbs.Query('The Title', type=ReleaseType.episode)),
        ('The Title type:series', webdbs.Query('The Title', type=ReleaseType.series)),
        ('The Title year:2000', webdbs.Query('The Title', year='2000')),
        ('The Title year:2003', webdbs.Query('The Title', year='2003')),
        ('The Title type:movie year:2000', webdbs.Query('The Title', type=ReleaseType.movie, year='2000')),
        ('The Title type:series year:2003', webdbs.Query('The Title', type=ReleaseType.series, year='2003')),
        ('The Title type:film', webdbs.Query('The Title', type=ReleaseType.movie)),
        ('The Title type:tv', webdbs.Query('The Title', type=ReleaseType.series)),
        ('The Title type:show', webdbs.Query('The Title', type=ReleaseType.series)),
        ('The Title type:tvshow', webdbs.Query('The Title', type=ReleaseType.series)),
        ('The Title id:foo', webdbs.Query('The Title', id='foo')),
        ('id:foo', webdbs.Query(id='foo')),
        ('id:foo year:2005', webdbs.Query(id='foo', year='2005')),
    ),
    ids=lambda v: str(v),
)
def test_Query_from_string(string, exp_query):
    assert webdbs.Query.from_string(string) == exp_query

@pytest.mark.parametrize(
    argnames=('string', 'exp_query'),
    argvalues=(
        ('The Title type:foo', webdbs.Query('The Title type:foo')),
        ('The Title year:bar', webdbs.Query('The Title year:bar')),
    ),
)
def test_Query_from_string_with_unknown_keyword_value(string, exp_query):
    assert webdbs.Query.from_string(string) == exp_query


@pytest.mark.parametrize('cls', (release.ReleaseInfo, release.ReleaseName))
@pytest.mark.parametrize(
    argnames=('release', 'exp_query'),
    argvalues=(
        ('The Title', webdbs.Query('The Title', type=ReleaseType.movie)),
        ('The Title S03', webdbs.Query('The Title', type=ReleaseType.season)),
        ('The Title S03', webdbs.Query('The Title', type=ReleaseType.season)),
        ('The Title S03E04', webdbs.Query('The Title', type=ReleaseType.episode)),
        ('The Title 2000', webdbs.Query('The Title', year='2000', type=ReleaseType.movie)),
        ('The Title 2001 S03E04', webdbs.Query('The Title', year='2001', type=ReleaseType.episode)),

    ),
)
def test_Query_from_release(cls, release, exp_query):
    obj = cls(release)
    assert webdbs.Query.from_release(obj) == exp_query


@pytest.mark.parametrize(
    argnames=('path', 'exp_ReleaseInfo_call'),
    argvalues=(
        ('path/to/Release Name', call('path/to/Release Name')),
        (123, call('123')),
    ),
    ids=lambda v: repr(v),
)
def test_Query_from_path(path, exp_ReleaseInfo_call, mocker):
    ReleaseInfo_mock = mocker.patch('upsies.utils.webdbs.common.release.ReleaseInfo')
    from_release_mock = mocker.patch('upsies.utils.webdbs.common.Query.from_release')
    return_value = webdbs.Query.from_path(path)
    assert ReleaseInfo_mock.call_args_list == [exp_ReleaseInfo_call]
    assert from_release_mock.call_args_list == [call(ReleaseInfo_mock.return_value)]
    assert return_value == from_release_mock.return_value


@pytest.mark.parametrize(
    argnames=('obj', 'path_exists', 'exp_from_method', 'exp_exception'),
    argvalues=(
        (webdbs.Query('Release Name'), False, None, None),
        ('Release Name', False, 'from_string', None),
        (os.path.join('path', 'to', 'Release Name'), False, 'from_path', None),
        ('path.in.current.directory', True, 'from_path', None),
        ('path.in.current.directory', False, 'from_string', None),
        (release.ReleaseInfo('Release Name'), False, 'from_release', None),
        (release.ReleaseName('Release Name'), False, 'from_release', None),
        ([1, 2, 3], False, None, TypeError('Unsupported type: list: [1, 2, 3]')),
    ),
    ids=lambda v: repr(v),
)
def test_Query_from_any(obj, path_exists, exp_from_method, exp_exception, mocker):
    from_methods = {
        'from_string': mocker.patch('upsies.utils.webdbs.common.Query.from_string'),
        'from_release': mocker.patch('upsies.utils.webdbs.common.Query.from_release'),
        'from_path': mocker.patch('upsies.utils.webdbs.common.Query.from_path'),
    }
    mocker.patch('os.path.exists', return_value=path_exists)
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            webdbs.Query.from_any(obj)
    else:
        return_value = webdbs.Query.from_any(obj)
        if exp_from_method:
            assert from_methods[exp_from_method].call_args_list == [call(obj)]
            assert return_value is from_methods[exp_from_method].return_value
        else:
            assert return_value is obj


@pytest.mark.parametrize(
    argnames=('query', 'exp_repr'),
    argvalues=(
        (webdbs.Query('The Title'),
         "Query(title='The Title')"),
        (webdbs.Query('The Title', type=ReleaseType.movie),
         "Query(title='The Title', type=ReleaseType.movie)"),
        (webdbs.Query('The Title', year='1999'),
         "Query(title='The Title', year='1999')"),
        (webdbs.Query('The Title', type=ReleaseType.season, year='1999'),
         "Query(title='The Title', year='1999', type=ReleaseType.season)"),
        (webdbs.Query('The Title', type=ReleaseType.season, year='1999', id='123'),
         "Query(title='The Title', year='1999', type=ReleaseType.season, id='123')"),
    ),
    ids=lambda value: str(value),
)
def test_Query_as_repr(query, exp_repr):
    assert repr(query) == exp_repr


@pytest.mark.asyncio
async def test_SearchResult_with_all_info():
    info = {
        'id' : '123',
        'url' : 'http://foo.bar/123',
        'type' : ReleaseType.movie,
        'year' : '2000',
        'title' : 'Foo',
        'title_original' : 'Le Foo',
        'title_english' : 'Fucking Foo',
        'genres' : ('foo', 'some bar'),
        'cast' : ('This Guy', 'That Dude'),
        'summary' : 'I dunno.',
        'countries' : ('Antarctica',),
    }
    sr = webdbs.SearchResult(**info)
    async_attributes = (
        'cast',
        'countries',
        'directors',
        'genres',
        'summary',
        'title_english',
        'title_original',
    )
    for k, v in info.items():
        if k in async_attributes:
            assert await getattr(sr, k)() == v
        else:
            assert getattr(sr, k) == v

def test_SearchResult_with_only_mandatory_info():
    info = {
        'id' : '123',
        'url' : 'http://foo.bar/123',
        'type' : ReleaseType.series,
        'year' : '2000',
        'title' : 'Foo',
    }
    sr = webdbs.SearchResult(**info)
    for k, v in info.items():
        assert getattr(sr, k) == v

def test_SearchResult_with_lacking_mandatory_info():
    info = {
        'id' : '123',
        'url' : 'http://foo.bar/123',
        'type' : ReleaseType.season,
        'year' : '2000',
        'title' : 'Foo',
    }
    for k in info:
        info_ = info.copy()
        del info_[k]
        with pytest.raises(TypeError, match=rf'missing 1 required keyword-only argument: {k!r}'):
            webdbs.SearchResult(**info_)

def test_SearchResult_with_valid_type():
    info = {
        'id' : '123',
        'url' : 'http://foo.bar/123',
        'year' : '2000',
        'title' : 'Foo',
    }
    for type in tuple(ReleaseType) + tuple(str(t) for t in ReleaseType):
        sr = webdbs.SearchResult(type=type, **info)
        assert sr.type == ReleaseType(type)

def test_SearchResult_with_invalid_type():
    info = {
        'id' : '123',
        'url' : 'http://foo.bar/123',
        'year' : '2000',
        'title' : 'Foo',
    }
    for type in ('foo', 'bar', 'baz', None):
        with pytest.raises(ValueError, match=rf'{type!r} is not a valid ReleaseType'):
            webdbs.SearchResult(type=type, **info)

def test_SearchResult_with_invalid_attribute():
    info = {
        'id' : '123',
        'url' : 'http://foo.bar/123',
        'type' : ReleaseType.series,
        'year' : '2000',
        'title' : 'Foo',
    }
    sr = webdbs.SearchResult(**info)
    with pytest.raises(AttributeError, match=r'foo'):
        sr.foo

@pytest.mark.parametrize(
    argnames=('id', 'exp_type'),
    argvalues=(
        ('123', str),
        (123.0, float),
        (123, int),
    ),
)
def test_SearchResult_preserves_id_type(id, exp_type):
    info = {
        'id' : id,
        'type': ReleaseType.series,
        'url' : 'http://foo.bar/123',
        'year' : '2000',
        'title' : 'Foo',
    }
    result = webdbs.SearchResult(**info)
    assert result.id == id
    assert isinstance(result.id, exp_type)

@pytest.mark.parametrize(
    argnames=('countries', 'exp_countries'),
    argvalues=(
        (['US'], ('United States',)),
        (AsyncMock(return_value=['US']), ('United States',)),
    ),
)
@pytest.mark.asyncio
async def test_SearchResult_normalizes_countries(countries, exp_countries):
    info = {
        'id' : '123',
        'type': ReleaseType.series,
        'url' : 'http://foo.bar/123',
        'year' : '2000',
        'title' : 'Foo',
        'countries': countries,
    }
    result = webdbs.SearchResult(**info)
    countries = await result.countries()
    assert countries == exp_countries

def test_SearchResult_repr():
    info = {
        'id' : '123',
        'title' : 'Foo',
        'type': ReleaseType.movie,
        'url' : 'http://foo.bar/123',
        'year' : '2000',
    }
    result = webdbs.SearchResult(**info)
    exp_repr_regex = re.compile(
        r"^SearchResult\("
        r"id='123', "
        r"title='Foo', "
        r"type=ReleaseType.movie, "
        r"url='http://foo.bar/123', "
        r"year='2000', "
        r"cast=<function async_get_cast at 0x[0-9a-f]+>, "
        r"countries=<function async_get_countries at 0x[0-9a-f]+>, "
        r"directors=<function async_get_directors at 0x[0-9a-f]+>, "
        r"genres=<function async_get_genres at 0x[0-9a-f]+>, "
        r"summary=<function async_get_summary at 0x[0-9a-f]+>, "
        r"title_english=<function async_get_title_english at 0x[0-9a-f]+>, "
        r"title_original=<function async_get_title_original at 0x[0-9a-f]+>"
        r"\)$"
    )
    repr_string = repr(result)
    print(repr_string)
    print(exp_repr_regex.pattern)
    assert exp_repr_regex.search(repr_string)


def test_Person():
    assert isinstance(webdbs.Person('Foo Bar'), str)
    assert webdbs.Person('Foo Bar').url == ''
    assert webdbs.Person('Foo Bar', url='http://foo').url == 'http://foo'

@pytest.mark.parametrize(
    argnames='args, kwargs, exp_repr',
    argvalues=(
        (('Hey Ho',), {}, "Person('Hey Ho')"),
        (('Hey Ho',), {'url': 'http://localhost/hey'}, "Person('Hey Ho', url='http://localhost/hey')"),
        (('Hey Ho', 'http://localhost/hey'), {}, "Person('Hey Ho', url='http://localhost/hey')"),
    ),
)
def test_Person_repr(args, kwargs, exp_repr):
    assert repr(webdbs.Person(*args, **kwargs)), exp_repr
