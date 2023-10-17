"""
Video metadata
"""

import collections
import functools
import glob
import json
import os
import re

from .. import constants, errors, utils
from . import closest_number, fs, os_family, release, subproc

import logging  # isort:skip
_log = logging.getLogger(__name__)

natsort = utils.LazyModule(module='natsort', namespace=globals())


NO_DEFAULT_VALUE = object()


if os_family() == 'windows':
    _mediainfo_executable = 'mediainfo.exe'
    _ffprobe_executable = 'ffprobe.exe'
else:
    _mediainfo_executable = 'mediainfo'
    _ffprobe_executable = 'ffprobe'


@functools.lru_cache(maxsize=None)
def _run_mediainfo(video_file_path, *args):
    fs.assert_file_readable(video_file_path)
    cmd = (_mediainfo_executable, video_file_path) + args

    # Translate DependencyError to ContentError so callers have to expect less
    # exceptions. Do not catch ProcessError because things like wrong mediainfo
    # arguments are bugs.
    try:
        return subproc.run(cmd, cache=True)
    except errors.DependencyError as e:
        raise errors.ContentError(e)


@functools.lru_cache(maxsize=None)
def mediainfo(path, only_first=True):
    """
    ``mediainfo`` output as a string

    The parent directory of `path` is redacted.

    :param str path: Path to video file or directory
    :param bool only_first: Whether to return mediainfo for each video file as a
        :class:`list` or to return mediainfo of the first video file (see
        :func:`find_videos`)

    :raise ContentError: if anything goes wrong
    """
    def remove_parent_directory(mi, parent_directory=utils.fs.dirname(path)):
        if parent_directory:
            return mi.replace(parent_directory + os.sep, '')
        else:
            return mi

    unique_id_default = 'Unique ID                                : 0 (0x0)'
    unique_id_regex = re.compile(r'^Unique ID\s*:\s*\d+', flags=re.MULTILINE)

    def ensure_unique_id_exists(mi):
        # Some mediainfo parsers expect a unique ID, but it doesn't always exist.
        if unique_id_regex.search(mi):
            return mi
        else:
            assert mi.startswith('General\n')
            return (
                mi[:len('General\n')]
                + unique_id_default + '\n'
                + mi[len('General\n'):]
            )

    def apply_fixes(mi):
        return remove_parent_directory(
            ensure_unique_id_exists(mi)
        )

    if not os.path.isdir(path):
        # If we get a file path, don't complain if it's not a video file. This
        # allows us to get mediainfo for .IFO files even though they are not
        # videos.
        mediainfo = _run_mediainfo(path)
        return apply_fixes(mediainfo)

    elif only_first:
        video_file = find_videos(path)[0]
        mediainfo = _run_mediainfo(video_file)
        return apply_fixes(mediainfo)

    else:
        video_files = find_videos(path)
        mediainfos = []
        for video_file in video_files:
            mediainfo = _run_mediainfo(video_file)
            mediainfos.append(apply_fixes(mediainfo))
        return mediainfos


@functools.lru_cache(maxsize=None)
def duration(path, default=NO_DEFAULT_VALUE):
    """
    Return video duration in seconds (float) or ``0.0`` if it can't be
    determined

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if anything goes wrong
    """
    if not os.path.exists(path) and default is not NO_DEFAULT_VALUE:
        return default
    return _duration(find_videos(path)[0])

def _duration(video_file_path):
    try:
        return _duration_from_ffprobe(video_file_path)
    except (RuntimeError, errors.DependencyError, errors.ProcessError):
        return _duration_from_mediainfo(video_file_path)

def _duration_from_ffprobe(video_file_path):
    cmd = (
        _ffprobe_executable,
        '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        make_ffmpeg_input(video_file_path),
    )
    length = subproc.run(cmd, ignore_errors=True)
    try:
        return float(length.strip())
    except ValueError:
        raise RuntimeError(f'Unexpected output from {cmd}: {length!r}')

def _duration_from_mediainfo(video_file_path):
    tracks = _tracks(video_file_path)
    try:
        return float(tracks['General'][0]['Duration'])
    except (KeyError, IndexError, TypeError, ValueError):
        raise RuntimeError(f'Unexpected tracks from {video_file_path}: {tracks!r}')


