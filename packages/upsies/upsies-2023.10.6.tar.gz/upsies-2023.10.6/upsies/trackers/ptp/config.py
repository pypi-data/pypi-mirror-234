"""
Concrete :class:`~.base.TrackerConfigBase` subclass for PTP
"""

import base64

from ...utils import argtypes, configfiles, imghosts, types
from ..base import TrackerConfigBase


class PtpTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly9wYXNzdGhlcG9wY29ybi5tZQ==').decode('ascii'),
        'username': '',
        'password': '',
        'announce_url': configfiles.config_value(
            value='',
            description='Your personal announce URL.',
        ),
        'source': 'PTP',
        'image_host': types.Choice('ptpimg', options=imghosts.imghost_names()),
        'screenshots_from_movie': configfiles.config_value(
            value=types.Integer(3, min=3, max=10),
            description='How many screenshots to make for single-video uploads.',
        ),
        'screenshots_from_episode': configfiles.config_value(
            value=types.Integer(2, min=2, max=10),
            description='How many screenshots to make per video for multi-video uploads.',
        ),
        'exclude': (
            r'\.(?i:nfo|txt|jpg|jpeg|png|sfv|md5|sub|idx|srt)$',
            r'/(?i:sample|extra|bonus|feature)',
            r'(?i:.*sample\.[a-z]+)$',
        ),
    }

    argument_definitions = {
        'submit': {
            ('--hardcoded-subtitles', '--hs'): {
                'help': 'Video contains hardcoded subtitles',
                'action': 'store_true',
            },
            ('--not-main-movie', '--nmm'): {
                'help': 'Upload ONLY contains extras, Rifftrax, Workprints',
                'action': 'store_true',
            },
            ('--personal-rip', '--pr'): {
                'help': 'Tag as your own encode',
                'action': 'store_true',
            },
            ('--screenshots', '--ss'): {
                'help': 'How many screenshots to make per video file',
                'type': argtypes.number_of_screenshots(min=1, max=10),
            },
            ('--upload-token', '--ut'): {
                'help': 'Upload token from staff',
            },
            ('--only-description', '--od'): {
                'help': 'Only generate description (do not upload anything)',
                'action': 'store_true',
                'group': 'generate-metadata',
            },
        },
    }
