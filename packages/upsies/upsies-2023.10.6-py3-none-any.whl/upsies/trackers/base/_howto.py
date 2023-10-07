"""
Standardized configuration and setup howto
"""

from ... import __project_name__, utils


class Howto:
    def __init__(self, tracker_cls):
        self._tracker_cls = tracker_cls
        self._section = 0

    def _autobump(self, sections):
        self._section += len(sections)
        return '\n'.join(sections).strip()

    @property
    def current_section(self):
        return self._section

    @property
    def bump_section(self):
        self._section += 1
        return ''

    @property
    def introduction(self):
        return self._autobump((
            (
                f'{self._section}. How To Read This Howto\n'
                '\n'
                f'   {self._section}.1 Words in ALL_CAPS_AND_WITH_UNDERSCORES are placeholders.\n'
                f'   {self._section}.2 Everything after "$" is a terminal command.\n'
            ),
        ))

    @property
    def screenshots(self):
        return self._autobump((
            (
                f'{self._section}. Screenshots (Optional)\n'
                '\n'
                f'   {self._section}.1 Specify how many screenshots to make.\n'
                f'       $ {__project_name__} set trackers.{self._tracker_cls.name}.screenshots NUMBER_OF_SCREENSHOTS\n'
            ),
            (
                f'   {self._section}.2 Specify where to host images.\n'
                f'       $ {__project_name__} set trackers.{self._tracker_cls.name}.image_host IMAGE_HOST\n'
                f'       Supported services: ' + ', '.join(utils.imghosts.imghost_names()) + '\n'
                '\n'
                f'   {self._section}.3 Configure image hosting service.\n'
                f'       $ {__project_name__} upload-images IMAGE_HOST --help\n'
            ),
        ))

    @property
    def autoseed(self):
        return self._autobump((
            (
                f'{self._section}. Add Uploaded Torrents To Client (Optional)\n'
                '\n'
                f'   {self._section}.1 Specify which client to add uploaded torrents to.\n'
                f'       $ {__project_name__} set trackers.{self._tracker_cls.name}.add_to CLIENT_NAME\n'
                f'       Supported clients: ' + ', '.join(utils.btclient.client_names()) + '\n'
            ),
            (
                f'   {self._section}.2 Specify your client connection.\n'
                f'       $ {__project_name__} set clients.CLIENT_NAME.url URL\n'
                f'       $ {__project_name__} set clients.CLIENT_NAME.username USERNAME\n'
                f'       $ {__project_name__} set clients.CLIENT_NAME.password PASSWORD\n'
                '\n'
                f'{self._section + 1}. Copy Uploaded Torrents To Directory (Optional)\n'
                '\n'
                f'   $ {__project_name__} set trackers.{self._tracker_cls.name}.copy_to /path/to/directory\n'
            ),
        ))

    @property
    def upload(self):
        return self._autobump((
            (
                f'{self._section}. Upload\n'
                '\n'
                f'   $ {__project_name__} submit {self._tracker_cls.name} --help\n'
                f'   $ {__project_name__} submit {self._tracker_cls.name} /path/to/content\n'
            ),
        ))