@functools.lru_cache(maxsize=None)
def tracks(path, default=NO_DEFAULT_VALUE):
    """
    ``mediainfo --Output=JSON`` as dictionary that maps each track's ``@type``
    to a list of the tracks

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if anything goes wrong
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    try:
        main_videos = find_videos(path)
    except errors.ContentError:
        # No video file found - use path as is. This allows us to get tracks
        # from an .IFO file, which isn't a video, so find_videos() raises
        # ContentError. _tracks()/_run_mediainfo() will still raise ContentError
        # if `path` mediainfo can't handle it.
        video_filepath = path
    else:
        video_filepath = main_videos[0]

    return _tracks(video_filepath)

def _tracks(video_file_path):
    stdout = _run_mediainfo(video_file_path, '--Output=JSON')
    tracks = {}
    try:
        for track in json.loads(stdout)['media']['track']:
            if track['@type'] not in tracks:
                tracks[track['@type']] = []
            tracks[track['@type']].append(track)
        return tracks
    except (ValueError, TypeError) as e:
        raise RuntimeError(f'{video_file_path}: Unexpected mediainfo output: {stdout}: {e}')
    except KeyError as e:
        raise RuntimeError(f'{video_file_path}: Unexpected mediainfo output: {stdout}: Missing field: {e}')


@functools.lru_cache(maxsize=None)
def default_track(type, path, default=NO_DEFAULT_VALUE):
    """
    Return default track

    :param str type: "video", "audio" or "text"
    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist or doesn't have a
        `type` track

         If this is not provided, raise :exc:`~.ContentError`.

    :raise ContentError: if anything goes wrong and `default` is not provided
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    all_tracks = tracks(path)

    # Find track marked as default
    try:
        for track in all_tracks[type.capitalize()]:
            if track.get('Default') == 'Yes':
                return track
    except KeyError:
        pass

    # Default to first track
    try:
        return all_tracks[type.capitalize()][0]
    except (KeyError, IndexError):
        pass

    if default is NO_DEFAULT_VALUE:
        raise errors.ContentError(f'{path}: No {type.lower()} track found: {all_tracks!r}')
    else:
        return default


@functools.lru_cache(maxsize=None)
def width(path, default=NO_DEFAULT_VALUE):
    """
    Return displayed width of video file `path`

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if width can't be determined
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    video_track = default_track('video', path)
    return _get_display_width(video_track)

def _get_display_width(video_track):
    try:
        width = int(video_track['Width'])
    except (KeyError, ValueError, TypeError):
        raise errors.ContentError('Unable to determine video width')
    else:
        _log.debug('Stored width: %r', width)
        # Actual aspect ratio may differ from display aspect ratio,
        # e.g. 960 x 534 is scaled up to 1280 x 534
        par = float(video_track.get('PixelAspectRatio') or 1.0)
        if par > 1.0:
            _log.debug('Display width: %r * %r = %r', width, par, width * par)
            width = width * par
        return int(width)


@functools.lru_cache(maxsize=None)
def height(path, default=NO_DEFAULT_VALUE):
    """
    Return displayed height of video file `path`

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if height can't be determined
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    video_track = default_track('video', path)
    return _get_display_height(video_track)

def _get_display_height(video_track):
    try:
        height = int(video_track['Height'])
    except (KeyError, ValueError, TypeError):
        raise errors.ContentError('Unable to determine video height')
    else:
        _log.debug('Stored height: %r', height)
        # Actual aspect ratio may differ from display aspect ratio,
        # e.g. 960 x 534 is scaled up to 1280 x 534
        par = float(video_track.get('PixelAspectRatio') or 1.0)
        if par < 1.0:
            _log.debug('Display height: (1 / %r) * %r = %r', par, height, (1 / par) * height)
            height = (1 / par) * height
        return int(height)


