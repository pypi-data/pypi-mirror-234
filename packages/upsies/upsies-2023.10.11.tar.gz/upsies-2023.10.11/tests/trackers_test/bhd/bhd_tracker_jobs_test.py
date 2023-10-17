from types import SimpleNamespace
from unittest.mock import DEFAULT, Mock, PropertyMock, call

import pytest

from upsies import __homepage__, __project_name__, errors, utils
from upsies.trackers import bhd


@pytest.fixture
def tracker():
    tracker = Mock()
    tracker.name = 'bhd'
    return tracker


@pytest.fixture
def imghost():
    class MockImageHost(utils.imghosts.base.ImageHostBase):
        name = 'mock image host'
        default_config = {}

        async def _upload_image(self, path):
            pass

    return MockImageHost()


@pytest.fixture
def bhd_tracker_jobs(imghost, tracker, tmp_path, mocker):
    content_path = tmp_path / 'Foo 2000 1080p BluRay x264-ASDF'

    bhd_tracker_jobs = bhd.BhdTrackerJobs(
        content_path=str(content_path),
        tracker=tracker,
        image_host=imghost,
        btclient=Mock(),
        torrent_destination=str(tmp_path / 'destination'),
        common_job_args={
            'home_directory': str(tmp_path / 'home_directory'),
            'ignore_cache': True,
        },
        options=None,
    )

    return bhd_tracker_jobs


@pytest.fixture
def mock_job_attributes(mocker):
    def mock_job_attributes(bhd_tracker_jobs):
        job_attrs = (
            # Background jobs
            'create_torrent_job',
            'mediainfo_job',
            'screenshots_job',
            'upload_screenshots_job',

            # Interactive jobs
            'tmdb_job',
            'imdb_job',
            'release_name_job',
            'category_job',
            'type_job',
            'source_job',
            'description_job',
            'scene_check_job',
            'tags_job',
        )
        for job_attr in job_attrs:
            mocker.patch.object(type(bhd_tracker_jobs), job_attr, PropertyMock(return_value=Mock(attr=job_attr)))

    return mock_job_attributes


