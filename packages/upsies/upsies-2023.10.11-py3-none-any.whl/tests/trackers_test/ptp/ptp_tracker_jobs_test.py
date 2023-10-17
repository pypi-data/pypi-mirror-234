from unittest.mock import Mock, PropertyMock, call

import pytest

from upsies import errors, utils
from upsies.trackers import ptp


@pytest.fixture
def tracker():
    tracker = Mock()
    tracker.name = 'ptp'
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
def ptp_tracker_jobs(imghost, tracker, tmp_path, mocker):
    content_path = tmp_path / 'Foo 2000 1080p BluRay x264-ASDF'

    ptp_tracker_jobs = ptp.PtpTrackerJobs(
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

    return ptp_tracker_jobs


@pytest.fixture
def mock_job_attributes(mocker):
    def mock_job_attributes(ptp_tracker_jobs):
        job_attrs = (
            # Common background jobs
            'create_torrent_job',
            'mediainfo_job',
            'screenshots_job',
            'upload_screenshots_job',
            'ptp_group_id_job',
            'description_job',
            'trumpable_job',

            # Common interactive jobs
            'type_job',
            'imdb_job',
            'source_job',
            'scene_check_job',

            # Interactive jobs that only run if movie does not exists on PTP yet
            'title_job',
            'year_job',
            'plot_job',
            'tags_job',
            'cover_art_job',
        )
        for job_attr in job_attrs:
            mocker.patch.object(
                type(ptp_tracker_jobs),
                job_attr,
                PropertyMock(return_value=Mock(attr=job_attr)),
            )

    return mock_job_attributes


def test_jobs_before_upload_items(ptp_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(ptp_tracker_jobs)

    assert tuple(job.attr for job in ptp_tracker_jobs.jobs_before_upload) == (
        # Common background jobs
        'create_torrent_job',
        'mediainfo_job',
        'screenshots_job',
        'upload_screenshots_job',
        'ptp_group_id_job',
        'description_job',
        'trumpable_job',

        # Common interactive jobs
        'type_job',
        'imdb_job',
        'source_job',
        'scene_check_job',

        # Interactive jobs that only run if movie does not exists on PTP yet
        'title_job',
        'year_job',
        'plot_job',
        'tags_job',
        'cover_art_job',
    )


def test_isolated_jobs__only_description(ptp_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(ptp_tracker_jobs)
    mocker.patch.object(type(ptp_tracker_jobs), 'options', PropertyMock(return_value={'only_description': True}))
    mocker.patch.object(ptp_tracker_jobs, 'get_job_and_dependencies')
    assert ptp_tracker_jobs.isolated_jobs is ptp_tracker_jobs.get_job_and_dependencies.return_value
    assert ptp_tracker_jobs.get_job_and_dependencies.call_args_list == [
        call(ptp_tracker_jobs.description_job, ptp_tracker_jobs.screenshots_job)
    ]

def test_isolated_jobs__no_isolated_jobs(ptp_tracker_jobs, mock_job_attributes, mocker):
    mock_job_attributes(ptp_tracker_jobs)
    mocker.patch.object(type(ptp_tracker_jobs), 'options', PropertyMock(return_value={}))
    mocker.patch.object(ptp_tracker_jobs, 'get_job_and_dependencies')
    assert ptp_tracker_jobs.isolated_jobs == ()
    assert ptp_tracker_jobs.get_job_and_dependencies.call_args_list == []


def test_type_job(ptp_tracker_jobs, mocker):
    ChoiceJob_mock = mocker.patch('upsies.jobs.dialog.ChoiceJob')
    mocker.patch.object(ptp_tracker_jobs, 'get_job_name')
    mocker.patch.object(ptp_tracker_jobs, 'make_precondition')
    mocker.patch.object(ptp_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert ptp_tracker_jobs.type_job is ChoiceJob_mock.return_value
    assert ChoiceJob_mock.call_args_list == [call(
        name=ptp_tracker_jobs.get_job_name.return_value,
        label='Type',
        precondition=ptp_tracker_jobs.make_precondition.return_value,
        autodetect=ptp_tracker_jobs.autodetect_type,
        choices=(
            ('Feature Film', 'Feature Film'),
            ('Short Film', 'Short Film'),
            ('Miniseries', 'Miniseries'),
            ('Stand-up Comedy', 'Stand-up Comedy'),
            ('Live Performance', 'Live Performance'),
            ('Movie Collection', 'Movie Collection'),
        ),
        callbacks={
            'finished': ptp_tracker_jobs.update_imdb_query,
        },
        common_job_arg='common job argument',
    )]
    assert ptp_tracker_jobs.get_job_name.call_args_list == [call('type')]
    assert ptp_tracker_jobs.make_precondition.call_args_list == [call('type_job')]
    assert ptp_tracker_jobs.common_job_args.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='release_type, main_video_duration, exp_return_value, exp_duration_calls',
    argvalues=(
        (utils.release.ReleaseType.season, 123, 'Miniseries', False),
        (utils.release.ReleaseType.movie, 45 * 60, 'Short Film', True),
        (utils.release.ReleaseType.movie, (45 * 60) + 1, None, True),
    ),
    ids=lambda v: str(v),
)
def test_autodetect_type(
        release_type, main_video_duration,
        exp_return_value, exp_duration_calls,
        ptp_tracker_jobs, mocker,
):
    mocker.patch.object(type(ptp_tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        type=release_type,
    )))

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.find_videos', return_value=iter(
            ('Foo.S01E01.mkv', 'Foo.S01E02.mkv', 'Foo.S01E03.mkv', 'Foo.sample.mkv'),
        )),
        'find_videos',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.filter_main_videos', return_value=iter(
            ('Foo.S01E01.mkv', 'Foo.S01E02.mkv', 'Foo.S01E03.mkv'),
        )),
        'filter_main_videos',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.duration', return_value=main_video_duration),
        'duration',
    )

    return_value = ptp_tracker_jobs.autodetect_type('job_')
    assert return_value == exp_return_value

    if exp_duration_calls:
        assert mocks.mock_calls == [
            call.find_videos(ptp_tracker_jobs.content_path),
            call.filter_main_videos(('Foo.S01E01.mkv', 'Foo.S01E02.mkv', 'Foo.S01E03.mkv', 'Foo.sample.mkv')),
            call.duration('Foo.S01E01.mkv'),
        ]
    else:
        assert mocks.mock_calls == []