@functools.lru_cache(maxsize=None)
def resolution(path, default=NO_DEFAULT_VALUE):
    """
    Return resolution of video file `path` as :class:`str` (e.g. "1080p")

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if resolution can't be determined
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    video_track = default_track('video', path)
    std_resolution = _get_closest_standard_resolution(video_track)
    scan_type = _scan_type(video_track)
    return f'{std_resolution}{scan_type}'


@functools.lru_cache(maxsize=None)
def resolution_int(path, default=NO_DEFAULT_VALUE):
    """
    Return resolution of video file `path` as :class:`int` (e.g. ``1080``)

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if resolution can't be determined
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    video_track = default_track('video', path)
    std_resolution = _get_closest_standard_resolution(video_track)
    return std_resolution


def _scan_type(video_track):
    # "p" or "i", default to "p"
    scan_type = str(video_track.get('ScanType', 'Progressive')).lower()
    if scan_type in ('interlaced', 'mbaff', 'paff'):
        return 'i'
    else:
        return 'p'

_standard_resolutions = (
    # (width, height, standard resolution)
    # 4:3
    (640, 480, 480),
    (720, 540, 540),
    (768, 576, 576),
    (960, 720, 720),
    (1440, 1080, 1080),
    (2880, 2160, 2160),
    (5760, 4320, 4320),

    # 16:9
    (853, 480, 480),
    (960, 540, 540),
    (1024, 576, 576),
    (1280, 720, 720),
    (1920, 1080, 1080),
    (3840, 2160, 2160),
    (7680, 4320, 4320),

    # 21:9
    (853, 365, 480),
    (960, 411, 540),
    (1024, 438, 576),
    (1280, 548, 720),
    (1920, 822, 1080),
    (3840, 1645, 2160),
    (7680, 3291, 4320),
)

def _get_closest_standard_resolution(video_track):
    actual_width = _get_display_width(video_track)
    actual_height = _get_display_height(video_track)

    # Find distances from actual display width/height to each standard
    # width/height. Categorize them by standard ratio.
    distances = collections.defaultdict(lambda: {})
    for std_width, std_height, std_resolution in _standard_resolutions:
        std_aspect_ratio = round(std_width / std_height, 1)
        w_dist = abs(std_width - actual_width)
        h_dist = abs(std_height - actual_height)
        resolution = (std_width, std_height, std_resolution)
        distances[std_aspect_ratio][w_dist] = distances[std_aspect_ratio][h_dist] = resolution

    # Find standard aspect ratio closest to the given aspect ratio
    actual_aspect_ratio = round(actual_width / actual_height, 1)
    std_aspect_ratios = tuple(distances)
    closest_std_aspect_ratio = closest_number(actual_aspect_ratio, std_aspect_ratios)

    # Pick the standard resolution with the lowest distance to the given resolution
    dists = distances[closest_std_aspect_ratio]
    std_width, std_height, std_resolution = sorted(dists.items())[0][1]

    _log.debug('Closest standard resolution: %r x %r [%.1f] -> %r x %r [%.1f] -> %r',
               actual_width, actual_height, actual_aspect_ratio,
               std_width, std_height, closest_std_aspect_ratio,
               std_resolution)
    return std_resolution


@functools.lru_cache(maxsize=None)
def frame_rate(path, default=NO_DEFAULT_VALUE):
    """
    Return FPS of default video track or ``0.0`` if it can't be determined

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if no video track is found
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    video_track = default_track('video', path)
    try:
        return float(video_track['FrameRate'])
    except (KeyError, ValueError, TypeError):
        return 0.0


@functools.lru_cache(maxsize=None)
def bit_depth(path, default=NO_DEFAULT_VALUE):
    """
    Return bit depth of default video track or ``0`` if it can't be determined

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if no video track is found
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    video_track = default_track('video', path)
    try:
        return int(video_track['BitDepth'])
    except (KeyError, ValueError):
        return 0