def test_jobs_before_upload_items(bhd_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(bhd_tracker_jobs)

    print(bhd_tracker_jobs.jobs_before_upload)
    assert tuple(job.attr for job in bhd_tracker_jobs.jobs_before_upload) == (
        # Background jobs
        'create_torrent_job',
        'mediainfo_job',
        'screenshots_job',
        'upload_screenshots_job',

        # Interactive jobs
        'tmdb_job',
        'imdb_job',
        'release_name_job',
        'category_job',
        'type_job',
        'source_job',
        'description_job',
        'scene_check_job',
        'tags_job',
    )


def test_isolated_jobs__only_description(bhd_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(bhd_tracker_jobs)
    mocker.patch.object(type(bhd_tracker_jobs), 'options', PropertyMock(return_value={'only_description': True}))
    mocker.patch.object(bhd_tracker_jobs, 'get_job_and_dependencies')
    assert bhd_tracker_jobs.isolated_jobs is bhd_tracker_jobs.get_job_and_dependencies.return_value
    assert bhd_tracker_jobs.get_job_and_dependencies.call_args_list == [
        call(bhd_tracker_jobs.description_job, bhd_tracker_jobs.screenshots_job)
    ]

def test_isolated_jobs__only_title(bhd_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(bhd_tracker_jobs)
    mocker.patch.object(type(bhd_tracker_jobs), 'options', PropertyMock(return_value={'only_title': True}))
    mocker.patch.object(bhd_tracker_jobs, 'get_job_and_dependencies')
    assert bhd_tracker_jobs.isolated_jobs is bhd_tracker_jobs.get_job_and_dependencies.return_value
    assert bhd_tracker_jobs.get_job_and_dependencies.call_args_list == [
        call(bhd_tracker_jobs.release_name_job, bhd_tracker_jobs.imdb_job)
    ]

def test_isolated_jobs__no_isolated_jobs(bhd_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(bhd_tracker_jobs)
    mocker.patch.object(type(bhd_tracker_jobs), 'options', PropertyMock(return_value={}))
    mocker.patch.object(bhd_tracker_jobs, 'get_job_and_dependencies')
    assert bhd_tracker_jobs.isolated_jobs == ()
    assert bhd_tracker_jobs.get_job_and_dependencies.call_args_list == []


def test_tmdb_job(bhd_tracker_jobs, mocker):
    assert bhd_tracker_jobs.tmdb_job.no_id_ok is True


def test_category_job(bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name_job', PropertyMock())
    ChoiceJob_mock = mocker.patch('upsies.jobs.dialog.ChoiceJob')
    mocker.patch.object(bhd_tracker_jobs, 'get_job_name')
    mocker.patch.object(bhd_tracker_jobs, 'make_precondition')
    mocker.patch.object(bhd_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert bhd_tracker_jobs.category_job is ChoiceJob_mock.return_value
    assert ChoiceJob_mock.call_args_list == [call(
        name=bhd_tracker_jobs.get_job_name.return_value,
        label='Category',
        precondition=bhd_tracker_jobs.make_precondition.return_value,
        prejobs=(
            bhd_tracker_jobs.release_name_job,
        ),
        autodetect=bhd_tracker_jobs.autodetect_category,
        choices=(
            ('Movie', '1'),
            ('TV', '2'),
        ),
        common_job_arg='common job argument',
    )]
    assert bhd_tracker_jobs.get_job_name.call_args_list == [call('category')]
    assert bhd_tracker_jobs.make_precondition.call_args_list == [call('category_job')]
    assert bhd_tracker_jobs.common_job_args.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='release_type, exp_return_value',
    argvalues=(
        (utils.release.ReleaseType.movie, 'Movie'),
        (utils.release.ReleaseType.series, 'TV'),
        (utils.release.ReleaseType.episode, 'TV'),
        (None, None),
    ),
    ids=lambda v: str(v),
)
def test_autodetect_category(release_type, exp_return_value, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        type=release_type,
    )))
    return_value = bhd_tracker_jobs.autodetect_category('_')
    assert return_value == exp_return_value


def test_type_job(bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name_job', PropertyMock())
    ChoiceJob_mock = mocker.patch('upsies.jobs.dialog.ChoiceJob')
    mocker.patch.object(bhd_tracker_jobs, 'get_job_name')
    mocker.patch.object(bhd_tracker_jobs, 'make_precondition')
    mocker.patch.object(bhd_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert bhd_tracker_jobs.type_job is ChoiceJob_mock.return_value
    assert ChoiceJob_mock.call_args_list == [call(
        name=bhd_tracker_jobs.get_job_name.return_value,
        label='Type',
        precondition=bhd_tracker_jobs.make_precondition.return_value,
        prejobs=(
            bhd_tracker_jobs.release_name_job,
        ),
        autodetect_and_finish=bhd_tracker_jobs.autodetect_type,
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
        common_job_arg='common job argument',
    )]
    assert bhd_tracker_jobs.get_job_name.call_args_list == [call('type')]
    assert bhd_tracker_jobs.make_precondition.call_args_list == [call('type_job')]
    assert bhd_tracker_jobs.common_job_args.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='resolution, source, exp_return_value',
    argvalues=(
        ('', 'DVD9', 'DVD 9'),
        ('', 'DVD5', 'DVD 5'),
        ('', 'DVD Remux', 'DVD Remux'),
        ('2160p', '', '2160p'),
        ('1080p', '', '1080p'),
        ('1080i', '', '1080i'),
        ('720p', '', '720p'),
        ('576p', '', '576p'),
        ('540p', '', '540p'),
        ('480p', '', '480p'),
        ('123p', '', None),
    ),
    ids=lambda v: str(v),
)
def test_autodetect_type(resolution, source, exp_return_value, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        resolution=resolution,
        source=source,
    )))
    return_value = bhd_tracker_jobs.autodetect_type('_')
    assert return_value == exp_return_value


def test_source_job(bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name_job', PropertyMock())
    ChoiceJob_mock = mocker.patch('upsies.jobs.dialog.ChoiceJob')
    mocker.patch.object(bhd_tracker_jobs, 'get_job_name')
    mocker.patch.object(bhd_tracker_jobs, 'make_precondition')
    mocker.patch.object(bhd_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert bhd_tracker_jobs.source_job is ChoiceJob_mock.return_value
    assert ChoiceJob_mock.call_args_list == [call(
        name=bhd_tracker_jobs.get_job_name.return_value,
        label='Source',
        precondition=bhd_tracker_jobs.make_precondition.return_value,
        prejobs=(
            bhd_tracker_jobs.release_name_job,
        ),
        autodetect_and_finish=bhd_tracker_jobs.autodetect_source,
        choices=(
            ('Blu-ray', 'Blu-ray'),
            ('HD-DVD', 'HD-DVD'),
            ('WEB', 'WEB'),
            ('HDTV', 'HDTV'),
            ('DVD', 'DVD'),
        ),
        common_job_arg='common job argument',
    )]
    assert bhd_tracker_jobs.get_job_name.call_args_list == [call('source')]
    assert bhd_tracker_jobs.make_precondition.call_args_list == [call('source_job')]
    assert bhd_tracker_jobs.common_job_args.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='source, exp_return_value',
    argvalues=(
        ('BluRay', 'Blu-ray'),
        ('BluRay Remux', 'Blu-ray'),
        ('WEB-DL', 'WEB'),
        ('WEBRip', 'WEB'),
        ('WEB', 'WEB'),
        ('DVD9', 'DVD'),
        ('DVD5', 'DVD'),
        ('DVD Remux', 'DVD'),
        ('Foo', None),
    ),
    ids=lambda v: str(v),
)
def test_autodetect_source(source, exp_return_value, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        source=source,
    )))
    return_value = bhd_tracker_jobs.autodetect_source('_')
    assert return_value == exp_return_value


def test_description_job(bhd_tracker_jobs, mocker):
    mocker.patch.object(bhd_tracker_jobs, 'get_job_name')
    mocker.patch.object(bhd_tracker_jobs, 'make_precondition')
    mocker.patch.object(bhd_tracker_jobs, 'generate_description', Mock())
    mocker.patch.object(type(bhd_tracker_jobs), 'upload_screenshots_job', PropertyMock())
    mocker.patch.object(type(bhd_tracker_jobs), 'mediainfo_job', PropertyMock())
    mocker.patch.object(bhd_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})
    TextFieldJob_mock = mocker.patch('upsies.jobs.dialog.TextFieldJob')

    assert bhd_tracker_jobs.description_job is TextFieldJob_mock.return_value
    assert TextFieldJob_mock.call_args_list == [call(
        name=bhd_tracker_jobs.get_job_name.return_value,
        label='Description',
        precondition=bhd_tracker_jobs.make_precondition.return_value,
        prejobs=(
            bhd_tracker_jobs.upload_screenshots_job,
            bhd_tracker_jobs.mediainfo_job,
        ),
        text=bhd_tracker_jobs.generate_description,
        hidden=True,
        finish_on_success=True,
        read_only=True,
        common_job_arg='common job argument',
    )]
    assert bhd_tracker_jobs.get_job_name.call_args_list == [call('description')]
    assert bhd_tracker_jobs.make_precondition.call_args_list == [call('description_job')]
    assert bhd_tracker_jobs.common_job_args.call_args_list == [call(ignore_cache=True)]


