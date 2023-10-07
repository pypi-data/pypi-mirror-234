"""
Exception classes

Abstraction layers should raise one of these exceptions if an error message
should be displayed to the user. If the programmer made a mistake, any
appropriate builtin exception (e.g. :class:`ValueError`, :class:`TypeError`) or
:class:`RuntimeError` should be raised.

For example, :func:`~.utils.http.get` always raises :class:`RequestError`,
regardless of which library is used or what went wrong, except when something
like caching fails, which is most likely due to a bug.
"""

import json

_NO_DEFAULT_VALUE = object()


class UpsiesError(Exception):
    """Base class for all exceptions raised by upsies"""

    def __eq__(self, other):
        if isinstance(other, type(self)) and str(other) == str(self):
            return True
        else:
            return NotImplemented


class ConfigError(UpsiesError):
    """Error while reading/writing config file or setting config file option"""


class UiError(UpsiesError):
    """Fatal user interface error that cannot be handled by the UI itself"""


class DependencyError(UpsiesError):
    """Some external tool is missing (e.g. ``mediainfo``)"""


class ContentError(UpsiesError):
    """
    Something is wrong with user-provided content, e.g. no video files in the
    given directory or no permission to read
    """

class ProcessError(UpsiesError):
    """Executing subprocess failed"""


class RequestError(UpsiesError):
    """Network request failed"""
    def __init__(self, msg, url='', headers={}, status_code=None, text=''):
        super().__init__(msg)
        self._url = url
        self._headers = headers
        self._status_code = status_code
        self._text = text

    @property
    def url(self):
        """URL that produced this exception"""
        return self._url

    @property
    def headers(self):
        """HTTP headers from server response or empty `dict`"""
        return self._headers

    @property
    def status_code(self):
        """HTTP status code (e.g. 404) or `None`"""
        return self._status_code

    @property
    def text(self):
        """Response string if available"""
        return self._text

    def json(self, default=_NO_DEFAULT_VALUE):
        """
        Parse the :attr:`text` as JSON

        :param default: Return value if :attr:`text` is not valid JSON

        :raise RequestError: if :attr:`text` is not proper JSON and `default` is
            not given
        """
        try:
            return json.loads(self.text)
        except ValueError as e:
            if default is _NO_DEFAULT_VALUE:
                raise RequestError(f'Malformed JSON: {str(self.text)}: {e}')
            else:
                return default


class ScreenshotError(UpsiesError):
    """Screenshot creation failed"""


class ImageResizeError(UpsiesError):
    """Image resizing failed"""


class ImageOptimizeError(UpsiesError):
    """Image optimization failed"""


class TorrentCreateError(UpsiesError):
    """Torrent file creation failed"""


class TorrentAddError(UpsiesError):
    """Adding torrent to client failed"""


def SubprocessError(exception, original_traceback):
    """Attach `original_traceback` to `exception`"""
    exception.original_traceback = f'Subprocess traceback:\n{original_traceback.strip()}'
    return exception


class SceneError(UpsiesError):
    """Base class for scene-related errors"""

class SceneRenamedError(SceneError):
    """Renamed scene release"""
    def __init__(self, *, original_name, existing_name):
        super().__init__(f'{existing_name} should be named {original_name}')
        self._original_name = original_name
        self._existing_name = existing_name

    @property
    def original_name(self):
        """What the release name should be"""
        return self._original_name

    @property
    def existing_name(self):
        """What the release name is"""
        return self._existing_name

class SceneFileSizeError(SceneError):
    """Scene release file size differs from original release"""
    def __init__(self, filename, *, original_size, existing_size):
        super().__init__(f'{filename} should be {original_size} bytes, not {existing_size}')
        self._filename = filename
        self._original_size = original_size
        self._existing_size = existing_size

    @property
    def filename(self):
        """Name of the file in the scene release"""
        return self._filename

    @property
    def original_size(self):
        """Size of the file in the scene release"""
        return self._original_size

    @property
    def existing_size(self):
        """Size of the file in the local file system"""
        return self._existing_size

class SceneMissingInfoError(UpsiesError):
    """Missing information about a file from a scene release"""
    def __init__(self, file_name):
        super().__init__(f'Missing information: {file_name}')

class SceneAbbreviatedFilenameError(UpsiesError):
    """
    An abbreviated scene file name (e.g. foo-bar.mkv) was provided

    These contain almost no information and should always be provided via a
    properly named parent directory.
    """
    def __init__(self, file_name):
        super().__init__(f'Abbreviated scene file name is verboten: {file_name}')


class FoundDupeError(RequestError):
    """
    Tried to upload files that have already been uploaded

    :param filenames: Sequence of file names that have already been uploaded
    """
    def __init__(self, filenames):

        if not filenames:
            msg = ['Potential duplicate files found']

        else:
            files_count = len(filenames)
            if files_count != 1:
                msg = [f'{files_count} potential duplicate files found']
            else:
                msg = ['1 potential duplicate file found']

            msg.append(':\n - ')
            msg.append('\n - '.join(filenames))

        super().__init__(''.join(msg))


class AnnounceUrlNotSetError(RequestError):
    """Announce URL is required but not provided by the user"""
    def __init__(self, *_, tracker):
        super().__init__('Announce URL is not set')
        self._tracker = tracker

    @property
    def tracker(self):
        """:attr:`~.TrackerBase` instance that raised this exception"""
        return self._tracker
