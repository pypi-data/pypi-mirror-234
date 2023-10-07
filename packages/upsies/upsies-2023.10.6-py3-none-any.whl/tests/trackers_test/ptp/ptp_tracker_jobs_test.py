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

    print(ptp_tracker_jobs.jobs_before_upload)
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
    argnames='hardcoded_subtitles, exp_hardcoded_subtitles_reasons',
    argvalues=(
        (True, [ptp.metadata.PtpTrumpableReason.HARDCODED_SUBTITLES]),
        (False, []),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.parametrize(
    argnames='languages, exp_no_english_sutitles_reasons',
    argvalues=(
        pytest.param(
            {},
            [ptp.metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES],
            id='No languages found',
        ),
        pytest.param(
            {'Audio': {}, 'Text': {}},
            [ptp.metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES],
            id='Empty languages found (should not happen in practice)',
        ),
        pytest.param(
            {'Audio': {'se'}, 'Text': {'se', 'dk', 'no'}},
            [ptp.metadata.PtpTrumpableReason.NO_ENGLISH_SUBTITLES],
            id='No English audio + No English subtitles',
        ),
        pytest.param(
            {'Audio': {'se'}, 'Text': {'se', 'en', 'dk', 'no'}},
            [],
            id='No English audio + English subtitles',
        ),
        pytest.param(
            {'Audio': {'en', 'se'}, 'Text': {'se', 'dk', 'no'}},
            [],
            id='English audio + No English subtitles',
        ),
        pytest.param(
            {'Audio': {'se', 'en'}, 'Text': {'en', 'se', 'dk', 'no'}},
            [],
            id='English audio + English subtitles',
        ),
    ),
    ids=lambda v: str(v),
)
async def test_autodetect_category(
        hardcoded_subtitles, exp_hardcoded_subtitles_reasons,
        languages, exp_no_english_sutitles_reasons,
        ptp_tracker_jobs, mocker,
):
    languages_mock = mocker.patch('upsies.utils.video.languages', return_value=languages)
    mocker.patch.object(type(ptp_tracker_jobs), 'options', PropertyMock(
        return_value={'hardcoded_subtitles': hardcoded_subtitles},
    ))

    return_value = await ptp_tracker_jobs.autodetect_trumpable('job_')
    assert return_value == (
        exp_hardcoded_subtitles_reasons
        + exp_no_english_sutitles_reasons
    )

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
)
def test__post_data_common_trumpable(trumpable_job_output, exp_post_data, ptp_tracker_jobs, mocker):
    mocker.patch.object(type(ptp_tracker_jobs), 'trumpable_job', PropertyMock(return_value=Mock(
        output=trumpable_job_output,
    )))
    assert ptp_tracker_jobs._post_data_common_trumpable == exp_post_data
