"""
Concrete :class:`~.base.TrackerBase` subclass for PTP
"""

import math
import re
import urllib

from ... import errors, utils
from ..base import TrackerBase
from .config import PtpTrackerConfig
from .jobs import PtpTrackerJobs

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PtpTracker(TrackerBase):
    name = 'ptp'
    label = 'PTP'

    setup_howto_template = (
        '{howto.introduction}\n'
        '\n'
        '{howto.current_section}. Login Credentials\n'
        '\n'
        '   {howto.current_section}.1 $ upsies set trackers.ptp.username USERNAME\n'
        '   {howto.current_section}.2 $ upsies set trackers.ptp.password PASSWORD\n'
        '{howto.bump_section}'
        '\n'
        '{howto.current_section}. Announce URL\n'
        '\n'
        '   The announce URL is required because the passkey is used for 2FA.\n'
        '\n'
        '   {howto.current_section}.1 $ upsies set trackers.ptp.announce_url ANNOUNCE_URL\n'
        '{howto.bump_section}'
        '\n'
        '{howto.current_section}. Screenshots\n'
        '\n'
        '   {howto.current_section}.1 Configure ptpimg.me API\n'
        '       $ upsies upload-images ptpimg --help\n'
        '\n'
        '   {howto.current_section}.2 Specify how many screenshots to make. (optional)\n'
        '       $ upsies set trackers.ptp.screenshots_from_movie NUMBER_OF_MOVIE_SCREENSHOTS\n'
        '       $ upsies set trackers.ptp.screenshots_from_episode NUMBER_OF_EPISODE_SCREENSHOTS\n'
        '{howto.bump_section}'
        '\n'
        '{howto.autoseed}\n'
        '\n'
        '{howto.upload}\n'
    )

    TrackerConfig = PtpTrackerConfig
    TrackerJobs = PtpTrackerJobs

    @property
    def _base_url(self):
        return self.options['base_url']

    @property
    def _ajax_url(self):
        return urllib.parse.urljoin(self._base_url, '/ajax.php')

    @property
    def _logout_url(self):
        return urllib.parse.urljoin(self._base_url, '/logout.php')

    @property
    def _upload_url(self):
        return urllib.parse.urljoin(self._base_url, '/upload.php')

    @property
    def _torrents_url(self):
        return urllib.parse.urljoin(self._base_url, '/torrents.php')

    @property
    def _announce_url(self):
        announce_url = self.options['announce_url']
        if not announce_url:
            raise errors.AnnounceUrlNotSetError(tracker=self)
        else:
            return self.options['announce_url']

    @property
    def _passkey(self):
        # Needed for logging in with ajax.php
        match = re.search(r'.*/([a-zA-Z0-9]+)/announce', self._announce_url)
        if match:
            return match.group(1)
        else:
            raise RuntimeError(f'Failed to find passkey in announce URL: {self._announce_url}')

    async def _request(self, method, *args, error_prefix='', **kwargs):
        # Because HTTP errors (e.g. 404) are raised, we treat RequestErrrors as
        # normal response so we can get the message from the HTML.
        try:
            # `method` is "GET" or "POST"
            response = await getattr(utils.http, method.lower())(
                *args,
                user_agent=True,
                follow_redirects=False,
                **kwargs,
            )
        except errors.RequestError as e:
            response = e

        # Get error from regular exception (e.g. "Connection refused") or the
        # HTML in response.
        try:
            self._maybe_raise_error(response)
        except errors.RequestError as e:
            # Prepend error_prefix to explain the general nature of the error.
            if error_prefix:
                raise errors.RequestError(f'{error_prefix}: {e}')
            else:
                raise e
        else:
            return response

    def _maybe_raise_error(self, response_or_request_error):
        # utils.http.get()/post() raise RequestError on HTTP status codes, but
        # we want to get the error message from the response text.
        # _maybe_raise_error_from_*() handle Response and RequestError.
        self._maybe_raise_error_from_json(response_or_request_error)
        self._maybe_raise_error_from_html(response_or_request_error)

        # If we got a RequestError and we didn't find an error message in the
        # text, we raise it. This handles any real RequestErrors, like
        # "Connection refused". We also raise any other exception so _request()
        # doesn't return it as a regular response.
        if isinstance(response_or_request_error, BaseException):
            raise response_or_request_error

    def _maybe_raise_error_from_json(self, response_or_request_error):
        # Get error message from ajax.php JSON Response or RequestError
        try:
            json = response_or_request_error.json()
        except errors.RequestError:
            # Response or RequestError is not JSON
            pass
        else:
            if (
                isinstance(json, dict)
                and json.get('Result') == 'Error'
                and json.get('Message')
            ):
                raise errors.RequestError(utils.html.as_text(json['Message']))

    def _maybe_raise_error_from_html(self, response_or_request_error):
        # Only attempt to find an error message if this looks like HTML. This
        # prevents a warning from bs4 about parsing non-HTML.
        text = str(response_or_request_error)
        if all(c in text for c in '<>\n'):
            doc = utils.html.parse(text)
            try:
                error_header_tag = doc.select('#content .page__title', string=re.compile(r'(?i:error)'))
                error_container_tag = error_header_tag[0].parent
                error_msg_tag = error_container_tag.find('div', attrs={'class': 'panel__body'})
                error_msg = error_msg_tag.get_text().strip()
                if error_msg:
                    raise errors.RequestError(error_msg)
            except (AttributeError, IndexError):
                # No error message found
                pass

    def _get_anti_csrf_token(self, response):
        json = response.json()
        try:
            return json['AntiCsrfToken']
        except KeyError:
            _log.debug('Failed to find "AntiCsrfToken": %r', response)
            raise

    async def _get_auth(self):
        assert self.is_logged_in
        response = await self._request('GET', self._base_url)
        doc = utils.html.parse(response)
        auth_regex = re.compile(r'logout\.php\?.*\bauth=([0-9a-fA-F]+)')
        logout_link_tag = doc.find('a', href=auth_regex)
        if logout_link_tag:
            logout_link_href = logout_link_tag['href']
            match = auth_regex.search(logout_link_href)
            return match.group(1)

        raise RuntimeError('Could not find auth')

    async def _login(self):
        if not self.options.get('username'):
            raise errors.RequestError('Login failed: No username configured')
        elif not self.options.get('password'):
            raise errors.RequestError('Login failed: No password configured')

        _log.debug('%s: Logging in as %r', self.name, self.options['username'])
        post_data = {
            'username': self.options['username'],
            'password': self.options['password'],
            'passkey': self._passkey,
            # 'keeplogged': '1',
        }
        response = await self._request(
            method='POST',
            url=f'{self._ajax_url}?action=login',
            data=post_data,
            error_prefix='Login failed',
        )
        self._anti_csrf_token = self._get_anti_csrf_token(response)

    async def _logout(self):
        try:
            _log.debug('%s: Logging out', self.name)
            await self._request(
                method='GET',
                url=self._logout_url,
                params={'auth': await self._get_auth()},
                error_prefix='Logout failed',
            )

        finally:
            if hasattr(self, '_anti_csrf_token'):
                delattr(self, '_anti_csrf_token')

    async def get_announce_url(self):
        return self._announce_url

    async def upload(self, tracker_jobs):
        post_data = tracker_jobs.post_data.copy()
        post_data['AntiCsrfToken'] = self._anti_csrf_token

        _log.debug('POSTing data:')
        for k, v in post_data.items():
            _log.debug(' * %s = %s', k, v)

        post_files = {
            'file_input': {
                'file': tracker_jobs.torrent_filepath,
                'mimetype': 'application/x-bittorrent',
            },
        }
        _log.debug('POSTing files: %r', post_files)

        response = await utils.http.post(
            url=self._upload_url,
            cache=False,
            user_agent=True,
            data=post_data,
            files=post_files,
            # Ignore the HTTP redirect (should be 302 Found) so we can get the
            # torrent URL from the "Location" response header
            follow_redirects=False,
        )

        # # Read previously received response for debugging
        # response_filepath = 'ptp_upload.response.content'
        # response = utils.http.Response(
        #     text=open(response_filepath).read(),
        #     bytes=open(response_filepath).read().encode('utf8'),
        # )

        return self._handle_upload_response(response)

    def _handle_upload_response(self, response):
        # "Location" header should contain the uploaded torrent's URL
        _log.debug('Upload response headers: %r', response.headers)
        location = response.headers.get('Location')
        _log.debug('Upload response location: %r', location)
        if location:
            torrent_page_url = urllib.parse.urljoin(self.options['base_url'], location)
            # Redirect URL should start with "https://.../torrents.php"
            if torrent_page_url.startswith(self._torrents_url):
                return torrent_page_url

        # Find error message in HTML
        doc = utils.html.parse(response)

        # Find and raise error message
        alert_tag = doc.find(class_='alert')
        if alert_tag:
            msg = utils.html.as_text(alert_tag)
            raise errors.RequestError(f'Upload failed: {msg}')

        # Failed to find error message
        dump_filepath = 'ptp_upload_failed.html'
        utils.html.dump(response, dump_filepath)
        raise errors.RequestError(f'Failed to interpret response (see {dump_filepath})')

    def normalize_imdb_id(self, imdb_id):
        """
        Format IMDb ID for PTP

        PTP expects 7-characters, right-padded with "0" and without the leading
        "tt".

        If `imdb_id` is falsy (e.g. `None`, empty string, etc), or if it isn't
        an IMDb ID, return "0".
        """
        imdb_id = str(imdb_id)
        match = re.search(r'^(?:tt|)(\d+)$', imdb_id)
        if match:
            imdb_id_digits = match.group(1)
            if set(imdb_id_digits) != {'0'}:
                return match.group(1).rjust(7, '0')
        return '0'

    async def get_ptp_group_id_by_imdb_id(self, imdb_id):
        """
        Convert IMDb ID to PTP group ID

        Any :class:`~.RequestError` is caught and passed to
        :meth:`.TrackerBase.error`.

        :return: PTP group ID or `None` if PTP doesn't have a group for
            `imdb_id`
        """
        _log.debug('%s: Fetching PTP group ID', imdb_id)
        try:
            await self.login()
            response = await self._request(
                method='GET',
                url=self._torrents_url,
                params={
                    'imdb': self.normalize_imdb_id(imdb_id),
                    'json': '1',
                },
                cache=True,
            )

        except errors.RequestError as e:
            self.error(e)

        else:
            match = re.search(r'id=(\d+)', response.headers.get('location', ''))
            if match:
                _log.debug('%s: PTP group ID: %s', imdb_id, match.group(1))
                return match.group(1)
            else:
                _log.debug('%s: No PTP group ID', imdb_id)

    async def get_ptp_metadata(self, imdb_id, key=None):
        """
        Get metadata from PTP website

        Any :class:`~.RequestError` is caught and passed to
        :meth:`.TrackerBase.error`.

        :param imdb_id: IMDb ID (e.g. ``tt123456``)
        """
        if key:
            _log.debug('%s: Fetching %s from PTP', imdb_id, key)
        else:
            _log.debug('%s: Fetching metadata from PTP', imdb_id)

        assert imdb_id, imdb_id

        try:
            await self.login()
            response = await self._request(
                method='GET',
                url=self._ajax_url,
                params={
                    'action': 'torrent_info',
                    'imdb': self.normalize_imdb_id(imdb_id),
                },
                cache=True,
            )
            # Raise RequestError if response is not valid JSON
            results = response.json()

        except errors.RequestError as e:
            self.error(e)

        else:
            assert len(results) == 1
            if key is None:
                _log.debug('%s: PTP metadata: %s', imdb_id, results[0])
                return results[0]
            else:
                _log.debug('%s: PTP %s: %s', imdb_id, key, results[0][key])
                return results[0][key]

    @staticmethod
    def calculate_piece_size(bytes):
        """
        Return the recommended piece size for a given content size

        :param bytes: Torrent's content size

            .. note:: Remember to exclude files that exist but won't be in the
                torrent (e.g. extras or ``*.nfo``).
        """
        exponent = math.ceil(math.log2(bytes / 1050))
        # Allowed piece size range: 32 KiB ... 16 MiB
        exponent = max(15, min(24, exponent))
        return int(math.pow(2, exponent))

    @staticmethod
    def calculate_piece_size_min_max(bytes):
        """
        Return the allowed minimum and maximum piece size for a given
        content size

        :param bytes: Torrent's content size

            .. note:: Remember to exclude files that exist but won't be in the
                torrent (e.g. extras or ``*.nfo``).

        :raise ValueError: if `bytes` is negative or otherwise unexpected
        """
        if bytes <= 0:
            raise ValueError(f'Unexpected size: {bytes!r}')

        # NOTE: The algorithm below is from the website's javascript.

        max_exponent = math.ceil(math.log2(bytes / 500))
        min_exponent = math.floor(math.log2(bytes / 2000))

        # 2^24 or 16MiB is the max for uTorrent 2.x
        min_exponent = min(24, min_exponent)
        max_exponent = min(24, max_exponent)

        # Compatibility for uTorrent 2.x creator which only supports up to 4 MiB piece sizes
        if min_exponent > 22 and bytes <= 128 * 1024 * 1024 * 1024:
            min_exponent = 22
        if min_exponent > 22 and bytes <= 256 * 1024 * 1024 * 1024:
            min_exponent = 23

        # Tiny torrents < ~40MiB need a sane lower bound
        min_exponent = max(15, min_exponent)
        max_exponent = max(18, max_exponent)

        return (
            math.pow(2, min_exponent),
            math.pow(2, max_exponent),
        )
