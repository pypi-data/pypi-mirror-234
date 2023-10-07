import base64
import re

import pytest

from upsies import utils
from upsies.trackers.mtv import MtvTrackerConfig


@pytest.fixture
def tracker_config():
    return MtvTrackerConfig()


def test_MtvTrackerConfig_defaults(tracker_config):
    assert set(tracker_config) == {
        'base_url',
        'username',
        'password',
        'announce_url',
        'source',
        'randomize_infohash',
        'image_host',
        'screenshots',
        'exclude',
        'anonymous',

        # Inherited from TrackerConfigBase
        'add_to',
        'copy_to',
    }


def test_MtvTrackerConfig_defaults_base_url(tracker_config):
    assert tracker_config['base_url'] == base64.b64decode('aHR0cHM6Ly93d3cubW9yZXRoYW50di5tZQ==').decode('ascii')


def test_MtvTrackerConfig_defaults_username(tracker_config):
    assert tracker_config['username'] == ''


def test_MtvTrackerConfig_defaults_password(tracker_config):
    assert tracker_config['password'] == ''


def test_MtvTrackerConfig_defaults_announce_url(tracker_config):
    assert tracker_config['announce_url'] == ''
    assert tracker_config['announce_url'].description == (
        'Your personal announce URL. Automatically fetched from the website if not set.'
    )


def test_MtvTrackerConfig_defaults_source(tracker_config):
    assert tracker_config['source'] == 'MTV'


def test_MtvTrackerConfig_defaults_image_host(tracker_config, assert_config_choice):
    assert_config_choice(
        choice=tracker_config['image_host'],
        value='imgbox',
        options=utils.imghosts.imghost_names(),
    )


def test_MtvTrackerConfig_defaults_screenshots(tracker_config, assert_config_number):
    assert_config_number(
        number=tracker_config['screenshots'],
        value=4,
        min=3,
        max=10,
        description='How many screenshots to make.',
    )


def test_MtvTrackerConfig_defaults_exclude(tracker_config):
    assert tracker_config['exclude'] == (
        re.compile(r'\.(?i:nfo|txt|jpg|jpeg|png|sfv|md5)$'),
        re.compile(r'/(?i:sample|extra|bonus|feature)'),
        re.compile(r'(?i:.*sample\.[a-z]+)$'),
    )


def test_MtvTrackerConfig_defaults_anonymous(tracker_config):
    assert isinstance(tracker_config['anonymous'], utils.types.Bool)
    assert not tracker_config['anonymous']
    assert tracker_config['anonymous'] == 'no'
    assert tracker_config['anonymous'].description == (
        'Whether your username is displayed on your uploads.'
    )


def test_MtvTrackerConfig_arguments(tracker_config):
    exp_argument_definitions = {
        'submit': {
            ('--screenshots', '--ss'),
            ('--only-description', '--od'),
            ('--only-title', '--ot'),
            ('--ignore-dupes', '--id'),
        },
    }
    assert set(tracker_config.argument_definitions) == set(exp_argument_definitions)
    for command in exp_argument_definitions:
        assert set(tracker_config.argument_definitions[command]) == exp_argument_definitions[command]


def test_MtvTrackerConfig_argument_definitions_submit_screenshots(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--screenshots', '--ss')] == {
        'help': ('How many screenshots to make '
                 f'(min={tracker_config["screenshots"].min}, '
                 f'max={tracker_config["screenshots"].max})'),
        'type': utils.argtypes.number_of_screenshots(
            min=tracker_config['screenshots'].min,
            max=tracker_config['screenshots'].max,
        ),
    }


def test_MtvTrackerConfig_argument_definitions_submit_only_description(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--only-description', '--od')] == {
        'help': 'Only generate description (do not upload anything)',
        'action': 'store_true',
        'group': 'generate-metadata',
    }


def test_MtvTrackerConfig_argument_definitions_submit_only_title(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--only-title', '--ot')] == {
        'help': 'Only generate title (do not upload anything)',
        'action': 'store_true',
        'group': 'generate-metadata',
    }


def test_MtvTrackerConfig_argument_definitions_submit_ignore_dupes(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--ignore-dupes', '--id')] == {
        'help': 'Force submission even if the tracker reports duplicates',
        'action': 'store_true',
    }
