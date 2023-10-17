"""
Find, download and re-upload poster for movie, series or season
"""

import os

from .. import errors, utils
from . import JobBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PosterJob(JobBase):
    """
    Find poster image on a :mod:`webdb <upsies.utils.webdbs>`, download it and
    optionally upload it to :mod:`image host <upsies.utils.imghosts>`

    This job adds the following signals to the :attr:`~.JobBase.signal`
    attribute:

        ``finding_poster``
            Emitted before `webdb` is queried for a poster. Registered
            callbacks get the ID of the release.

        ``found_poster``
            Emitted after the poster was found. Registered callbacks get the URL
            to the poster image as a positional argument.

        ``downloading_poster``
            Emitted before the poster is downloaded. Registered callbacks get
            the URL to the poster image as a positional argument.

        ``downloaded_poster``
            Emitted after the poster was downloaded. Registered callbacks get
            the file path to the downloaded poster image as a positional
            argument.

        ``resizing_poster``
            Emitted before the poster is resized. Registered callbacks get the
            file path to the original poster image as a positional argument.

        ``resized_poster``
            Emitted after the poster was resized. Registered callbacks get the
            file path to the resized poster image as a positional argument.

        ``uploading_poster``
            Emitted before the poster is uploaded. Registered callbacks get the
            file path to the resized poster image as a positional argument.

        ``uploaded_poster``
            Emitted after the poster is uploaded. Registered callbacks get the
            URL to the resized poster image as a positional argument.
    """

    name = 'poster'
    label = 'Poster'

    cache_id = None
    """
    This job doesn't cache its output

    If the created poster is deleted, its cached output path is still
    regurgitated even though it doesn't exist anymore.

    Everything is already cached by the utilities, except for the image
    resizing, which should be reasonably fast.
    """

    def initialize(self, *, webdb, webdb_id, season=None, imghost=None, width=512, height=1024):
        """
        Set internal state

        :param webdb: Instance of :class:`~.WebDbApiBase` subclass
        :param webdb_id: ID for `webdb`
        :param season: Season number or `None`
        :param imghost: Instance of :class:`~.ImageHostBase` subclass or `None`
        :param int width: Maximum poster width in pixels
        :param int height: Maximum poster height in pixels

        `webdb_id` and/or `webdb` can also be `None`. In that case, this job
        must be created with `autostart` set to False. `webdb_id` and/or `webdb`
        must then be passed as keyword arguments to :meth:`start`.
        """
        self._webdb = webdb
        self._webdb_id = webdb_id
        self._season = season
        self._imghost = imghost
        self._width = int(width)
        self._height = int(height)

        self.signal.add('finding_poster')
        self.signal.add('found_poster')
        self.signal.add('downloading_poster')
        self.signal.add('downloaded_poster')
        self.signal.add('resizing_poster')
        self.signal.add('resized_poster')
        self.signal.add('uploading_poster')
        self.signal.add('uploaded_poster')

    def start(self, *, webdb=None, webdb_id=None, season=None):
        """
        Same as :meth:`~.JobBase.start`, but with the added possibility of providing
        `webdb`, `webdb_id` and `season` after initialization
        """
        # Set internal states
        super().start()

        _log.debug('Starting poster job: %r, %r, %r', webdb, webdb_id, season)
        self.attach_task(
            coro=self._work(
                webdb=webdb or self._webdb,
                webdb_id=webdb_id or self._webdb_id,
                season=season or self._season,
            ),
            finish_when_done=True,
        )

    async def _work(self, webdb, webdb_id, season=None):
        original_url = await self._get_poster_url(webdb, webdb_id, season)
        if original_url:
            original_filepath = self._get_poster_filepath(webdb, webdb_id, season, original_url)
            original_filepath = await self._download_poster(original_url, original_filepath)
            if original_filepath:
                resized_filepath = self._resize_poster(original_filepath)
                if resized_filepath:
                    if self._imghost:
                        resized_url = await self._upload_poster(resized_filepath)
                        self.send(resized_url)
                    else:
                        self.send(resized_filepath)

    async def _get_poster_url(self, webdb, webdb_id, season):
        self.signal.emit('finding_poster', webdb_id)
        try:
            url = await webdb.poster_url(webdb_id, season=season)
        except errors.RequestError as e:
            self.error(f'Failed to find poster: {e}')
        else:
            if not url:
                self.error('Failed to find poster: There is no poster')
            else:
                _log.debug('Found poster for %s: %r', webdb_id, url)
                self.signal.emit('found_poster', url)
                return url

    def _get_poster_filepath(self, webdb, webdb_id, season, url):
        filename = f'{webdb.name}={utils.fs.sanitize_filename(webdb_id)}'
        if season:
            season = str(utils.release.Episodes.from_string(f'S{season}'))
            filename += f'.{season}'

        url_extension = utils.fs.file_extension(url)
        if url_extension:
            filename += f'.{url_extension}'

        return os.path.join(self.cache_directory, filename)

    async def _download_poster(self, url, filepath):
        self.signal.emit('downloading_poster', url)
        try:
            filepath_sanitized = await utils.http.download(
                url,
                filepath,
                cache=not self.ignore_cache,
            )
        except errors.RequestError as e:
            self.error(f'Failed to download poster: {e}')
        else:
            self.signal.emit('downloaded_poster', filepath_sanitized)
            return filepath_sanitized

    def _resize_poster(self, filepath):
        filename = '.'.join((
            utils.fs.basename(utils.fs.strip_extension(filepath)),
            f'{self._width}x{self._height}',
            utils.fs.file_extension(filepath),
        ))

        self.signal.emit('resizing_poster', filepath)
        try:
            resized_filepath = utils.image.resize(
                filepath,
                target_directory=self.home_directory,
                target_filename=filename,
                width=self._width,
                height=self._height,
            )
        except errors.ImageResizeError as e:
            self.error(f'Failed to resize poster: {e}')
        else:
            self.signal.emit('resized_poster', resized_filepath)
            return resized_filepath

    async def _upload_poster(self, filepath):
        self.signal.emit('uploading_poster', filepath)
        try:
            resized_url = await self._imghost.upload(filepath)
        except errors.RequestError as e:
            self.error(f'Failed to upload poster: {e}')
        else:
            self.signal.emit('uploaded_poster', resized_url)
            return resized_url
