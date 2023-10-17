from unittest.mock import AsyncMock, PropertyMock

from upsies import __project_name__, utils
from upsies.trackers import base


def make_MockTracker(**kwargs):
    class MockTracker(base.TrackerBase):
        name = 'asdf'
        label = 'AsdF'
        TrackerJobs = PropertyMock()
        TrackerConfig = PropertyMock()
        login = AsyncMock()
        logout = AsyncMock()
        _login = AsyncMock()
        _logout = AsyncMock()
        is_logged_in = PropertyMock()
        get_announce_url = AsyncMock()
        upload = AsyncMock()

    return MockTracker(**kwargs)


def test_Howto_current_section_and_bump_section():
    howto = base._howto.Howto(tracker_cls=type(make_MockTracker()))
    for i in range(10):
        for _ in range(3):
            assert howto.current_section == i

        assert howto.bump_section == ''

        for _ in range(3):
            assert howto.current_section == i + 1

def test_Howto_introduction():
    howto = base._howto.Howto(tracker_cls=type(make_MockTracker()))
    howto._section = 123
    assert howto.introduction == (
        '123. How To Read This Howto\n'
        '\n'
        '   123.1 Words in ALL_CAPS_AND_WITH_UNDERSCORES are placeholders.\n'
        '   123.2 Everything after "$" is a terminal command.'
    )

def test_Howto_screenshots():
    tracker_cls = type(make_MockTracker())
    howto = base._howto.Howto(tracker_cls=tracker_cls)
    howto._section = 6
    assert howto.screenshots == (
        '6. Screenshots (Optional)\n'
        '\n'
        '   6.1 Specify how many screenshots to make.\n'
        f'       $ {__project_name__} set trackers.{tracker_cls.name}.screenshots NUMBER_OF_SCREENSHOTS\n'
        '\n'
        '   6.2 Specify where to host images.\n'
        f'       $ {__project_name__} set trackers.{tracker_cls.name}.image_host IMAGE_HOST\n'
        '       Supported services: dummy, freeimage, imgbb, imgbox, ptpimg\n'
        '\n'
        '   6.3 Configure image hosting service.\n'
        f'       $ {__project_name__} upload-images IMAGE_HOST --help'
    )

def test_Howto_autoseed():
    tracker_cls = type(make_MockTracker())
    howto = base._howto.Howto(tracker_cls=tracker_cls)
    howto._section = 7
    assert howto.autoseed == (
        '7. Add Uploaded Torrents To Client (Optional)\n'
        '\n'
        '   7.1 Specify which client to add uploaded torrents to.\n'
        f'       $ {__project_name__} set trackers.{tracker_cls.name}.add_to CLIENT_NAME\n'
        f'       Supported clients: {", ".join(n for n in utils.btclient.client_names())}\n'
        '\n'
        '   7.2 Specify your client connection.\n'
        f'       $ {__project_name__} set clients.CLIENT_NAME.url URL\n'
        f'       $ {__project_name__} set clients.CLIENT_NAME.username USERNAME\n'
        f'       $ {__project_name__} set clients.CLIENT_NAME.password PASSWORD\n'
        '\n'
        '8. Copy Uploaded Torrents To Directory (Optional)\n'
        '\n'
        f'   $ {__project_name__} set trackers.{tracker_cls.name}.copy_to /path/to/directory'
    )

def test_Howto_upload():
    tracker_cls = type(make_MockTracker())
    howto = base._howto.Howto(tracker_cls=tracker_cls)
    howto._section = 123
    assert howto.upload == (
        '123. Upload\n'
        '\n'
        f'   $ {__project_name__} submit {tracker_cls.name} --help\n'
        f'   $ {__project_name__} submit {tracker_cls.name} /path/to/content'
    )
