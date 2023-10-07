import base64
import re

import pytest

from upsies import utils
from upsies.trackers.ptp import PtpTrackerConfig


@pytest.fixture
def tracker_config():
    return PtpTrackerConfig()


def test_PtpTrackerConfig_defaults(tracker_config):
    assert set(tracker_config) == {
        'base_url',
        'username',
        'password',
        'announce_url',
        'source',
        'randomize_infohash',
        'image_host',
        'screenshots_from_movie',
        'screenshots_from_episode',
        'exclude',

        # Inherited from TrackerConfigBase
        'add_to',
        'copy_to',
    }


def test_PtpTrackerConfig_defaults_base_url(tracker_config):
    assert tracker_config['base_url'] == base64.b64decode('aHR0cHM6Ly9wYXNzdGhlcG9wY29ybi5tZQ==').decode('ascii')


def test_PtpTrackerConfig_defaults_username(tracker_config):
    assert tracker_config['username'] == ''


def test_PtpTrackerConfig_defaults_password(tracker_config):
    assert tracker_config['password'] == ''


def test_PtpTrackerConfig_defaults_announce_url(tracker_config):
    assert tracker_config['announce_url'] == ''
    assert tracker_config['announce_url'].description == (
        'Your personal announce URL.'
    )


def test_PtpTrackerConfig_defaults_source(tracker_config):
    assert tracker_config['source'] == 'PTP'


def test_PtpTrackerConfig_defaults_image_host(tracker_config, assert_config_choice):
    assert_config_choice(
        choice=tracker_config['image_host'],
        value='ptpimg',
        options=utils.imghosts.imghost_names(),
    )


def test_PtpTrackerConfig_defaults_screenshots_from_movie(tracker_config, assert_config_number):
    assert_config_number(
        number=tracker_config['screenshots_from_movie'],
        value=3,
        min=3,
        max=10,
        description='How many screenshots to make for single-video uploads.',
    )


def test_PtpTrackerConfig_defaults_screenshots_from_episode(tracker_config, assert_config_number):
    assert_config_number(
        number=tracker_config['screenshots_from_episode'],
        value=2,
        min=2,
        max=10,
        description='How many screenshots to make per video for multi-video uploads.',
    )


def test_PtpTrackerConfig_defaults_exclude(tracker_config):
    assert tracker_config['exclude'] == (
        re.compile(r'\.(?i:nfo|txt|jpg|jpeg|png|sfv|md5|sub|idx|srt)$'),
        re.compile(r'/(?i:sample|extra|bonus|feature)'),
        re.compile(r'(?i:.*sample\.[a-z]+)$'),
    )


def test_PtpTrackerConfig_arguments(tracker_config):
    exp_argument_definitions = {
        'submit': {
            ('--hardcoded-subtitles', '--hs'),
            ('--not-main-movie', '--nmm'),
            ('--personal-rip', '--pr'),
            ('--screenshots', '--ss'),
            ('--upload-token', '--ut'),
            ('--only-description', '--od'),
        },
    }
    assert set(tracker_config.argument_definitions) == set(exp_argument_definitions)
    for command in exp_argument_definitions:
        assert set(tracker_config.argument_definitions[command]) == exp_argument_definitions[command]


def test_PtpTrackerConfig_argument_definitions_submit_hardcoded_subtitles(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--hardcoded-subtitles', '--hs')] == {
        'help': 'Video contains hardcoded subtitles',
        'action': 'store_true',
    }


def test_PtpTrackerConfig_argument_definitions_submit_not_main_movie(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--not-main-movie', '--nmm')] == {
        'help': 'Upload ONLY contains extras, Rifftrax, Workprints',
        'action': 'store_true',
    }


def test_PtpTrackerConfig_argument_definitions_submit_personal_rip(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--personal-rip', '--pr')] == {
        'help': 'Tag as your own encode',
        'action': 'store_true',
    }


def test_PtpTrackerConfig_argument_definitions_submit_screenshots(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--screenshots', '--ss')] == {
        'help': 'How many screenshots to make per video file',
        'type': utils.argtypes.number_of_screenshots(min=1, max=10),
    }


def test_PtpTrackerConfig_argument_definitions_submit_upload_token(tracker_config):
    assert tracker_config.argument_definitions['submit'][('--upload-token', '--ut')] == {
        'help': 'Upload token from staff',
    }
