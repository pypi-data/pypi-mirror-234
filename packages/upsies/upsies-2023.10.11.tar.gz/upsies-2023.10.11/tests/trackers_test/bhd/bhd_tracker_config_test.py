import base64
import re

import pytest

from upsies import utils
from upsies.trackers.bhd import BhdTrackerConfig


@pytest.fixture
def tracker_config():
    return BhdTrackerConfig()


def test_BhdTrackerConfig_defaults(tracker_config):
    assert set(tracker_config) == {
        'upload_url',
        'announce_url',
        'announce_passkey',
        'apikey',
        'source',
        'randomize_infohash',
        'anonymous',
        'draft',
        'image_host',
        'screenshots',
        'exclude',

        # Inherited from TrackerConfigBase
        'add_to',
        'copy_to',
    }


def test_BhdTrackerConfig_defaults_upload_url(tracker_config):
    assert tracker_config['upload_url'] == base64.b64decode('aHR0cHM6Ly9iZXlvbmQtaGQubWUvYXBpL3VwbG9hZA==').decode('ascii')


def test_BhdTrackerConfig_defaults_announce_url(tracker_config):
    assert tracker_config['announce_url'] == base64.b64decode('aHR0cHM6Ly9iZXlvbmQtaGQubWUvYW5ub3VuY2U=').decode('ascii')
    assert tracker_config['announce_url'].description == (
        'The announce URL without the private passkey.'
    )


def test_BhdTrackerConfig_defaults_announce_passkey(tracker_config):
    assert tracker_config['announce_passkey'] == ''
    assert tracker_config['announce_passkey'].description == (
        'The private part of the announce URL.\n'
        'Get it from the website: My Security -> Passkey'
    )


def test_BhdTrackerConfig_defaults_apikey(tracker_config):
    assert tracker_config['apikey'] == ''
    assert tracker_config['apikey'].description == (
        'Your personal private API key.\n'
        'Get it from the website: My Security -> API key'
    )


def test_BhdTrackerConfig_defaults_source(tracker_config):
    assert tracker_config['source'] == 'BHD'


def test_BhdTrackerConfig_defaults_anonymous(tracker_config):
    assert isinstance(tracker_config['anonymous'], utils.types.Bool)
    assert not tracker_config['anonymous']
    assert tracker_config['anonymous'] == 'no'
    assert tracker_config['anonymous'].description == (
        'Whether your username is displayed on your uploads.'
    )


def test_BhdTrackerConfig_defaults_draft(tracker_config):
    assert isinstance(tracker_config['draft'], utils.types.Bool)
    assert not tracker_config['draft']
    assert tracker_config['draft'] == 'no'


def test_BhdTrackerConfig_defaults_image_host(tracker_config, assert_config_choice):
    assert_config_choice(
        choice=tracker_config['image_host'],
        value='imgbox',
        options=utils.imghosts.imghost_names(),
    )


def test_BhdTrackerConfig_defaults_screenshots(tracker_config, assert_config_number):
    assert_config_number(
        number=tracker_config['screenshots'],
        value=4,
        min=3,
        max=10,
        description='How many screenshots to make.',
    )


def test_BhdTrackerConfig_defaults_exclude(tracker_config):
    assert tracker_config['exclude'] == (
        re.compile(r'\.(?i:nfo|txt|jpg|jpeg|png|sfv|md5|idx|sub|srt)$'),
        re.compile(r'/(?i:sample|extra|bonus|feature)'),
        re.compile(r'(?i:.*sample\.[a-z]+)$'),
    )


def test_BhdTrackerConfig_arguments(tracker_config):
    exp_argument_definitions = {
        'submit': {
            ('--custom-edition', '--ce'),
            ('--draft', '--dr'),
            ('--personal-rip', '--pr'),
            ('--screenshots', '--ss'),
            ('--special', '--sp'),
            ('--only-description', '--od'),
            ('--only-title', '--ot'),
        },
    }
    assert set(tracker_config.argument_definitions) == set(exp_argument_definitions)
    for command in exp_argument_definitions:
        assert set(tracker_config.argument_definitions[command]) == exp_argument_definitions[command]


def test_BhdTrackerConfig_argument_definitions_submit_custom_edition(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--custom-edition', '--ce')] == {
        'help': 'Non-standard edition, e.g. "Final Cut"',
        'default': '',
    }


def test_BhdTrackerConfig_argument_definitions_submit_draft(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--draft', '--dr')] == {
        'help': 'Upload as draft',
        'action': 'store_true',
        'default': None,
    }


def test_BhdTrackerConfig_argument_definitions_submit_personal_rip(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--personal-rip', '--pr')] == {
        'help': 'Tag as your own encode',
        'action': 'store_true',
    }


def test_BhdTrackerConfig_argument_definitions_submit_screenshots(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--screenshots', '--ss')] == {
        'help': ('How many screenshots to make '
                 f'(min={tracker_config["screenshots"].min}, '
                 f'max={tracker_config["screenshots"].max})'),
        'type': utils.argtypes.number_of_screenshots(
            min=tracker_config['screenshots'].min,
            max=tracker_config['screenshots'].max,
        ),
    }


def test_BhdTrackerConfig_argument_definitions_submit_special(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--special', '--sp')] == {
        'help': 'Tag as special episode, e.g. Christmas special (ignored for movie uploads)',
        'action': 'store_true',
    }


def test_BhdTrackerConfig_argument_definitions_submit_only_description(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--only-description', '--od')] == {
        'help': 'Only generate description (do not upload anything)',
        'action': 'store_true',
        'group': 'generate-metadata',
    }


def test_BhdTrackerConfig_argument_definitions_submit_only_title(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--only-title', '--ot')] == {
        'help': 'Only generate title (do not upload anything)',
        'action': 'store_true',
        'group': 'generate-metadata',
    }