def test_image_host_config(bhd_tracker_jobs, mocker):
    assert bhd_tracker_jobs.image_host_config == {
        'common': {'thumb_width': 350},
    }


@pytest.mark.parametrize(
    argnames='screenshot_tags, mediainfo_tags, exp_bbcode',
    argvalues=(
        (
            '<screenshot tags>',
            '',
            (
                '[center]\n<screenshot tags>\n[/center]\n\n'
                f'[align=right][size=1]Shared with [url={__homepage__}]{__project_name__}[/url][/size][/align]'
            ),
        ),
        (
            '<screenshot tags>',
            '<mediainfo tags>',
            (
                '[center]\n<screenshot tags>\n[/center]\n'
                '[center][h3]Mediainfo[/h3][/center]\n'
                '<mediainfo tags>\n\n'
                f'[align=right][size=1]Shared with [url={__homepage__}]{__project_name__}[/url][/size][/align]'
            ),
        ),
    ),
)
def test_generate_description(screenshot_tags, mediainfo_tags, exp_bbcode, bhd_tracker_jobs, mocker):
    mocker.patch.object(bhd_tracker_jobs, '_generate_description_screenshots', return_value=screenshot_tags)
    mocker.patch.object(bhd_tracker_jobs, '_generate_description_mediainfos', return_value=mediainfo_tags)
    bbcode = bhd_tracker_jobs.generate_description()
    assert bbcode == exp_bbcode


