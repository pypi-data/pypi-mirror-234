import re
from unittest.mock import AsyncMock, MagicMock, Mock, PropertyMock, call

import pytest

from upsies import __homepage__, __project_name__, errors, utils
from upsies.trackers import mtv


@pytest.fixture
def tracker():
    tracker = Mock()
    tracker.name = 'mtv'
    tracker.options = {
        'exclude': [],
    }
    return tracker


@pytest.fixture
def imghost():
    class MockImageHost(utils.imghosts.base.ImageHostBase):
        name = 'mock image host'
        default_config = {}
        _upload_image = AsyncMock()

    return MockImageHost()


@pytest.fixture
def mtv_tracker_jobs(imghost, tracker, tmp_path, mocker):
    content_path = tmp_path / 'Foo 2000 1080p BluRay x264-ASDF'

    mtv_tracker_jobs = mtv.MtvTrackerJobs(
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

    return mtv_tracker_jobs


@pytest.fixture
def mock_job_attributes(mocker):
    def mock_job_attributes(mtv_tracker_jobs):
        job_attrs = (
            # Background jobs
            'create_torrent_job',
            'mediainfo_job',
            'screenshots_job',
            'upload_screenshots_job',

            # Interactive jobs
            'category_job',
            'imdb_job',
            'scene_check_job',
            'title_job',
            'description_job',
        )
        for job_attr in job_attrs:
            mocker.patch.object(type(mtv_tracker_jobs), job_attr, PropertyMock(return_value=Mock(attr=job_attr)))

    return mock_job_attributes


def test_MtvTrackerJobs_jobs_before_upload(mock_job_attributes, mtv_tracker_jobs):
    mock_job_attributes(mtv_tracker_jobs)

    print(mtv_tracker_jobs.jobs_before_upload)
    assert tuple(job.attr for job in mtv_tracker_jobs.jobs_before_upload) == (
        # Background jobs
        'create_torrent_job',
        'mediainfo_job',
        'screenshots_job',
        'upload_screenshots_job',

        # Interactive jobs
        'category_job',
        'imdb_job',
        'scene_check_job',
        'title_job',
        'description_job',
    )


def test_isolated_jobs__only_description(mtv_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(mtv_tracker_jobs)
    mocker.patch.object(type(mtv_tracker_jobs), 'options', PropertyMock(return_value={'only_description': True}))
    mocker.patch.object(mtv_tracker_jobs, 'get_job_and_dependencies')
    assert mtv_tracker_jobs.isolated_jobs is mtv_tracker_jobs.get_job_and_dependencies.return_value
    assert mtv_tracker_jobs.get_job_and_dependencies.call_args_list == [
        call(mtv_tracker_jobs.description_job, mtv_tracker_jobs.screenshots_job)
    ]

def test_isolated_jobs__only_title(mtv_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(mtv_tracker_jobs)
    mocker.patch.object(type(mtv_tracker_jobs), 'options', PropertyMock(return_value={'only_title': True}))
    mocker.patch.object(mtv_tracker_jobs, 'get_job_and_dependencies')
    assert mtv_tracker_jobs.isolated_jobs is mtv_tracker_jobs.get_job_and_dependencies.return_value
    assert mtv_tracker_jobs.get_job_and_dependencies.call_args_list == [
        call(mtv_tracker_jobs.title_job)
    ]

def test_isolated_jobs__no_isolated_jobs(mtv_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(mtv_tracker_jobs)
    mocker.patch.object(type(mtv_tracker_jobs), 'options', PropertyMock(return_value={}))
    mocker.patch.object(mtv_tracker_jobs, 'get_job_and_dependencies')
    assert mtv_tracker_jobs.isolated_jobs == ()
    assert mtv_tracker_jobs.get_job_and_dependencies.call_args_list == []


def test_MtvTrackerJobs_category_job(mtv_tracker_jobs, mocker):
    ChoiceJob_mock = mocker.patch('upsies.jobs.dialog.ChoiceJob')
    mocker.patch.object(mtv_tracker_jobs, 'get_job_name')
    mocker.patch.object(mtv_tracker_jobs, 'make_precondition')
    mocker.patch.object(mtv_tracker_jobs, 'autodetect_category')
    mocker.patch.object(type(mtv_tracker_jobs), '_categories', PropertyMock(return_value=[
        {'label': 'movie', 'value': '1'},
        {'label': 'series', 'value': '2'},
        {'label': 'vegetable', 'value': '3'},
    ]))
    mocker.patch.object(mtv_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert mtv_tracker_jobs.category_job is ChoiceJob_mock.return_value
    assert ChoiceJob_mock.call_args_list == [call(
        name=mtv_tracker_jobs.get_job_name.return_value,
        label='Category',
        precondition=mtv_tracker_jobs.make_precondition.return_value,
        autodetect=mtv_tracker_jobs.autodetect_category,
        choices=[
            ('movie', '1'),
            ('series', '2'),
            ('vegetable', '3'),
        ],
        callbacks={
            'finished': mtv_tracker_jobs.update_imdb_query,
        },
        common_job_arg='common job argument',
    )]

    assert mtv_tracker_jobs.get_job_name.call_args_list == [call('category')]
    assert mtv_tracker_jobs.make_precondition.call_args_list == [call('category_job')]
    assert mtv_tracker_jobs.common_job_args.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='old_type, new_type, exp_type',
    argvalues=(
        (utils.release.ReleaseType.movie, utils.release.ReleaseType.season, utils.release.ReleaseType.season),
        (utils.release.ReleaseType.movie, utils.release.ReleaseType.episode, utils.release.ReleaseType.episode),
        (utils.release.ReleaseType.movie, utils.release.ReleaseType.unknown, utils.release.ReleaseType.unknown),
        (utils.release.ReleaseType.season, utils.release.ReleaseType.movie, utils.release.ReleaseType.movie),
        (utils.release.ReleaseType.season, utils.release.ReleaseType.episode, utils.release.ReleaseType.episode),
        (utils.release.ReleaseType.season, utils.release.ReleaseType.unknown, utils.release.ReleaseType.unknown),
        (utils.release.ReleaseType.episode, utils.release.ReleaseType.movie, utils.release.ReleaseType.movie),
        (utils.release.ReleaseType.episode, utils.release.ReleaseType.season, utils.release.ReleaseType.season),
        (utils.release.ReleaseType.episode, utils.release.ReleaseType.unknown, utils.release.ReleaseType.unknown),
        (utils.release.ReleaseType.unknown, utils.release.ReleaseType.movie, utils.release.ReleaseType.movie),
        (utils.release.ReleaseType.unknown, utils.release.ReleaseType.season, utils.release.ReleaseType.season),
        (utils.release.ReleaseType.unknown, utils.release.ReleaseType.episode, utils.release.ReleaseType.episode),
        (None, utils.release.ReleaseType.movie, utils.release.ReleaseType.movie),
        (utils.release.ReleaseType.movie, None, utils.release.ReleaseType.movie),
        (utils.release.ReleaseType.season, None, utils.release.ReleaseType.season),
        (utils.release.ReleaseType.episode, None, utils.release.ReleaseType.episode),
    ),
)
def test_update_imdb_query(old_type, new_type, exp_type, mtv_tracker_jobs, mocker):
    mocker.patch.object(type(mtv_tracker_jobs), 'imdb_job', PropertyMock(
        return_value=Mock(
            query=Mock(type=old_type),
        ),
    ))
    mocker.patch.object(type(mtv_tracker_jobs), 'chosen_release_type', PropertyMock(
        return_value=new_type,
    ))
    assert mtv_tracker_jobs.imdb_job.query.type == old_type
    mtv_tracker_jobs.update_imdb_query('ignored category_job')
    assert mtv_tracker_jobs.imdb_job.query.type == exp_type


@pytest.mark.parametrize(
    argnames='release_type, exp_typ',
    argvalues=(
        (utils.release.ReleaseType.movie, 'Movie'),
        (utils.release.ReleaseType.season, 'Season'),
        (utils.release.ReleaseType.episode, 'Episode'),
        ('wat', RuntimeError('Unsupported type: wat')),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize(
    argnames='resolution_int, exp_resolution',
    argvalues=(
        (719, 'SD'),
        (720, 'HD'),
        (721, 'HD'),
    ),
    ids=lambda v: repr(v),
)
def test_MtvTrackerJobs_autodetect_category(resolution_int, exp_resolution, release_type, exp_typ, mtv_tracker_jobs, mocker):
    mocker.patch('upsies.utils.video.resolution_int', Mock(return_value=resolution_int))
    mocker.patch.object(mtv_tracker_jobs, 'release_name', Mock(type=release_type))

    if isinstance(exp_typ, Exception):
        exp_exception = exp_typ
    else:
        exp_exception = None

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            mtv_tracker_jobs.autodetect_category('mock job')
    else:
        category = mtv_tracker_jobs.autodetect_category('mock job')
        assert category == f'{exp_resolution} {exp_typ}'


@pytest.mark.parametrize(
    argnames='choice',
    argvalues=[c['value'] for c in mtv.MtvTrackerJobs._categories] + [None],
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize(
    argnames='category_job_is_finished',
    argvalues=(True, False),
    ids=lambda v: repr(v),
)
def test_MtvTrackerJobs_chosen_release_type(category_job_is_finished, choice, mtv_tracker_jobs, mocker):
    mocker.patch.object(type(mtv_tracker_jobs), 'category_job', PropertyMock(return_value=Mock(
        is_finished=category_job_is_finished,
        choice=choice,
    )))

    if category_job_is_finished and choice is not None:
        exp_return_value = mtv.MtvTrackerJobs._category_value_type_map[choice]
    else:
        exp_return_value = None

    assert mtv_tracker_jobs.chosen_release_type is exp_return_value


def test_MtvTrackerJobs_release_name_separator(mtv_tracker_jobs, mocker):
    assert mtv_tracker_jobs.release_name_separator == '.'


def test_MtvTrackerJobs_release_name_translation(mtv_tracker_jobs, mocker):
    assert mtv_tracker_jobs.release_name_translation == {
        'edition': {
            re.compile(r"^Director's Cut$"): r'DC',
        },
        'group': {
            re.compile(r'^NOGROUP$'): r'NOGRP',
        },
    }


def test_MtvTrackerJobs_title_job(mtv_tracker_jobs, mocker):
    TextFieldJob_mock = mocker.patch('upsies.jobs.dialog.TextFieldJob')
    mocker.patch.object(mtv_tracker_jobs, 'get_job_name')
    mocker.patch.object(type(mtv_tracker_jobs), 'category_job', PropertyMock())
    mocker.patch.object(type(mtv_tracker_jobs), 'scene_check_job', PropertyMock())
    mocker.patch.object(type(mtv_tracker_jobs), 'imdb_job', PropertyMock())
    mocker.patch.object(mtv_tracker_jobs, 'make_precondition')
    mocker.patch.object(mtv_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert mtv_tracker_jobs.title_job is TextFieldJob_mock.return_value
    assert TextFieldJob_mock.call_args_list == [call(
        name=mtv_tracker_jobs.get_job_name.return_value,
        label='Title',
        prejobs=(
            mtv_tracker_jobs.category_job,
            mtv_tracker_jobs.scene_check_job,
            mtv_tracker_jobs.imdb_job,
        ),
        text=mtv_tracker_jobs.generate_title,
        validator=mtv_tracker_jobs.validate_title,
        precondition=mtv_tracker_jobs.make_precondition.return_value,
        common_job_arg='common job argument',
    )]
    assert mtv_tracker_jobs.get_job_name.call_args_list == [call('title')]
    assert mtv_tracker_jobs.make_precondition.call_args_list == [call('title_job')]
    assert mtv_tracker_jobs.common_job_args.call_args_list == [call()]


@pytest.fixture
def mtv_tracker_jobs_for_generate_title(mtv_tracker_jobs, mocker):
    mocks = Mock()
    mocker.patch.object(type(mtv_tracker_jobs), 'chosen_release_type', PropertyMock())
    mocker.patch.object(type(mtv_tracker_jobs), 'scene_check_job', PropertyMock(return_value=Mock(
        is_finished=True,
        is_scene_release='YOU FORGOT TO SET THIS',
    )))
    mocks.attach_mock(mtv_tracker_jobs.scene_check_job.wait, 'scene_check_job_wait')
    mocks.attach_mock(
        mocker.patch('upsies.utils.predbs.MultiPredbApi.search', AsyncMock()),
        'scene_search',
    )
    mocker.patch.object(type(mtv_tracker_jobs), 'imdb_job', PropertyMock(return_value=Mock(
        is_finished=True,
    )))
    mocker.patch.object(type(mtv_tracker_jobs), 'imdb_id', PropertyMock(return_value='mock imdb_id'))
    mocks.attach_mock(mtv_tracker_jobs.imdb_job.wait, 'imdb_job_wait')
    mocker.patch.object(mtv_tracker_jobs, 'release_name', MagicMock(
        fetch_info=AsyncMock(),
    ))
    mocks.attach_mock(mtv_tracker_jobs.release_name.fetch_info, 'fetch_info')
    return mtv_tracker_jobs, mocks

@pytest.mark.parametrize('job_attribute', ('scene_check_job', 'imdb_job'))
@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__unfinished_depency_job(job_attribute,
                                                                     mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    getattr(mtv_tracker_jobs, job_attribute).is_finished = False

    with pytest.raises(AssertionError):
        await mtv_tracker_jobs.generate_title()

    assert mocks.mock_calls == []

@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__scene__movie(mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    mtv_tracker_jobs.scene_check_job.is_scene_release = True
    type(mtv_tracker_jobs).chosen_release_type = PropertyMock(return_value=utils.release.ReleaseType.movie)
    mocks.scene_search.return_value = ['Scene.2000-ASDF', 'Foo.2000-ASDF']
    mtv_tracker_jobs.release_name.__str__.return_value = 'Generated.Title.2012-ARF'

    return_value = await mtv_tracker_jobs.generate_title()
    assert return_value == 'Scene.2000-ASDF'

    assert mocks.mock_calls == [
        call.scene_search(mtv_tracker_jobs.content_path),
    ]

@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__scene__episode(mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    mtv_tracker_jobs.scene_check_job.is_scene_release = True
    type(mtv_tracker_jobs).chosen_release_type = PropertyMock(return_value=utils.release.ReleaseType.episode)
    mocks.scene_search.return_value = ['Scene.S03E06.2000-ASDF', 'Foo.S04E08.2000-ASDF']
    mtv_tracker_jobs.release_name.__str__.return_value = 'Generated.Title.E02E04-ARF'

    return_value = await mtv_tracker_jobs.generate_title()
    assert return_value == 'Scene.S03E06.2000-ASDF'

    assert mocks.mock_calls == [
        call.scene_search(mtv_tracker_jobs.content_path),
    ]

@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__scene__season(mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    mtv_tracker_jobs.scene_check_job.is_scene_release = True
    type(mtv_tracker_jobs).chosen_release_type = PropertyMock(return_value=utils.release.ReleaseType.season)
    mocks.scene_search.return_value = ['Scene.S03E06.2000-ASDF', 'Foo.S04E08.2000-ASDF']
    mtv_tracker_jobs.release_name.__str__.return_value = 'Generated.Title.E02E04-ARF'

    return_value = await mtv_tracker_jobs.generate_title()
    assert return_value == 'Generated.Title.E02E04-ARF'

    assert mocks.mock_calls == [
        call.fetch_info(
            webdb=mtv_tracker_jobs.imdb,
            webdb_id=mtv_tracker_jobs.imdb_id,
        ),
    ]

@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__nonscene__movie(mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    mtv_tracker_jobs.scene_check_job.is_scene_release = False
    type(mtv_tracker_jobs).chosen_release_type = PropertyMock(return_value=utils.release.ReleaseType.movie)
    mocks.scene_search.return_value = ['Scene.2000-ASDF', 'Foo.2000-ASDF']
    mtv_tracker_jobs.release_name.__str__.return_value = 'Generated.Title.2012-ARF'

    return_value = await mtv_tracker_jobs.generate_title()
    assert return_value == 'Generated.Title.2012-ARF'

    assert mocks.mock_calls == [
        call.fetch_info(
            webdb=mtv_tracker_jobs.imdb,
            webdb_id=mtv_tracker_jobs.imdb_id,
        ),
    ]

@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__nonscene__episode(mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    mtv_tracker_jobs.scene_check_job.is_scene_release = False
    type(mtv_tracker_jobs).chosen_release_type = PropertyMock(return_value=utils.release.ReleaseType.episode)
    mocks.scene_search.return_value = ['Scene.S03E06.2000-ASDF', 'Foo.S04E08.2000-ASDF']
    mtv_tracker_jobs.release_name.__str__.return_value = 'Generated.Title.2012-ARF'

    return_value = await mtv_tracker_jobs.generate_title()
    assert return_value == 'Generated.Title.2012-ARF'

    assert mocks.mock_calls == [
        call.fetch_info(
            webdb=mtv_tracker_jobs.imdb,
            webdb_id=mtv_tracker_jobs.imdb_id,
        ),
    ]

@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__nonscene__season(mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    mtv_tracker_jobs.scene_check_job.is_scene_release = False
    type(mtv_tracker_jobs).chosen_release_type = PropertyMock(return_value=utils.release.ReleaseType.season)
    mocks.scene_search.return_value = ['Scene.S03.2000-ASDF', 'Foo.S04.2000-ASDF']
    mtv_tracker_jobs.release_name.__str__.return_value = 'Generated.Title.S02-ARF'

    return_value = await mtv_tracker_jobs.generate_title()
    assert return_value == 'Generated.Title.S02-ARF'

    assert mocks.mock_calls == [
        call.fetch_info(
            webdb=mtv_tracker_jobs.imdb,
            webdb_id=mtv_tracker_jobs.imdb_id,
        ),
    ]

@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__getting_title_from_predb_fails(mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    mtv_tracker_jobs.scene_check_job.is_scene_release = True
    type(mtv_tracker_jobs).chosen_release_type = PropertyMock(return_value=utils.release.ReleaseType.movie)
    mocks.scene_search.side_effect = errors.RequestError('Your request sucks')
    mtv_tracker_jobs.release_name.__str__.return_value = 'Generated.Title-ARF'

    return_value = await mtv_tracker_jobs.generate_title()
    assert return_value == 'Generated.Title-ARF'

    assert mocks.mock_calls == [
        call.scene_search(mtv_tracker_jobs.content_path),
    ]

@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_title__getting_title_from_webdb_fails(mtv_tracker_jobs_for_generate_title, mocker):
    mtv_tracker_jobs, mocks = mtv_tracker_jobs_for_generate_title
    mtv_tracker_jobs.scene_check_job.is_scene_release = False
    type(mtv_tracker_jobs).chosen_release_type = PropertyMock(return_value='whatever')
    mocks.fetch_info.side_effect = errors.RequestError('Your request sucks')
    mtv_tracker_jobs.release_name.__str__.return_value = 'Generated.Title-ARF'

    return_value = await mtv_tracker_jobs.generate_title()
    assert return_value == 'Generated.Title-ARF'

    assert mocks.mock_calls == [
        call.fetch_info(
            webdb=mtv_tracker_jobs.imdb,
            webdb_id=mtv_tracker_jobs.imdb_id,
        ),
    ]


@pytest.mark.parametrize(
    argnames='title, exp_exception',
    argvalues=(
        ('Valid.Title', None),
        ('', ValueError('Title must not be empty')),
        (' ', ValueError('Title must not be empty')),
        ('    ', ValueError('Title must not be empty')),
        ('Invalid.Title.UNKNOWN_SEASON', ValueError('Replace "UNKNOWN_SEASON" with the correct season')),
        ('Invalid.Title.UNKNOWN_SEASON.720p', ValueError('Replace "UNKNOWN_SEASON" with the correct season')),
        ('Invalid.Title.UNKNOWN_VIDEO_FORMAT', ValueError('Replace "UNKNOWN_VIDEO_FORMAT" with the correct video format')),
        ('Invalid.Title.UNKNOWN_VIDEO_FORMAT.720p', ValueError('Replace "UNKNOWN_VIDEO_FORMAT" with the correct video format')),
    ),
)
def test_MtvTrackerJobs_validate_title(title, exp_exception, mtv_tracker_jobs):
    if isinstance(exp_exception, Exception):
        with pytest.raises(type(exp_exception), match=rf'{re.escape(str(exp_exception))}$'):
            mtv_tracker_jobs.validate_title(title)
    else:
        assert mtv_tracker_jobs.validate_title(title) is None

    def validate_title(self, text):
        if not text.strip():
            raise ValueError('Title must not be empty')

        match = re.search(rf'{utils.release.DELIM}(UNKNOWN_([A-Z_]+)){utils.release.DELIM}', text)
        if match:
            placeholder = match.group(1)
            name = match.group(2)
            raise ValueError(f'Replace "{placeholder}" with the correct {name.lower()}')


def test_MtvTrackerJobs_image_host_config(mtv_tracker_jobs, mocker):
    assert mtv_tracker_jobs.image_host_config == {
        'common': {'thumb_width': 300},
    }


def test_MtvTrackerJobs_description_job(mtv_tracker_jobs, mocker):
    TextFieldJob_mock = mocker.patch('upsies.jobs.dialog.TextFieldJob')
    mocker.patch.object(mtv_tracker_jobs, 'get_job_name')
    mocker.patch.object(type(mtv_tracker_jobs), 'mediainfo_job', PropertyMock())
    mocker.patch.object(type(mtv_tracker_jobs), 'upload_screenshots_job', PropertyMock())
    mocker.patch.object(mtv_tracker_jobs, 'make_precondition')
    mocker.patch.object(mtv_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert mtv_tracker_jobs.description_job is TextFieldJob_mock.return_value
    assert TextFieldJob_mock.call_args_list == [call(
        name=mtv_tracker_jobs.get_job_name.return_value,
        label='Description',
        prejobs=(
            mtv_tracker_jobs.mediainfo_job,
            mtv_tracker_jobs.upload_screenshots_job,
        ),
        text=mtv_tracker_jobs.generate_description,
        precondition=mtv_tracker_jobs.make_precondition.return_value,
        finish_on_success=True,
        read_only=True,
        hidden=True,
        common_job_arg='common job argument',
    )]
    assert mtv_tracker_jobs.get_job_name.call_args_list == [call('description')]
    assert mtv_tracker_jobs.make_precondition.call_args_list == [call('description_job')]
    assert mtv_tracker_jobs.common_job_args.call_args_list == [call(ignore_cache=True)]


class ImageUrl(str):
    def __new__(cls, *args, thumbnail=True, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        self._thumbnail = thumbnail
        return self

    @property
    def thumbnail_url(self):
        if self._thumbnail:
            return f'thumb_{self}'

@pytest.mark.parametrize(
    argnames='mediainfos_and_screenshots, exp_description',
    argvalues=(
        pytest.param(
            {
                'path/to/foo.mkv': {
                    'mediainfo': '<mediainfo for foo.mkv>',
                    'screenshot_urls': [ImageUrl('foo.1.png'), ImageUrl('foo.2.png'), ImageUrl('foo.3.png'), ImageUrl('foo.4.png')],
                },
            },
            (
                '[mediainfo]<mediainfo for foo.mkv>[/mediainfo]\n'
                '[center]'
                '[url=foo.1.png][img]thumb_foo.1.png[/img][/url]    [url=foo.2.png][img]thumb_foo.2.png[/img][/url]'
                '\n\n'
                '[url=foo.3.png][img]thumb_foo.3.png[/img][/url]    [url=foo.4.png][img]thumb_foo.4.png[/img][/url]'
                '[/center]'
                '\n'
                '[align=right][size=1]'
                f'Shared with [url={__homepage__}]{__project_name__}[/url]'
                '[/size][/align]'
            ),
            id='Single mkv',
        ),
        pytest.param(
            {
                'path/to/foo.mkv': {
                    'mediainfo': '',
                    'screenshot_urls': [ImageUrl('foo.1.png'), ImageUrl('foo.2.png'), ImageUrl('foo.3.png'), ImageUrl('foo.4.png')],
                },
            },
            (
                '[center]'
                '[url=foo.1.png][img]thumb_foo.1.png[/img][/url]    [url=foo.2.png][img]thumb_foo.2.png[/img][/url]'
                '\n\n'
                '[url=foo.3.png][img]thumb_foo.3.png[/img][/url]    [url=foo.4.png][img]thumb_foo.4.png[/img][/url]'
                '[/center]'
                '\n'
                '[align=right][size=1]'
                f'Shared with [url={__homepage__}]{__project_name__}[/url]'
                '[/size][/align]'
            ),
            id='Single mkv / Missing mediainfo',
        ),
        pytest.param(
            {
                'path/to/foo.1.mkv': {
                    'mediainfo': '<mediainfo for foo.1.mkv>',
                    'screenshot_urls': [ImageUrl('foo.11.png'), ImageUrl('foo.12.png'), ImageUrl('foo.13.png'), ImageUrl('foo.14.png')],
                },
                'path/to/foo.2.mkv': {
                    'mediainfo': '<mediainfo for foo.2.mkv>',
                    'screenshot_urls': [ImageUrl('foo.21.png'), ImageUrl('foo.22.png'), ImageUrl('foo.23.png'), ImageUrl('foo.24.png')],
                },
                'path/to/foo.3.mkv': {
                    'mediainfo': '<mediainfo for foo.3.mkv>',
                    'screenshot_urls': [ImageUrl('foo.31.png'), ImageUrl('foo.32.png'), ImageUrl('foo.33.png'), ImageUrl('foo.34.png')],
                },
            },
            (
                '[mediainfo]<mediainfo for foo.1.mkv>[/mediainfo]\n'
                '[center]'
                '[url=foo.11.png][img]thumb_foo.11.png[/img][/url]    [url=foo.12.png][img]thumb_foo.12.png[/img][/url]'
                '\n\n'
                '[url=foo.13.png][img]thumb_foo.13.png[/img][/url]    [url=foo.14.png][img]thumb_foo.14.png[/img][/url]'
                '[/center]'
                '\n[hr]\n'
                '[mediainfo]<mediainfo for foo.2.mkv>[/mediainfo]\n'
                '[center]'
                '[url=foo.21.png][img]thumb_foo.21.png[/img][/url]    [url=foo.22.png][img]thumb_foo.22.png[/img][/url]'
                '\n\n'
                '[url=foo.23.png][img]thumb_foo.23.png[/img][/url]    [url=foo.24.png][img]thumb_foo.24.png[/img][/url]'
                '[/center]'
                '\n[hr]\n'
                '[mediainfo]<mediainfo for foo.3.mkv>[/mediainfo]\n'
                '[center]'
                '[url=foo.31.png][img]thumb_foo.31.png[/img][/url]    [url=foo.32.png][img]thumb_foo.32.png[/img][/url]'
                '\n\n'
                '[url=foo.33.png][img]thumb_foo.33.png[/img][/url]    [url=foo.34.png][img]thumb_foo.34.png[/img][/url]'
                '[/center]'
                '\n'
                '[align=right][size=1]'
                f'Shared with [url={__homepage__}]{__project_name__}[/url]'
                '[/size][/align]'
            ),
            id='Multiple mkv',
        ),
        pytest.param(
            {
                'path/to/dvd/VIDEO_TS/VTS_01_0.IFO': {
                    'mediainfo': '<mediainfo for VTS_01_0.IFO>',
                    'screenshot_urls': [],
                },
                'path/to/dvd/VIDEO_TS/VTS_01_1.VOB': {
                    'mediainfo': '<mediainfo for VTS_01_1.VOB>',
                    'screenshot_urls': [ImageUrl('VTS_011.png'), ImageUrl('VTS_012.png'), ImageUrl('VTS_013.png'), ImageUrl('VTS_014.png')],
                },
            },
            (
                '[mediainfo]<mediainfo for VTS_01_0.IFO>[/mediainfo]\n'
                '[mediainfo]<mediainfo for VTS_01_1.VOB>[/mediainfo]\n'
                '[center]'
                '[url=VTS_011.png][img]thumb_VTS_011.png[/img][/url]    [url=VTS_012.png][img]thumb_VTS_012.png[/img][/url]'
                '\n\n'
                '[url=VTS_013.png][img]thumb_VTS_013.png[/img][/url]    [url=VTS_014.png][img]thumb_VTS_014.png[/img][/url]'
                '[/center]'
                '\n'
                '[align=right][size=1]'
                f'Shared with [url={__homepage__}]{__project_name__}[/url]'
                '[/size][/align]'
            ),
            id='Single VIDEO_TS',
        ),
        pytest.param(
            {
                'path/to/dvd/disc1/VIDEO_TS/VTS_01_0.IFO': {
                    'mediainfo': '<mediainfo for disc1/VTS_01_0.IFO>',
                    'screenshot_urls': [],
                },
                'path/to/dvd/disc1/VIDEO_TS/VTS_01_1.VOB': {
                    'mediainfo': '<mediainfo for disc1/VTS_01_1.VOB>',
                    'screenshot_urls': [ImageUrl('1/VTS_011.png'), ImageUrl('1/VTS_012.png'),
                                        ImageUrl('1/VTS_013.png'), ImageUrl('1/VTS_014.png')],
                },
            },
            (
                '[mediainfo]<mediainfo for disc1/VTS_01_0.IFO>[/mediainfo]\n'
                '[mediainfo]<mediainfo for disc1/VTS_01_1.VOB>[/mediainfo]\n'
                '[center]'
                '[url=1/VTS_011.png][img]thumb_1/VTS_011.png[/img][/url]    [url=1/VTS_012.png][img]thumb_1/VTS_012.png[/img][/url]'
                '\n\n'
                '[url=1/VTS_013.png][img]thumb_1/VTS_013.png[/img][/url]    [url=1/VTS_014.png][img]thumb_1/VTS_014.png[/img][/url]'
                '[/center]'
                '\n'
                '[align=right][size=1]'
                f'Shared with [url={__homepage__}]{__project_name__}[/url]'
                '[/size][/align]'
            ),
            id='Multiple VIDEO_TS',
        ),
    ),
)
@pytest.mark.asyncio
async def test_MtvTrackerJobs_generate_description(mediainfos_and_screenshots, exp_description, mtv_tracker_jobs, mocker):
    mocker.patch.object(type(mtv_tracker_jobs), 'mediainfos_and_screenshots', PropertyMock(
        return_value=mediainfos_and_screenshots,
    ))
    description = await mtv_tracker_jobs.generate_description()
    assert description == exp_description


def test_MtvTrackerJobs_mediainfo_from_all_videos(mtv_tracker_jobs):
    assert mtv_tracker_jobs.mediainfo_from_all_videos is False


def test_MtvTrackerJobs_screenshots_from_all_videos(mtv_tracker_jobs):
    assert mtv_tracker_jobs.screenshots_from_all_videos is False


def test_MtvTrackerJobs_post_data_autofill(mtv_tracker_jobs):
    assert mtv_tracker_jobs.post_data_autofill == {
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


@pytest.mark.parametrize('anonymous, exp_anonymous', ((True, '1'), (False, '0')))
@pytest.mark.parametrize('ignore_dupes, exp_ignoredupes', ((True, '1'), (False, None)))
def test_MtvTrackerJobs_post_data_upload(anonymous, exp_anonymous, ignore_dupes, exp_ignoredupes,
                                         mtv_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(mtv_tracker_jobs)
    mocker.patch.object(mtv_tracker_jobs, 'get_job_attribute')
    mocker.patch.object(mtv_tracker_jobs, 'get_job_output')
    mocker.patch.object(type(mtv_tracker_jobs), 'options', PropertyMock(return_value={
        'anonymous': anonymous,
        'ignore_dupes': ignore_dupes,
    }))

    assert mtv_tracker_jobs.post_data_upload == {
        'submit': 'true',
        'category': mtv_tracker_jobs.get_job_attribute.return_value,
        'Resolution': '0',
        'source': '12',
        'origin': '6',
        'title': mtv_tracker_jobs.get_job_output.return_value,
        'genre_tags': '---',
        'autocomplete_toggle': 'on',
        'image': '',
        'desc': mtv_tracker_jobs.get_job_output.return_value,
        'fontfont': '-1',
        'fontsize': '-1',
        'groupDesc': '',
        'anonymous': exp_anonymous,
        'ignoredupes': exp_ignoredupes,
        'imdbID': mtv_tracker_jobs.get_job_output.return_value,
        # 'tmdbID': ...,
        # 'thetvdbID': ...,
        # 'tvmazeID': ...,
    }

    assert mtv_tracker_jobs.get_job_attribute.call_args_list == [call(mtv_tracker_jobs.category_job, 'choice')]
    assert mtv_tracker_jobs.get_job_output.call_args_list == [
        call(mtv_tracker_jobs.title_job, slice=0),
        call(mtv_tracker_jobs.description_job, slice=0),
        call(mtv_tracker_jobs.imdb_job, slice=0),
    ]


def test_MtvTrackerJobs_torrent_filepath(mtv_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(mtv_tracker_jobs)
    mocker.patch.object(mtv_tracker_jobs, 'get_job_output')

    assert mtv_tracker_jobs.torrent_filepath == mtv_tracker_jobs.get_job_output.return_value

    assert mtv_tracker_jobs.get_job_output.call_args_list == [
        call(mtv_tracker_jobs.create_torrent_job, slice=0),
    ]
