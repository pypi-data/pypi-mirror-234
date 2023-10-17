import re

import pytest

from upsies import utils
from upsies.trackers.base import TrackerConfigBase


def test_TrackerConfigBase_defaults():
    assert TrackerConfigBase.defaults == {}


def test_TrackerConfigBase_argument_definitions():
    assert TrackerConfigBase.argument_definitions == {}


@pytest.fixture
def make_TrackerConfig():
    def make_TrackerConfig(defaults={}):
        # Avoid NameError bug (https://github.com/python/cpython/issues/87546)
        defaults_ = defaults

        class TestTrackerConfig(TrackerConfigBase):
            defaults = defaults_

        return TestTrackerConfig

    return make_TrackerConfig


@pytest.fixture
def make_tracker_config(make_TrackerConfig):
    def make_tracker_config(defaults={}, userconfig={}):
        TestTrackerConfig = make_TrackerConfig(defaults=defaults)
        return TestTrackerConfig(userconfig)

    return make_tracker_config


def test_unknown_option(make_TrackerConfig):
    TrackerConfig = make_TrackerConfig()
    with pytest.raises(ValueError, match="Unknown option: 'foo'"):
        TrackerConfig({'foo': 'bar'})


def test_user_value_is_converted_to_base_type(make_TrackerConfig, mocker):
    mocker.patch('upsies.trackers.base.TrackerConfigBase._common_defaults', {'count': 123, 'ratio': 3.14})
    TrackerConfig = make_TrackerConfig({'my_list': ['a', 'b', 'c']})
    config = TrackerConfig({'count': '300', 'ratio': 3, 'my_list': ('d', 'e', 'f')})

    assert config == {
        'count': 300,
        'ratio': 3.0,
        'my_list': ['d', 'e', 'f'],
    }
    assert isinstance(config['count'], int)
    assert isinstance(config['ratio'], float)
    assert isinstance(config['my_list'], list)


@pytest.mark.parametrize(
    argnames='defaults, userconfig, exp_value',
    argvalues=(
        ({}, {}, ''),
        ({'source': 'FOO'}, {}, 'FOO'),
        ({'source': 'FOO'}, {'source': ''}, ''),
        ({'source': 'FOO'}, {'source': 'BAR'}, 'BAR'),
    ),
    ids=lambda v: repr(v),
)
def test_source_value(defaults, userconfig, exp_value, make_tracker_config):
    config = make_tracker_config(defaults=defaults, userconfig=userconfig)
    assert config['source'] == exp_value

def test_source_description(make_tracker_config):
    config = make_tracker_config()
    assert config['source'].description == 'Value of the "source" field in generated torrents.'


@pytest.mark.parametrize(
    argnames='defaults, userconfig, exp_value',
    argvalues=(
        ({}, {}, False),
        ({'randomize_infohash': 'yes'}, {}, True),
        ({'randomize_infohash': 'false'}, {}, False),
        ({'randomize_infohash': 'true'}, {'randomize_infohash': 'false'}, False),
        ({'randomize_infohash': 'no'}, {'randomize_infohash': 'true'}, True),
    ),
    ids=lambda v: repr(v),
)
def test_randomize_infohash_value(defaults, userconfig, exp_value, make_tracker_config):
    config = make_tracker_config(defaults=defaults, userconfig=userconfig)
    assert config['randomize_infohash'] == exp_value

def test_randomize_infohash_description(make_tracker_config):
    config = make_tracker_config()
    assert config['randomize_infohash'].description == (
        'Whether the info hash of generated torrents is randomized '
        'by including a random number in the metadata.\n'
        'WARNING: The tracker may choke on the non-standard field '
        'or remove the random number, forcing you to manually download '
        'the torrent.'
    )


@pytest.mark.parametrize(
    argnames='defaults, userconfig, exp_value',
    argvalues=(
        ({}, {}, ()),
        ({'exclude': ['foo', 'bar']}, {}, (re.compile(r'foo'), re.compile(r'bar'))),
        ({'exclude': ['foo', 'bar']}, {'exclude': ['this', 'that']}, (re.compile(r'this'), re.compile(r'that'))),
        ({'exclude': ['foo', 'bar']}, {'exclude': []}, ()),
    ),
    ids=lambda v: repr(v),
)
def test_exclude_value(defaults, userconfig, exp_value, make_tracker_config):
    config = make_tracker_config(defaults=defaults, userconfig=userconfig)
    assert config['exclude'] == exp_value

def test_exclude_description(make_tracker_config):
    config = make_tracker_config()
    assert config['exclude'].description == 'List of regular expressions. Matching files are excluded from generated torrents.'


CLIENT_NAMES = utils.btclient.client_names()

@pytest.mark.parametrize(
    argnames='defaults, userconfig, exp_result',
    argvalues=(
        ({}, {}, ''),
        ({'add_to': CLIENT_NAMES[0]}, {}, CLIENT_NAMES[0]),
        ({'add_to': CLIENT_NAMES[0]}, {'add_to': CLIENT_NAMES[1]}, CLIENT_NAMES[1]),
        ({'add_to': CLIENT_NAMES[0]}, {'add_to': ''}, ''),
        ({'add_to': 'foo'}, {'add_to': CLIENT_NAMES[1]}, ValueError(f'Not one of {", ".join(c for c in CLIENT_NAMES)}: foo')),
        ({'add_to': CLIENT_NAMES[0]}, {'add_to': 'bar'}, ValueError(f'Not one of {", ".join(c for c in CLIENT_NAMES)}: bar')),
    ),
    ids=lambda v: repr(v),
)
def test_add_to_value(defaults, userconfig, exp_result, make_TrackerConfig):
    TrackerConfig = make_TrackerConfig(defaults)
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            TrackerConfig(userconfig)
    else:
        config = TrackerConfig(userconfig)
        assert config['add_to'] == exp_result

def test_add_to_description(make_tracker_config):
    config = make_tracker_config()
    assert config['add_to'].description == 'BitTorrent client to add torrent to after submission.'


@pytest.mark.parametrize(
    argnames='defaults, userconfig, exp_value',
    argvalues=(
        ({}, {}, ''),
        ({'copy_to': 'some/path'}, {}, 'some/path'),
        ({'copy_to': 'some/path'}, {'copy_to': 'other/path'}, 'other/path'),
        ({'copy_to': 'some/path'}, {'copy_to': ''}, ''),
    ),
    ids=lambda v: repr(v),
)
def test_copy_to_value(defaults, userconfig, exp_value, make_tracker_config):
    config = make_tracker_config(defaults=defaults, userconfig=userconfig)
    assert config['copy_to'] == exp_value

def test_copy_to_description(make_tracker_config):
    config = make_tracker_config()
    assert config['copy_to'].description == 'Directory path to copy torrent to after submission.'