def test__generate_description_screenshots(bhd_tracker_jobs, mocker):
    mocker.patch.object(bhd_tracker_jobs, 'make_screenshots_grid')
    mocker.patch.object(bhd_tracker_jobs, 'upload_screenshots_job', return_value=Mock(
        is_finished=True,
    ))

    return_value = bhd_tracker_jobs._generate_description_screenshots()
    assert return_value == bhd_tracker_jobs.make_screenshots_grid.return_value
    assert bhd_tracker_jobs.make_screenshots_grid.call_args_list == [
        call(
            screenshots=bhd_tracker_jobs.upload_screenshots_job.uploaded_images,
            columns=2,
            horizontal_spacer='   ',
            vertical_spacer='\n\n',
        ),
    ]


@pytest.mark.parametrize(
    argnames='content_path, description_mediainfos, exp_bbcode',
    argvalues=(
        (
            '/path/to/content',
            {},
            '',
        ),
        (
            '/path/to/foo.mkv',
            {
                '/path/to/foo.mkv': '<mediainfo for foo.mkv>',
            },
            '[hide=foo.mkv][code]<mediainfo for foo.mkv>[/code][/hide]',
        ),
        (
            '/path/to/content',
            {
                '/path/to/content/foo.mkv': '<mediainfo for foo.mkv>',
            },
            '[hide=content/foo.mkv][code]<mediainfo for foo.mkv>[/code][/hide]',
        ),
        (
            '/path/to/content',
            {
                '/path/to/content/foo.s01e01.mkv': '<mediainfo for foo.s01e01.mkv>',
                '/path/to/content/foo.s01e02.mkv': '<mediainfo for foo.s01e02.mkv>',
                '/path/to/content/foo.s01e03.mkv': '<mediainfo for foo.s01e03.mkv>',
            },
            (
                '[hide=content/foo.s01e01.mkv][code]<mediainfo for foo.s01e01.mkv>[/code][/hide]\n'
                '[hide=content/foo.s01e02.mkv][code]<mediainfo for foo.s01e02.mkv>[/code][/hide]\n'
                '[hide=content/foo.s01e03.mkv][code]<mediainfo for foo.s01e03.mkv>[/code][/hide]'
            ),
        ),
    ),
    ids=lambda v: repr(v),
)
def test__generate_description_mediainfos(content_path, description_mediainfos, exp_bbcode, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), '_description_mediainfos', PropertyMock(
        return_value=description_mediainfos,
    ))
    mocker.patch.object(type(bhd_tracker_jobs), 'content_path', PropertyMock(
        return_value=content_path,
    ))
    bbcode = bhd_tracker_jobs._generate_description_mediainfos()
    assert bbcode == exp_bbcode


@pytest.mark.parametrize(
    argnames='mediainfos_by_file, exp_description_mediainfos',
    argvalues=(
        pytest.param(
            {
                'path/to/foo.mkv': '<single mediainfo does not go in description>',
            },
            {},
            id='Single mediainfo',
        ),
        pytest.param(
            {
                'path/to/foo/foo.s01e01.mkv': '<mediainfo for foo.s01e01.mkv>',
                'path/to/foo/foo.s01e02.mkv': '<mediainfo for foo.s01e02.mkv>',
                'path/to/foo/foo.s01e03.mkv': '',  # mediainfo may be empty
                'path/to/foo/foo.s01e04.mkv': '<mediainfo for foo.s01e04.mkv>',
            },
            {
                'path/to/foo/foo.s01e01.mkv': '<mediainfo for foo.s01e01.mkv>',
                'path/to/foo/foo.s01e02.mkv': '<mediainfo for foo.s01e02.mkv>',
                'path/to/foo/foo.s01e04.mkv': '<mediainfo for foo.s01e04.mkv>',
            },
            id='Multiple files (season)',
        ),
        pytest.param(
            {
                'path/to/foo/VIDEO_TS/VTS_01_0.IFO': '<mediainfo for VTS_01_0.IFO>',
                'path/to/foo/VIDEO_TS/VTS_01_1.VOB': '<mediainfo for VTS_01_1.VOB>',
            },
            {
                'path/to/foo/VIDEO_TS/VTS_01_0.IFO': '<mediainfo for VTS_01_0.IFO>',
                'path/to/foo/VIDEO_TS/VTS_01_1.VOB': '<mediainfo for VTS_01_1.VOB>',
            },
            id='Multiple mediainfos (DVD)',
        ),
    ),
)
def test__description_mediainfos(mediainfos_by_file, exp_description_mediainfos, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'mediainfo_job', PropertyMock(return_value=Mock(
        is_finished=True,
        mediainfos_by_file=mediainfos_by_file,
    )))
    description_mediainfos = bhd_tracker_jobs._description_mediainfos
    assert description_mediainfos == exp_description_mediainfos


