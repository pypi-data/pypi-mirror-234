"""
Concrete :class:`~.base.TrackerJobsBase` subclass for MTV
"""

import functools
import re

from ... import __homepage__, __project_name__, errors, jobs, utils
from ...utils.release import ReleaseType
from ..base import TrackerJobsBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class MtvTrackerJobs(TrackerJobsBase):

    @functools.cached_property
    def jobs_before_upload(self):
        return (
            # Background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,

            # Interactive jobs
            self.category_job,
            self.imdb_job,
            self.scene_check_job,
            self.title_job,
            self.description_job,
        )

    @property
    def isolated_jobs(self):
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
                self.title_job,
            )
        else:
            # Activate all jobs
            return ()

    @functools.cached_property
    def category_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('category'),
            label='Category',
            precondition=self.make_precondition('category_job'),
            autodetect=self.autodetect_category,
            choices=[
                (c['label'], c['value'])
                for c in self._categories
            ],
            callbacks={
                'finished': self.update_imdb_query,
            },
            **self.common_job_args(),
        )

    def update_imdb_query(self, category_job_):
        """
        Set :attr:`~.webdbs.common.Query.type` on
        :attr:`~.TrackerJobsBase.imdb_job` to :attr:`chosen_release_type`
        """
        old_type = self.imdb_job.query.type
        new_type = self.chosen_release_type
        if new_type is not None:
            _log.debug('Updating IMDb query from %s to %s', old_type, new_type)
            self.imdb_job.query.type = new_type

    _categories = (
        {'label': 'HD Season', 'value': '5', 'type': ReleaseType.season},
        {'label': 'HD Episode', 'value': '3', 'type': ReleaseType.episode},
        {'label': 'HD Movie', 'value': '1', 'type': ReleaseType.movie},
        {'label': 'SD Season', 'value': '6', 'type': ReleaseType.season},
        {'label': 'SD Episode', 'value': '4', 'type': ReleaseType.episode},
        {'label': 'SD Movie', 'value': '2', 'type': ReleaseType.movie},
    )

    _category_value_type_map = {
        c['value']: c['type']
        for c in _categories
    }

    def autodetect_category(self, _):
        # "HD" or "SD"
        if utils.video.resolution_int(self.content_path) >= 720:
            resolution = 'HD'
        else:
            resolution = 'SD'

        # "Movie", "Episode" or "Season"
        if self.release_name.type is ReleaseType.movie:
            typ = 'Movie'
        elif self.release_name.type is ReleaseType.season:
            typ = 'Season'
        elif self.release_name.type is ReleaseType.episode:
            typ = 'Episode'
        else:
            raise RuntimeError(f'Unsupported type: {self.release_name.type}')

        category = f'{resolution} {typ}'
        _log.debug('Autodetected category: %r', category)
        return category

    @property
    def chosen_release_type(self):
        """
        :class:`~.types.ReleaseType` enum derived from :attr:`category_job` or
        `None` if :attr:`category_job` is not finished yet
        """
        if self.category_job.is_finished:
            choice = self.get_job_attribute(self.category_job, 'choice')
            return self._category_value_type_map.get(choice)

    release_name_separator = '.'

    release_name_translation = {
        'edition': {
            re.compile(r"^Director's Cut$"): r'DC',
        },
        'group': {
            re.compile(r'^NOGROUP$'): r'NOGRP',
        },
    }

    @functools.cached_property
    def title_job(self):
        """
        :class:`~.jobs.dialog.TextFieldJob` instance with text set to the
        release title

        Unlike :attr:`~.TrackerJobsBase.release_name_job`, this uses the
        original scene release name for movie and episode scene releases.
        """
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('title'),
            label='Title',
            precondition=self.make_precondition('title_job'),
            prejobs=(
                self.category_job,
                self.scene_check_job,
                self.imdb_job,
            ),
            text=self.generate_title,
            validator=self.validate_title,
            **self.common_job_args(),
        )

    async def generate_title(self):
        assert self.scene_check_job.is_finished
        assert self.imdb_job.is_finished

        try:
            if self.chosen_release_type in (ReleaseType.movie, ReleaseType.episode):
                if self.scene_check_job.is_scene_release:
                    # Use the original scene release name instead of a
                    # standardized release name. We rely on scene_check_job
                    # making sure that the file/directory name is the correct
                    # release name.
                    search_results = await utils.predbs.MultiPredbApi().search(self.content_path)
                    assert len(search_results) >= 1, search_results
                    return search_results[0]

            # We're dealing with a non-scene release or season pack.
            # We may generate a title.
            await self.release_name.fetch_info(webdb=self.imdb, webdb_id=self.imdb_id)

        except errors.RequestError as e:
            _log.debug('Fetching title failed: %r', e)

        return str(self.release_name)

    def validate_title(self, text):
        if not text.strip():
            raise ValueError('Title must not be empty')

        match = re.search(rf'(?:{utils.release.DELIM}|$)(UNKNOWN_([A-Z_]+))(?:{utils.release.DELIM}|$)', text)
        if match:
            placeholder = match.group(1)
            name = match.group(2).lower().replace('_', ' ')
            raise ValueError(f'Replace "{placeholder}" with the correct {name}')

    image_host_config = {
        'common': {'thumb_width': 300},
    }

    @functools.cached_property
    def description_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('description'),
            label='Description',
            precondition=self.make_precondition('description_job'),
            prejobs=(
                self.mediainfo_job,
                self.upload_screenshots_job,
            ),
            text=self.generate_description,
            finish_on_success=True,
            read_only=True,
            hidden=True,
            # Don't cache job output because the number of screenshots can be
            # changed by the user between runs.
            **self.common_job_args(ignore_cache=True),
        )

    async def generate_description(self):
        sections = []
        section = []
        for video_path, info in self.mediainfos_and_screenshots.items():
            if info['mediainfo']:
                section.append(
                    f'[mediainfo]{info["mediainfo"]}[/mediainfo]\n'
                )

            if info['screenshot_urls']:
                section.append((
                    '[center]'
                    + self.make_screenshots_grid(
                        screenshots=info['screenshot_urls'],
                        columns=2,
                        horizontal_spacer='    ',
                        vertical_spacer='\n\n',
                    )
                    + '[/center]'
                ))
                sections.append(''.join(section))
                section.clear()

        description = '\n[hr]\n'.join(sections)
        promotion = (
            '[align=right][size=1]'
            f'Shared with [url={__homepage__}]{__project_name__}[/url]'
            '[/size][/align]'
        )
        return (
            description
            + '\n'
            + promotion
        )

    @property
    def post_data_autofill(self):
        return {
            'submit': 'true',
            'MAX_FILE_SIZE': '2097152',
            'fillonly': 'auto fill',
            'category': '0',
            'Resolution': '0',
            'source': '12',
            'origin': '6',
            'title': '',
            'genre_tags': '---',
            'taglist': '',
            'autocomplete_toggle': 'on',
            'image': '',
            'desc': '',
            'fontfont': '-1',
            'fontsize': '-1',
            'groupDesc': '',
            'anonymous': '0',
        }

    @property
    def post_data_upload(self):
        return {
            'submit': 'true',
            'category': self.get_job_attribute(self.category_job, 'choice'),
            'Resolution': '0',
            'source': '12',
            'origin': '6',
            'title': self.get_job_output(self.title_job, slice=0),
            'genre_tags': '---',
            'autocomplete_toggle': 'on',
            'image': '',
            'desc': self.get_job_output(self.description_job, slice=0),
            'fontfont': '-1',
            'fontsize': '-1',
            'groupDesc': '',
            'anonymous': '1' if self.options['anonymous'] else '0',
            'ignoredupes': '1' if self.options['ignore_dupes'] else None,
            'imdbID': self.get_job_output(self.imdb_job, slice=0),
            # 'tmdbID': ...,
            # 'thetvdbID': ...,
            # 'tvmazeID': ...,
        }

    @property
    def torrent_filepath(self):
        return self.get_job_output(self.create_torrent_job, slice=0)
