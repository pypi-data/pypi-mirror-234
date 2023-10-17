"""
Concrete :class:`~.base.TrackerConfigBase` subclass for MTV
"""

import base64

from ...utils import argtypes, configfiles, imghosts, types
from ..base import TrackerConfigBase


class MtvTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly93d3cubW9yZXRoYW50di5tZQ==').decode('ascii'),
        'username': '',
        'password': '',
        'announce_url': configfiles.config_value(
            value='',
            description='Your personal announce URL. Automatically fetched from the website if not set.',
        ),
        'source': 'MTV',
        'image_host': types.Choice('imgbox', options=imghosts.imghost_names()),
        'screenshots': configfiles.config_value(
            value=types.Integer(4, min=3, max=10),
            description='How many screenshots to make.',
        ),
        'exclude': (
            r'\.(?i:nfo|txt|jpg|jpeg|png|sfv|md5)$',
            r'/(?i:sample|extra|bonus|feature)',
            r'(?i:.*sample\.[a-z]+)$',
        ),
        'anonymous': configfiles.config_value(
            value=types.Bool('no'),
            description='Whether your username is displayed on your uploads.',
        ),
    }

    argument_definitions = {
        'submit': {
            ('--screenshots', '--ss'): {
                'help': ('How many screenshots to make '
                         f'(min={defaults["screenshots"].min}, '
                         f'max={defaults["screenshots"].max})'),
                'type': argtypes.number_of_screenshots(
                    min=defaults['screenshots'].min,
                    max=defaults['screenshots'].max,
                ),
            },
            ('--only-description', '--od'): {
                'help': 'Only generate description (do not upload anything)',
                'action': 'store_true',
                'group': 'generate-metadata',
            },
            ('--only-title', '--ot'): {
                'help': 'Only generate title (do not upload anything)',
                'action': 'store_true',
                'group': 'generate-metadata',
            },
            ('--ignore-dupes', '--id'): {
                'help': 'Force submission even if the tracker reports duplicates',
                'action': 'store_true',
            },
        },
    }
