"""
Create screenshots from video file and optionally upload them
"""

import functools

from .... import jobs, utils
from .base import CommandBase


class screenshots(CommandBase):
    """Create screenshots from video file and optionally upload them"""

    names = ('screenshots', 'ss')

    argument_definitions = {
        'CONTENT': {
            'type': utils.argtypes.content,
            'help': 'Path to release content',
        },
        ('--exclude-files', '--ef'): {
            'nargs': '+',
            'metavar': 'PATTERN',
            'help': ('Glob pattern to exclude from CONTENT '
                     '(matched case-insensitively against path relative to CONTENT)'),
            'default': (),
        },
        ('--exclude-files-regex', '--efr'): {
            'nargs': '+',
            'metavar': 'PATTERN',
            'help': ('Regular expression to exclude from CONTENT '
                     '(matched case-sensitively against path relative to CONTENT)'),
            'type': utils.argtypes.regex,
            'default': (),
        },
        ('--timestamps', '-t'): {
            'nargs': '+',
            'default': (),
            'type': utils.argtypes.timestamp,
            'metavar': 'TIMESTAMP',
            'help': 'Space-separated list of [[HH:]MM:]SS strings',
        },
        ('--number', '-n'): {
            'type': utils.argtypes.integer,
            'help': 'How many screenshots to make in total',
            'default': 0,
        },
        ('--from-all-videos', '-a'): {
            'action': 'store_true',
            'help': 'Make NUMBER screenshots from each video file beneath CONTENT',
        },
        ('--optimize', '--opt'): {
            'type': utils.argtypes.one_of(utils.image.optimization_levels),
            'default': None,
            'metavar': 'LEVEL',
            'help': f'File size optimization level: {", ".join(utils.image.optimization_levels)}',
        },
        ('--upload-to', '-u'): {
            'type': utils.argtypes.imghost,
            'metavar': 'IMAGEHOST',
            'help': ('Case-insensitive name of image hosting service\n'
                     'Supported services: ' + ', '.join(utils.imghosts.imghost_names())),
        },
        ('--output-directory', '-o'): {
            'default': '',  # Current working directory
            'metavar': 'PATH',
            'help': 'Directory where screenshots are put (created on demand)',
        },
    }

    @functools.cached_property
    def screenshots_job(self):
        return jobs.screenshots.ScreenshotsJob(
            home_directory=self.args.output_directory,
            cache_directory=self.cache_directory,
            ignore_cache=self.args.ignore_cache,
            content_path=self.args.CONTENT,
            exclude_files=(
                tuple(self.args.exclude_files)
                + tuple(self.args.exclude_files_regex)
            ),
            timestamps=self.args.timestamps,
            count=self.args.number,
            from_all_videos=self.args.from_all_videos,
            optimize=(
                self.args.optimize
                if self.args.optimize is not None else
                self.config['config']['screenshots']['optimize']
            ),
        )

    @functools.cached_property
    def upload_screenshots_job(self):
        if self.args.upload_to:
            imghost_job = jobs.imghost.ImageHostJob(
                home_directory=self.home_directory,
                cache_directory=self.cache_directory,
                ignore_cache=self.args.ignore_cache,
                imghost=utils.imghosts.imghost(
                    name=self.args.upload_to,
                    options=self.config['imghosts'][self.args.upload_to],
                ),
            )
            # Timestamps and number of screenshots are determined in a
            # subprocess, we have to wait for that before we can set the number
            # of expected screenhots.
            self.screenshots_job.signal.register('screenshots_total', imghost_job.set_images_total)
            # Pass ScreenshotsJob's output to ImageHostJob input.
            self.screenshots_job.signal.register('output', imghost_job.enqueue)
            # Tell imghost_job to finish the current upload and then finish.
            self.screenshots_job.signal.register('finished', lambda _: imghost_job.finalize())
            return imghost_job

    @functools.cached_property
    def jobs(self):
        return (
            self.screenshots_job,
            self.upload_screenshots_job,
        )