hdr_formats = {
    'DV': {
        # Dolby Vision[ / <more information>]
        'HDR_Format': re.compile(r'^Dolby Vision'),
    },
    # "HDR10+ Profile A" or "HDR10+ Profile B"
    'HDR10+': {
        'HDR_Format_Compatibility': re.compile(r'HDR10\+'),
    },
    'HDR10': (
        {'HDR_Format_Compatibility': re.compile(r'HDR10(?!\+)')},
        {'colour_primaries': re.compile(r'BT\.2020')},
    ),
    'HDR': (
        {'HDR_Format_Compatibility': re.compile(r'HDR')},
        {'HDR_Format': re.compile(r'HDR')},
    ),
}
"""
Map HDR format names (e.g. "Dolby Vision") to dictionaries that map
mediainfo video track fields to regular expressions that must match the fields'
values
"""

@functools.lru_cache(maxsize=None)
def hdr_format(path, default=NO_DEFAULT_VALUE):
    """
    Return HDR format based on `hdr_formats`, e.g. "HDR10", or empty string

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if no video track is found
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    def is_match(video_track, conditions):
        if isinstance(conditions, collections.abc.Mapping):
            # `conditions` maps field names to field value matching regexes
            for key, regex in conditions.items():
                value = video_track.get(key, '')
                if regex.search(value):
                    return True
        else:
            # `conditions` is a sequence of mappings that map field names to
            # field value matching regexes (see above)
            for condition in conditions:
                if is_match(video_track, condition):
                    return True
        return False

    video_track = default_track('video', path)
    for hdr_format, conditions in hdr_formats.items():
        if is_match(video_track, conditions):
            return hdr_format
    return ''


@functools.lru_cache(maxsize=None)
def has_dual_audio(path, default=NO_DEFAULT_VALUE):
    """
    Return `True` if `path` contains multiple audio tracks with different
    languages and one of them is English, `False` otherwise

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if reading `path` fails
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    languages = set()
    audio_tracks = tracks(path).get('Audio', ())
    for track in audio_tracks:
        if 'commentary' not in track.get('Title', '').lower():
            language = track.get('Language', '')
            if language:
                languages.add(language.casefold()[:2])
    if len(languages) > 1:
        return True
    else:
        return False


def is_bt601(path, default=NO_DEFAULT_VALUE):
    """
    Whether `path` is BT.601 (~SD) video

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if reading `path` fails
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    # https://rendezvois.github.io/video/screenshots/programs-choices/#color-matrix
    if _get_color_matrix(path, 'BT.601'):
        return True
    elif _get_color_matrix(path, 'BT.470 System B/G'):
        return True
    else:
        # Assume BT.601 if there is no HD video track
        video_tracks = tracks(path).get('Video', ())
        for video_track in video_tracks:
            resolution = _get_closest_standard_resolution(video_track)
            if resolution >= 720:
                return False
        return True

def is_bt709(path, default=NO_DEFAULT_VALUE):
    """
    Whether `path` is BT.709 (~HD) video

    See :func:`is_bt601`.
    """
    return _get_color_matrix(path, 'BT.709', default=default)

def is_bt2020(path, default=NO_DEFAULT_VALUE):
    """
    Whether `path` is BT.2020 (~UHD) video

    See :func:`is_bt601`.
    """
    return _get_color_matrix(path, 'BT.2020', default=default)

def _get_color_matrix(path, name, default=NO_DEFAULT_VALUE):
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    # https://rendezvois.github.io/video/screenshots/programs-choices/#color-matrix
    video_tracks = tracks(path).get('Video', ())
    for video_track in video_tracks:
        if video_track.get('matrix_coefficients', '').startswith(name):
            return True
    return False


@functools.lru_cache(maxsize=None)
def languages(path, default=NO_DEFAULT_VALUE, exclude_commentary=True):
    """
    Extract ``Language`` fields from each track for each track type

    Example return value:

    .. code::

        {
            'Audio': {'en', 'dk'},
            'Text': {'en', 'cz', 'pt'},
        }

    :param str path: Path to video file or directory
    :param default: Default language for each track that doesn't specify one
    :param exclude_commentary: Ignore any track with a ``Title`` field that
        contains the string "commentary" (case-insensitive)

    :raise ContentError: if reading `path` fails
    """
    all_tracks = utils.video.tracks(path)
    languages = collections.defaultdict(set)
    for type, tracks in all_tracks.items():
        for track in tracks:
            title = track.get('Title', '').lower()
            if not exclude_commentary or 'commentary' not in title:
                language = track.get('Language', None)
                if language is not None:
                    languages[type].add(language)
                elif default is not NO_DEFAULT_VALUE:
                    languages[type].add(default)
    return dict(languages)


@functools.lru_cache(maxsize=None)
def has_commentary(path, default=NO_DEFAULT_VALUE):
    """
    Return `True` if `path` has an audio track with "Commentary"
    (case-insensitive) in its title, `False` otherwise

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if reading `path` fails
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    audio_tracks = tracks(path).get('Audio', ())
    for track in audio_tracks:
        title = track.get('Title', '').lower()
        if any(word in title for word in ('commentary', 'comments')):
            return True
    return False


