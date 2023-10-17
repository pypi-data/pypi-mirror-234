"""
Provide :mod:`aiobtclientapi` APIs
"""

import aiobtclientapi
import aiobtclientrpc

from .. import errors, utils


def client_names():
    """
    Return sequence of valid `client_name` values that may be passed to
    :class:`BittorrentClient`
    """
    return aiobtclientapi.client_names()


def client_defaults(client_name):
    """
    Create default client configuration

    :param client_name: Name of the client (see :func:`client_names`)

    The return value is a :class:`dict` with the following keys:

        - ``url``
        - ``username``
        - ``password``
        - ``check_after_add``

    If `client_name` is ``"qbittorrent"``, there is also a ``category`` key.
    """
    for cls in aiobtclientapi.api_classes():
        if cls.name == client_name:
            config = {
                'url': cls.URL.default,
                'username': '',
                'password': '',
                'check_after_add': utils.configfiles.config_value(
                    value=utils.types.Bool('no'),
                    description=(
                        'Whether added torrents should be hash checked'
                        + (
                            '\nNOTE: This has no effect for Transmission, which makes this decision on its own.'
                            if cls.name == 'transmission' else
                            ''
                        )
                    ),
                ),
            }

            if cls.name == 'qbittorrent':
                # Only qBittorrent has categories
                config['category'] = utils.configfiles.config_value(
                    value='',
                    description='Add added torrents to this category',
                )
            return config


class BtClient:
    """
    Thin wrapper class around a :class:`aiobtclientapi.APIBase` subclass

    :param name: Name of the client (see
        :func:`aiobtclientapi.names`)
    :param url: How to connect to the client API
    :param username: API password for authentication
    :param password: API password for authentication
    :param download_path: Where to download added torrents to
    :param check_after_add: Verify added torrents if content already exists
    :param category: Add torrents to this category if the client supports
        categories
    """

    def __init__(self, name, *, url, username, password, download_path, check_after_add, category=''):
        self._api = aiobtclientapi.api(
            name=name,
            url=url,
            username=username,
            password=password,
        )
        self._download_path = download_path
        self._check_after_add = check_after_add
        self._category = category

    @property
    def name(self):
        """Name of the client (same as :attr:`aiobtclientrpc.RPCBase.name`)"""
        return self._api.name

    @property
    def label(self):
        """Label of the client (same as :attr:`aiobtclientrpc.RPCBase.label`)"""
        return self._api.label

    async def add_torrent(self, torrent):
        """
        Add `torrent` to client

        :param torrent: ``.torrent`` file/URL, magnet link or infohash
        """
        response = await self._api.add(
            torrent,
            location=self._download_path,
            verify=self._check_after_add,
        )

        for error in response.errors:
            raise errors.TorrentAddError(response.errors[0])
        else:
            infohash = (response.added + response.already_added)[0]

            if self._category:
                await self._set_category(infohash, str(self._category))

            return infohash

    async def _set_category(self, infohash, category):
        if self._api.name != 'qbittorrent':
            raise RuntimeError(f'Categories are not supported for {self._api.label}')
        else:
            try:
                await self._api.call(
                    'torrents/setCategory',
                    hashes=infohash,
                    category=str(self._category),
                )
            except aiobtclientrpc.RPCError as e:
                if 'incorrect category name' in str(e).lower():
                    raise errors.TorrentAddError(f'Unknown category: {self._category}')
                else:
                    raise e