@pytest.mark.parametrize(
    argnames='type_job_output, exp_query_type',
    argvalues=(
        ([], '<original query type>'),
        (['Feature Film'], utils.release.ReleaseType.movie),
        (['Miniseries'], utils.release.ReleaseType.season),
        (['<anything else>'], '<original query type>'),
    ),
    ids=lambda v: str(v),
)
def test_update_imdb_query(type_job_output, exp_query_type, ptp_tracker_jobs, mocker):
    mocker.patch.object(type(ptp_tracker_jobs), 'imdb_job', PropertyMock(return_value=Mock(
        query=Mock(
            type='<original query type>',
        ),
    )))
    mocker.patch.object(type(ptp_tracker_jobs), 'type_job', PropertyMock(return_value=Mock(
        is_finished=True,
        output=type_job_output,
    )))

    return_value = ptp_tracker_jobs.update_imdb_query('job_')
    assert return_value is None
    assert ptp_tracker_jobs.imdb_job.query.type == exp_query_type


def test_trumpable_job(ptp_tracker_jobs, mocker):
    mocker.patch.object(type(ptp_tracker_jobs), 'release_name_job', PropertyMock())
    CustomJob_mock = mocker.patch('upsies.jobs.custom.CustomJob')
    mocker.patch.object(ptp_tracker_jobs, 'get_job_name')
    mocker.patch.object(ptp_tracker_jobs, 'make_precondition')
    mocker.patch.object(ptp_tracker_jobs, 'common_job_args', return_value={'common_job_arg': 'common job argument'})

    assert ptp_tracker_jobs.trumpable_job is CustomJob_mock.return_value
    assert CustomJob_mock.call_args_list == [call(
        name=ptp_tracker_jobs.get_job_name.return_value,
        label='Trumpable',
        precondition=ptp_tracker_jobs.make_precondition.return_value,
        worker=ptp_tracker_jobs.autodetect_trumpable,
        no_output_is_ok=True,
        catch=(
            errors.ContentError,
        ),
        common_job_arg='common job argument',
    )]
    assert ptp_tracker_jobs.get_job_name.call_args_list == [call('trumpable')]
    assert ptp_tracker_jobs.make_precondition.call_args_list == [call('trumpable_job')]
    assert ptp_tracker_jobs.common_job_args.call_args_list == [call(ignore_cache=True)]


