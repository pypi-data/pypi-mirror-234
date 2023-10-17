"""
Base class for tracker configuration
"""

from ... import utils

import logging  # isort:skip
_log = logging.getLogger(__name__)


class TrackerConfigBase(dict):
    """
    Dictionary with default values that are defined by the subclass

    Some keys defined by this base class always exist.
    """

    # Options that are available for all trackers
    _common_defaults = {
        'source': utils.configfiles.config_value(
            value='',
            description='Value of the "source" field in generated torrents.',
        ),
        'randomize_infohash': utils.configfiles.config_value(
            value=utils.types.Bool('no'),
            description=(
                'Whether the info hash of generated torrents is randomized '
                'by including a random number in the metadata.\n'
                'WARNING: The tracker may choke on the non-standard field '
                'or remove the random number, forcing you to manually download '
                'the torrent.'
            ),
        ),
        'exclude': utils.configfiles.config_value(
            value=utils.types.ListOf(
                item_type=utils.types.RegEx,
                iterable=(),
            ),
            description='List of regular expressions. Matching files are excluded from generated torrents.',
        ),
        'add_to': utils.configfiles.config_value(
            value=utils.types.Choice(
                value='',
                empty_ok=True,
                options=utils.btclient.client_names(),
            ),
            description='BitTorrent client to add torrent to after submission.',
        ),
        'copy_to': utils.configfiles.config_value(
            value='',
            description='Directory path to copy torrent to after submission.',
        ),
    }

    defaults = {}
    """Default values"""

    argument_definitions = {}
    """CLI argument definitions (see :attr:`.CommandBase.argument_definitions`)"""

    def __new__(cls, config={}):
        # Merge generic and tracker-specific defaults
        combined_defaults = cls._merge(cls._common_defaults, cls.defaults)

        # Check user-given config for unknown options
        for k in config:
            if k not in combined_defaults:
                raise ValueError(f'Unknown option: {k!r}')

        # Merge user-given config with defaults
        self = super().__new__(cls)
        self.update(cls._merge(combined_defaults, config))
        return self

    @staticmethod
    def _merge(a, b):
        # Copy a
        combined = {}
        combined.update(a)

        # Update a with values from b
        for k, v in b.items():
            if k in combined:
                # Ensure same value type from a
                cls = type(combined[k])
                combined[k] = cls(v)
            else:
                # Append new value
                combined[k] = v

        return combined

    # If the config is passed as config={...}, super().__init__() will interpret
    # as a key-value pair that ends up in the config.
    def __init__(cls, *args, **kwargs):
        pass