_audio_format_translations = (
    # (<format>, <<key>:<regex> dictionary>)
    # - All <regex>s must match each <key> to identify <format>.
    # - All identified <format>s are appended (e.g. "TrueHD Atmos").
    # - {<key>: None} means <key> must not exist.
    ('AAC', {'Format': re.compile(r'^AAC$')}),
    ('DD', {'Format': re.compile(r'^AC-3$')}),
    ('DDP', {'Format': re.compile(r'^E-AC-3$')}),
    ('TrueHD', {'Format': re.compile(r'MLP ?FBA')}),
    ('TrueHD', {'Format_Commercial_IfAny': re.compile(r'TrueHD')}),
    ('Atmos', {'Format_Commercial_IfAny': re.compile(r'Atmos')}),
    ('DTS', {'Format': re.compile(r'^DTS$'), 'Format_Commercial_IfAny': None}),
    ('DTS-ES', {'Format_Commercial_IfAny': re.compile(r'DTS-ES')}),
    ('DTS-HD', {'Format_Commercial_IfAny': re.compile(r'DTS-HD(?! Master Audio)')}),
    ('DTS-HD MA', {
        'Format_Commercial_IfAny': re.compile(r'DTS-HD Master Audio'),
        'Format_AdditionalFeatures': re.compile(r'XLL$'),
    }),
    ('DTS:X', {'Format_AdditionalFeatures': re.compile(r'XLL X')}),
    ('FLAC', {'Format': re.compile(r'FLAC')}),
    ('MP3', {'Format': re.compile(r'MPEG Audio')}),
    ('Vorbis', {'Format': re.compile(r'\bVorbis\b')}),
    ('Vorbis', {'Format': re.compile(r'\bOgg\b')}),
    ('Opus', {'Format': re.compile(r'\bOpus\b')}),
)

@functools.lru_cache(maxsize=None)
def audio_format(path, default=NO_DEFAULT_VALUE):
    """
    Return audio format (e.g. "AAC", "MP3") or empty string

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist or has no audio track,
        raise :exc:`~.ContentError` if not provided

    :raise ContentError: if no audio track is found and no `default` is provided
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    try:
        audio_track = default_track('audio', path)
    except errors.ContentError:
        if default is NO_DEFAULT_VALUE:
            raise
        else:
            audio_track = {}

    def is_match(regexs, audio_track):
        for key,regex in regexs.items():
            if regex is None:
                if key in audio_track:
                    # `key` must not exists but it does
                    return False
            else:
                # regex is not None
                if key not in audio_track:
                    # `key` doesn't exist
                    return False
                elif not regex.search(audio_track.get(key, '')):
                    # `key` has value that doesn't match `regex`
                    return False
        # All `regexs` match and no forbidden keys exist in `audio_track`
        return True

    parts = []
    for fmt, regexs in _audio_format_translations:
        if fmt not in parts and is_match(regexs, audio_track):
            parts.append(fmt)
    return ' '.join(parts)


# NOTE: guessit only recognizes 7.1, 5.1, 2.0 and 1.0
_audio_channels_translations = (
    ('1.0', re.compile(r'^1$')),
    ('2.0', re.compile(r'^2$')),
    ('2.0', re.compile(r'^3$')),
    ('2.0', re.compile(r'^4$')),
    ('2.0', re.compile(r'^5$')),
    ('5.1', re.compile(r'^6$')),
    ('5.1', re.compile(r'^7$')),
    ('7.1', re.compile(r'^8$')),
    ('7.1', re.compile(r'^9$')),
    ('7.1', re.compile(r'^10$')),
)

@functools.lru_cache(maxsize=None)
def audio_channels(path, default=NO_DEFAULT_VALUE):
    """
    Return audio channels (e.g. "5.1") or empty_string

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist or has no audio track,
        raise :exc:`~.ContentError` if not provided

    :raise ContentError: if no audio track is found and no `default` is provided
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    try:
        audio_track = default_track('audio', path)
    except errors.ContentError:
        if default is NO_DEFAULT_VALUE:
            raise
        else:
            audio_track = {}

    audio_channels = ''
    channels = audio_track.get('Channels', '')
    for achan,regex in _audio_channels_translations:
        if regex.search(channels):
            audio_channels = achan
            break

    return audio_channels