def test_mediainfo_from_all_videos(bhd_tracker_jobs, mocker):
    assert bhd_tracker_jobs.mediainfo_from_all_videos is False


def test_screenshots_from_all_videos(bhd_tracker_jobs, mocker):
    assert bhd_tracker_jobs.screenshots_from_all_videos is False


def test_tags_job(bhd_tracker_jobs, mocker):
    mocker.patch.object(bhd_tracker_jobs, 'get_job_name')
    mocker.patch.object(bhd_tracker_jobs, 'make_precondition')
    mocker.patch.object(bhd_tracker_jobs, 'generate_tags', Mock())
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name_job', PropertyMock())
    mocker.patch.object(type(bhd_tracker_jobs), 'scene_check_job', PropertyMock())
    mocker.patch.object(bhd_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})
    TextFieldJob_mock = mocker.patch('upsies.jobs.dialog.TextFieldJob')

    assert bhd_tracker_jobs.tags_job is TextFieldJob_mock.return_value
    assert TextFieldJob_mock.call_args_list == [call(
        name=bhd_tracker_jobs.get_job_name.return_value,
        label='Tags',
        precondition=bhd_tracker_jobs.make_precondition.return_value,
        prejobs=(
            bhd_tracker_jobs.release_name_job,
            bhd_tracker_jobs.scene_check_job,
        ),
        text=bhd_tracker_jobs.generate_tags,
        finish_on_success=True,
        read_only=True,
        common_job_arg='common job argument',
    )]
    assert bhd_tracker_jobs.get_job_name.call_args_list == [call('tags')]
    assert bhd_tracker_jobs.make_precondition.call_args_list == [call('tags_job')]
    assert bhd_tracker_jobs.common_job_args.call_args_list == [call()]


class MockReleaseName(SimpleNamespace):
    def __init__(self, **kwargs):
        self.source = []
        self.has_commentary = False
        self.has_dual_audio = False
        self.edition = []
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockOptions(dict):
    def __init__(self, **kwargs):
        self['personal_rip'] = False
        for k, v in kwargs.items():
            self[k] = v

@pytest.mark.parametrize('is_scene_release', (False, True), ids=('is scene', 'not scene'))
@pytest.mark.parametrize('hybrid, hybrid_position', ((None, None), ('Hybrid', 0), ('Hybrid', -1)), ids=lambda v: str(v))
@pytest.mark.parametrize(
    argnames='release_name, options, exp_tags',
    argvalues=(
        (MockReleaseName(source=['WEBRip']), MockOptions(), ('WEBRip',)),
        (MockReleaseName(source=['WEB-DL']), MockOptions(), ['WEBDL']),
        (MockReleaseName(has_commentary=True), MockOptions(), ['Commentary']),
        (MockReleaseName(has_dual_audio=True), MockOptions(), ['DualAudio']),
        (MockReleaseName(edition='Open Matte'), MockOptions(), ['OpenMatte']),
        (MockReleaseName(edition='2in1'), MockOptions(), ['2in1']),
        (MockReleaseName(edition='4k Remastered'), MockOptions(), ['4kRemaster']),
        (MockReleaseName(), MockOptions(personal_rip=True), ['Personal']),
        (MockReleaseName(), MockOptions(), []),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_generate_tags(release_name, options, hybrid, hybrid_position, is_scene_release, exp_tags, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name_job', PropertyMock(return_value=Mock(
        is_finished=True,
    )))
    mocker.patch.object(type(bhd_tracker_jobs), 'scene_check_job', PropertyMock(return_value=Mock(
        is_finished=True,
    )))
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name', PropertyMock(return_value=release_name))
    mocker.patch.object(type(bhd_tracker_jobs), 'options', options)

    def get_job_attribute(job, attribute):
        if job is bhd_tracker_jobs.scene_check_job:
            return is_scene_release
        else:
            return DEFAULT

    mocker.patch.object(bhd_tracker_jobs, 'get_job_attribute', side_effect=get_job_attribute, return_value=None)

    exp_tags = list(exp_tags)

    if hybrid:
        bhd_tracker_jobs.release_name.source.insert(hybrid_position, 'Hybrid')
        exp_tags.append('Hybrid')

    if is_scene_release:
        exp_tags.append('Scene')

    tags = sorted((await bhd_tracker_jobs.generate_tags()).split())
    assert tags == sorted(exp_tags)

    assert bhd_tracker_jobs.get_job_attribute.call_args_list == [call(bhd_tracker_jobs.scene_check_job, 'is_scene_release')]


