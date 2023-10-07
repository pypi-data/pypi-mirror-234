"""
Concrete :class:`~.base.TrackerJobsBase` subclass for BHD
"""

import functools
import io

from ... import __homepage__, __project_name__, errors, jobs, utils
from ..base import TrackerJobsBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class BhdTrackerJobs(TrackerJobsBase):

    @functools.cached_property
    def jobs_before_upload(self):
        return (
            # Background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,

            # Interactive jobs
            self.tmdb_job,
            self.imdb_job,
            self.release_name_job,
            self.category_job,
            self.type_job,
            self.source_job,
            self.description_job,
            self.scene_check_job,
            self.tags_job,
        )

    @property
    def isolated_jobs(self):
        """
        Sequence of job attribute names (e.g. "imdb_job") that were singled
        out by the user, e.g. with a CLI argument
        """
        if self.options.get('only_description', False):
            return self.get_job_and_dependencies(
                self.description_job,
                # `screenshots_job` is needed by `upload_screenshots_job`, but
                # `upload_screenshots_job` is a `QueueJobBase`, which doesn't
                # know anything about the job it gets input from and therefore
                # can't tells us that it needs `screenshots_job`.
                self.screenshots_job,
            )
        elif self.options.get('only_title', False):
            return self.get_job_and_dependencies(
                self.release_name_job,
                # `release_name_job` doesn't depend on `imdb_job` (or any other
                # webdb), but we want the correct name, year, etc in the release
                # name.
                self.imdb_job,
            )
        else:
            # Activate all jobs in jobs_before/after_upload
            return ()

    @functools.cached_property
    def tmdb_job(self):
        tmdb_job = super().tmdb_job
        tmdb_job.no_id_ok = True
        return tmdb_job

    @functools.cached_property
    def category_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('category'),
            label='Category',
            precondition=self.make_precondition('category_job'),
            prejobs=(
                self.release_name_job,
            ),
            autodetect=self.autodetect_category,
            choices=(
                ('Movie', '1'),
                ('TV', '2'),
            ),
            **self.common_job_args(),
        )

    _autodetect_category_map = {
        'Movie': lambda release_name: release_name.type is utils.release.ReleaseType.movie,
        'TV': lambda release_name: release_name.type in (utils.release.ReleaseType.season,
                                                         utils.release.ReleaseType.episode)
    }

    def autodetect_category(self, _):
        approved_release_name = self.release_name
        _log.debug('Autodetecting category: Approved release type: %r', approved_release_name.type)
        for label, is_match in self._autodetect_category_map.items():
            if is_match(approved_release_name):
                return label

    @functools.cached_property
    def type_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('type'),
            label='Type',
            precondition=self.make_precondition('type_job'),
            prejobs=(
                self.release_name_job,
            ),
            autodetect_and_finish=self.autodetect_type,
            choices=(
                ('UHD 100', 'UHD 100'),
                ('UHD 66', 'UHD 66'),
                ('UHD 50', 'UHD 50'),
                ('UHD Remux', 'UHD Remux'),
                ('BD 50', 'BD 50'),
                ('BD 25', 'BD 25'),
                ('BD Remux', 'BD Remux'),
                ('2160p', '2160p'),
                ('1080p', '1080p'),
                ('1080i', '1080i'),
                ('720p', '720p'),
                ('576p', '576p'),
                ('540p', '540p'),
                ('DVD 9', 'DVD 9'),
                ('DVD 5', 'DVD 5'),
                ('DVD Remux', 'DVD Remux'),
                ('480p', '480p'),
                ('Other', 'Other'),
            ),
            focused='Other',
            **self.common_job_args(),
        )

    _autodetect_type_map = {
        'DVD 9': lambda release_name: release_name.source == 'DVD9',
        'DVD 5': lambda release_name: release_name.source == 'DVD5',
        'DVD Remux': lambda release_name: release_name.source == 'DVD Remux',
        '2160p': lambda release_name: release_name.resolution == '2160p',
        '1080p': lambda release_name: release_name.resolution == '1080p',
        '1080i': lambda release_name: release_name.resolution == '1080i',
        '720p': lambda release_name: release_name.resolution == '720p',
        '576p': lambda release_name: release_name.resolution == '576p',
        '540p': lambda release_name: release_name.resolution == '540p',
        '480p': lambda release_name: release_name.resolution == '480p',
    }

    def autodetect_type(self, _):
        approved_release_name = self.release_name
        _log.debug('Autodetecting type: Approved resolution: %r', approved_release_name.resolution)
        _log.debug('Autodetecting type: Approved source: %r', approved_release_name.source)
        for label, is_match in self._autodetect_type_map.items():
            if is_match(approved_release_name):
                return label

    @functools.cached_property
    def source_job(self):
        # 'output' signal is only emitted when job succeeds while 'finished'
        # signal is also emitted when job fails (e.g. when Ctrl-c is pressed)
        self.release_name_job.signal.register('output', self.autodetect_source)

        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('source'),
            label='Source',
            precondition=self.make_precondition('source_job'),
            prejobs=(
                self.release_name_job,
            ),
            autodetect_and_finish=self.autodetect_source,
            choices=(
                ('Blu-ray', 'Blu-ray'),
                ('HD-DVD', 'HD-DVD'),
                ('WEB', 'WEB'),
                ('HDTV', 'HDTV'),
                ('DVD', 'DVD'),
            ),
            **self.common_job_args(),
        )

    # Map type_job labels to matchers
    _autodetect_source_map = {
        'Blu-ray': lambda release_name: 'BluRay' in release_name.source,
        'HD-DVD': lambda release_name: 'HD-DVD' in release_name.source,
        'WEB': lambda release_name: 'WEB' in release_name.source,
        'HDTV': lambda release_name: 'HDTV' in release_name.source,
        'DVD': lambda release_name: 'DVD' in release_name.source,
    }

    def autodetect_source(self, _):
        approved_release_name = self.release_name
        _log.debug('Autodetecting source: Approved source: %r', approved_release_name.source)
        for label, is_match in self._autodetect_source_map.items():
            if is_match(approved_release_name):
                return label

    @functools.cached_property
    def description_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('description'),
            label='Description',
            precondition=self.make_precondition('description_job'),
            prejobs=(
                self.upload_screenshots_job,
                self.mediainfo_job,
            ),
            text=self.generate_description,
            hidden=True,
            finish_on_success=True,
            read_only=True,
            **self.common_job_args(ignore_cache=True),
        )

    image_host_config = {
        'common': {'thumb_width': 350},
    }

    def generate_description(self):
        screenshot_tags = self._generate_description_screenshots()
        mediainfo_tags = self._generate_description_mediainfos()
        promotion_tag = (
            '[align=right][size=1]'
            f'Shared with [url={__homepage__}]{__project_name__}[/url]'
            '[/size][/align]'
        )

        description_parts = [
            '[center]\n'
            + screenshot_tags
            + '\n[/center]'
        ]
        if mediainfo_tags:
            # Include mediainfos if there are multiple (e.g. for IFO/VOB or if
            # `mediainfo_from_all_videos` is True)
            description_parts.append(
                '\n'
                + '[center][h3]Mediainfo[/h3][/center]\n'
                + mediainfo_tags
            )
        description_parts.append(f'\n\n{promotion_tag}')

        return ''.join(description_parts)

    def _generate_description_screenshots(self):
        assert self.upload_screenshots_job.is_finished
        return self.make_screenshots_grid(
            screenshots=self.upload_screenshots_job.uploaded_images,
            columns=2,
            horizontal_spacer='   ',
            vertical_spacer='\n\n',
        )

    def _generate_description_mediainfos(self):
        mediainfo_tags = []
        for video_filepath, mediainfo in self._description_mediainfos.items():
            filetitle = self.get_relative_file_path(video_filepath)
            mediainfo_tags.append(
                f'[hide={filetitle}][code]{mediainfo}[/code][/hide]'
            )
        return '\n'.join(mediainfo_tags)

    @property
    def _description_mediainfos(self):
        # If there are multiple files in the release, mediainfo for each file is
        # put in the description. Otherwise, the only needed mediainfo is passed
        # separately from the description
        assert self.mediainfo_job.is_finished
        mediainfos_by_file = self.mediainfo_job.mediainfos_by_file
        if len(mediainfos_by_file) >= 2:
            return {
                filepath: mediainfo
                for filepath, mediainfo in mediainfos_by_file.items()
                if mediainfo
            }
        else:
            return {}

    mediainfo_from_all_videos = False
    screenshots_from_all_videos = False

    @functools.cached_property
    def tags_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('tags'),
            label='Tags',
            precondition=self.make_precondition('tags_job'),
            prejobs=(
                self.release_name_job,
                self.scene_check_job,
            ),
            text=self.generate_tags,
            finish_on_success=True,
            read_only=True,
            **self.common_job_args(),
        )

    async def generate_tags(self):
        assert self.release_name_job.is_finished
        assert self.scene_check_job.is_finished

        # Any additional tags separated by comma(s). (Commentary, 2in1, Hybrid,
        # OpenMatte, 2D3D, WEBRip, WEBDL, 3D, 4kRemaster, DualAudio, EnglishDub,
        # Personal, Scene, DigitalExtras, Extras)
        tags = []
        if 'WEBRip' in self.release_name.source:
            tags.append('WEBRip')
        elif 'WEB-DL' in self.release_name.source:
            tags.append('WEBDL')
        if 'Hybrid' in self.release_name.source:
            tags.append('Hybrid')
        if self.release_name.has_commentary:
            tags.append('Commentary')
        if self.release_name.has_dual_audio:
            tags.append('DualAudio')
        if 'Open Matte' in self.release_name.edition:
            tags.append('OpenMatte')
        if '2in1' in self.release_name.edition:
            tags.append('2in1')
        if '4k Remastered' in self.release_name.edition:
            tags.append('4kRemaster')
        if self.get_job_attribute(self.scene_check_job, 'is_scene_release'):
            tags.append('Scene')
        if self.options['personal_rip']:
            tags.append('Personal')

        # TODO: 2D3D
        # TODO: 3D
        # TODO: EnglishDub
        # TODO: DigitalExtras
        # TODO: Extras

        return '\n'.join(tags)

    @property
    def post_data(self):
        return {
            'name': self.get_job_output(self.release_name_job, slice=0),
            'category_id': self.get_job_attribute(self.category_job, 'choice'),
            'type': self.get_job_attribute(self.type_job, 'choice'),
            'source': self.get_job_attribute(self.source_job, 'choice'),
            'imdb_id': self.get_job_output(self.imdb_job, slice=0),
            'tmdb_id': self.post_data_tmdb_id,
            'description': self.get_job_output(self.description_job, slice=0),
            'edition': self.post_data_edition,
            'custom_edition': self.options['custom_edition'],
            'tags': ','.join(self.get_job_output(self.tags_job, slice=0).split('\n')),
            'nfo': self.post_data_nfo,
            'pack': self.post_data_pack,
            'sd': self.post_data_sd,
            'special': self.post_data_special,
            'anon': '1' if self.options['anonymous'] else '0',
            'live': '0' if self.options['draft'] else '1',
        }

    @functools.cached_property
    def post_data_tmdb_id(self):
        # TMDb ID may be 0 for non-existing shows
        if self.tmdb_job.output:
            return self.get_job_output(self.tmdb_job, slice=0).split('/')[1]
        else:
            return 0

    @functools.cached_property
    def post_data_edition(self):
        # The edition of the uploaded release. (Collector, Director, Extended,
        # Limited, Special, Theatrical, Uncut or Unrated)
        edition = self.release_name.edition
        _log.debug('Approved edition: %r', edition)
        if "Collector's Edition" in edition:
            return 'Collector'
        elif "Director's Cut" in edition:
            return 'Director'
        elif 'Extended Cut' in edition:
            return 'Extended'
        elif 'Limited' in edition:
            return 'Limited'
        elif 'Special Edition' in edition:
            return 'Special'
        elif 'Theatrical Cut' in edition:
            return 'Theatrical'
        elif 'Uncut' in edition or 'Uncensored' in edition:
            return 'Uncut'
        elif 'Unrated' in edition:
            return 'Unrated'

    @property
    def post_data_pack(self):
        # The TV pack flag for when the torrent contains a complete season.
        # (0 = No TV pack or 1 = TV Pack). Default is 0
        if self.release_name.type is utils.release.ReleaseType.season:
            return '1'
        else:
            return '0'

    @property
    def post_data_sd(self):
        # The SD flag. (0 = Not Standard Definition, 1 = Standard Definition).
        # Default is 0
        try:
            height = int(self.release_name.resolution[:-1])
        except ValueError:
            return '0'
        else:
            return '1' if height < 720 else '0'

    max_nfo_size = 500_000

    @property
    def post_data_nfo(self):
        try:
            return utils.string.read_nfo(self.content_path)
        except errors.ContentError as e:
            self.error(e)

    @property
    def post_data_special(self):
        # The TV special flag for when the torrent contains a TV special. (0 =
        # Not a TV special, 1 = TV Special). Default is 0
        if self.release_name.type is utils.release.ReleaseType.episode:
            if self.options['special']:
                return '1'
        return '0'

    # TODO
    # @property
    # def post_data_region(self):
    #     # The region in which the disc was released. Only for discs! (AUS,
    #     # CAN, CEE, CHN, ESP, EUR, FRA, GBR, GER, HKG, ITA, JPN, KOR, NOR,
    #     # NLD, RUS, TWN or USA)

    @property
    def torrent_filepath(self):
        return self.get_job_output(self.create_torrent_job, slice=0)

    @property
    def mediainfo_filehandle(self):
        mediainfo = self.get_job_output(self.mediainfo_job, slice=0)
        return io.BytesIO(bytes(mediainfo, 'utf-8'))