_video_translations = (
    ('x264', {'Encoded_Library_Name': re.compile(r'^x264$')}),
    ('x265', {'Encoded_Library_Name': re.compile(r'^x265$')}),
    ('XviD', {'Encoded_Library_Name': re.compile(r'^XviD$')}),
    ('H.264', {'Format': re.compile(r'^AVC$')}),
    ('H.265', {'Format': re.compile(r'^HEVC$')}),
    ('VP9', {'Format': re.compile(r'^VP9$')}),
    ('MPEG-2', {'Format': re.compile(r'^MPEG Video$')}),
)

@functools.lru_cache(maxsize=None)
def video_format(path, default=NO_DEFAULT_VALUE):
    """
    Return video format or x264/x265/XviD if they were used or empty string if
    it can't be determined

    :param str path: Path to video file or directory

        For directories, the first video is used. See :func:`find_videos`.
    :param default: Return value if `path` doesn't exist, raise
        :exc:`~.ContentError` if not provided

    :raise ContentError: if no video track is found
    """
    if default is not NO_DEFAULT_VALUE and not os.path.exists(path):
        return default

    def translate(video_track):
        for vfmt,regexs in _video_translations:
            for key,regex in regexs.items():
                value = video_track.get(key)
                if value:
                    if regex.search(value):
                        return vfmt
        return ''

    video_track = default_track('video', path)
    video_format = translate(video_track)
    _log.debug('Detected video format: %s', video_format)
    return video_format


@functools.lru_cache(maxsize=None)
def find_videos(path):
    """
    Find video files, excluding nfo, screenshots, samples, etc

    Paths to Blu-ray trees (directories that contain a "BDMV" directory) are
    simply returned.

    If there are any "VIDEO_TS" (DVD) directories beneath `path` and its
    subdirectories, the largest VOB file for each "VIDEO_TS" directory is
    returned.

    For season packs (i.e. directories that contain files with "S..E.." in their
    name), episodes are returned and all other files are excluded.

    In all other cases that are not described above, directories are walked
    recursively, video files are detected by file extension and sorted naturally
    (e.g. "2.mkv" is sorted before "10.mkv"), and found video files are filtered
    through :func:`filter_main_videos` to exclude samples and such.

    :param str path: Path to file or directory

    :return: Sequence of video file paths

    :raise ContentError: if no video file can be found
    """
    def normalize_files(files):
        return natsort.natsorted(str(f) for f in files)

    # Blu-ray
    if os.path.isdir(os.path.join(path, 'BDMV')):
        # ffmpeg can read BDMV with the "bluray:" protocol
        return normalize_files([path])

    # DVD
    if os.path.isdir(path):
        # ffmpeg doesn't have a "dvd:" protocol so we return the largest VOB
        # file in each VIDEO_TS subdirectory beneath `path`
        files = []
        for video_ts_path in for_each_video_ts(path):
            all_vobs = utils.fs.file_list(video_ts_path, extensions=('VOB',))
            main_vob = find_main_vob(all_vobs)
            if main_vob:
                files.append(main_vob)
        if files:
            return normalize_files(files)

    # Directory containing video files or video file
    files = fs.file_list(path, extensions=constants.VIDEO_FILE_EXTENSIONS)

    # Find episodes in season pack by file name for better accuracy and to avoid
    # time consuming system calls in filter_main_videos()
    episode_regex = re.compile(
        rf'(?:^|{release.DELIM})'
        rf'(?i:S|Season{release.DELIM}?)\d+{release.DELIM}?(?i:E|Episode{release.DELIM}?)\d+'
        rf'{release.DELIM}'
    )
    episodes = [
        file
        for file in files
        if episode_regex.search(os.path.basename(file))
    ]
    if episodes:
        return normalize_files(episodes)

    if not files:
        raise errors.ContentError(f'{path}: No video file found')
    else:
        # To avoid using samples, extras, very short .VOBs (e.g. menus), remove
        # any videos that are very short compared to the average duration.
        considered_files = filter_main_videos(files)
        return normalize_files(considered_files)