@pytest.mark.parametrize('draft, exp_live', ((True, '0'), (False, '1'),))
@pytest.mark.parametrize('anonymous, exp_anon', ((True, '1'), (False, '0'),))
def test_post_data(anonymous, exp_anon, draft, exp_live, bhd_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(bhd_tracker_jobs)
    mocker.patch.object(bhd_tracker_jobs, 'get_job_output', side_effect=(
        'mock release name',
        'tt00123456',
        'mock description',
        'Some\nMock\nTags',
    ))
    mocker.patch.object(bhd_tracker_jobs, 'get_job_attribute', side_effect=(
        'mock category',
        'mock type',
        'mock source',
    ))
    mocker.patch.object(type(bhd_tracker_jobs), 'options', PropertyMock(return_value={
        'custom_edition': 'mock custom edition',
        'anonymous': anonymous,
        'draft': draft,
    }))
    mocker.patch.object(type(bhd_tracker_jobs), 'post_data_tmdb_id', PropertyMock(return_value='1234'))
    mocker.patch.object(type(bhd_tracker_jobs), 'post_data_edition', PropertyMock(return_value='mock edition'))
    mocker.patch.object(type(bhd_tracker_jobs), 'post_data_nfo', PropertyMock(return_value='mock nfo'))
    mocker.patch.object(type(bhd_tracker_jobs), 'post_data_pack', PropertyMock(return_value='mock pack'))
    mocker.patch.object(type(bhd_tracker_jobs), 'post_data_sd', PropertyMock(return_value='mock sd'))
    mocker.patch.object(type(bhd_tracker_jobs), 'post_data_special', PropertyMock(return_value='mock special'))

    assert bhd_tracker_jobs.post_data == {
        'name': 'mock release name',
        'category_id': 'mock category',
        'type': 'mock type',
        'source': 'mock source',
        'imdb_id': 'tt00123456',
        'tmdb_id': '1234',
        'description': 'mock description',
        'edition': 'mock edition',
        'custom_edition': 'mock custom edition',
        'tags': 'Some,Mock,Tags',
        'nfo': 'mock nfo',
        'pack': 'mock pack',
        'sd': 'mock sd',
        'special': 'mock special',
        'anon': exp_anon,
        'live': exp_live,
    }
    assert bhd_tracker_jobs.get_job_output.call_args_list == [
        call(bhd_tracker_jobs.release_name_job, slice=0),
        call(bhd_tracker_jobs.imdb_job, slice=0),
        call(bhd_tracker_jobs.description_job, slice=0),
        call(bhd_tracker_jobs.tags_job, slice=0),
    ]
    assert bhd_tracker_jobs.get_job_attribute.call_args_list == [
        call(bhd_tracker_jobs.category_job, 'choice'),
        call(bhd_tracker_jobs.type_job, 'choice'),
        call(bhd_tracker_jobs.source_job, 'choice'),
    ]


@pytest.mark.parametrize(
    argnames='tmdb_job_output, exp_tmdb_id, exp_get_job_output_called',
    argvalues=(
        ((), 0, False),
        (('movie/1234'), '1234', True),
    ),
    ids=lambda v: repr(v),
)
def test_post_data_tmdb_id(tmdb_job_output, exp_tmdb_id, exp_get_job_output_called, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'tmdb_job', PropertyMock(return_value=Mock(
        output=tmdb_job_output,
    )))
    mocker.patch.object(type(bhd_tracker_jobs), 'get_job_output', return_value=tmdb_job_output)
    assert bhd_tracker_jobs.post_data_tmdb_id == exp_tmdb_id
    if exp_get_job_output_called:
        assert bhd_tracker_jobs.get_job_output.call_args_list == [
            call(bhd_tracker_jobs.tmdb_job, slice=0),
        ]
    else:
        assert bhd_tracker_jobs.get_job_output.call_args_list == []


@pytest.mark.parametrize(
    argnames='edition, exp_edition',
    argvalues=(
        ("Collector's Edition", 'Collector'),
        ("Director's Cut", 'Director'),
        ('Extended Cut', 'Extended'),
        ('Limited', 'Limited'),
        ('Special Edition', 'Special'),
        ('Theatrical Cut', 'Theatrical'),
        ('Uncut', 'Uncut'),
        ('Uncensored', 'Uncut'),
        ('Unrated', 'Unrated'),
        ('Super Duper Custom Cut', None),
        ('', None),
    ),
)
def test_post_data_edition(edition, exp_edition, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        edition=edition,
    )))
    assert bhd_tracker_jobs.post_data_edition == exp_edition


