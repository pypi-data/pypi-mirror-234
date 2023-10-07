"""
Abstract base class for tracker jobs
"""

import abc
import builtins
import collections
import functools
import pathlib

from ... import errors, jobs, utils

import logging  # isort:skip
_log = logging.getLogger(__name__)


class TrackerJobsBase(abc.ABC):
    """
    Base class for tracker-specific :class:`jobs <upsies.jobs.base.JobBase>`

    This base class defines general-purpose jobs that can be used by subclasses
    by returning them in their :attr:`jobs_before_upload` or
    :attr:`jobs_after_upload` attributes. It also provides all objects that are
    needed by any one of those jobs.

    Job instances are provided as :func:`functools.cached_property`, i.e. jobs
    are created only once per session.

    Subclasses that need to run background tasks should pass them to
    :meth:`.JobBase.attach_task` or to :meth:`.TrackerBase.attach_task`.

    For a description of the arguments see the corresponding properties.
    """

    def __init__(self, *, content_path, tracker,
                 reuse_torrent_path=None, exclude_files=(),
                 btclient=None, torrent_destination=None,
                 screenshots_optimization=None, image_host=None,
                 options=None, common_job_args=None):
        self._content_path = content_path
        self._reuse_torrent_path = reuse_torrent_path
        self._tracker = tracker
        self._screenshots_optimization = screenshots_optimization
        self._image_host = image_host
        self._btclient = btclient
        self._torrent_destination = torrent_destination
        self._exclude_files = exclude_files
        self._common_job_args = common_job_args or {}
        self._options = options or {}
        self._signal = utils.signal.Signal('warning', 'error', 'exception')

    @property
    def content_path(self):
        """
        Content path to generate metadata for

        This is the same object that was passed as a initialization argument.
        """
        return self._content_path

    @property
    def tracker(self):
        """
        :class:`~.trackers.base.TrackerBase` subclass

        This is the same object that was passed as a initialization argument.
        """
        return self._tracker

    @property
    def reuse_torrent_path(self):
        """
        Path to an existing torrent file that matches :attr:`content_path`

        See :func:`.torrent.create`.
        """
        return self._reuse_torrent_path

    @property
    def torrent_destination(self):
        """
        Where to copy the generated torrent file to or `None`

        This is the same object that was passed as a initialization argument.
        """
        return self._torrent_destination

    @property
    def exclude_files(self):
        """
        Sequence of glob and regular expression patterns to exclude from the
        generated torrent

        See the ``exclude_files`` argument of
        :meth:`.CreateTorrentJob.initialize`.

        This should also be used by :attr:`screenshots_job` to avoid making
        screenshots from files that aren't in the torrent.
        """
        return self._exclude_files

    @property
    def options(self):
        """
        Configuration options provided by the user

        This is the same object that was passed as a initialization argument.
        """
        return self._options

    @property
    def image_host(self):
        """
        :class:`~.base.ImageHostBase` instance or `None`

        This is the same object that was passed as a initialization argument.
        """
        return self._image_host

    @property
    def btclient(self):
        """
        :class:`~.btclient.BtClient` instance or `None`

        This is the same object that was passed as a initialization argument.
        """
        return self._btclient

    def common_job_args(self, **overload):
        """
        Keyword arguments that are passed to all jobs or empty `dict`

        :param overload: Keyword arguments add or replace values from the
            initialization argument
        """
        return {
            **self._common_job_args,
            **overload,
        }

    @property
    @abc.abstractmethod
    def jobs_before_upload(self):
        """
        Sequence of jobs that need to finish before :meth:`~.TrackerBase.upload` can
        be called
        """

    @functools.cached_property
    def jobs_after_upload(self):
        """
        Sequence of jobs that are started after :meth:`~.TrackerBase.upload`
        finished

        .. note:: Jobs returned by this class should have
                  :attr:`~.JobBase.autostart` set to `False` or they will be
                  started before submission is attempted.

        By default, this returns :attr:`add_torrent_job` and
        :attr:`copy_torrent_job`.
        """
        return (
            self.add_torrent_job,
            self.copy_torrent_job,
        )

    @property
    def isolated_jobs(self):
        """
        Sequence of job names (e.g. ``"imdb_job"``) that were singled out by the
        user (e.g. with a CLI argument) to create only a subset of the usual
        metadata

        If this sequence is empty, all jobs in :attr:`jobs_before_upload` and
        :attr:`jobs_after_upload` are enabled.
        """
        return ()

    def get_job_and_dependencies(self, *jobs):
        """
        Combine all `jobs` and their dependencies recursively into flat list

        :param jobs: :class:`~.JobBase` instances

        Dependencies are gathered from each job's :attr:`~.JobBase.prejobs` and
        :meth:`~.JobBase.presignal`\\ s.

        .. warning:: This is not a foolproof way to find all dependencies.

                     :class:`~.QueueJobBase` instances, for example, don't where
                     their input comes from, so they don't know anything about
                     which jobs they depend on. There are also
                     :attr:`~.JobBase.precondition`\\ s, which can define
                     arbitrary requirements.

        :return: Sequence of :class:`~.JobBase` instances
        """
        all_jobs = []

        def add_job(job):
            if job not in all_jobs:
                all_jobs.append(job)

        def add_prejobs(job):
            for prejob in job.prejobs:
                add_job(prejob)
                add_prejobs(prejob)
                add_jobs_from_presignals(prejob)

        def add_jobs_from_presignals(job):
            for presignal_job in job.presignals:
                add_job(presignal_job)
                add_prejobs(presignal_job)
                add_jobs_from_presignals(presignal_job)

        for j in jobs:
            add_job(j)
            add_prejobs(j)
            add_jobs_from_presignals(j)

        return all_jobs

    @property
    def submission_ok(self):
        """
        Whether the created metadata should be submitted

        The base class implementation returns `False` if there are any
        :attr:`isolated_jobs`. Otherwise, it returns `True` only if all
        :attr:`jobs_before_upload` have an :attr:`~.base.JobBase.exit_code` of
        ``0`` or a falsy :attr:`~.base.JobBase.is_enabled` value.

        Subclasses should always call the parent class implementation to ensure
        all metadata was created successfully.
        """
        if self.isolated_jobs:
            # If some jobs are disabled, required metadata is missing and we
            # can't submit
            return False
        else:
            enabled_jobs_before_upload = tuple(
                job for job in self.jobs_before_upload
                if job and job.is_enabled
            )
            enabled_jobs_succeeded = all(
                job.exit_code == 0
                for job in enabled_jobs_before_upload
            )
            return bool(
                enabled_jobs_before_upload
                and enabled_jobs_succeeded
            )

    @property
    def signal(self):
        """
        :class:`~.signal.Signal` instance with the signals ``warning``, ``error``
        and ``exception``
        """
        return self._signal

    def warn(self, warning):
        """
        Emit ``warning`` signal (see :attr:`signal`)

        Emit a warning for any non-critical issue that the user can choose to
        ignore or fix.
        """
        self.signal.emit('warning', warning)

    def error(self, error):
        """
        Emit ``error`` signal (see :attr:`signal`)

        Emit an error for any critical but expected issue that can't be
        recovered from (e.g. I/O error).
        """
        self.signal.emit('error', error)

    def exception(self, exception):
        """
        Emit ``exception`` signal (see :attr:`signal`)

        Emit an exception for any critical and unexpected issue that should be
        reported as a bug.
        """
        self.signal.emit('exception', exception)

    @functools.cached_property
    def imdb(self):
        """:class:`~.webdbs.imdb.ImdbApi` instance"""
        return utils.webdbs.webdb('imdb')

    @functools.cached_property
    def tmdb(self):
        """:class:`~.webdbs.tmdb.TmdbApi` instance"""
        return utils.webdbs.webdb('tmdb')

    @functools.cached_property
    def tvmaze(self):
        """:class:`~.webdbs.tvmaze.TvmazeApi` instance"""
        return utils.webdbs.webdb('tvmaze')

    def get_job_name(self, name):
        """
        Return job name that is unique for this tracker

        It's important for tracker jobs to have unique names to avoid re-using
        cached output from another tracker's job with the same name.

        Standard jobs have names so that cached output will be re-used by other
        trackers if possible. This function is mainly for unique and custom jobs
        that are only used for one tracker but might share the same name with
        other trackers.
        """
        suffix = f'.{self.tracker.name}'
        if name.endswith(suffix):
            return name
        else:
            return f'{name}{suffix}'

    @functools.cached_property
    def create_torrent_job(self):
        """:class:`~.jobs.torrent.CreateTorrentJob` instance"""
        return jobs.torrent.CreateTorrentJob(
            content_path=self.content_path,
            reuse_torrent_path=self.reuse_torrent_path,
            tracker=self.tracker,
            exclude_files=self.exclude_files,
            precondition=self.make_precondition('create_torrent_job'),
            **self.common_job_args(),
        )

    @functools.cached_property
    def add_torrent_job(self):
        """:class:`~.jobs.torrent.AddTorrentJob` instance"""
        if self._btclient and self.create_torrent_job:
            add_torrent_job = jobs.torrent.AddTorrentJob(
                autostart=False,
                btclient=self._btclient,
                precondition=self.make_precondition('add_torrent_job'),
                **self.common_job_args(),
            )

            # Pass CreateTorrentJob output to AddTorrentJob input.
            self.create_torrent_job.signal.register('output', add_torrent_job.enqueue)

            # Tell AddTorrentJob to finish the current upload and then finish.
            self.create_torrent_job.signal.register('finished', self.finalize_add_torrent_job)

            return add_torrent_job

    def finalize_add_torrent_job(self, _):
        self.add_torrent_job.finalize()

    @functools.cached_property
    def copy_torrent_job(self):
        """:class:`~.jobs.torrent.CopyTorrentJob` instance"""
        if self.torrent_destination and self.create_torrent_job:
            copy_torrent_job = jobs.torrent.CopyTorrentJob(
                autostart=False,
                destination=self.torrent_destination,
                precondition=self.make_precondition('copy_torrent_job'),
                **self.common_job_args(),
            )
            # Pass CreateTorrentJob output to CopyTorrentJob input.
            self.create_torrent_job.signal.register('output', copy_torrent_job.enqueue)
            # Tell CopyTorrentJob to finish when CreateTorrentJob is done.
            self.create_torrent_job.signal.register('finished', self.finalize_copy_torrent_job)
            return copy_torrent_job

    def finalize_copy_torrent_job(self, _):
        self.copy_torrent_job.finalize()

    @functools.cached_property
    def release_name(self):
        """
        :class:`~.release.ReleaseName` instance with
        :attr:`release_name_translation` applied
        """
        return utils.release.ReleaseName(
            path=self.content_path,
            translate=self.release_name_translation,
            separator=self.release_name_separator,
        )

    release_name_separator = None
    """See :attr:`.ReleaseName.separator`"""

    release_name_translation = {}
    """See ``translate`` argument of :attr:`~.utils.release.ReleaseName`"""

    @functools.cached_property
    def release_name_job(self):
        """
        :class:`~.jobs.dialog.TextFieldJob` instance with text set to
        :attr:`release_name`

        The text is automatically updated when :attr:`imdb_job` sends an ID.
        """
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('release-name'),
            label='Release Name',
            text=str(self.release_name),
            callbacks={
                'output': self.release_name.set_release_info,
            },
            precondition=self.make_precondition('release_name_job'),
            **self.common_job_args(),
        )

    async def update_release_name_from(self, webdb, webdb_id):
        """
        Update :attr:`release_name_job` with web DB information

        :param webdb: :class:`~.webdbs.base.WebDbApiBase` instance
        :param webdb_id: ID for `webdb`

        This is a convenience wrapper around :meth:`.ReleaseName.fetch_info` and
        :meth:`.TextFieldJob.fetch_text`.
        """
        await self.release_name_job.fetch_text(
            coro=self.release_name.fetch_info(webdb=webdb, webdb_id=webdb_id),
            nonfatal_exceptions=(errors.RequestError,),
            default=str(self.release_name),
        )
        _log.debug('Updated release name: %s', self.release_name)

    @functools.cached_property
    def imdb_job(self):
        """:class:`~.jobs.webdb.WebDbSearchJob` instance"""
        return jobs.webdb.WebDbSearchJob(
            query=self.content_path,
            db=self.imdb,
            callbacks={
                'output': self._handle_imdb_id,
            },
            precondition=self.make_precondition('imdb_job'),
            **self.common_job_args(),
        )

    def _handle_imdb_id(self, imdb_id):
        # Update other webdb queries with IMDb info
        self.tracker.attach_task(self._propagate_webdb_info(self.imdb, imdb_id))

        # Upload poster image from appropriate webdb
        if self._poster_webdb is self.imdb:
            self._start_poster_job(self.imdb, imdb_id)

    @property
    def imdb_id(self):
        """IMDb ID if :attr:`imdb_job` is finished or `None`"""
        return self._get_webdb_id_from_job(self.imdb_job)

    @functools.cached_property
    def tmdb_job(self):
        """:class:`~.jobs.webdb.WebDbSearchJob` instance"""
        return jobs.webdb.WebDbSearchJob(
            query=self.content_path,
            db=self.tmdb,
            callbacks={
                'output': self._handle_tmdb_id,
            },
            precondition=self.make_precondition('tmdb_job'),
            **self.common_job_args(),
        )

    def _handle_tmdb_id(self, tmdb_id):
        # Update other webdb queries with TMDb info
        self.tracker.attach_task(self._propagate_webdb_info(self.tmdb, tmdb_id))

        if self._poster_webdb is self.tmdb:
            self._start_poster_job(self.tmdb, tmdb_id)

    @property
    def tmdb_id(self):
        """TMDb ID if :attr:`tmdb_job` is finished or `None`"""
        return self._get_webdb_id_from_job(self.tmdb_job)

    @functools.cached_property
    def tvmaze_job(self):
        """:class:`~.jobs.webdb.WebDbSearchJob` instance"""
        return jobs.webdb.WebDbSearchJob(
            query=self.content_path,
            db=self.tvmaze,
            callbacks={
                'output': self._handle_tvmaze_id,
            },
            precondition=self.make_precondition('tvmaze_job'),
            **self.common_job_args(),
        )

    def _handle_tvmaze_id(self, tvmaze_id):
        # Update other webdb queries with TVmaze info
        self.tracker.attach_task(self._propagate_webdb_info(self.tvmaze, tvmaze_id))

        if self._poster_webdb is self.tvmaze:
            self._start_poster_job(self.tvmaze, tvmaze_id)

    @property
    def tvmaze_id(self):
        """TVmaze ID if :attr:`tvmaze_job` is finished or `None`"""
        return self._get_webdb_id_from_job(self.tvmaze_job)

    def _get_webdb_id_from_job(self, webdb_job):
        if webdb_job.is_finished and webdb_job.output:
            return webdb_job.output[0]

    async def _propagate_webdb_info(self, webdb, webdb_id):
        target_webdb_jobs = [
            j for j in (getattr(self, f'{name}_job') for name in utils.webdbs.webdb_names())
            if (
                webdb.name not in j.name
                and j.is_enabled
                and not j.is_finished
            )
        ]

        title_english = await webdb.title_english(webdb_id)
        title_original = await webdb.title_original(webdb_id)
        query = utils.webdbs.Query(
            type=await webdb.type(webdb_id),
            title=title_english or title_original,
            year=await webdb.year(webdb_id),
        )

        _log.debug('Propagating %s info to: %r: %s', webdb.name, [j.name for j in target_webdb_jobs], query)
        for job in target_webdb_jobs:
            job.query.update(query)

        await self.update_release_name_from(webdb, webdb_id)

    @functools.cached_property
    def screenshots_job(self):
        """
        :class:`~.jobs.screenshots.ScreenshotsJob` instance

        The number of screenshots to make is taken the :attr:`screenshots_count`
        attribute.
        """
        return jobs.screenshots.ScreenshotsJob(
            content_path=self.content_path,
            exclude_files=self.exclude_files,
            count=self.screenshots_count,
            from_all_videos=self.screenshots_from_all_videos,
            optimize=self._screenshots_optimization,
            precondition=self.make_precondition('screenshots_job'),
            **self.common_job_args(),
        )

    @property
    def screenshots_count(self):
        """
        How many screenshots to make

        The default implementation uses :attr:`options`\\ ``["screenshots"]``
        with `None` as the default value, which creates a default number of
        screenshots.
        """
        return self.options.get('screenshots')

    @property
    def screenshots_from_all_videos(self):
        """
        Whether to make :attr:`screenshots_count` screenshots from all
        videos or just the first one

        See :meth:`.ScreenshotsJob.initialize`.

        The default implementation is always `False`.
        """
        return False

    image_host_config = {}
    """
    Dictionary that maps an image hosting service :attr:`~.ImageHostBase.name`
    to :attr:`~.ImageHostBase.default_config` values

    ``common`` is a special image host whose values are always applied.

    Values from a specific image hosting service overload ``common`` values.

    Example:

    >>> image_host_config = {
    ...     # Always generate 300p thumbnails
    ...     "common": {"thumb_width": 300},
    ...     # Use API key for specific image hosting service
    ...     "myhost": {"apikey": "d34db33f"},
    ... }
    """

    @functools.cached_property
    def upload_screenshots_job(self):
        """:class:`~.jobs.imghost.ImageHostJob` instance"""
        if self.image_host and self.screenshots_job:
            imghost_job = jobs.imghost.ImageHostJob(
                imghost=self.image_host,
                precondition=self.make_precondition('upload_screenshots_job'),
                **self.common_job_args(),
            )
            # Timestamps and number of screenshots are determined in a
            # subprocess, we have to wait for that before we can set the number
            # of expected screenhots.
            self.screenshots_job.signal.register('screenshots_total', imghost_job.set_images_total)
            # Pass ScreenshotsJob's output to ImageHostJob input.
            self.screenshots_job.signal.register('output', imghost_job.enqueue)
            # Tell imghost_job to finish the current upload and then finish.
            self.screenshots_job.signal.register('finished', self.finalize_upload_screenshots_job)
            return imghost_job

    def finalize_upload_screenshots_job(self, _):
        self.upload_screenshots_job.finalize()

    @functools.cached_property
    def poster_job(self):
        """
        :class:`~.jobs.poster.PosterJob` instance

        This is started automatically when an appropriate webdb job finishes.
        """
        return jobs.poster.PosterJob(
            autostart=False,
            webdb_id=None,
            webdb=None,
            imghost=self.image_host,
            width=self.poster_max_width,
            height=self.poster_max_height,
            precondition=self.make_precondition('poster_job'),
            **self.common_job_args(),
        )

    def _start_poster_job(self, webdb, webdb_id):
        self.poster_job.start(
            webdb=webdb,
            webdb_id=webdb_id,
            season=self.release_name.only_season,
        )

    poster_max_width = 300
    """Maximum poster image width"""

    poster_max_height = 500
    """Maximum poster image height"""

    @functools.cached_property
    def _poster_webdb(self):
        """:class:`~.webdbs.base.WebDbApiBase` instance for finding poster image"""
        if (
                self.poster_job.is_enabled
                and not self.poster_job.is_started
                and self.poster_job in self.jobs_before_upload
        ):
            if (
                    self.tvmaze_job.is_enabled
                    and self.tvmaze_job in self.jobs_before_upload
                    and self.release_name.type in (utils.release.ReleaseType.season,
                                                   utils.release.ReleaseType.episode)
            ):
                return self.tvmaze

            elif (
                    self.imdb_job.is_enabled
                    and self.imdb_job in self.jobs_before_upload
            ):
                return self.imdb

            elif (
                    self.tmdb_job.is_enabled
                    and self.tmdb_job in self.jobs_before_upload
            ):
                return self.tmdb

            else:
                raise RuntimeError('You must add a WebDbSearchJob instance to jobs_before_upload')

    @functools.cached_property
    def mediainfo_job(self):
        """:class:`~.jobs.mediainfo.MediainfoJob` instance"""
        return jobs.mediainfo.MediainfoJob(
            content_path=self.content_path,
            from_all_videos=self.mediainfo_from_all_videos,
            exclude_files=self.exclude_files,
            precondition=self.make_precondition('mediainfo_job'),
            **self.common_job_args(),
        )

    @property
    def mediainfo_from_all_videos(self):
        """
        Whether to get the ``mediainfo`` output from all videos or just the
        first one

        See :meth:`.MediainfoJob.initialize`.

        The default implementation is always `False`.
        """
        return False

    @property
    def mediainfos_and_screenshots(self):
        """
        Map video file paths to mediainfo and screenshot URLs

        This property uses the results of :attr:`mediainfo_job` and
        :attr:`upload_screenshots_job`, and therefore both jobs must be
        :attr:`finished <upsies.jobs.base.JobBase.is_finished>`.

        Every key in the returned :class:`dict` is a path to a video file of
        which ``mediainfo`` was collected and/or screenshots were uploaded.

        Every value is a :class:`dict` with the keys ``mediainfo`` and
        ``screenshot_urls``.

        ``mediainfo`` is the return value of :func:`~.video.mediainfo` for the
        corresponding video file.

        ``screenshot_urls`` is a :class:`list` of screenshot URLs for the
        corresponding video file.

        .. note:: For DVDs (directories with a VIDEO_TS subdirectory), an
                  ``mediainfo`` includes an .IFO and a .VOB key while
                  ``screenshot_urls`` is empty for the .IFO key.

                  ``mediainfo`` may also be an empty :class:`str`, for example
                  if :attr:`mediainfo_from_all_videos` is `False`.

        Season example:

        .. code::

            {
              "/path/to/season/Foo.S01E01.mkv": {
                "mediainfo": "<mediainfo for Foo.S01E01.mkv>",
                "screenshot_urls": [
                  "https://image.host/Foo.S01E01.mkv.0:48:08.png",
                  "https://image.host/Foo.S01E01.mkv.1:12:12.png",
                ]
              },
            }

        DVD example:

        .. code::

            {
              "/path/to/DVD/VIDEO_TS/VTS_01_0.IFO": {
                "mediainfo": "<mediainfo for VTS_01_0.IFO>",
                "screenshot_urls": [],
              }
              "/path/to/DVD/VIDEO_TS/VTS_01_1.VOB": {
                "mediainfo": "<mediainfo for VTS_01_1.VOB>",
                "screenshot_urls": [
                  "https://image.host/VTS_01_1.VOB.0:14:58.png",
                  "https://image.host/VTS_01_1.VOB.0:26:12.png"
                ]
              }
            }
        """
        mediainfos_and_screenshots = collections.defaultdict(
            lambda: {
                'mediainfo': '',
                'screenshot_urls': [],
            }
        )

        # NOTE: Don't expect all mediainfos/screenshots to exist. A fatal
        #       KeyError traceback is always worse than manually adding missing
        #       metadata to a semi-successful upload.

        assert self.mediainfo_job.is_finished
        for video_path, mediainfo in self.mediainfo_job.mediainfos_by_file.items():
            mediainfos_and_screenshots[video_path]['mediainfo'] = mediainfo

        # `screenshots_count` screenshots for each `video_path`
        assert self.upload_screenshots_job.is_finished
        urls_by_file = self.upload_screenshots_job.urls_by_file
        screenshots_by_file = self.screenshots_job.screenshots_by_file
        for video_path, screenshot_paths in screenshots_by_file.items():
            for screenshot_path in screenshot_paths:
                screenshot_url = urls_by_file.get(screenshot_path, None)
                if screenshot_url:
                    mediainfos_and_screenshots[video_path]['screenshot_urls'].append(screenshot_url)

        return dict(mediainfos_and_screenshots)

    @functools.cached_property
    def scene_check_job(self):
        """:class:`~.jobs.scene.SceneCheckJob` instance"""
        common_job_args = self.common_job_args(ignore_cache=True)
        common_job_args['force'] = self.options.get('is_scene')
        return jobs.scene.SceneCheckJob(
            content_path=self.content_path,
            precondition=self.make_precondition('scene_check_job'),
            **common_job_args,
        )

    def make_precondition(self, job_attr, precondition=None):
        """
        Return :attr:`~.base.JobBase.precondition` function for job

        The returned function takes into account :attr:`jobs_before_upload`,
        :attr:`jobs_after_upload` and :attr:`isolated_jobs`.

        :param str job_attr: Name of the job attribute this precondition is for

            By convention, this should be ``"<name>_job"``.

        :param callable precondition: Custom :attr:`~.base.JobBase.precondition`

            `precondition` must be either `None` or return anything truthy for
            the job to get enabled.
        """
        def custom_precondition(precondition=precondition):
            return precondition is None or precondition()

        def precondition():
            job = getattr(self, job_attr)
            if not (
                    job in self.jobs_before_upload
                    or job in self.jobs_after_upload
            ):
                # Subclass doesn't use this job
                return False

            isolated_jobs = self.isolated_jobs
            if isolated_jobs and job in isolated_jobs:
                # Jobs was isolated by user (i.e. other jobs are disabled)
                return custom_precondition()

            if not isolated_jobs:
                # No isolated jobs means all jobs in jobs_before/after_upload are enabled
                return custom_precondition()

            return False

        # Rename precondition function to make debugging more readable
        precondition.__qualname__ = f'{job_attr}_precondition'
        return precondition

    _NO_DEFAULT = object()

    def get_job_output(self, job, slice=None, default=_NO_DEFAULT):
        """
        Helper method for getting output from job

        `job` must be finished.

        :param job: :class:`~.jobs.base.JobBase` instance
        :param slice: :class:`int` to get a specific item from `job`'s output,
            `None` to return all output as a list, or a :class:`slice` object to
            return only one or more items of the output
        :param default: Default value if `job` is not finished or getting
            `slice` from `job`'s output fails.

        :raise RuntimeError: if `job` is not finished or getting `slice` from
            :attr:`~.base.JobBase.output` raises an :class:`IndexError`
        :return: :class:`list` or :class:`str`
        """
        if not job.is_finished:
            if default is not self._NO_DEFAULT:
                return default
            else:
                raise RuntimeError(f'Unfinished job: {job.name}')
        else:
            if slice is None:
                slice = builtins.slice(None, None)
            try:
                return job.output[slice]
            except IndexError:
                raise RuntimeError(f'Job finished with insufficient output: {job.name}: {job.output}')

    def get_job_attribute(self, job, attribute, default=_NO_DEFAULT):
        """
        Helper method for getting an attribute from job

        :param job: :class:`~.jobs.base.JobBase` instance
        :param str attribute: Name of attribute to get from `job`
        :param default: Default value if `job` is not finished

        :raise RuntimeError: if `job` is not finished
        :raise AttributeError: if `attribute` is not an attribute of `job`
        """
        if not job.is_finished:
            if default is not self._NO_DEFAULT:
                return default
            else:
                raise RuntimeError(f'Unfinished job: {job.name}')
        else:
            return getattr(job, attribute)

    def get_relative_file_path(self, filepath):
        """
        Return `filepath` relative to :attr:`content_path`

        The first path component of the returned path is the last component of
        :attr:`content_path`.

        :raise ValueError: if logical `filepath` is not a subpath of logical
            :attr:`content_path` ("logical" means that relative path components
            are resolved while symbolic links are not resolved to get an
            absolute path)
        """
        filepath_abs = pathlib.Path(filepath).absolute()
        content_path_parent = pathlib.Path(self.content_path).absolute().parent
        try:
            return str(filepath_abs.relative_to(content_path_parent))
        except ValueError:
            raise ValueError(f'{str(filepath_abs)!r} is not a subpath of {str(content_path_parent)!r}')

    def make_screenshots_grid(self, screenshots, columns=2, horizontal_spacer='  ', vertical_spacer='\n'):
        """
        Return BBcode for screenshots in a grid layout

        :param screenshots: Sequence of :class:`~.imghosts.common.UploadedImage`
            objects (URLs with a ``thumbnail_url`` attribute)
        :param int columns: How many columns to split screenshots into
        :param str horizontal_spacer: String between columns
        :param str vertical_spacer: String between rows

        :raise RuntimeError: if any screenshot doesn't have a thumbnail
        """
        groups = utils.as_groups(
            screenshots,
            group_sizes=(columns,),
            default=None,
        )

        rows = []
        for screenshots in groups:
            cells = []
            for screenshot in screenshots:
                # `screenshot` is `None` at the end if the number of screenshots
                # is not perfectly divisible by `columns`
                if screenshot is not None:
                    if screenshot.thumbnail_url is None:
                        raise RuntimeError(f'No thumbnail for {screenshot}')
                    cells.append(f'[url={screenshot}][img]{screenshot.thumbnail_url}[/img][/url]')

            # Space between columns
            rows.append(horizontal_spacer.join(cells))

        # Space between rows
        return vertical_spacer.join(rows)
