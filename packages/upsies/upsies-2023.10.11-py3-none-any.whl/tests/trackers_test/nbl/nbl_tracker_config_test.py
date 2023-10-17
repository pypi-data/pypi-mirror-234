import base64

import pytest

from upsies.trackers.nbl import NblTrackerConfig


@pytest.fixture
def tracker_config():
    return NblTrackerConfig()


def test_NblTrackerConfig_defaults(tracker_config):
    assert set(tracker_config) == {
        'upload_url',
        'announce_url',
        'apikey',
        'source',
        'randomize_infohash',
        'exclude',

        # Inherited from TrackerConfigBase
        'add_to',
        'copy_to',
    }


def test_NblTrackerConfig_defaults_base_url(tracker_config):
    assert tracker_config['upload_url'] == base64.b64decode('aHR0cHM6Ly9uZWJ1bGFuY2UuaW8vdXBsb2FkLnBocA==').decode('ascii')


def test_NblTrackerConfig_defaults_password(tracker_config):
    assert tracker_config['apikey'] == ''
    assert tracker_config['apikey'].description == (
        'Your personal private API key.\n'
        'Get it from the website: <USERNAME> -> Settings -> API keys'
    )


def test_NblTrackerConfig_defaults_announce_url(tracker_config):
    assert tracker_config['announce_url'] == ''
    assert tracker_config['announce_url'].description == (
        'The complete announce URL with your private passkey.\n'
        'Get it from the website: Shows -> Upload -> Your personal announce URL'
    )


def test_NblTrackerConfig_defaults_source(tracker_config):
    assert tracker_config['source'] == 'NBL'


def test_NblTrackerConfig_defaults_exclude(tracker_config):
    assert tracker_config['exclude'] == ()


def test_NblTrackerConfig_argument_definitions(tracker_config):
    assert tracker_config.argument_definitions == {}