def filter_main_videos(video_file_paths):
    r"""
    Filter `video_file_paths` for main video files

    Exclude any non-videos (see :const:`~.constants.VIDEO_FILE_EXTENSIONS`) and
    any videos that are smaller than 75 % of the average file size
    (e.g. samples).

    If `video_file_paths` contains any .VOB files from a DVD (path ends with
    ``/VIDEO_TS/VTS_\d+_\d+\.VOB``), return the largest .VOB file from each
    VIDEO_TS directory.

    .. note:: Because this function is decorated with
       :func:`functools.lru_cache`, `video_file_paths` should be a tuple (or any
       other hashable sequence).

    :params video_file_paths: Hashable sequence of video file paths

    :return: Filtered subset of `video_file_paths` as a sequence
    """
    # Single video file
    paths = tuple(video_file_paths)
    if len(paths) < 2:
        return paths

    # DVD (VIDEO_TS)
    main_video_ts_videos = _filter_main_videos_dvd(paths)
    if main_video_ts_videos:
        return main_video_ts_videos

    # Exclude non-video files
    only_video_paths = (
        fp for fp in paths
        if utils.fs.file_extension(fp).lower() in constants.VIDEO_FILE_EXTENSIONS
    )
    # Get size of each video
    sizes = {fp: utils.fs.file_size(fp) for fp in only_video_paths}
    # Exclude video files with no size (fs.file_size() may return `None`)
    sizes = {fp: size for fp, size in sizes.items() if size}

    # Exclude video files with size below average
    if sizes:
        avg = sum(sizes.values()) / len(sizes)
    else:
        avg = 0
    min_size = avg * 0.75
    return tuple(
        filepath for filepath, filesize in sizes.items()
        if filesize >= min_size
    )


def _filter_main_videos_dvd(video_file_paths):
    vob_sets = collections.defaultdict(lambda: [])
    # Group files by common VIDEO_TS parent directory
    for video_file_path in video_file_paths:
        match = re.search(
            rf'^(.*{utils.fs.OS_SEP_REGEX}VIDEO_TS)({utils.fs.OS_SEP_REGEX}VTS_\d+_\d+.[A-Z]+)$',
            video_file_path,
        )
        if match:
            video_ts_path = match.group(1)
            vob_sets[video_ts_path].append(video_file_path)

    # Return main VOB file for each VIDEO_TS directory
    main_vobs = []
    for video_ts_path_, vob_paths in vob_sets.items():
        main_vob = find_main_vob(vob_paths)
        if main_vob:
            main_vobs.append(main_vob)
    return main_vobs


