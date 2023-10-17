"""
Find, download and re-upload poster for movie, series or season
"""

import functools

from .... import jobs, utils
from .base import CommandBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class poster(CommandBase):
    """Download, resize and re-upload poster from IMDb or similar website"""

    names = ('poster',)

    argument_definitions = {
        'RELEASE': {
            'type': utils.argtypes.release,
            'help': 'Release name or path to release content',
        },
        ('--db', '-d'): {
            'type': utils.argtypes.webdb,
            'help': ('Case-insensitive database name (default: imdb)\n'
                     'Supported databases: ' + ', '.join(utils.webdbs.webdb_names())),
            'default': None,
        },
        ('--upload-to', '-u'): {
            'type': utils.argtypes.imghost,
            'metavar': 'IMAGEHOST',
            'help': ('Case-insensitive name of image hosting service\n'
                     'Supported services: ' + ', '.join(utils.imghosts.imghost_names())),
            'default': None,
        },
        ('--width', '-w'): {
            'help': 'Maximum poster width in pixels (default: 500)',
            'type': utils.argtypes.integer,
            'default': 500,
        },
        ('--height', '-t'): {
            'help': 'Maximum poster height in pixels (default: 1000)',
            'type': utils.argtypes.integer,
            'default': 1000,
        },
    }

    @functools.cached_property
    def release_name(self):
        return utils.release.ReleaseName(self.args.RELEASE)

    @functools.cached_property
    def webdb(self):
        if self.args.db:
            return utils.webdbs.webdb(self.args.db)
        elif self.release_name.type in (utils.release.ReleaseType.season,
                                        utils.release.ReleaseType.episode):
            return utils.webdbs.webdb('tvmaze')
        else:
            return utils.webdbs.webdb('imdb')

    @functools.cached_property
    def imghost(self):
        if self.args.upload_to:
            return utils.imghosts.imghost(
                name=self.args.upload_to,
                options=self.config['imghosts'][self.args.upload_to],
                cache_directory=self.cache_directory,
            )

    @functools.cached_property
    def jobs(self):
        return (
            self.webdb_job,
            self.poster_job,
        )

    @functools.cached_property
    def webdb_job(self):
        return jobs.webdb.WebDbSearchJob(
            home_directory=self.cache_directory,
            cache_directory=self.cache_directory,
            ignore_cache=self.args.ignore_cache,
            query=utils.webdbs.Query.from_release(self.release_name),
            db=self.webdb,
            callbacks={
                'output': self.start_poster_job,
            },
        )

    def start_poster_job(self, webdb_id):
        self.poster_job.start(
            webdb_id=webdb_id,
            season=self.release_name.only_season,
        )

    @functools.cached_property
    def poster_job(self):
        return jobs.poster.PosterJob(
            home_directory=self.home_directory if self.imghost else '.',
            cache_directory=self.cache_directory,
            ignore_cache=self.args.ignore_cache,
            autostart=False,
            webdb_id=None,
            webdb=self.webdb,
            imghost=self.imghost,
            width=self.args.width,
            height=self.args.height,
        )