@pytest.mark.parametrize(
    argnames='approved_type, exp_pack',
    argvalues=(
        (utils.types.ReleaseType.movie, '0'),
        (utils.types.ReleaseType.season, '1'),
        (utils.types.ReleaseType.episode, '0'),
    ),
)
def test_post_data_pack(approved_type, exp_pack, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        type=approved_type,
    )))
    assert bhd_tracker_jobs.post_data_pack == exp_pack


@pytest.mark.parametrize(
    argnames='resolution, exp_sd',
    argvalues=(
        ('2160p', '0'),
        ('1080p', '0'),
        ('1080i', '0'),
        ('720p', '0'),
        ('576p', '1'),
        ('540p', '1'),
        ('480p', '1'),
        ('asdf', '0'),
        ('', '0'),
    ),
)
def test_post_data_sd(resolution, exp_sd, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        resolution=resolution,
    )))
    assert bhd_tracker_jobs.post_data_sd == exp_sd


@pytest.mark.parametrize(
    argnames='read_nfo_result, exp_return_value, exp_error_calls',
    argvalues=(
        ('the nfo text', 'the nfo text', []),
        (errors.ContentError('nope'), None, [call(errors.ContentError('nope'))]),
    ),
    ids=lambda v: repr(v),
)
def test_post_data_nfo(read_nfo_result, exp_return_value, exp_error_calls, bhd_tracker_jobs, mocker):
    if isinstance(read_nfo_result, Exception):
        mocker.patch('upsies.utils.string.read_nfo', side_effect=read_nfo_result)
    else:
        mocker.patch('upsies.utils.string.read_nfo', return_value=read_nfo_result)
    mocker.patch.object(bhd_tracker_jobs, 'error')
    return_value = bhd_tracker_jobs.post_data_nfo
    assert return_value == exp_return_value
    assert bhd_tracker_jobs.error.call_args_list == exp_error_calls


@pytest.mark.parametrize(
    argnames='approved_type, options, exp_special',
    argvalues=(
        (utils.types.ReleaseType.movie, {'special': False}, '0'),
        (utils.types.ReleaseType.season, {'special': False}, '0'),
        (utils.types.ReleaseType.episode, {'special': False}, '0'),
        (utils.types.ReleaseType.movie, {'special': True}, '0'),
        (utils.types.ReleaseType.season, {'special': True}, '0'),
        (utils.types.ReleaseType.episode, {'special': True}, '1'),
    ),
)
def test_post_data_special(approved_type, options, exp_special, bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        type=approved_type,
    )))
    mocker.patch.object(type(bhd_tracker_jobs), 'options', PropertyMock(return_value=options))
    assert bhd_tracker_jobs.post_data_special == exp_special


def test_torrent_filepath(bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'create_torrent_job', PropertyMock(return_value=Mock(
        output=('path/to/file.torrent',),
    )))
    assert bhd_tracker_jobs.torrent_filepath == 'path/to/file.torrent'


def test_mediainfo_filehandle(bhd_tracker_jobs, mocker):
    mocker.patch.object(type(bhd_tracker_jobs), 'mediainfo_job', PropertyMock(return_value=Mock(
        output=('mock mediainfo',),
    )))
    assert bhd_tracker_jobs.mediainfo_filehandle.read() == b'mock mediainfo'