def find_main_vobs(video_ts_files):
    """
    Return largest set of VOB files

    VOB files are split into sets by their file names, ignoring the second
    number, e.g. ``VTS_01_*.VOB``, ``VTS_02_*.VOB``, ``VTS_03_*.VOB``, etc.

    The largest set of VOB files in bytes is the main set.

    Any other files (e.g. ``VIDEO_TS.*``, ``*.IFO``, ``*.BUP``) are ignored.

    :param video_ts_files: Sequence of files from a DVD'S "VIDEO_TS" directory
    """
    all_vobs = (
        filepath for filepath in video_ts_files
        if re.search(rf'{utils.fs.OS_SEP_REGEX}VIDEO_TS{utils.fs.OS_SEP_REGEX}VTS_\d+_\d+\.VOB$', filepath)
    )
    vob_sets = collections.defaultdict(lambda: [])
    for vob_path in all_vobs:
        # Find the largest sets of VOBs (e.g. VTS_01_*.VOB). We go by file size
        # instead of duration because we don't want to pick the VOB that is 20
        # hours of black (yes, that happened). The largest set should be the
        # main feature because it has the most complexity.
        vob_name = utils.fs.basename(vob_path)
        match = re.search(r'^(\w+_\d+)_\d+\.VOB$', vob_name)
        if match:
            set_name = match.group(1)
            vob_sets[set_name].append(vob_path)

    # Sort by VOB sets by combined size (largest first)
    sorted_vob_sets = sorted(
        vob_sets.values(),
        key=lambda vob_paths: sum(
            # file_size() returns `None` if size can't be determined
            (utils.fs.file_size(path) or 0)
            for path in vob_paths
        ),
        reverse=True,
    )

    # Return largest VOB set
    if sorted_vob_sets:
        return sorted_vob_sets[0]
    else:
        return []


def find_main_vob(video_ts_files):
    """
    Return largest VOB from the largest set of VOB files

    The main set of VOB files is determined by :func:`find_main_vobs`.

    If there are no VOB files, return `None`.

    :param video_ts_files: Sequence of files from a DVD'S "VIDEO_TS" directory
    """
    # Find largest VOB set (e.g. VTS_01_*.VOB)
    main_vobs = find_main_vobs(video_ts_files)
    if main_vobs:
        # Reverse sort VOBs by SIZE to get the largest VOB
        sorted_main_set = sorted(
            main_vobs,
            key=lambda vob_path: utils.fs.file_size(vob_path),
            reverse=True,
        )
        return sorted_main_set[0]


def vob2ifo(vob_path):
    """
    Translate VOB file to corresponding IFO file

    VOB and IFO files are used in VIDEO_TS directories on DVDs.

    :raise ValueError: if `vob_path` does not match expected naming pattern
    """
    filename = utils.fs.basename(vob_path)
    match = re.search(r'^(VTS_\d+_)\d+\.VOB$', filename)
    if match:
        return os.path.join(
            utils.fs.dirname(vob_path),
            match.group(1) + '0.IFO',
        )
    else:
        raise ValueError(f'This does not look like a VOB file: {vob_path}')


def for_each_video_ts(path):
    """
    Iterate over "VIDEO_TS" directories beneath `path`

    Subdirectories of `path` are searched recursively.
    """
    video_ts_paths = natsort.natsorted(
        glob.glob(
            f'{path}{utils.fs.OS_SEP_REGEX}**{utils.fs.OS_SEP_REGEX}VIDEO_TS',
            recursive=True,
        )
    )
    for video_ts_path in video_ts_paths:
        if os.path.isdir(video_ts_path):
            yield video_ts_path


@functools.lru_cache(maxsize=None)
def make_ffmpeg_input(path):
    """
    Make `path` palatable for ffmpeg

    - If path is a directory and contains a subdirectory named "BDMV", "bluray:"
      is prepended to `path`.

    - If path is a directory and contains a subdirectory named "VIDEO_TS", the
      largest .VOB file is returned. (ffmpeg does not support DVD directory
      structures.)

    - By default, `path` is returned unchanged.

    :param str path: Path to file or directory
    """
    # Detect Blu-ray
    if os.path.exists(os.path.join(path, 'BDMV')):
        return f'bluray:{path}'

    # Detect DVD
    if os.path.isdir(os.path.join(path, 'VIDEO_TS')):
        # FFmpeg doesn't seem to support reading DVD.  We work around this
        # by finding the first .VOB with a reasonable length.
        vobs = fs.file_list(os.path.join(path, 'VIDEO_TS'), extensions=('VOB',))
        _log.debug('All VOBs: %r', vobs)
        main_vobs = filter_main_videos(vobs)
        _log.debug('Main VOBs: %r', main_vobs)
        if main_vobs:
            return main_vobs[0]

    return str(path)
