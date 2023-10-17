import os
import re
import time
from unittest.mock import AsyncMock, Mock, PropertyMock, call, patch

import pytest

from upsies.utils import webdbs
from upsies.utils.release import Episodes, ReleaseInfo, ReleaseName
from upsies.utils.types import ReleaseType


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_name_argument(ReleaseInfo_mock, mocker):
    rn = ReleaseName('path/to/something', name='the real something')
    assert ReleaseInfo_mock.call_args_list == [call('the real something')]
    assert rn._info is ReleaseInfo_mock.return_value


def test_release_info_attribute():
    path = 'path/to/Foo Season 1 1080p BluRay DTS-ASDF/Foo S01E02 Uncut x264.mkv'
    rn = ReleaseName(path)
    assert isinstance(rn.release_info, ReleaseInfo)
    assert rn.release_info == ReleaseInfo(path)


def test_set_release_info(mocker):
    mocker.patch('upsies.utils.video.audio_format', return_value='DTS')
    rn = ReleaseName('path/to/Foo Season 1 1080p BluRay DTS-ASDF/Foo S01E02 Uncut x264.mkv')
    assert str(rn) == 'Foo S01E02 Uncut 1080p BluRay DTS x264-ASDF'
    rn.set_release_info('path/to/Bar Season 2 720p Limited WEBDL FLAC-AsdF/Bar S02E03 x265.mkv')
    assert str(rn) == 'Bar S02E03 Limited 720p WEB-DL DTS x265-AsdF'


