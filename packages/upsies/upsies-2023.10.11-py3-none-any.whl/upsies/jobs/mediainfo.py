"""
Wrapper for ``mediainfo`` command
"""

import asyncio
import os

from .. import errors, utils
from . import JobBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class MediainfoJob(JobBase):
    """
    Get output from ``mediainfo`` command

    See :func:`.utils.video.mediainfo` for more information.
    """

    name = 'mediainfo'
    label = 'Mediainfo'

    # Don't show mediainfo output in TUI. It is printed out to stdout if this is
    # the only/final job.
    hidden = True

    @property
    def cache_id(self):
        """Final segment of `content_path` and `from_all_videos` argument"""
        return (
            utils.fs.basename(self._content_path),
            'from_all_videos' if self._from_all_videos else 'from_first_video',
            [
                # `re.Pattern` objects or glob strings
                (exclude.pattern if hasattr(exclude, 'pattern') else str(exclude))
                for exclude in self._exclude_files
            ],
        )

    def initialize(self, *, content_path, from_all_videos=False, exclude_files=()):
        """
        Set internal state

        :param content_path: Path to video file or directory that contains a
            video file
        :param bool from_all_videos: Whether to get ``mediainfo`` output from
            each video file or only from the first video
        :param exclude_files: Sequence of glob patterns (:class:`str`) and
            :class:`re.Pattern` objects (return value from :func:`re.compile`)
            that are matched against the relative path beneath `content_path`

            Glob patterns are matched case-insensitively.

            .. note:: Non-video files and stuff like `Sample.mkv` are always
                      excluded by :func:`.video.filter_main_videos`.
        """
        self._content_path = content_path
        self._from_all_videos = from_all_videos
        self._exclude_files = exclude_files
        self._mediainfos_by_file = {}
        self.signal.add('mediainfo', record=True)
        self.signal.register('mediainfo', self._store_mediainfos_by_file)

    def execute(self):
        """Call ``mediainfo`` in an asynchronous thread"""
        self.attach_task(
            coro=self._generate_mediainfos(),
            finish_when_done=True,
        )

    async def _generate_mediainfos(self):
        # Exclude files specified by the user
        video_filepaths = utils.torrent.filter_files(
            content_path=self._content_path,
            exclude=self._exclude_files,
        )
        # Exclude irrelevant files (non-videos, sample.mkv, etc)
        video_filepaths = utils.video.filter_main_videos(video_filepaths)
        for video_filepath in video_filepaths:
            # DVD
            if utils.fs.dirname(video_filepath).endswith(f'{os.sep}VIDEO_TS'):
                ifo_filepath = utils.video.vob2ifo(video_filepath)
                vob_filepath = video_filepath
                mediainfos_or_exceptions = await asyncio.gather(
                    utils.run_async(utils.video.mediainfo, ifo_filepath),
                    utils.run_async(utils.video.mediainfo, vob_filepath),
                    return_exceptions=True,
                )
                assert len(mediainfos_or_exceptions) == len((ifo_filepath, vob_filepath))
                for filepath, mi_or_exc in zip((ifo_filepath, vob_filepath), mediainfos_or_exceptions):
                    if isinstance(mi_or_exc, errors.ContentError):
                        self.error(mi_or_exc)
                    elif isinstance(mi_or_exc, Exception):
                        raise mi_or_exc
                    else:
                        self.send(mi_or_exc)
                        self.signal.emit('mediainfo', filepath, mi_or_exc)

            # Normal video file(s)
            else:
                try:
                    mi = await utils.run_async(utils.video.mediainfo, video_filepath)
                except errors.ContentError as e:
                    self.error(e)
                else:
                    self.send(mi)
                    self.signal.emit('mediainfo', video_filepath, mi)

            if not self._from_all_videos:
                break

    def _store_mediainfos_by_file(self, filepath, mediainfo):
        self._mediainfos_by_file[filepath] = mediainfo

    @property
    def mediainfos_by_file(self):
        """
        Map source video file paths to ``mediainfo`` outputs gathered so far

        .. note:: For DVDs (directories with a VIDEO_TS subdirectory), one
                  mediainfo is made for an ``.IFO`` file and a second mediainfo
                  is made for a ``.VOB`` file.
        """
        return {
            filepath: mediainfo
            for filepath, mediainfo in self._mediainfos_by_file.items()
        }