@pytest.mark.parametrize(
    argnames='options, exp_hardcoded_subtitles_from_options, exp_no_english_subtitles_from_options',
    argvalues=(
        ({}, None, None),
        ({'hardcoded_subtitles': None, 'no_english_subtitles': None}, None, None),
        ({'hardcoded_subtitles': None, 'no_english_subtitles': True}, None, True),
        ({'hardcoded_subtitles': None, 'no_english_subtitles': False}, None, False),
        ({'hardcoded_subtitles': True, 'no_english_subtitles': None}, True, None),
        ({'hardcoded_subtitles': False, 'no_english_subtitles': None}, False, None),
        ({'hardcoded_subtitles': False, 'no_english_subtitles': True}, False, True),
        ({'hardcoded_subtitles': True, 'no_english_subtitles': False}, True, False),
        ({'hardcoded_subtitles': True, 'no_english_subtitles': True}, True, True),
        ({'hardcoded_subtitles': False, 'no_english_subtitles': False}, False, False),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.parametrize(
    argnames=(
        'audio_languages, subtitle_languages, '
        'exp_hardcoded_subtitles_from_autodetection, exp_no_english_subtitles_from_autodetection'
    ),
    argvalues=(
        pytest.param(
            None, None, None, True,
            id='No languages',
        ),
        pytest.param(
            {'se'},
            {},
            None,
            True,
            id='No English audio + No subtitles',
        ),
        pytest.param(
            {'se'},
            {'se', 'dk', 'no'},
            None,
            True,
            id='No English audio + No English subtitles',
        ),
        pytest.param(
            {'se'},
            {'se', 'en', 'dk', 'no'},
            None,
            False,
            id='No English audio + English subtitles',
        ),
        pytest.param(
            {'se', 'en'},
            {'se', 'dk', 'no'},
            None,
            False,
            id='English audio + No English subtitles',
        ),
        pytest.param(
            {'se', 'en'},
            {'en', 'se', 'dk', 'no'},
            None,
            False,
            id='English audio + English subtitles',
        ),
    ),
    ids=lambda v: str(v),
)
async def test_autodetect_trumpable(
        options,
        exp_hardcoded_subtitles_from_options, exp_no_english_subtitles_from_options,
        audio_languages, subtitle_languages,
        exp_hardcoded_subtitles_from_autodetection, exp_no_english_subtitles_from_autodetection,
        ptp_tracker_jobs, mocker,
):
    mocker.patch.object(type(ptp_tracker_jobs), 'options', PropertyMock(return_value=options))

    languages_mock = mocker.patch('upsies.utils.video.languages', return_value=(
        {'Audio': audio_languages}
        if audio_languages is not None else
        {}
    ))

    mocker.patch.object(type(ptp_tracker_jobs), 'subtitles', PropertyMock(return_value=(
        [
            Mock(language=language)
            for language in subtitle_languages
        ]
        if subtitle_languages is not None else
        []
    )))

    return_value = await ptp_tracker_jobs.autodetect_trumpable('job_')

    exp_hardcoded_subtitles = (
        exp_hardcoded_subtitles_from_options
        if exp_hardcoded_subtitles_from_options is not None else
        exp_hardcoded_subtitles_from_autodetection
    )

    exp_no_english_subtitles = (
        exp_no_english_subtitles_from_options
        if exp_no_english_subtitles_from_options is not None else
        exp_no_english_subtitles_from_autodetection
    )

    exp_reasons = []
    if exp_hardcoded_subtitles:
        exp_reasons.append(ptp.metadata.PtpTrumpableReason.HARDCODED_SUBTITLES)
    if exp_no_english_subtitles:
        exp_reasons.append(ptp.metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES)

    assert return_value == exp_reasons

    if exp_no_english_subtitles_from_options is None:
        assert languages_mock.call_args_list == [
            call(ptp_tracker_jobs.content_path),
        ]


@pytest.mark.parametrize(
    argnames='trumpable_job_output, exp_post_data',
    argvalues=(
        ((), {'trumpable[]': []}),
        (
            (
                str(ptp.metadata.PtpTrumpableReason.HARDCODED_SUBTITLES),
            ),
            {
                'trumpable[]': [
                    ptp.metadata.PtpTrumpableReason.HARDCODED_SUBTITLES.value,
                ],
            },
        ),
        (
            (
                str(ptp.metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES),
            ),
            {
                'trumpable[]': [
                    ptp.metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES.value,
                ],
            },
        ),
        (
            (
                str(ptp.metadata.PtpTrumpableReason.HARDCODED_SUBTITLES),
                str(ptp.metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES),
            ),
            {
                'trumpable[]': [
                    ptp.metadata.PtpTrumpableReason.HARDCODED_SUBTITLES.value,
                    ptp.metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES.value,
                ],
            },
        ),
    ),
    ids=lambda v: str(v),
)
def test__post_data_common_trumpable(trumpable_job_output, exp_post_data, ptp_tracker_jobs, mocker):
    mocker.patch.object(type(ptp_tracker_jobs), 'trumpable_job', PropertyMock(return_value=Mock(
        output=trumpable_job_output,
    )))
    assert ptp_tracker_jobs._post_data_common_trumpable == exp_post_data