@patch('upsies.utils.release.ReleaseInfo', Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='path, name, translate, exp_repr',
    argvalues=(
        ('path/to/something', None, None,
         "ReleaseName('path/to/something')"),
        ('path/to/something', 'The Name', None,
         "ReleaseName('path/to/something', name='The Name')"),
        ('path/to/something', 'The Name', {'foo': 'bar'},
         "ReleaseName('path/to/something', name='The Name', translate={'foo': 'bar'})"),
        ('path/to/something', None, {'foo': 'bar'},
         "ReleaseName('path/to/something', translate={'foo': 'bar'})"),
    ),
)
def test_repr(path, name, translate, exp_repr):
    rn = ReleaseName(path=path, name=name, translate=translate)
    assert repr(rn) == exp_repr


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_str(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    with patch.object(rn, 'format') as format_mock:
        format_mock.return_value = 'Pretty Release Name'
        assert str(rn) == 'Pretty Release Name'
        format_mock.call_args_list == [call()]


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='attr',
    argvalues=tuple(ReleaseName('')),
)
def test_getitem(ReleaseInfo_mock, attr):
    ReleaseInfo_mock.return_value = {attr: 'mock value', 'type': ReleaseType.movie}
    rn = ReleaseName('path/to/something')
    if not attr.startswith('_'):
        rn[attr]
    with pytest.raises(KeyError, match=r"^'format'$"):
        rn['format']
    with pytest.raises(TypeError, match=r"^Not a string: 123$"):
        rn[123]


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_usage_as_dictionary_in_str_format(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {
        'type': ReleaseType.movie,
        'title': 'The Foo',
        'year': '1998',
        'source': 'BluRay',
        'resolution': '1080p',
        'audio_codec': 'AC3',
        'audio_channels': '5.1',
        'video_codec': 'x264',
        'group': 'ASDF',
    }
    rn = ReleaseName('path/to/something')
    fmt = '{title} ({year}) {audio_format} {video_format} {source}-{group}'
    assert fmt.format(**rn) == 'The Foo (1998) AC3 x264 BluRay-ASDF'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_path(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.path == 'path/to/something'
    rn = ReleaseName(123)
    assert rn.path == '123'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_separator(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.separator == ' '
    rn.separator = 'asdf'
    assert rn.separator == 'asdf'
    rn.separator = 123
    assert rn.separator == '123'
    rn.separator = None
    assert rn.separator == ' '


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_type_getter(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'type': ReleaseType.movie}
    assert ReleaseName('path/to/something').type is ReleaseType.movie
    ReleaseInfo_mock.return_value = {'type': ReleaseType.season}
    assert ReleaseName('path/to/something').type is ReleaseType.season
    ReleaseInfo_mock.return_value = {'type': ReleaseType.episode}
    assert ReleaseName('path/to/something').type is ReleaseType.episode
    ReleaseInfo_mock.return_value = {}
    assert ReleaseName('path/to/something').type is ReleaseType.unknown

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='value, exp_value',
    argvalues=(
        ('movie', ReleaseType.movie),
        ('season', ReleaseType.season),
        ('episode', ReleaseType.episode),
        ('', ReleaseType.unknown),
        (ReleaseType.movie, ReleaseType.movie),
        (ReleaseType.season, ReleaseType.season),
        (ReleaseType.episode, ReleaseType.episode),
        (ReleaseType.unknown, ReleaseType.unknown),
    ),
)
def test_type_setter_with_valid_value(ReleaseInfo_mock, value, exp_value):
    rn = ReleaseName('path/to/something')
    rn.type = value
    assert rn.type is exp_value

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_type_setter_with_invalid_value(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    with pytest.raises(ValueError, match=r"^'asdf' is not a valid ReleaseType$"):
        rn.type = 'asdf'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_getter(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'title': 'The Foo'}
    assert ReleaseName('path/to/something').title == 'The Foo'
    ReleaseInfo_mock.return_value = {'title': 'The Bar'}
    assert ReleaseName('path/to/something').title == 'The Bar'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_setter(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.title != 'The Baz'
    rn.title = 'The Baz'
    assert rn.title == 'The Baz'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': 'Bar', 'year': '2015'}
    translation = {
        'title': {
            re.compile(r'o+'): r'00',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    rn.year_required = True
    assert rn.title == 'The F00'
    assert rn.title_aka == 'Bar'
    assert rn.title_with_aka == 'The F00 AKA Bar'
    assert rn.title_with_aka_and_year == 'The F00 AKA Bar 2015'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_aka_getter(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': ''}
    assert ReleaseName('path/to/something').title_aka == ''
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': 'The Bar'}
    assert ReleaseName('path/to/something').title_aka == 'The Bar'
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': 'The Foo'}
    assert ReleaseName('path/to/something').title_aka == ''

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_aka_setter(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.title_aka != 'The Baz'
    rn.title_aka = 'The Baz'
    assert rn.title_aka == 'The Baz'
    rn.title = 'The Baz'
    assert rn.title_aka == ''

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_aka_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': 'Bar', 'year': '2015'}
    translation = {
        'title_aka': {
            re.compile(r'(\w+)r'): r'R-\1',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    rn.year_required = True
    assert rn.title == 'The Foo'
    assert rn.title_aka == 'R-Ba'
    assert rn.title_with_aka == 'The Foo AKA R-Ba'
    assert rn.title_with_aka_and_year == 'The Foo AKA R-Ba 2015'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_with_aka(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': ''}
    assert ReleaseName('path/to/something').title_with_aka == 'The Foo'
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': 'The Bar'}
    assert ReleaseName('path/to/something').title_with_aka == 'The Foo AKA The Bar'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_with_aka_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': 'Bar', 'year': '2015'}
    translation = {
        'title_with_aka': {
            re.compile(r' +AKA +'): r': ',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    rn.year_required = True
    assert rn.title == 'The Foo'
    assert rn.title_aka == 'Bar'
    assert rn.title_with_aka == 'The Foo: Bar'
    assert rn.title_with_aka_and_year == 'The Foo: Bar 2015'


@pytest.mark.parametrize(
    argnames='date, year, country, year_required, country_required, exp_title_with_aka_and_year',
    argvalues=(
        ('', '2003', 'UK', False, False, 'The Foo'),
        ('', '2003', 'UK', False, True, 'The Foo UK'),
        ('', '2003', 'UK', False, False, 'The Foo'),
        ('', '2003', 'UK', True, False, 'The Foo 2003'),
        ('', '2003', 'UK', True, True, 'The Foo 2003 UK'),

        ('1999-10-03', '2003', 'UK', False, False, 'The Foo 1999-10-03'),
        ('1999-10-03', '2003', 'UK', False, True, 'The Foo 1999-10-03 UK'),
        ('1999-10-03', '2003', 'UK', False, False, 'The Foo 1999-10-03'),
        ('1999-10-03', '2003', 'UK', True, False, 'The Foo 1999-10-03'),
        ('1999-10-03', '2003', 'UK', True, True, 'The Foo 1999-10-03 UK'),
    ),
    ids=lambda v: str(v),
)
def test_title_with_aka_and_year(date, year, country, year_required, country_required, exp_title_with_aka_and_year, mocker):
    rn = ReleaseName('path/to/something')

    mocker.patch.object(type(rn), 'title_with_aka', PropertyMock(return_value='The Foo'))
    mocker.patch.object(type(rn), 'date', PropertyMock(return_value=date))
    mocker.patch.object(type(rn), 'year', PropertyMock(return_value=year))
    mocker.patch.object(type(rn), 'year_required', PropertyMock(return_value=year_required))
    mocker.patch.object(type(rn), 'country', PropertyMock(return_value=country))
    mocker.patch.object(type(rn), 'country_required', PropertyMock(return_value=country_required))

    rn.year_required = year_required
    rn.country_required = country_required
    assert rn.title_with_aka_and_year == exp_title_with_aka_and_year

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_title_with_aka_and_year_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'title': 'The Foo', 'aka': 'Bar', 'year': '2015'}
    translation = {
        'title_with_aka_and_year': {
            re.compile(r'(.*) (\d+)'): r'"\1" \2',
            re.compile(r'(\d+)'): r'(\1)',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    rn.year_required = True
    assert rn.title == 'The Foo'
    assert rn.title_aka == 'Bar'
    assert rn.title_with_aka == 'The Foo AKA Bar'
    assert rn.title_with_aka_and_year == '"The Foo AKA Bar" (2015)'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_year_getter_with_movie(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'year': '2000', 'type': ReleaseType.movie}
    assert ReleaseName('path/to/something').year == '2000'
    ReleaseInfo_mock.return_value = {'year': '', 'type': ReleaseType.movie}
    assert ReleaseName('path/to/something').year == 'UNKNOWN_YEAR'
    ReleaseInfo_mock.return_value = {'type': ReleaseType.movie}
    assert ReleaseName('path/to/something').year == 'UNKNOWN_YEAR'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize('type', (ReleaseType.season, ReleaseType.episode))
def test_year_getter_with_series(ReleaseInfo_mock, type):
    ReleaseInfo_mock.return_value = {'year': '2000', 'type': type}
    assert ReleaseName('path/to/something').year == '2000'
    ReleaseInfo_mock.return_value = {'year': '', 'type': type}
    assert ReleaseName('path/to/something').year == ''
    ReleaseInfo_mock.return_value = {'type': type}
    assert ReleaseName('path/to/something').year == ''

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='year, exp_year',
    argvalues=(
        ('1880', '1880'),
        ('1990', '1990'),
        ('2015', '2015'),
        (time.strftime('%Y'), time.strftime('%Y')),
        (int(time.strftime('%Y')) + 1, str(int(time.strftime('%Y')) + 1)),
        (int(time.strftime('%Y')) + 2, str(int(time.strftime('%Y')) + 2)),
        ('', ''),
        (None, ''),
    ),
)
def test_year_setter_with_valid_year(ReleaseInfo_mock, year, exp_year):
    rn = ReleaseName('path/to/something')
    assert rn.year == ''
    rn.year = year
    assert rn.year == exp_year

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='year, exp_exception, exp_message',
    argvalues=(
        ([], TypeError, 'Not a number: []'),
        ('foo', ValueError, 'Invalid year: foo'),
        ('1879', ValueError, 'Invalid year: 1879'),
        (int(time.strftime('%Y')) + 3, ValueError, f'Invalid year: {int(time.strftime("%Y")) + 3}'),
    ),
)
def test_year_setter_with_invalid_year(ReleaseInfo_mock, year, exp_exception, exp_message):
    rn = ReleaseName('path/to/something')
    assert rn.year == ''
    with pytest.raises(exp_exception, match=rf'^{re.escape(exp_message)}$'):
        rn.year = year

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_year_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'year': '2012'}
    translation = {
        'year': {
            re.compile(r'(\d+)'): r'\1 CE',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.year == '2012 CE'
    rn.year = '1995'
    assert rn.year == '1995 CE'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='year_required, year, exp_year',
    argvalues=(
        (False, '', ''),
        (True, '', 'UNKNOWN_YEAR'),
        (False, '1234', '1234'),
        (True, '1234', '1234'),
    ),
)
def test_year_required(ReleaseInfo_mock, year_required, year, exp_year):
    ReleaseInfo_mock.return_value = {'year': year}
    rn = ReleaseName('path/to/something')
    rn.year_required = year_required
    assert rn.year_required is year_required
    assert rn.year == exp_year


@pytest.mark.parametrize('country_required', (False, True))
@pytest.mark.parametrize('country', (None, '', 'UK'))
def test_country_getter(country, country_required, mocker):
    mocker.patch('upsies.utils.release.ReleaseInfo', Mock(return_value={
        'country': country,
    }))
    rn = ReleaseName('path/to/something')
    rn.country_required = country_required
    if country_required:
        if country:
            assert rn.country == country
        else:
            assert rn.country == 'UNKNOWN_COUNTRY'
    else:
        if country:
            assert rn.country == country
        else:
            assert rn.country == ''

@pytest.mark.parametrize(
    argnames='country, exp_country',
    argvalues=(
        ('UK', 'UK'),
        ([1, 2, 3], '[1, 2, 3]'),
        ('', ''),
        (None, ''),
    ),
)
def test_country_setter(country, exp_country, mocker):
    mocker.patch('upsies.utils.release.ReleaseInfo', Mock(return_value={}))
    rn = ReleaseName('path/to/something')
    assert rn.country == ''
    rn.country = country
    assert rn.country == exp_country

def test_country_is_translated(mocker):
    mocker.patch('upsies.utils.release.ReleaseInfo', Mock(return_value={
        'country': 'UK',
    }))
    translation = {
        'country': {
            re.compile(r'^(.+)$'): r'[\1]',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.country == '[UK]'
    rn.country = 'US'
    assert rn.country == '[US]'


def test_country_required(mocker):
    mocker.patch('upsies.utils.release.ReleaseInfo', Mock(return_value={}))
    rn = ReleaseName('path/to/something')
    assert not hasattr(rn, '_country_required')
    assert rn.country_required is False
    rn.country_required = 1
    assert rn.country_required is True
    rn.country_required = 0
    assert rn.country_required is False


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='type, episodes, exp_string',
    argvalues=(
        (ReleaseType.movie, Episodes({}), ''),
        (ReleaseType.movie, Episodes({3: ()}), ''),
        (ReleaseType.movie, Episodes({3: (1, 2), 4: ()}), ''),
        (ReleaseType.movie, Episodes({3: (1, 2), 4: (3, 4)}), ''),

        (ReleaseType.season, Episodes({}), 'UNKNOWN_SEASON'),
        (ReleaseType.season, Episodes({3: ()}), 'S03'),
        (ReleaseType.season, Episodes({3: (), 4: ()}), 'S03S04'),
        (ReleaseType.season, Episodes({3: (1, 2), 4: ()}), 'S03E01E02S04'),
        (ReleaseType.season, Episodes({3: (1, 2), 4: (3, 4)}), 'S03E01E02S04E03E04'),

        (ReleaseType.episode, Episodes({}), 'UNKNOWN_EPISODE'),
        (ReleaseType.episode, Episodes({3: ()}), 'UNKNOWN_EPISODE'),
        (ReleaseType.episode, Episodes({3: (), 4: ()}), 'UNKNOWN_EPISODE'),
        (ReleaseType.episode, Episodes({3: (1, 2), 4: ()}), 'S03E01E02S04'),
        (ReleaseType.episode, Episodes({3: (1, 2), 4: (3, 4)}), 'S03E01E02S04E03E04'),

        (ReleaseType.unknown, Episodes({}), ''),
        (ReleaseType.unknown, Episodes({3: ()}), 'S03'),
        (ReleaseType.unknown, Episodes({3: (), 4: ()}), 'S03S04'),
        (ReleaseType.unknown, Episodes({3: (1, 2), 4: ()}), 'S03E01E02S04'),
        (ReleaseType.unknown, Episodes({3: (1, 2), 4: (3, 4)}), 'S03E01E02S04E03E04'),
    ),
)
def test_episodes_getter(ReleaseInfo_mock, type, episodes, exp_string):
    ReleaseInfo_mock.return_value = {'episodes': episodes, 'type': type}
    assert ReleaseName('path/to/something').episodes == exp_string

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='type, value, exp_episodes',
    argvalues=(
        (ReleaseType.movie, 'foo.S03S04.bar', ''),
        (ReleaseType.movie, '3', ''),
        (ReleaseType.movie, 3, ''),
        (ReleaseType.movie, (3, '4'), ''),
        (ReleaseType.movie, {3: (1, 2), '4': ()}, ''),
        (ReleaseType.movie, '', ''),
        (ReleaseType.season, 'foo.S03S04.bar', 'S03S04'),
        (ReleaseType.season, 'foo.S03E10.bar', 'S03E10'),
        (ReleaseType.season, '3', 'S03'),
        (ReleaseType.season, 3, 'S03'),
        (ReleaseType.season, (3, '4'), 'S03S04'),
        (ReleaseType.season, {3: (1, 2), '4': ()}, 'S03E01E02S04'),
        (ReleaseType.season, '', 'UNKNOWN_SEASON'),
        (ReleaseType.episode, 'foo.S03S04.bar', 'UNKNOWN_EPISODE'),
        (ReleaseType.episode, 'foo.S03E10.bar', 'S03E10'),
        (ReleaseType.episode, 'foo.S03E10E11.bar', 'S03E10E11'),
        (ReleaseType.episode, '3', 'UNKNOWN_EPISODE'),
        (ReleaseType.episode, 3, 'UNKNOWN_EPISODE'),
        (ReleaseType.episode, (3, '4'), 'UNKNOWN_EPISODE'),
        (ReleaseType.episode, {3: (1, 2), '4': ()}, 'S03E01E02S04'),
        (ReleaseType.episode, '', 'UNKNOWN_EPISODE'),
        (ReleaseType.unknown, 'foo.S03S04.bar', 'S03S04'),
        (ReleaseType.unknown, 'foo.S03E10.bar', 'S03E10'),
        (ReleaseType.unknown, 'foo.S03E10E11.bar', 'S03E10E11'),
        (ReleaseType.unknown, '3', 'S03'),
        (ReleaseType.unknown, 3, 'S03'),
        (ReleaseType.unknown, (3, '4'), 'S03S04'),
        (ReleaseType.unknown, {3: (1, 2), '4': ()}, 'S03E01E02S04'),
        (ReleaseType.unknown, '', ''),
    ),
)
def test_episodes_setter_with_valid_value(ReleaseInfo_mock, type, value, exp_episodes):
    rn = ReleaseName('path/to/something')
    rn.type = type
    rn.episodes = value
    assert rn.episodes == exp_episodes

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_episodes_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'episodes': Episodes({3: ()})}
    translation = {
        'episodes': {
            re.compile(r'S0*'): r'Season ',
            re.compile(r'E0*'): r', Episode ',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.episodes == 'Season 3'
    rn.episodes = 'S03E12'
    assert rn.episodes == 'Season 3, Episode 12'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_episodes_dict(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.episodes_dict == {}
    rn.episodes = 'S03E12S04E13S05S06E12E20'
    assert rn.episodes_dict == {
        '3': ['12'],
        '4': ['13'],
        '5': [],
        '6': ['12', '20'],
    }


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_only_season(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.only_season is None
    rn.episodes = 'S03E12S04E13S05S06E12E20'
    assert rn.only_season is None
    rn.episodes = 'S02'
    assert rn.only_season == '2'
    rn.episodes = 'S02S010'
    assert rn.only_season is None


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='type, episode_title, exp_episode_title',
    argvalues=(
        (ReleaseType.movie, 'Something', ''),
        (ReleaseType.movie, '', ''),
        (ReleaseType.season, 'Something', ''),
        (ReleaseType.season, '', ''),
        (ReleaseType.episode, 'Something', 'Something'),
        (ReleaseType.episode, '', ''),
        (ReleaseType.unknown, 'Something', ''),
        (ReleaseType.unknown, '', ''),
    ),
)
def test_episode_title_getter(ReleaseInfo_mock, type, episode_title, exp_episode_title):
    ReleaseInfo_mock.return_value = {'episode_title': episode_title, 'type': type}
    rn = ReleaseName('path/to/something')
    assert rn.episode_title == exp_episode_title
    rn.type = ReleaseType.episode
    assert rn.episode_title == episode_title

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize('episode_title, exp_episode_title', (('Foo', 'Foo'), (123, '123')))
def test_episode_title_setter(ReleaseInfo_mock, episode_title, exp_episode_title):
    rn = ReleaseName('path/to/something')
    rn.type = ReleaseType.episode
    rn.episode_title = episode_title
    assert rn.episode_title == exp_episode_title

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_episode_title_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'episode_title': 'This Episode', 'type': ReleaseType.episode}
    translation = {
        'episode_title': {
            re.compile(r'(?i:this)'): r'That',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.episode_title == 'That Episode'
    rn.episode_title = 'foo'
    assert rn.episode_title == 'foo'


@pytest.mark.parametrize(
    argnames='release_type, date, exp_date',
    argvalues=(
        (ReleaseType.unknown, '2000-10-20', ''),
        (ReleaseType.movie, '2000-10-20', ''),
        (ReleaseType.season, '2000-10-20', ''),
        (ReleaseType.episode, '2000-10-20', '2000-10-20'),
        (ReleaseType.episode, None, ''),
    ),
)
@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_date_getter(ReleaseInfo_mock, release_type, date, exp_date):
    ReleaseInfo_mock.return_value = {'type': release_type, 'date': date}
    assert ReleaseName('path/to/something').date == exp_date

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_date_setter(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    rn.type = ReleaseType.episode
    assert rn.date == ''
    rn.date = '1234-56-78'
    assert rn.date == '1234-56-78'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_date_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'type': ReleaseType.episode}
    translation = {
        'date': {
            re.compile(r'(\d{4})-(\d{2})-(\d{2})'): r'\3-\2-\1',
            re.compile(r'-'): r'.',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    rn.date = '1234-56-78'
    assert rn.date == '78.56.1234'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_service_getter(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'service': 'FOO'}
    assert ReleaseName('path/to/something').service == 'FOO'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_service_setter(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.service == ''
    rn.service = 'FOO'
    assert rn.service == 'FOO'
    rn.service = 256
    assert rn.service == '256'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_service_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'service': 'Asdf'}
    translation = {
        'service': {
            re.compile(r'Asdf'): r'ASDF',
            re.compile(r'(.*)TV'): r'Tee\1Vee',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.service == 'ASDF'
    rn.service = 'AsdfTV'
    assert rn.service == 'TeeASDFVee'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_edition_getter_returns_same_list_with_no_edition(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.edition is rn.edition
    assert isinstance(rn.edition, list)

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_edition_getter_returns_same_list_with_given_edition(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'edition': ["Director's Cut", 'Unrated']}
    rn = ReleaseName('path/to/something')
    assert rn.edition == ["Director's Cut", 'Unrated']
    assert rn.edition is rn.edition
    assert isinstance(rn.edition, list)

@patch('upsies.utils.release.ReleaseInfo', Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='edition_list, has_dual_audio, exp_edition',
    argvalues=(
        ([], True, ['Dual Audio']),
        ([], False, []),
        (['Dual Audio'], True, ['Dual Audio']),
        (['Dual Audio'], False, []),
        (['Dual Audio', 'Dual Audio'], False, []),
    ),
)
def test_edition_getter_autodetects_dual_audio(edition_list, has_dual_audio, exp_edition, mocker):
    rn = ReleaseName('path/to/something')
    rn._info['edition'] = edition_list
    mocker.patch.object(type(rn), 'has_dual_audio', PropertyMock(return_value=has_dual_audio))
    # Ensure "Dual Audio" is only appended once
    for _ in range(3):
        assert rn.edition == exp_edition

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='edition, exp_edition',
    argvalues=(
        (('Special Edition',), ['Special Edition']),
        ((1, 2, 3), ['1', '2', '3']),
    ),
)
def test_edition_setter(ReleaseInfo_mock, edition, exp_edition):
    rn = ReleaseName('path/to/something')
    rn.edition = edition
    assert rn.edition == exp_edition
    assert rn.edition is rn.edition

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_edition_is_translated(ReleaseInfo_mock, mocker):
    ReleaseInfo_mock.return_value = {'edition': ['foo', 'bar', 'baz']}
    rn = ReleaseName('path/to/something')
    translation = {
        'edition': {
            re.compile(r'o+'): r'00',
            re.compile(r'b(\w+)'): r'\1F',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.edition == ['f00', 'arF', 'azF']
    rn.edition = ('noo', 'nar', 'naz')
    assert rn.edition == ['n00', 'nar', 'naz']


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='source, exp_source',
    argvalues=(
        ('WEB-DL', 'WEB-DL'),
        ('', 'UNKNOWN_SOURCE'),
    ),
)
def test_source_getter(ReleaseInfo_mock, source, exp_source):
    ReleaseInfo_mock.return_value = {'source': source}
    assert ReleaseName('path/to/something').source == exp_source

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='video_ts_size, exp_source',
    argvalues=(
        (4.7e9, 'DVD5'),
        (4.7e9 + 1, 'DVD9'),
    ),
)
def test_source_getter_with_video_ts(ReleaseInfo_mock, video_ts_size, exp_source, mocker):
    ReleaseInfo_mock.return_value = {'source': 'Ignored'}
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.fs.find_name', return_value='path/to/something/VIDEO_TS'),
        'find_name',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.fs.path_size', return_value=video_ts_size),
        'path_size',
    )
    assert ReleaseName('path/to/something').source == exp_source
    assert mocks.mock_calls == [
        call.find_name('VIDEO_TS', 'path/to/something', validator=os.path.isdir),
        call.path_size('path/to/something'),
    ]

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='bdmv_size, exp_source',
    argvalues=(
        (25e9 + 0, 'BD25'),
        (25e9 + 1, 'BD50'),
        (50e9 + 0, 'BD50'),
        (50e9 + 1, 'BD66'),
        (66e9 + 0, 'BD66'),
        (66e9 + 1, 'BD100'),
    ),
)
def test_source_getter_with_bdmv(ReleaseInfo_mock, bdmv_size, exp_source, mocker):
    ReleaseInfo_mock.return_value = {'source': 'Ignored'}
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.fs.find_name', side_effect=[None, 'path/to/something/BDMV']),
        'find_name',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.fs.path_size', return_value=bdmv_size),
        'path_size',
    )
    assert ReleaseName('path/to/something').source == exp_source
    assert mocks.mock_calls == [
        call.find_name('VIDEO_TS', 'path/to/something', validator=os.path.isdir),
        call.find_name('BDMV', 'path/to/something', validator=os.path.isdir),
        call.path_size('path/to/something'),
    ]

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@pytest.mark.parametrize(
    argnames='source, exp_source',
    argvalues=(
        ('BluRay', 'BluRay'),
        ('', 'UNKNOWN_SOURCE'),
        (123, '123'),
    ),
)
def test_source_setter(ReleaseInfo_mock, source, exp_source):
    rn = ReleaseName('path/to/something')
    rn.source = source
    assert rn.source == exp_source

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_source_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'source': 'Blu-Ray'}
    translation = {
        'source': {
            re.compile(r'-'): r'',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.source == 'BluRay'
    rn.source = 'asdf'
    assert rn.source == 'asdf'
    rn.source = 'WEB-DL'
    assert rn.source == 'WEBDL'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@patch('upsies.utils.video.resolution')
def test_resolution_getter_prefers_mediainfo(resolution_mock, ReleaseInfo_mock):
    resolution_mock.return_value = '720p'
    ReleaseInfo_mock.return_value = {'resolution': '1080p'}
    assert ReleaseName('path/to/something').resolution == '720p'
    assert resolution_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@patch('upsies.utils.video.resolution')
def test_resolution_getter_defaults_to_guess(resolution_mock, ReleaseInfo_mock):
    resolution_mock.return_value = None
    ReleaseInfo_mock.return_value = {'resolution': '1080p'}
    assert ReleaseName('path/to/something').resolution == '1080p'
    assert resolution_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@patch('upsies.utils.video.resolution')
def test_resolution_getter_defaults_to_placeholder(resolution_mock, ReleaseInfo_mock):
    resolution_mock.return_value = None
    ReleaseInfo_mock.return_value = {}
    assert ReleaseName('path/to/something').resolution == 'UNKNOWN_RESOLUTION'
    assert resolution_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_resolution_setter(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.resolution == 'UNKNOWN_RESOLUTION'
    rn.resolution = '1080p'
    assert rn.resolution == '1080p'
    rn.resolution = ''
    assert rn.resolution == 'UNKNOWN_RESOLUTION'
    rn.resolution = 1080
    assert rn.resolution == '1080'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
@patch('upsies.utils.video.resolution')
def test_resolution_is_translated(resolution_mock, ReleaseInfo_mock):
    resolution_mock.return_value = None
    ReleaseInfo_mock.return_value = {'resolution': '1080i'}
    translation = {
        'resolution': {
            re.compile(r'(\d+)i'): r'\1I',
            re.compile(r'x'): r':',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.resolution == '1080I'
    rn.resolution = 'asdf'
    assert rn.resolution == 'asdf'
    rn.resolution = '1080x1920'
    assert rn.resolution == '1080:1920'


@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.audio_format')
def test_audio_format_getter_prefers_mediainfo(audio_format_mock, ReleaseInfo_mock):
    audio_format_mock.return_value = 'AC3'
    ReleaseInfo_mock.return_value = {'audio_codec': 'DD+'}
    assert ReleaseName('path/to/something').audio_format == 'AC3'
    assert audio_format_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.audio_format')
def test_audio_format_getter_defaults_to_guess(audio_format_mock, ReleaseInfo_mock):
    audio_format_mock.return_value = None
    ReleaseInfo_mock.return_value = {'audio_codec': 'DD+'}
    assert ReleaseName('path/to/something').audio_format == 'DD+'
    assert audio_format_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.audio_format')
def test_audio_format_getter_defaults_to_empty_string(audio_format_mock, ReleaseInfo_mock):
    audio_format_mock.return_value = None
    ReleaseInfo_mock.return_value = {'audio_codec': ''}
    assert ReleaseName('path/to/something').audio_format == ''
    assert audio_format_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
def test_audio_format_setter(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {}
    rn = ReleaseName('path/to/something')
    assert rn.audio_format == ''
    rn.audio_format = 'AC3'
    assert rn.audio_format == 'AC3'
    rn.audio_format = ''
    assert rn.audio_format == ''
    rn.audio_format = 'DD+'
    assert rn.audio_format == 'DD+'

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.audio_format')
def test_audio_format_is_translated(audio_format_mock, ReleaseInfo_mock):
    audio_format_mock.return_value = None
    ReleaseInfo_mock.return_value = {'audio_codec': 'fooo'}
    translation = {
        'audio_format': {
            re.compile(r'\w(o+)'): r'b\1',
            re.compile(r'oo'): r'00',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.audio_format == 'b00o'
    rn.audio_format = 'asdf'
    assert rn.audio_format == 'asdf'
    rn.audio_format = 'noooo'
    assert rn.audio_format == 'b0000'


@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.audio_channels')
def test_audio_channels_getter_prefers_mediainfo(audio_channels_mock, ReleaseInfo_mock):
    audio_channels_mock.return_value = '5.1'
    ReleaseInfo_mock.return_value = {'audio_channels': '7.1'}
    assert ReleaseName('path/to/something').audio_channels == '5.1'
    assert audio_channels_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.audio_channels')
def test_audio_channels_getter_defaults_to_guess(audio_channels_mock, ReleaseInfo_mock):
    audio_channels_mock.return_value = None
    ReleaseInfo_mock.return_value = {'audio_channels': '7.1'}
    assert ReleaseName('path/to/something').audio_channels == '7.1'
    assert audio_channels_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.audio_channels')
def test_audio_channels_getter_defaults_to_empty_string(audio_channels_mock, ReleaseInfo_mock):
    audio_channels_mock.return_value = None
    ReleaseInfo_mock.return_value = {}
    assert ReleaseName('path/to/something').audio_channels == ''
    assert audio_channels_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
def test_audio_channels_setter(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {}
    rn = ReleaseName('path/to/something')
    assert rn.audio_channels == ''
    rn.audio_channels = '2.0'
    assert rn.audio_channels == '2.0'
    rn.audio_channels = ''
    assert rn.audio_channels == ''
    rn.audio_channels = 2.0
    assert rn.audio_channels == '2.0'

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.audio_channels')
def test_audio_channels_is_translated(audio_channels_mock, ReleaseInfo_mock):
    audio_channels_mock.return_value = None
    ReleaseInfo_mock.return_value = {'audio_channels': '5.1'}
    translation = {'audio_channels': {re.compile(r'\.'): r':'}}
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.audio_channels == '5:1'
    rn.audio_channels = 'asdf'
    assert rn.audio_channels == 'asdf'
    rn.audio_channels = '2.0'
    assert rn.audio_channels == '2:0'


@pytest.mark.parametrize(
    argnames='_hdr_format, path_exists, hdr_from_mediainfo, hdr_from_release_info, exp_value',
    argvalues=(
        ('custom HDR format', 'path_does_not_exist', 'HDR [mediainfo]', 'HDR [release info]', 'custom HDR format'),
        ('custom HDR format', 'path_does_exist', 'HDR [mediainfo]', 'HDR [release info]', 'custom HDR format'),
        ('', 'path_does_not_exist', 'HDR [mediainfo]', 'HDR [release info]', ''),
        ('', 'path_does_exist', 'HDR [mediainfo]', 'HDR [release info]', ''),
        (None, 'path_does_not_exist', 'HDR [mediainfo]', 'HDR [release info]', 'HDR [release info]'),
        (None, 'path_does_exist', 'HDR [mediainfo]', 'HDR [release info]', 'HDR [mediainfo]'),
        (None, 'path_does_exist', '', 'HDR [release info]', 'HDR [release info]'),
        (None, 'path_does_exist', '', '', ''),
    ),
    ids=lambda v: str(v),
)
def test_hdr_format_getter(_hdr_format, path_exists, hdr_from_mediainfo, hdr_from_release_info, exp_value, mocker):
    rn = ReleaseName('path/to/something')

    mocker.patch('os.path.exists', Mock(return_value=True if path_exists == 'path_does_exist' else False))
    mocker.patch('upsies.utils.video.hdr_format', Mock(return_value=hdr_from_mediainfo))
    mocker.patch.object(rn, '_info', {
        'hdr_format': hdr_from_release_info,
    })
    if _hdr_format is not None:
        mocker.patch.object(rn, '_hdr_format', _hdr_format, create=True)

    assert rn.hdr_format == exp_value

@pytest.mark.parametrize(
    argnames='value, exp_result',
    argvalues=(
        (None, ''),
        ('', ''),
        ('DV', 'DV'),
        ('HDR', 'HDR'),
        ('foo', ValueError("Unknown HDR format: 'foo'")),
    ),
    ids=lambda v: str(v),
)
def test_hdr_format_setter(value, exp_result, mocker):
    rn = ReleaseName('path/to/something')

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            rn.hdr_format = value
    else:
        rn.hdr_format = value
        assert rn.hdr_format == exp_result

def test_hdr_format_is_translated(mocker):
    mocker.patch('upsies.utils.release.ReleaseInfo', Mock(return_value={'hdr_format': 'HDR10'}))
    translation = {
        'hdr_format': {
            re.compile(r'(?i:hdr)'): r'ABC',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.hdr_format == 'ABC10'
    rn.hdr_format = 'DV'
    assert rn.hdr_format == 'DV'
    rn.hdr_format = 'HDR10+'
    assert rn.hdr_format == 'ABC10+'


@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.video_format')
def test_video_format_getter_prefers_mediainfo(video_format_mock, ReleaseInfo_mock):
    video_format_mock.return_value = 'x264'
    ReleaseInfo_mock.return_value = {'video_codec': 'x265'}
    assert ReleaseName('path/to/something').video_format == 'x264'
    assert video_format_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.video_format')
def test_video_format_getter_defaults_to_guess(video_format_mock, ReleaseInfo_mock):
    video_format_mock.return_value = None
    ReleaseInfo_mock.return_value = {'video_codec': 'x265'}
    assert ReleaseName('path/to/something').video_format == 'x265'
    assert video_format_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.video_format')
def test_video_format_getter_defaults_to_placeholder(video_format_mock, ReleaseInfo_mock):
    video_format_mock.return_value = None
    ReleaseInfo_mock.return_value = {}
    assert ReleaseName('path/to/something').video_format == 'UNKNOWN_VIDEO_FORMAT'
    assert video_format_mock.call_args_list == [call('path/to/something', default=None)]

@patch('upsies.utils.release.ReleaseInfo')
def test_video_format_setter(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {}
    rn = ReleaseName('path/to/something')
    assert rn.video_format == 'UNKNOWN_VIDEO_FORMAT'
    rn.video_format = 'x265'
    assert rn.video_format == 'x265'
    rn.video_format = ''
    assert rn.video_format == 'UNKNOWN_VIDEO_FORMAT'
    rn.video_format = 264
    assert rn.video_format == '264'

@patch('upsies.utils.release.ReleaseInfo')
@patch('upsies.utils.video.video_format')
def test_video_format_is_translated(video_format_mock, ReleaseInfo_mock):
    video_format_mock.return_value = None
    ReleaseInfo_mock.return_value = {'video_codec': 'x264'}
    translation = {
        'video_format': {
            re.compile(r'x(\d+)'): r'H.\1',
            re.compile(r'H\.?'): r'Harry',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.video_format == 'Harry264'
    rn.video_format = 'asdf'
    assert rn.video_format == 'asdf'
    rn.video_format = 'H265'
    assert rn.video_format == 'Harry265'


@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_group_getter(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'group': 'ASDF'}
    assert ReleaseName('path/to/something').group == 'ASDF'
    ReleaseInfo_mock.return_value = {'release_group': ''}
    assert ReleaseName('path/to/something').group == 'NOGROUP'
    ReleaseInfo_mock.return_value = {}
    assert ReleaseName('path/to/something').group == 'NOGROUP'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_group_setter(ReleaseInfo_mock):
    rn = ReleaseName('path/to/something')
    assert rn.group == 'NOGROUP'
    rn.group = 'ASDF'
    assert rn.group == 'ASDF'
    rn.group = ''
    assert rn.group == 'NOGROUP'
    rn.group = 123
    assert rn.group == '123'

@patch('upsies.utils.release.ReleaseInfo', new_callable=lambda: Mock(return_value={}))
def test_group_is_translated(ReleaseInfo_mock):
    ReleaseInfo_mock.return_value = {'group': 'A-SDF'}
    translation = {
        'group': {
            re.compile(r'-'): r'_',
        },
    }
    rn = ReleaseName('path/to/something', translate=translation)
    assert rn.group == 'A_SDF'
    rn.group = 'F-o-o'
    assert rn.group == 'F_o_o'


@pytest.mark.parametrize(
    argnames='path_exists, has_commentary, release_info, exp_value',
    argvalues=(
        ('path_exists', True, {'has_commentary': True}, True),
        ('path_exists', True, {'has_commentary': False}, True),

        ('path_exists', False, {'has_commentary': True}, False),
        ('path_exists', False, {'has_commentary': False}, False),

        ('path_exists', None, {'has_commentary': True}, False),
        ('path_exists', None, {'has_commentary': False}, False),

        ('path_does_not_exist', True, {'has_commentary': True}, True),
        ('path_does_not_exist', True, {'has_commentary': False}, False),

        ('path_does_not_exist', False, {'has_commentary': True}, True),
        ('path_does_not_exist', False, {'has_commentary': False}, False),

        ('path_does_not_exist', None, {'has_commentary': True}, True),
        ('path_does_not_exist', None, {'has_commentary': False}, False),
    ),
    ids=lambda v: str(v),
)
def test_has_commentary(path_exists, has_commentary, release_info, exp_value, mocker):
    mocker.patch(
        'upsies.utils.video.has_commentary',
        Mock(return_value=has_commentary),
    )
    mocker.patch(
        'upsies.utils.release.ReleaseInfo',
        Mock(return_value=release_info),
    )
    mocker.patch(
        'os.path.exists',
        Mock(return_value=True if path_exists == 'path_exists' else False),
    )
    rn = ReleaseName('path/to/something')
    assert rn.has_commentary is exp_value
    rn.has_commentary = ''
    assert rn.has_commentary is False
    rn.has_commentary = 1
    assert rn.has_commentary is True
    rn.has_commentary = None
    assert rn.has_commentary is exp_value


@pytest.mark.parametrize(
    argnames='path_exists, has_dual_audio, release_info, exp_value',
    argvalues=(
        ('path_exists', True, {'edition': ['Dual Audio']}, True),
        ('path_exists', True, {'edition': []}, True),

        ('path_exists', False, {'edition': ['Dual Audio']}, False),
        ('path_exists', False, {'edition': []}, False),

        ('path_exists', None, {'edition': ['Dual Audio']}, False),
        ('path_exists', None, {'edition': []}, False),

        ('path_does_not_exist', True, {'edition': ['Dual Audio']}, True),
        ('path_does_not_exist', True, {'edition': []}, False),

        ('path_does_not_exist', False, {'edition': ['Dual Audio']}, True),
        ('path_does_not_exist', False, {'edition': []}, False),

        ('path_does_not_exist', None, {'edition': ['Dual Audio']}, True),
        ('path_does_not_exist', None, {'edition': []}, False),
    ),
    ids=lambda v: str(v),
)
def test_has_dual_audio(path_exists, has_dual_audio, release_info, exp_value, mocker):
    mocker.patch(
        'upsies.utils.video.has_dual_audio',
        Mock(return_value=has_dual_audio),
    )
    mocker.patch(
        'upsies.utils.release.ReleaseInfo',
        Mock(return_value=release_info),
    )
    mocker.patch(
        'os.path.exists',
        Mock(return_value=True if path_exists == 'path_exists' else False),
    )
    rn = ReleaseName('path/to/something')
    assert rn.has_dual_audio is exp_value
    rn.has_dual_audio = ''
    assert rn.has_dual_audio is False
    rn.has_dual_audio = 1
    assert rn.has_dual_audio is True
    rn.has_dual_audio = None
    assert rn.has_dual_audio is exp_value


@pytest.mark.parametrize('release_type', tuple(ReleaseType), ids=lambda v: repr(v))
def test_is_complete_handles_all_ReleaseTypes(release_type):
    rn = ReleaseName('path/to/something')
    rn.type = release_type
    assert rn.is_complete is False

@pytest.mark.parametrize(
    argnames='release_name, release_type, needed_attrs',
    argvalues=(
        ('The Foo 1998 1080p BluRay DTS x264-ASDF', ReleaseType.movie, ReleaseName._needed_attrs[ReleaseType.movie]),
        ('The Foo S03 1080p BluRay DTS x264-ASDF', ReleaseType.season, ReleaseName._needed_attrs[ReleaseType.season]),
        ('The Foo S03E04 1080p BluRay DTS x264-ASDF', ReleaseType.episode, ReleaseName._needed_attrs[ReleaseType.episode]),
    ),
    ids=lambda v: str(v),
)
def test_is_complete(release_name, release_type, needed_attrs):
    rn = ReleaseName(release_name)
    rn.type = release_type
    assert rn.is_complete is True
    for attr in needed_attrs:
        value = getattr(rn, attr)
        setattr(rn, attr, '')
        assert rn.type is release_type
        assert rn.is_complete is False
        setattr(rn, attr, value)
        assert rn.is_complete is True


@pytest.mark.parametrize(
    argnames='source, frame_rate, exp_dvd_encoding',
    argvalues=(
        ('NonDVD', 25, None),
        ('DVD', 0, None),
        ('DVD', 25, 'PAL'),
        ('DVD', 30, 'NTSC'),
        ('DVD5', 0, None),
        ('DVD5', 25, 'PAL'),
        ('DVD5', 30, 'NTSC'),
        ('DVD9', 0, None),
        ('DVD9', 25, 'PAL'),
        ('DVD9', 30, 'NTSC'),
        ('DVDRip', 0, None),
        ('DVDRip', 25, 'PAL'),
        ('DVDRip', 30, 'NTSC'),
    ),
    ids=lambda v: str(v),
)
def test_dvd_encoding(source, frame_rate, exp_dvd_encoding, mocker):
    release = 'path/to/release'
    rn = ReleaseName(release)
    mocker.patch.object(type(rn), 'source', PropertyMock(return_value=source))
    mocker.patch('upsies.utils.video.frame_rate', return_value=frame_rate)
    dvd_encoding = rn.dvd_encoding
    assert dvd_encoding == exp_dvd_encoding


@pytest.mark.parametrize('callback', (None, Mock()), ids=['without callback', 'with callback'])
@pytest.mark.asyncio
async def test_fetch_info(callback, mocker):
    rn = ReleaseName('Foo 2000 1080p BluRay DTS x264-ASDF')

    mocks = AsyncMock()
    mocker.patch.object(rn, '_update_attributes', mocks._update_attributes)
    mocker.patch.object(rn, '_update_type', mocks._update_type)
    mocker.patch.object(rn, '_update_country', mocks._update_country)
    mocker.patch.object(rn, '_update_year_country_required', mocks._update_year_country_required)

    webdb = Mock()
    webdb_id = 'mock id'

    fetch_info_kwargs = {'webdb': webdb, 'webdb_id': webdb_id, 'callback': callback}
    return_value = await rn.fetch_info(**fetch_info_kwargs)
    assert return_value is rn

    assert mocks.mock_calls == [
        call._update_attributes(webdb, webdb_id),
        call._update_type(webdb, webdb_id),
        call._update_country(webdb, webdb_id),
        call._update_year_country_required(webdb, webdb_id),
    ]
    if callback:
        assert callback.call_args_list == [call(rn)]


@pytest.mark.parametrize('no_value', ('', None))
@pytest.mark.parametrize(
    argnames='info',
    argvalues=(
        {'title_original': 'Le Foo', 'title_english': 'The Foo', 'year': '2000'},
        {'title_original': '', 'title_english': '', 'year': ''},

        {'title_original': 'Le Foo', 'title_english': 'The Foo', 'year': ''},
        {'title_original': 'Le Foo', 'title_english': '', 'year': '2000'},
        {'title_original': '', 'title_english': 'The Foo', 'year': '2000'},

        {'title_original': 'Le Foo', 'title_english': '', 'year': ''},
        {'title_original': '', 'title_english': 'The Foo', 'year': ''},
        {'title_original': '', 'title_english': '', 'year': '2000'},
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_update_attributes(info, no_value, mocker):
    rn = ReleaseName('path/to/something')
    rn.title = 'Guessed Title'
    rn.title_aka = 'Guessed AKA'
    rn.year = '1999'

    webdb = Mock(gather=AsyncMock(return_value={
        k: v if v else no_value
        for k, v in info.items()
    }))
    webdb_id = 'mock id'

    await rn._update_attributes(webdb, webdb_id)

    assert rn.title == (info['title_original'] or 'Guessed Title')
    assert rn.title_aka == (info['title_english'] or 'Guessed AKA')
    assert rn.year == (info['year'] or '1999')

    assert webdb.gather.call_args_list == [
        call(webdb_id, 'title_english', 'title_original', 'year'),
    ]


@pytest.mark.parametrize(
    argnames='guessed_type, webdb_type, exp_type',
    argvalues=(
        (ReleaseType.movie, ReleaseType.movie, ReleaseType.movie),
        (ReleaseType.movie, ReleaseType.season, ReleaseType.season),
        (ReleaseType.movie, ReleaseType.episode, ReleaseType.episode),
        (ReleaseType.movie, ReleaseType.unknown, ReleaseType.movie),
        (ReleaseType.season, ReleaseType.movie, ReleaseType.movie),
        (ReleaseType.season, ReleaseType.season, ReleaseType.season),
        (ReleaseType.season, ReleaseType.episode, ReleaseType.episode),
        (ReleaseType.season, ReleaseType.unknown, ReleaseType.season),
        # For episodes, we trust guessed type more than IMDb et al
        (ReleaseType.episode, ReleaseType.movie, ReleaseType.episode),
        (ReleaseType.episode, ReleaseType.season, ReleaseType.episode),
        (ReleaseType.episode, ReleaseType.episode, ReleaseType.episode),
        (ReleaseType.episode, ReleaseType.unknown, ReleaseType.episode),
    ),
)
@pytest.mark.asyncio
async def test_update_type(guessed_type, webdb_type, exp_type, mocker):
    webdb = Mock(type=AsyncMock(return_value=webdb_type))
    webdb_id = 'mock id'

    rn = ReleaseName('path/to/something')
    mocker.patch.object(rn, '_info', {'type': guessed_type})

    assert rn.type == guessed_type
    await rn._update_type(webdb, webdb_id)
    assert rn.type == exp_type
    assert webdb.type.call_args_list == [call(webdb_id)]


@pytest.mark.parametrize(
    argnames='guessed_country, webdb_countries, exp_country',
    argvalues=(
        ('DK', NotImplementedError('This is not implemented'), 'DK'),
        ('DK', [], 'DK'),
        ('DK', ['Sweden', 'Finland'], 'SE'),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_update_country(guessed_country, webdb_countries, exp_country, mocker):
    if isinstance(webdb_countries, Exception):
        webdb = Mock(countries=AsyncMock(side_effect=webdb_countries))
    else:
        webdb = Mock(countries=AsyncMock(return_value=webdb_countries))
    webdb_id = 'mock id'

    rn = ReleaseName('path/to/something')
    mocker.patch.object(rn, '_info', {'country': guessed_country})

    assert rn.country == guessed_country
    await rn._update_country(webdb, webdb_id)
    assert rn.country == exp_country
    assert webdb.countries.call_args_list == [call(webdb_id)]


@pytest.mark.parametrize('release_type', (ReleaseType.movie, ReleaseType.season, ReleaseType.episode))
@pytest.mark.parametrize(
    argnames='attributes, results, exp_year_required, exp_country_required',
    argvalues=(
        # Series: unique name, irrelevant year, irrelevant countries
        (
            {'title': 'The Foo', 'year': None, 'countries': []},
            (
                ('The Foo', '2000', ['US']),
                ('The Foe', '2000', ['US']),
                ('The Bar', '2000', ['US']),
                ('The Bar 2', None, ['US']),
                ('The Baz 2', '2000', None),
            ),
            None, None,
        ),

        # Series: common name, unique year, irrelevant countries
        (
            {'title': 'The Foo', 'year': '2001', 'countries': []},
            (
                ('The FOO', '2000', ['US']),
                ('The Föö', '2001', ['US']),
                ('The Fóò', '2002', ['US']),
                ('The Bar', '2000', ['US']),
                ('The Baz', '2000', ['US']),
                ('The Bar 2', None, ['US']),
                ('The Baz 2', '2000', None),
            ),
            True, None,
        ),

        # Series: common name, common year, unique countries
        (
            {'title': 'The Foo', 'year': '2002', 'countries': ['UK']},
            (
                ('The FOO', '2002', ['US']),
                ('The Föö', '2002', ['UK']),
                ('The Fóò', '2002', ['US']),
                ('The Bar', '2002', ['US']),
                ('The Baz', '2002', ['US']),
                ('The Bar 2', None, ['US']),
                ('The Baz 2', '2002', None),
            ),
            None, True,
        ),

        # Series: common name, common year, common countries
        (
            {'title': 'The Foo', 'year': '2003', 'countries': ['UK']},
            (
                ('The FOO', '2003', ['US']),
                ('The Föö', '2003', ['UK']),
                ('The Fóò', '2003', ['UK']),
                ('The Bar', '2003', ['US']),
                ('The Bar 2', None, ['US']),
                ('The Baz 2', '2003', None),
            ),
            True, True,
        ),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_update_year_country_required(release_type, attributes, results, exp_year_required, exp_country_required, mocker):
    from types import SimpleNamespace
    mocked_results = [
        SimpleNamespace(title=r[0], year=r[1], countries=AsyncMock(return_value=r[2]))
        for r in results
    ]
    webdb = Mock(
        search=AsyncMock(return_value=mocked_results),
        year=AsyncMock(return_value=attributes['year']),
        countries=AsyncMock(return_value=attributes['countries']),
    )
    webdb_id = 'tt123'

    rn = ReleaseName('path/to/something')
    mocker.patch.object(type(rn), 'type', PropertyMock(return_value=release_type))
    mocker.patch.object(type(rn), 'title', PropertyMock(return_value=attributes['title']))

    orig_year_required = rn.year_required
    orig_country_required = rn.country_required

    if release_type is ReleaseType.movie:
        exp_year_required = orig_year_required
        exp_country_required = orig_country_required
    else:
        if exp_year_required is None:
            exp_year_required = orig_year_required
        if exp_country_required is None:
            exp_country_required = orig_country_required

    await rn._update_year_country_required(webdb, webdb_id)

    assert rn.year_required is exp_year_required
    assert rn.country_required is exp_country_required

    if release_type is ReleaseType.movie:
        assert webdb.mock_calls == []
    else:
        exp_query = webdbs.Query(title='The Foo', type=ReleaseType.series)
        assert webdb.mock_calls == [
            call.search(exp_query),
            call.year(webdb_id),
            call.countries(webdb_id),
        ]


TITLE_WITH_AKA_AND_YEAR = {
    'Foo: Bär... AKA B-a-z & Quux 2003': {
        ' ': 'Foo: Bär... AKA B-a-z & Quux 2003',
        '.': 'Foo.Bär.AKA.B-a-z.and.Quux.2003',
    },
}

@pytest.mark.parametrize('title_with_aka_and_year', TITLE_WITH_AKA_AND_YEAR.keys())
@pytest.mark.parametrize(
    argnames='release_type, exp_episodes_included',
    argvalues=(
        (ReleaseType.movie, False),
        (ReleaseType.season, True),
        (ReleaseType.episode, True),
    ),
)
@pytest.mark.parametrize(
    argnames='resolution, dvd_encoding, exp_resolution',
    argvalues=(
        ('123p', None, '123p'),
        ('123p', 'NTSC-PAL', 'NTSC-PAL'),
    ),
)
@pytest.mark.parametrize(
    argnames='separator_attribute, separator_argument, exp_separator',
    argvalues=(
        (' ', None, ' '),
        (' ', '.', '.'),
        ('.', None, '.'),
        ('.', ' ', ' '),
    ),
)
@pytest.mark.parametrize(
    argnames='attributes, exp_release_name',
    argvalues=(
        (
            {'service': '', 'edition': (), 'audio_format': '', 'audio_channels': ''},
            '{title_with_aka_and_year_and_episodes}{s}{resolution}{s}{source}{s}{video_format}-{group}',
        ),
        (
            {'service': 'ABC', 'edition': (), 'audio_format': '', 'audio_channels': ''},
            '{title_with_aka_and_year_and_episodes}{s}{resolution}{s}ABC{s}{source}{s}{video_format}-{group}',
        ),
        (
            {'service': '', 'edition': ('DC',), 'audio_format': 'DTS', 'audio_channels': ''},
            '{title_with_aka_and_year_and_episodes}{s}DC{s}{resolution}{s}{source}{s}DTS{s}{video_format}-{group}',
        ),
        (
            {'service': '', 'edition': ('DC', 'FE'), 'audio_format': 'DTS', 'audio_channels': ''},
            '{title_with_aka_and_year_and_episodes}{s}DC{s}FE{s}{resolution}{s}{source}{s}DTS{s}{video_format}-{group}',
        ),
        (
            {'service': '', 'edition': (), 'audio_format': 'DTS', 'audio_channels': '3.4'},
            '{title_with_aka_and_year_and_episodes}{s}{resolution}{s}{source}{s}DTS{s}3.4{s}{video_format}-{group}',
        ),
        (
            {'service': 'ABC', 'edition': ('DC',), 'audio_format': 'DTS', 'audio_channels': '3.4'},
            '{title_with_aka_and_year_and_episodes}{s}DC{s}{resolution}{s}ABC{s}{source}{s}DTS{s}3.4{s}{video_format}-{group}',
        ),
        (
            {'service': '', 'edition': (), 'audio_format': '', 'audio_channels': '', 'hdr_format': 'HDR10',},
            '{title_with_aka_and_year_and_episodes}{s}{resolution}{s}{source}{s}HDR10{s}{video_format}-{group}',
        ),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.asyncio
async def test_format(
        title_with_aka_and_year,
        release_type, exp_episodes_included,
        resolution, dvd_encoding, exp_resolution,
        separator_attribute, separator_argument, exp_separator,
        attributes, exp_release_name,
        mocker,
):
    rn = ReleaseName('irrelevant/path/to/content')

    static_attributes = {
        'episodes': 'S__E__',
        'source': 'DLRip',
        'video_format': 'VC',
        'group': 'ASDF',
    }
    for name, value in static_attributes.items():
        mocker.patch.object(type(rn), name, PropertyMock(return_value=value))
    for name, value in attributes.items():
        mocker.patch.object(type(rn), name, PropertyMock(return_value=value))

    mocker.patch.object(type(rn), 'type', PropertyMock(return_value=release_type))
    mocker.patch.object(type(rn), 'dvd_encoding', PropertyMock(return_value=dvd_encoding))
    mocker.patch.object(type(rn), 'resolution', PropertyMock(return_value=resolution))
    mocker.patch.object(type(rn), 'separator', PropertyMock(return_value=separator_attribute))
    mocker.patch.object(type(rn), 'title_with_aka_and_year', PropertyMock(return_value=title_with_aka_and_year))
    exp_title_with_aka_and_year_and_episodes = TITLE_WITH_AKA_AND_YEAR[title_with_aka_and_year][exp_separator]
    if exp_episodes_included:
        exp_title_with_aka_and_year_and_episodes += exp_separator + static_attributes['episodes']

    release_name = rn.format(separator=separator_argument)
    exp_release_name_resolved = exp_release_name.format(
        s=exp_separator,
        title_with_aka_and_year_and_episodes=exp_title_with_aka_and_year_and_episodes,
        resolution=exp_resolution,
        **static_attributes,
    )
    assert release_name == exp_release_name_resolved
