import builtins
import os
import pathlib
import re
import types
from unittest.mock import AsyncMock, Mock, PropertyMock, call

import pytest

from upsies import errors, utils
from upsies.trackers.base import TrackerJobsBase


@pytest.fixture
def tracker():
    tracker = Mock()
    tracker.configure_mock(
        name='AsdF',
        options={
            'announce' : 'http://foo.bar',
            'source'   : 'AsdF',
            'exclude'  : ('a', 'b'),
        },
    )
    return tracker


def make_TestTrackerJobs(**kwargs):
    class TestTrackerJobs(TrackerJobsBase):
        jobs_before_upload = PropertyMock()

    default_kwargs = {
        'content_path': '',
        'tracker': Mock(
            options={
                'announce' : 'http://foo.bar',
                'source'   : 'AsdF',
                'exclude'  : ('a', 'b'),
            },
        ),
        'reuse_torrent_path': '',
        'btclient': Mock(),
        'torrent_destination': '',
        'image_host': '',
        'screenshots_optimization': 'my optimization level',
        'common_job_args': {},
    }
    return TestTrackerJobs(**{**default_kwargs, **kwargs})


def test_arguments():
    kwargs = {
        'content_path': Mock(),
        'tracker': Mock(),
        'reuse_torrent_path': Mock(),
        'exclude_files': Mock(),
        'btclient': Mock(),
        'torrent_destination': Mock(),
        'image_host': Mock(),
        'options': {'mock': 'config'},
    }
    tracker_jobs = make_TestTrackerJobs(**kwargs)
    for k, v in kwargs.items():
        assert getattr(tracker_jobs, k) is v


@pytest.mark.parametrize(
    argnames='common_job_args, overload, exp_return_value',
    argvalues=(
        (
            {'home_directory': 'initial/path', 'ignore_cache': 'mock bool'},
            {'home_directory': 'overloaded/path'},
            {'home_directory': 'overloaded/path', 'ignore_cache': 'mock bool'},
        ),
        (
            {'home_directory': 'initial/path', 'ignore_cache': 'mock bool'},
            {'additional_value': 'something'},
            {'home_directory': 'initial/path', 'ignore_cache': 'mock bool', 'additional_value': 'something'},
        ),
    ),
    ids=lambda v: repr(v),
)
def test_common_job_args(common_job_args, overload, exp_return_value):
    tracker_jobs = make_TestTrackerJobs(common_job_args=common_job_args)
    return_value = tracker_jobs.common_job_args(**overload)
    assert return_value == exp_return_value


def test_signals(mocker):
    Signal_mock = mocker.patch('upsies.utils.signal.Signal')
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.signal is Signal_mock.return_value
    assert Signal_mock.call_args_list == [call('warning', 'error', 'exception')]
    tracker_jobs.warn('foo')
    assert Signal_mock.return_value.emit.call_args_list == [
        call('warning', 'foo'),
    ]
    tracker_jobs.error('bar')
    assert Signal_mock.return_value.emit.call_args_list == [
        call('warning', 'foo'),
        call('error', 'bar'),
    ]
    tracker_jobs.exception('baz')
    assert Signal_mock.return_value.emit.call_args_list == [
        call('warning', 'foo'),
        call('error', 'bar'),
        call('exception', 'baz'),
    ]


def test_imdb():
    tracker_jobs = make_TestTrackerJobs()
    assert isinstance(tracker_jobs.imdb, utils.webdbs.imdb.ImdbApi)

def test_tmdb():
    tracker_jobs = make_TestTrackerJobs()
    assert isinstance(tracker_jobs.tvmaze, utils.webdbs.tvmaze.TvmazeApi)

def test_tvmaze():
    tracker_jobs = make_TestTrackerJobs()
    assert isinstance(tracker_jobs.tvmaze, utils.webdbs.tvmaze.TvmazeApi)


def test_jobs_after_upload(mocker):
    add_torrent_job_mock = mocker.patch('upsies.trackers.base.TrackerJobsBase.add_torrent_job')
    copy_torrent_job_mock = mocker.patch('upsies.trackers.base.TrackerJobsBase.copy_torrent_job')
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.jobs_after_upload == (
        add_torrent_job_mock,
        copy_torrent_job_mock,
    )


def test_isolated_jobs(mocker):
    tracker_jobs = make_TestTrackerJobs()
    assert tracker_jobs.isolated_jobs == ()


class Job(str):
    def __new__(cls, name, *, prejobs=(), presignals={}):
        self = super().__new__(
            cls,
            f'Job({name!r}, '
            + 'prejobs=' + ', '.join(repr(j.name) for j in prejobs) + ', '
            + 'presignals=' + ', '.join(repr(j.name) for j in presignals) + ', '
        )
        self.name = str(name)
        self.prejobs = tuple(prejobs)
        self.presignals = dict(presignals)
        return self

@pytest.mark.parametrize(
    argnames='jobs, exp_job_names',
    argvalues=(
        pytest.param(
            [
                Job(name='a'),
                Job(name='b'),
                Job(name='c'),
            ],
            ['a', 'b', 'c'],
            id='No dependencies',
        ),

        # NOTE: `...` or `Ellipsis` is a built-in Python singleton. We use it
        #       here to show that we only need the keys/jobs in `presignals` and
        #       the values are ignored.

        pytest.param(
            [
                Job(name='a', prejobs=[
                    Job(name='x', prejobs=[Job(name='1')]),
                    Job(name='y', prejobs=[Job(name='2', prejobs=[Job(name='ɑ')])]),
                    Job(name='c', prejobs=[]),
                ]),
                Job(name='b', prejobs=[
                    Job(name='x', prejobs=[Job(name='1')]),
                    Job(name='z', prejobs=[Job(name='3')]),
                ]),
                Job(name='c', prejobs=[]),

            ],
            ['a', 'x', '1', 'y', '2', 'ɑ', 'c', 'b', 'z', '3'],
            id='Dependencies from prejobs',
        ),

        pytest.param(
            [
                Job(name='a', presignals={Job(name='ɑ'): ...}),
                Job(name='b', presignals={
                    Job(name='x'): ...,
                    Job(name='y', presignals={Job(name='1'): ...}): ...,
                }),
                Job(name='c', presignals={
                    Job(name='y', presignals={Job(name='1'): ...}): ...,
                    Job(name='z', presignals={
                        Job(name='2'): ...,
                        Job(name='3', presignals={Job(name='ɑ'): ...}): ...,
                    }): ...,
                }),
            ],
            ['a', 'ɑ', 'b', 'x', 'y', '1', 'c', 'z', '2', '3'],
            id='Dependencies from presignals',
        ),

        pytest.param(
            [
                Job(name='c', prejobs=[
                    Job(name='z', presignals={
                        Job(name='2'): ...,
                    }),
                ]),
            ],
            ['c', 'z', '2'],
            id='Job depends on prejobs with presignals',
        ),

        pytest.param(
            [
                Job(name='c', presignals={
                    Job(name='z', prejobs=[
                        Job(name='2'),
                    ]): ...,
                }),
            ],
            ['c', 'z', '2'],
            id='Job depends on presignals with prejobs',
        ),

        pytest.param(
            [
                Job(name='a', prejobs=[Job(name='ɑ')], presignals={Job(name='1'): ...}),
                Job(name='b', presignals={
                    Job(name='x'): ...,
                    Job(name='y', prejobs=[Job(name='1')]): ...,
                }),
                Job(name='c', prejobs=[
                    Job(name='y', prejobs=[Job(name='1')]),
                    Job(
                        name='z',
                        prejobs=[Job(name='10'), Job(name='20')],
                        presignals={
                            Job(
                                name='2',
                                presignals={
                                    Job(
                                        name='β',
                                        prejobs=[
                                            Job(name='a', prejobs=[Job(name='ɑ')], presignals={Job(name='1'): ...}),
                                            Job(name='y', prejobs=[Job(name='1')]),
                                        ],
                                    ): ...,
                                },
                            ): ...,
                            Job(
                                name='3',
                                prejobs=[
                                    Job(name='a', prejobs=[Job(name='ɑ')], presignals={Job(name='1'): ...}),
                                ],
                                presignals={
                                    Job(name='a', prejobs=[Job(name='ɑ')], presignals={Job(name='1'): ...}): ...,
                                    Job(name='y', prejobs=[Job(name='1')]): ...,
                                },
                            ): ...,
                        },
                    ),
                ]),
            ],
            ['a', 'ɑ', '1', 'b', 'x', 'y', 'c', 'z', '10', '20', '2', 'β', '3'],
            id='Lots of mixed nested dependencies',
        ),
    ),
)
def test_get_job_and_dependencies(jobs, exp_job_names):
    tracker_jobs = make_TestTrackerJobs()
    required_jobs = tracker_jobs.get_job_and_dependencies(*jobs)
    assert [j.name for j in required_jobs] == exp_job_names


@pytest.mark.parametrize('isolated_jobs', ((), ('mock isolated job',)))
@pytest.mark.parametrize(
    argnames='jobs_before_upload, exp_submission_ok',
    argvalues=(
        ((), False),
        # All jobs exited successfully
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True)), True),

        # Job exited with non-zero exit_code
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True), Mock(exit_code=1, is_enabled=True)), False),
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=1, is_enabled=True), Mock(exit_code=0, is_enabled=True)), False),
        ((Mock(exit_code=1, is_enabled=True), Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True)), False),

        # Job is disabled
        ((Mock(exit_code=None, is_enabled=False), Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=True)), True),
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=None, is_enabled=False), Mock(exit_code=0, is_enabled=True)), True),
        ((Mock(exit_code=0, is_enabled=True), Mock(exit_code=0, is_enabled=False), Mock(exit_code=None, is_enabled=False)), True),
    ),
)
def test_submission_ok(isolated_jobs, jobs_before_upload, exp_submission_ok, mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(type(tracker_jobs), 'jobs_before_upload', PropertyMock(return_value=jobs_before_upload))
    mocker.patch.object(type(tracker_jobs), 'isolated_jobs', PropertyMock(return_value=isolated_jobs))
    if isolated_jobs:
        assert tracker_jobs.submission_ok is False
    else:
        assert tracker_jobs.submission_ok == exp_submission_ok


@pytest.mark.parametrize(
    argnames='job_name, tracker_name, exp_name',
    argvalues=(
        ('myjob', 'mytracker', 'myjob.mytracker'),
        ('myjob.mytracker', 'mytracker', 'myjob.mytracker'),
    ),
)
def test_get_job_name(job_name, tracker_name, exp_name, tracker, mocker):
    tracker.name = tracker_name
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        tracker=tracker,
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.get_job_name(job_name) == exp_name


def test_create_torrent_job(mocker):
    CreateTorrentJob_mock = mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        reuse_torrent_path='path/to/existing.torrent',
        tracker='mock tracker',
        exclude_files=('a', 'b', 'c'),
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.create_torrent_job is CreateTorrentJob_mock.return_value
    assert CreateTorrentJob_mock.call_args_list == [
        call(
            content_path='path/to/content',
            reuse_torrent_path='path/to/existing.torrent',
            tracker='mock tracker',
            exclude_files=('a', 'b', 'c'),
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('create_torrent_job')]

def test_create_torrent_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        tracker='mock tracker',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.create_torrent_job is tracker_jobs.create_torrent_job


@pytest.mark.parametrize(
    argnames='btclient, create_torrent_job, exp_add_torrent_job_is_None',
    argvalues=(
        (Mock(), Mock(), False),
        (None, Mock(), True),
        (Mock(), None, True),
    ),
)
def test_add_torrent_job(btclient, create_torrent_job, exp_add_torrent_job_is_None, mocker):
    AddTorrentJob_mock = mocker.patch('upsies.jobs.torrent.AddTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        tracker='mock tracker',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        btclient=btclient,
    )
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock(return_value=create_torrent_job))
    mocker.patch.object(tracker_jobs, 'make_precondition')
    if exp_add_torrent_job_is_None:
        assert tracker_jobs.add_torrent_job is None
        assert AddTorrentJob_mock.call_args_list == []
        assert tracker_jobs.make_precondition.call_args_list == []
    else:
        assert tracker_jobs.add_torrent_job is AddTorrentJob_mock.return_value
        assert AddTorrentJob_mock.call_args_list == [
            call(
                autostart=False,
                btclient=btclient,
                precondition=tracker_jobs.make_precondition.return_value,
                home_directory='path/to/home',
                ignore_cache='mock bool',
            ),
        ]
        assert tracker_jobs.create_torrent_job.signal.register.call_args_list == [
            call('output', tracker_jobs.add_torrent_job.enqueue),
            call('finished', tracker_jobs.finalize_add_torrent_job),
        ]
        assert tracker_jobs.make_precondition.call_args_list == [call('add_torrent_job')]

def test_add_torrent_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.torrent.AddTorrentJob', side_effect=(Mock(), Mock()))
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        tracker='mock tracker',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        btclient='bittorrent client mock',
    )
    assert tracker_jobs.add_torrent_job is tracker_jobs.add_torrent_job


def test_finalize_add_torrent_job(mocker):
    mocker.patch('upsies.jobs.torrent.AddTorrentJob')
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        tracker='mock tracker',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        btclient='bittorrent client mock',
    )
    mocker.patch.object(tracker_jobs, 'add_torrent_job')
    tracker_jobs.finalize_add_torrent_job('mock job')
    assert tracker_jobs.add_torrent_job.finalize.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='torrent_destination, create_torrent_job, exp_copy_torrent_job_is_None',
    argvalues=(
        ('some/path', Mock(), False),
        (None, Mock(), True),
        ('some/path', None, True),
    ),
)
def test_copy_torrent_job(torrent_destination, create_torrent_job, exp_copy_torrent_job_is_None, tracker, mocker):
    CopyTorrentJob_mock = mocker.patch('upsies.jobs.torrent.CopyTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        torrent_destination=torrent_destination,
        tracker=tracker,
    )
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock(return_value=create_torrent_job))
    mocker.patch.object(tracker_jobs, 'make_precondition')
    if exp_copy_torrent_job_is_None:
        assert tracker_jobs.copy_torrent_job is None
        assert CopyTorrentJob_mock.call_args_list == []
        assert tracker_jobs.make_precondition.call_args_list == []
    else:
        assert tracker_jobs.copy_torrent_job is CopyTorrentJob_mock.return_value
        assert CopyTorrentJob_mock.call_args_list == [
            call(
                autostart=False,
                destination=torrent_destination,
                precondition=tracker_jobs.make_precondition.return_value,
                home_directory='path/to/home',
                ignore_cache='mock bool',
            ),
        ]
        assert tracker_jobs.create_torrent_job.signal.register.call_args_list == [
            call('output', tracker_jobs.copy_torrent_job.enqueue),
            call('finished', tracker_jobs.finalize_copy_torrent_job),
        ]
        assert tracker_jobs.make_precondition.call_args_list == [call('copy_torrent_job')]

def test_copy_torrent_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.torrent.CopyTorrentJob', side_effect=(Mock(), Mock()))
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        torrent_destination='path/to/torrent/destination',
    )
    assert tracker_jobs.copy_torrent_job is tracker_jobs.copy_torrent_job


def test_finalize_copy_torrent_job(mocker):
    mocker.patch('upsies.jobs.torrent.CopyTorrentJob')
    mocker.patch('upsies.jobs.torrent.CreateTorrentJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        tracker='mock tracker',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        btclient='bittorrent client mock',
    )
    mocker.patch.object(tracker_jobs, 'copy_torrent_job')
    tracker_jobs.finalize_copy_torrent_job('mock job')
    assert tracker_jobs.copy_torrent_job.finalize.call_args_list == [call()]


def test_release_name(mocker):
    ReleaseName_mock = mocker.patch('upsies.utils.release.ReleaseName')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.release_name is ReleaseName_mock.return_value
    assert ReleaseName_mock.call_args_list == [
        call(
            path='path/to/content',
            translate=tracker_jobs.release_name_translation,
            separator=tracker_jobs.release_name_separator,
        ),
    ]


def test_release_name_job(tracker, mocker):
    TextFieldJob_mock = mocker.patch('upsies.jobs.dialog.TextFieldJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        tracker=tracker,
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocker.patch.object(type(tracker_jobs), 'release_name', PropertyMock())
    mocker.patch.object(tracker_jobs, 'get_job_name')
    mocker.patch.object(tracker_jobs, 'make_precondition')

    release_name_job = tracker_jobs.release_name_job
    assert release_name_job is TextFieldJob_mock.return_value
    assert TextFieldJob_mock.call_args_list == [
        call(
            name=tracker_jobs.get_job_name.return_value,
            label='Release Name',
            text=str(tracker_jobs.release_name),
            callbacks={
                'output': tracker_jobs.release_name.set_release_info,
            },
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('release_name_job')]

def test_release_name_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.dialog.TextFieldJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.release_name_job is tracker_jobs.release_name_job


@pytest.mark.asyncio
async def test_update_release_name_from(mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    mocker.patch.object(type(tracker_jobs), 'release_name', PropertyMock(return_value=Mock(
        fetch_info=Mock(),
    )))
    mocker.patch.object(type(tracker_jobs), 'release_name_job', PropertyMock(return_value=Mock(
        fetch_text=AsyncMock(),
    )))
    webdb = Mock()
    await tracker_jobs.update_release_name_from(webdb, 'tt123456')
    assert tracker_jobs.release_name_job.fetch_text.call_args_list == [
        call(
            coro=tracker_jobs.release_name.fetch_info.return_value,
            nonfatal_exceptions=(errors.RequestError,),
            default=str(tracker_jobs.release_name),
        ),
    ]
    assert tracker_jobs.release_name.fetch_info.call_args_list == [call(webdb=webdb, webdb_id='tt123456')]


def test_imdb_job(mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    WebDbSearchJob_mock = mocker.patch('upsies.jobs.webdb.WebDbSearchJob')
    mocker.patch.object(tracker_jobs, 'make_precondition')
    imdb_job = tracker_jobs.imdb_job
    assert imdb_job is WebDbSearchJob_mock.return_value
    assert WebDbSearchJob_mock.call_args_list == [
        call(
            query='path/to/content',
            db=tracker_jobs.imdb,
            callbacks={
                'output': tracker_jobs._handle_imdb_id,
            },
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('imdb_job')]

def test_imdb_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.webdb.WebDbSearchJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.imdb_job is tracker_jobs.imdb_job


@pytest.mark.parametrize(
    argnames='imdb_id, imdb, poster_webdb, exp_start_poster_job_calls',
    argvalues=(
        ('imdb id', 'mock imdb', None, []),
        ('imdb id', 'mock imdb', 'mock imdb', [call._start_poster_job('mock imdb', 'imdb id')]),
        ('imdb id', 'mock imdb', 'mock otherdb', []),
    ),
)
def test_handle_imdb_id(imdb_id, imdb, poster_webdb, exp_start_poster_job_calls, mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker_jobs.tracker, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_propagate_webdb_info', Mock()), '_propagate_webdb_info')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_start_poster_job'), '_start_poster_job')
    mocker.patch.object(type(tracker_jobs), 'imdb', PropertyMock(return_value=imdb))
    mocker.patch.object(type(tracker_jobs), '_poster_webdb', PropertyMock(return_value=poster_webdb))

    tracker_jobs._handle_imdb_id(imdb_id)
    assert mocks.mock_calls == [
        call._propagate_webdb_info(tracker_jobs.imdb, imdb_id),
        call.attach_task(tracker_jobs._propagate_webdb_info.return_value),
    ] + exp_start_poster_job_calls


def test_imdb_id_property(mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, '_get_webdb_id_from_job')
    return_value = tracker_jobs.imdb_id
    assert return_value is tracker_jobs._get_webdb_id_from_job.return_value
    assert tracker_jobs._get_webdb_id_from_job.call_args_list == [call(tracker_jobs.imdb_job)]


def test_tmdb_job(mocker):
    WebDbSearchJob_mock = mocker.patch('upsies.jobs.webdb.WebDbSearchJob')
    webdb_mock = mocker.patch('upsies.utils.webdbs.webdb')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.tmdb_job is WebDbSearchJob_mock.return_value
    assert WebDbSearchJob_mock.call_args_list == [
        call(
            query='path/to/content',
            db=webdb_mock.return_value,
            callbacks={
                'output': tracker_jobs._handle_tmdb_id,
            },
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        ),
    ]
    assert webdb_mock.call_args_list == [call('tmdb')]
    assert tracker_jobs.make_precondition.call_args_list == [call('tmdb_job')]


def test_tmdb_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.webdb.WebDbSearchJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.tmdb_job is tracker_jobs.tmdb_job


@pytest.mark.parametrize(
    argnames='tmdb_id, tmdb, poster_webdb, exp_start_poster_job_calls',
    argvalues=(
        ('tmdb id', 'mock tmdb', None, []),
        ('tmdb id', 'mock tmdb', 'mock tmdb', [call._start_poster_job('mock tmdb', 'tmdb id')]),
        ('tmdb id', 'mock tmdb', 'mock otherdb', []),
    ),
)
def test_handle_tmdb_id(tmdb_id, tmdb, poster_webdb, exp_start_poster_job_calls, mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker_jobs.tracker, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_propagate_webdb_info', Mock()), '_propagate_webdb_info')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_start_poster_job'), '_start_poster_job')
    mocker.patch.object(type(tracker_jobs), 'tmdb', PropertyMock(return_value=tmdb))
    mocker.patch.object(type(tracker_jobs), '_poster_webdb', PropertyMock(return_value=poster_webdb))

    tracker_jobs._handle_tmdb_id(tmdb_id)
    assert mocks.mock_calls == [
        call._propagate_webdb_info(tracker_jobs.tmdb, tmdb_id),
        call.attach_task(tracker_jobs._propagate_webdb_info.return_value),
    ] + exp_start_poster_job_calls


def test_tmdb_id_property(mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, '_get_webdb_id_from_job')
    return_value = tracker_jobs.tmdb_id
    assert return_value is tracker_jobs._get_webdb_id_from_job.return_value
    assert tracker_jobs._get_webdb_id_from_job.call_args_list == [call(tracker_jobs.tmdb_job)]


def test_tvmaze_job(mocker):
    WebDbSearchJob_mock = mocker.patch('upsies.jobs.webdb.WebDbSearchJob')
    webdb_mock = mocker.patch('upsies.utils.webdbs.webdb')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.tvmaze_job is WebDbSearchJob_mock.return_value
    assert WebDbSearchJob_mock.call_args_list == [
        call(
            query='path/to/content',
            db=webdb_mock.return_value,
            callbacks={
                'output': tracker_jobs._handle_tvmaze_id,
            },
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        ),
    ]
    assert webdb_mock.call_args_list == [call('tvmaze')]
    assert tracker_jobs.make_precondition.call_args_list == [call('tvmaze_job')]

def test_tvmaze_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.webdb.WebDbSearchJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.tvmaze_job is tracker_jobs.tvmaze_job


@pytest.mark.parametrize(
    argnames='tvmaze_id, tvmaze, poster_webdb, exp_start_poster_job_calls',
    argvalues=(
        ('tvmaze id', 'mock tvmaze', None, []),
        ('tvmaze id', 'mock tvmaze', 'mock tvmaze', [call._start_poster_job('mock tvmaze', 'tvmaze id')]),
        ('tvmaze id', 'mock tvmaze', 'mock otherdb', []),
    ),
)
def test_handle_tvmaze_id(tvmaze_id, tvmaze, poster_webdb, exp_start_poster_job_calls, mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(tracker_jobs.tracker, 'attach_task'), 'attach_task')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_propagate_webdb_info', Mock()), '_propagate_webdb_info')
    mocks.attach_mock(mocker.patch.object(tracker_jobs, '_start_poster_job'), '_start_poster_job')
    mocker.patch.object(type(tracker_jobs), 'tvmaze', PropertyMock(return_value=tvmaze))
    mocker.patch.object(type(tracker_jobs), '_poster_webdb', PropertyMock(return_value=poster_webdb))

    tracker_jobs._handle_tvmaze_id(tvmaze_id)
    assert mocks.mock_calls == [
        call._propagate_webdb_info(tracker_jobs.tvmaze, tvmaze_id),
        call.attach_task(tracker_jobs._propagate_webdb_info.return_value),
    ] + exp_start_poster_job_calls


def test_tvmaze_id_property(mocker):
    tracker_jobs = make_TestTrackerJobs()
    mocker.patch.object(tracker_jobs, '_get_webdb_id_from_job')
    return_value = tracker_jobs.tvmaze_id
    assert return_value is tracker_jobs._get_webdb_id_from_job.return_value
    assert tracker_jobs._get_webdb_id_from_job.call_args_list == [call(tracker_jobs.tvmaze_job)]


@pytest.mark.parametrize(
    argnames='webdb_job, exp_return_value',
    argvalues=(
        (Mock(is_finished=False, output=[]), None),
        (Mock(is_finished=False, output=['mock id']), None),
        (Mock(is_finished=False, output=['mock id', 'another mock id']), None),
        (Mock(is_finished=True, output=[]), None),
        (Mock(is_finished=True, output=['mock id']), 'mock id'),
        (Mock(is_finished=True, output=['mock id', 'another mock id']), 'mock id'),
    ),
)
def test_get_webdb_id_from_job(webdb_job, exp_return_value, mocker):
    tracker_jobs = make_TestTrackerJobs()
    return_value = tracker_jobs._get_webdb_id_from_job(webdb_job)
    assert return_value == exp_return_value


@pytest.mark.parametrize('english_title', ('', 'English Title'))
@pytest.mark.parametrize('origin_job_is_finished', (False, True))
@pytest.mark.asyncio
async def test_propagate_webdb_info(origin_job_is_finished, english_title, mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocks = Mock(
        update_release_name_from=AsyncMock(),
    )
    mocker.patch.object(tracker_jobs, 'update_release_name_from', mocks.update_release_name_from)
    mocker.patch('upsies.utils.webdbs.webdb_names', mocks.webdb_names)
    mocks.webdb_names.return_value = ('adb', 'bdb', 'cdb', 'ddb')

    mocker.patch('upsies.utils.webdbs.Query', mocks.Query)

    def make_db(name, type, title_english, title_original, year):
        return types.SimpleNamespace(
            name=name,
            type=AsyncMock(return_value=type),
            title_english=AsyncMock(return_value=title_english),
            title_original=AsyncMock(return_value=title_original),
            year=AsyncMock(return_value=year),
        )

    adb = make_db('adb', 'type from adb', english_title, 'original title from adb', 'year from adb')
    bdb = make_db('bdb', 'type from bdb', 'english title from bdb', 'original title from bdb', 'year from bdb')
    cdb = make_db('cdb', 'type from cdb', 'english title from cdb', 'original title from cdb', 'year from cdb')
    ddb = make_db('ddb', 'type from ddb', 'english title from ddb', 'original title from ddb', 'year from ddb')
    mocker.patch.object(type(tracker_jobs), 'adb', PropertyMock(return_value=adb), create=True)
    mocker.patch.object(type(tracker_jobs), 'bdb', PropertyMock(return_value=bdb), create=True)
    mocker.patch.object(type(tracker_jobs), 'cdb', PropertyMock(return_value=cdb), create=True)
    mocker.patch.object(type(tracker_jobs), 'ddb', PropertyMock(return_value=ddb), create=True)

    def make_db_job(name, is_enabled, is_finished, search):
        return types.SimpleNamespace(
            name=name,
            is_enabled=is_enabled,
            is_finished=is_finished,
            search=search,
            query=getattr(mocks, name[:name.index('-')]).query,
        )

    adb_job = make_db_job('adb-id', True, origin_job_is_finished, mocks.adb.search)
    bdb_job = make_db_job('bdb-id', False, True, mocks.bdb.search)
    cdb_job = make_db_job('cdb-id', True, False, mocks.cdb.search)
    ddb_job = make_db_job('ddb-id', True, True, mocks.ddb.search)
    mocker.patch.object(type(tracker_jobs), 'adb_job', PropertyMock(return_value=adb_job), create=True)
    mocker.patch.object(type(tracker_jobs), 'bdb_job', PropertyMock(return_value=bdb_job), create=True)
    mocker.patch.object(type(tracker_jobs), 'cdb_job', PropertyMock(return_value=cdb_job), create=True)
    mocker.patch.object(type(tracker_jobs), 'ddb_job', PropertyMock(return_value=ddb_job), create=True)

    await tracker_jobs._propagate_webdb_info(tracker_jobs.adb, '123456')

    exp_title = english_title or 'original title from adb'
    assert mocks.mock_calls == [
        call.webdb_names(),
        call.Query(type='type from adb', title=exp_title, year='year from adb'),
        call.cdb.query.update(mocks.Query.return_value),
        call.update_release_name_from(tracker_jobs.adb, '123456'),
    ]


def test_screenshots_job(mocker):
    ScreenshotsJob_mock = mocker.patch('upsies.jobs.screenshots.ScreenshotsJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    mocker.patch.object(type(tracker_jobs), 'screenshots_count', PropertyMock())
    mocker.patch.object(type(tracker_jobs), 'screenshots_from_all_videos', PropertyMock())
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock())
    assert tracker_jobs.screenshots_job is ScreenshotsJob_mock.return_value
    assert ScreenshotsJob_mock.call_args_list == [
        call(
            content_path='path/to/content',
            exclude_files=tracker_jobs.exclude_files,
            count=tracker_jobs.screenshots_count,
            from_all_videos=tracker_jobs.screenshots_from_all_videos,
            optimize=tracker_jobs._screenshots_optimization,
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('screenshots_job')]

def test_screenshots_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.screenshots.ScreenshotsJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    mocker.patch.object(type(tracker_jobs), 'create_torrent_job', PropertyMock())
    assert tracker_jobs.screenshots_job is tracker_jobs.screenshots_job


def test_screenshots_count(mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        options={'screenshots': 123},
    )
    assert tracker_jobs.screenshots_count == 123


def test_screenshots_from_all_videos(mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.screenshots_from_all_videos is False


def test_image_host_config():
    assert TrackerJobsBase.image_host_config == {}


@pytest.mark.parametrize(
    argnames='image_host, screenshots_job, exp_upload_screenshots_job_is_None',
    argvalues=(
        (Mock(), Mock(), False),
        (None, Mock(), True),
        (Mock(), None, True),
    ),
)
def test_upload_screenshots_job(image_host, screenshots_job, exp_upload_screenshots_job_is_None, mocker):
    ImageHostJob_mock = mocker.patch('upsies.jobs.imghost.ImageHostJob')
    mocker.patch('upsies.jobs.screenshots.ScreenshotsJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        image_host=image_host,
    )
    mocker.patch.object(type(tracker_jobs), 'screenshots_job', PropertyMock(return_value=screenshots_job))
    mocker.patch.object(tracker_jobs, 'make_precondition')
    if exp_upload_screenshots_job_is_None:
        assert tracker_jobs.upload_screenshots_job is None
        assert ImageHostJob_mock.call_args_list == []
        assert tracker_jobs.make_precondition.call_args_list == []
    else:
        assert tracker_jobs.upload_screenshots_job is ImageHostJob_mock.return_value
        assert ImageHostJob_mock.call_args_list == [call(
            imghost=image_host,
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        )]
        # ScreenshotsJob also registers a callback for "timestamps"
        assert tracker_jobs.screenshots_job.signal.register.call_args_list == [
            call('screenshots_total', tracker_jobs.upload_screenshots_job.set_images_total),
            call('output', tracker_jobs.upload_screenshots_job.enqueue),
            call('finished', tracker_jobs.finalize_upload_screenshots_job),
        ]
        assert tracker_jobs.make_precondition.call_args_list == [call('upload_screenshots_job')]

def test_upload_screenshots_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.imghost.ImageHostJob', side_effect=(Mock(), Mock()))
    mocker.patch('upsies.jobs.screenshots.ScreenshotsJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        image_host=Mock(),
    )
    assert tracker_jobs.upload_screenshots_job is tracker_jobs.upload_screenshots_job


def test_poster_job(mocker):
    PosterJob_mock = mocker.patch('upsies.jobs.poster.PosterJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.poster_job is PosterJob_mock.return_value
    assert PosterJob_mock.call_args_list == [
        call(
            autostart=False,
            webdb_id=None,
            webdb=None,
            imghost=tracker_jobs.image_host,
            width=tracker_jobs.poster_max_width,
            height=tracker_jobs.poster_max_height,
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('poster_job')]

def test_poster_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.poster.PosterJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.poster_job is tracker_jobs.poster_job


def test_start_poster_job(mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocker.patch.object(tracker_jobs.poster_job, 'start')
    mocker.patch.object(type(tracker_jobs.release_name), 'only_season', PropertyMock(return_value='3'))

    tracker_jobs._start_poster_job('mock webdb', 'webdb id')
    assert tracker_jobs.poster_job.start.call_args_list == [call(
        webdb='mock webdb',
        webdb_id='webdb id',
        season='3',
    )]


@pytest.mark.parametrize(
    argnames='is_enabled, is_started, in_jobs_before_upload',
    argvalues=(
        (False, False, False),

        (False, False, True),
        (False, True, False),
        (True, False, False),

        (False, True, True),
        # (True, False, True),  # poster_job is enabled
        (True, True, False),

        (True, True, True),
    ),
)
def test_poster_webdb_when_poster_job_is_disabled(is_enabled, is_started, in_jobs_before_upload, mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocker.patch.object(type(tracker_jobs), 'poster_job', PropertyMock(return_value=Mock(
        is_enabled=is_enabled,
        is_started=is_started,
    )))
    if in_jobs_before_upload:
        jobs_before_upload = ('foo', tracker_jobs.poster_job, 'bar')
    else:
        jobs_before_upload = ('foo', 'bar')
    mocker.patch.object(type(tracker_jobs), 'jobs_before_upload', PropertyMock(return_value=jobs_before_upload))

    assert tracker_jobs._poster_webdb is None

@pytest.mark.parametrize(
    argnames=(
        'tvmaze_is_enabled, tvmaze_in_jobs_before_upload, release_type, '
        'imdb_is_enabled, imdb_in_jobs_before_upload, '
        'tmdb_is_enabled, tmdb_in_jobs_before_upload, '
        'exp_result'
    ),
    argvalues=(
        pytest.param(
            True, True, utils.types.ReleaseType.season,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            'tvmaze',
            id='tvmaze for season',
        ),
        pytest.param(
            True, True, utils.types.ReleaseType.episode,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            'tvmaze',
            id='tvmaze for episode',
        ),
        pytest.param(
            True, True, utils.types.ReleaseType.movie,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            'imdb',
            id='imdb for movie',
        ),
        pytest.param(
            True, False, utils.types.ReleaseType.series,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            'imdb',
            id='imdb if tvmaze is not used',
        ),
        pytest.param(
            False, True, utils.types.ReleaseType.series,  # TVmaze
            True, True,  # IMDb
            True, True,  # TMDb
            'imdb',
            id='imdb if tvmaze is not enabled',
        ),
        pytest.param(
            False, False, utils.types.ReleaseType.movie,  # TVmaze
            True, False,  # IMDb
            True, True,  # TMDb
            'tmdb',
            id='tmdb if imdb is not used',
        ),
        pytest.param(
            False, False, utils.types.ReleaseType.movie,  # TVmaze
            False, True,  # IMDb
            True, True,  # TMDb
            'tmdb',
            id='tmdb if imdb is not enabled',
        ),
        pytest.param(
            True, False, utils.types.ReleaseType.movie,  # TVmaze
            True, False,  # IMDb
            True, False,  # TMDb
            RuntimeError('You must add a WebDbSearchJob instance to jobs_before_upload'),
            id='error if no webdb job is used',
        ),
        pytest.param(
            False, True, utils.types.ReleaseType.movie,  # TVmaze
            False, True,  # IMDb
            False, True,  # TMDb
            RuntimeError('You must add a WebDbSearchJob instance to jobs_before_upload'),
            id='error if no webdb job is enabled',
        ),
    ),
)
def test_poster_webdb_returns(
        tvmaze_is_enabled, tvmaze_in_jobs_before_upload, release_type,
        imdb_is_enabled, imdb_in_jobs_before_upload,
        tmdb_is_enabled, tmdb_in_jobs_before_upload,
        exp_result,
        mocker,
):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocker.patch.object(type(tracker_jobs), 'poster_job', PropertyMock(return_value=Mock(
        is_enabled=True,
        is_started=False,
    )))
    mocker.patch.object(type(tracker_jobs), 'imdb_job', PropertyMock(return_value=Mock(is_enabled=imdb_is_enabled)))
    mocker.patch.object(type(tracker_jobs), 'tmdb_job', PropertyMock(return_value=Mock(is_enabled=tmdb_is_enabled)))
    mocker.patch.object(type(tracker_jobs), 'tvmaze_job', PropertyMock(return_value=Mock(is_enabled=tvmaze_is_enabled)))
    mocker.patch.object(type(tracker_jobs.release_name), 'type', PropertyMock(return_value=release_type))

    jobs_before_upload = ['foo', tracker_jobs.poster_job, 'bar']
    if imdb_in_jobs_before_upload:
        jobs_before_upload.insert(1, tracker_jobs.imdb_job)
    if tmdb_in_jobs_before_upload:
        jobs_before_upload.insert(1, tracker_jobs.tmdb_job)
    if tvmaze_in_jobs_before_upload:
        jobs_before_upload.insert(1, tracker_jobs.tvmaze_job)
    print(jobs_before_upload)
    mocker.patch.object(type(tracker_jobs), 'jobs_before_upload', PropertyMock(return_value=jobs_before_upload))

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker_jobs._poster_webdb
    else:
        assert tracker_jobs._poster_webdb is getattr(tracker_jobs, exp_result)


def test_finalize_upload_screenshots_job(mocker):
    mocker.patch('upsies.jobs.screenshots.ScreenshotsJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        tracker='mock tracker',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        btclient='bittorrent client mock',
    )
    mocker.patch.object(tracker_jobs, 'upload_screenshots_job')
    tracker_jobs.finalize_upload_screenshots_job('mock job')
    assert tracker_jobs.upload_screenshots_job.finalize.call_args_list == [call()]


def test_mediainfo_job(mocker):
    MediainfoJob_mock = mocker.patch('upsies.jobs.mediainfo.MediainfoJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    mocker.patch.object(type(tracker_jobs), 'mediainfo_from_all_videos', PropertyMock(
        return_value='maybe from_all_videos?',
    )),
    mocker.patch.object(type(tracker_jobs), 'exclude_files', PropertyMock(
        return_value='exclude these files!',
    )),
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.mediainfo_job is MediainfoJob_mock.return_value
    assert MediainfoJob_mock.call_args_list == [
        call(
            content_path='path/to/content',
            from_all_videos='maybe from_all_videos?',
            exclude_files='exclude these files!',
            precondition=tracker_jobs.make_precondition.return_value,
            home_directory='path/to/home',
            ignore_cache='mock bool',
        ),
    ]
    assert tracker_jobs.make_precondition.call_args_list == [call('mediainfo_job')]

def test_mediainfo_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.mediainfo.MediainfoJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.mediainfo_job is tracker_jobs.mediainfo_job


def test_mediainfos_and_screenshots(mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )

    mocker.patch.object(type(tracker_jobs), 'mediainfo_job', PropertyMock(return_value=Mock(mediainfos_by_file={
        'path/to/foo.mkv': '<mediainfo for foo.mkv>',
        'path/to/bar/VIDEO_TS/VTS_01_0.IFO': '<mediainfo for bar/VTS_01_0.IFO>',
        'path/to/bar/VIDEO_TS/VTS_01_1.VOB': '<mediainfo for bar/VTS_01_1.VOB>',
    })))
    mocker.patch.object(type(tracker_jobs), 'screenshots_job', PropertyMock(return_value=Mock(screenshots_by_file={
        'path/to/foo.mkv': ('path/to/foo.1.png', 'path/to/foo.2.png'),
        'path/to/bar/VIDEO_TS/VTS_01_1.VOB': ('VTS_01_1.VOB.1.jpg',),
        'path/to/baz.mkv': ('path/to/baz.1.png', 'path/to/baz.2.png', 'path/to/baz.3.png'),
    })))
    mocker.patch.object(type(tracker_jobs), 'upload_screenshots_job', PropertyMock(return_value=Mock(urls_by_file={
        'path/to/foo.1.png': 'https://foo.1.png',
        'path/to/foo.2.png': 'https://foo.2.png',
        'VTS_01_1.VOB.1.jpg': 'https://VTS_01_1.VOB.1.jpg',
        'path/to/baz.1.png': 'https://baz.1.png',
        'path/to/baz.2.png': 'https://baz.2.png',
    })))

    assert tracker_jobs.mediainfos_and_screenshots == {
        'path/to/foo.mkv': {
            'mediainfo': '<mediainfo for foo.mkv>',
            'screenshot_urls': ['https://foo.1.png', 'https://foo.2.png'],
        },
        'path/to/bar/VIDEO_TS/VTS_01_0.IFO': {
            'mediainfo': '<mediainfo for bar/VTS_01_0.IFO>',
            'screenshot_urls': [],
        },
        'path/to/bar/VIDEO_TS/VTS_01_1.VOB': {
            'mediainfo': '<mediainfo for bar/VTS_01_1.VOB>',
            'screenshot_urls': ['https://VTS_01_1.VOB.1.jpg'],
        },
        'path/to/baz.mkv': {
            'mediainfo': '',
            'screenshot_urls': ['https://baz.1.png', 'https://baz.2.png'],
        },
    }


@pytest.mark.parametrize(
    argnames='options, common_job_args, exp_kwargs',
    argvalues=(
        ({}, {'ignore_cache': True}, {'ignore_cache': True, 'force': None}),
        ({}, {'ignore_cache': False}, {'ignore_cache': True, 'force': None}),
        ({'is_scene': None}, {'ignore_cache': True}, {'ignore_cache': True, 'force': None}),
        ({'is_scene': None}, {'ignore_cache': False}, {'ignore_cache': True, 'force': None}),
        ({'is_scene': True}, {'ignore_cache': True}, {'ignore_cache': True, 'force': True}),
        ({'is_scene': True}, {'ignore_cache': False}, {'ignore_cache': True, 'force': True}),
        ({'is_scene': False}, {'ignore_cache': True}, {'ignore_cache': True, 'force': False}),
        ({'is_scene': False}, {'ignore_cache': False}, {'ignore_cache': True, 'force': False}),
    ),
    ids=lambda v: repr(v),
)
def test_scene_check_job(options, common_job_args, exp_kwargs, mocker):
    SceneCheckJob_mock = mocker.patch('upsies.jobs.scene.SceneCheckJob')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args=common_job_args,
    )
    mocker.patch.object(type(tracker_jobs), 'options', PropertyMock(return_value=options))
    mocker.patch.object(tracker_jobs, 'make_precondition')
    assert tracker_jobs.scene_check_job is SceneCheckJob_mock.return_value
    assert SceneCheckJob_mock.call_args_list == [call(
        content_path='path/to/content',
        precondition=tracker_jobs.make_precondition.return_value,
        **exp_kwargs,
    )]
    assert tracker_jobs.make_precondition.call_args_list == [call('scene_check_job')]

def test_scene_check_job_is_singleton(mocker):
    mocker.patch('upsies.jobs.scene.SceneCheckJob', side_effect=(Mock(), Mock()))
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    assert tracker_jobs.scene_check_job is tracker_jobs.scene_check_job


@pytest.mark.parametrize(
    argnames='job_attr, jobs_before_upload, jobs_after_upload, isolated_jobs, custom_precondition, exp_return_value',
    argvalues=(
        ('foo_job', (), (), (), None, False),
        ('foo_job', (), (), (), Mock(return_value=True), False),
        ('foo_job', (), (), (), Mock(return_value=False), False),

        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), (), None, True),
        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=True), True),
        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=False), False),

        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), (), None, True),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=True), True),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=False), False),

        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), (), None, True),
        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=True), True),
        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), (), Mock(return_value=False), False),

        ('baz_job', ('foo_job',), ('bar_job',), (), None, False),
        ('baz_job', ('foo_job',), ('bar_job',), (), Mock(return_value=True), False),
        ('baz_job', ('foo_job',), ('bar_job',), (), Mock(return_value=False), False),

        ('bar_job', (), ('bar_job',), (), None, True),
        ('bar_job', (), ('bar_job',), (), Mock(return_value=True), True),
        ('bar_job', (), ('bar_job',), (), Mock(return_value=False), False),

        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), None, True),
        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), Mock(return_value=True), True),
        ('foo_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), Mock(return_value=False), False),

        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), None, False),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), Mock(return_value=True), False),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job',), Mock(return_value=False), False),

        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), None, True),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), Mock(return_value=True), True),
        ('bar_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), Mock(return_value=False), False),

        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), None, False),
        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), Mock(return_value=True), False),
        ('baz_job', ('foo_job', 'bar_job'), ('baz_job',), ('foo_job', 'bar_job'), Mock(return_value=False), False),
    ),
    ids=lambda v: str(v),
)
def test_make_precondition(job_attr, jobs_before_upload, jobs_after_upload, isolated_jobs, custom_precondition,
                           exp_return_value, mocker):
    tracker_jobs = make_TestTrackerJobs()
    for attr in ('foo_job', 'bar_job', 'baz_job'):
        mocker.patch.object(type(tracker_jobs), attr, PropertyMock(), create=True)
    mocker.patch.object(type(tracker_jobs), 'jobs_before_upload', PropertyMock(
        return_value=[getattr(tracker_jobs, attr) for attr in jobs_before_upload],
    ))
    mocker.patch.object(type(tracker_jobs), 'jobs_after_upload', PropertyMock(
        return_value=[getattr(tracker_jobs, attr) for attr in jobs_after_upload],
    ))
    mocker.patch.object(type(tracker_jobs), 'isolated_jobs', PropertyMock(
        return_value=[getattr(tracker_jobs, attr) for attr in isolated_jobs],
    ))
    precondition = tracker_jobs.make_precondition(job_attr, precondition=custom_precondition)
    return_value = precondition()
    assert return_value == exp_return_value


@pytest.mark.parametrize(
    argnames='job, slice, default, exp_result',
    argvalues=(
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            None,
            TrackerJobsBase._NO_DEFAULT,
            ('foo', 'bar', 'baz'),
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            0,
            'ignored default',
            'foo',
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            1,
            TrackerJobsBase._NO_DEFAULT,
            'bar',
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            2,
            'ignored default',
            'baz',
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            builtins.slice(1, 3),
            TrackerJobsBase._NO_DEFAULT,
            ('bar', 'baz'),
        ),

        # Job is not Finished
        (
            Mock(is_finished=False, output=('foo', 'bar', 'baz')),
            None,
            TrackerJobsBase._NO_DEFAULT,
            RuntimeError('Unfinished job: asdf'),
        ),
        (
            Mock(is_finished=False, output=('foo', 'bar', 'baz')),
            None,
            'my default',
            'my default',
        ),
        (
            Mock(is_finished=False, output=('foo', 'bar', 'baz')),
            None,
            None,
            None,
        ),

        # Slicing output fails with IndexError
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            10,
            TrackerJobsBase._NO_DEFAULT,
            RuntimeError("Job finished with insufficient output: asdf: ('foo', 'bar', 'baz')"),
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            10,
            'my default',
            RuntimeError("Job finished with insufficient output: asdf: ('foo', 'bar', 'baz')"),
        ),
        (
            Mock(is_finished=True, output=('foo', 'bar', 'baz')),
            10,
            None,
            RuntimeError("Job finished with insufficient output: asdf: ('foo', 'bar', 'baz')"),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_job_output(job, slice, default, exp_result, mocker):
    job.configure_mock(name='asdf')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            tracker_jobs.get_job_output(job, slice, default=default)
    else:
        output = tracker_jobs.get_job_output(job, slice, default=default)
        assert output == exp_result


@pytest.mark.parametrize(
    argnames='job, attribute, default, exp_result',
    argvalues=(
        (
            Mock(is_finished=True, foo='bar'),
            'foo',
            TrackerJobsBase._NO_DEFAULT,
            'bar',
        ),
        (
            Mock(is_finished=True, foo='bar'),
            'foo',
            'ignored default',
            'bar',
        ),
        (
            Mock(is_finished=False, foo='bar'),
            'foo',
            TrackerJobsBase._NO_DEFAULT,
            RuntimeError('Unfinished job: asdf'),
        ),
        (
            Mock(is_finished=False, foo='bar'),
            'foo',
            'my default',
            'my default',
        ),
        (
            Mock(is_finished=True, foo='bar', spec=()),
            'no_such_attribute',
            TrackerJobsBase._NO_DEFAULT,
            AttributeError('no_such_attribute'),
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_get_job_attribute(job, attribute, default, exp_result, mocker):
    job.configure_mock(name='asdf')
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'{re.escape(str(exp_result))}'):
            tracker_jobs.get_job_attribute(job, attribute, default=default)
    else:
        value = tracker_jobs.get_job_attribute(job, attribute, default=default)
        assert value == exp_result


@pytest.mark.parametrize(
    argnames='file_path, content_path, exp_result',
    argvalues=(
        (
            '/path/to/somewhere',
            '/this/is/completely/different',
            ValueError(r"'[\w+/]*to/somewhere' is not a subpath of '[\w+/]*completely'"),
        ),
        (
            '{tmp_path}/file.mkv',
            '{tmp_path}/file.mkv',
            'file.mkv',
        ),
        (
            '{tmp_path}/content/file_in_directory.mkv',
            '{tmp_path}/content',
            'content/file_in_directory.mkv',
        ),
        (
            '{tmp_path}/content/extras/file_in_subdirectory.mkv',
            '{tmp_path}/content',
            'content/extras/file_in_subdirectory.mkv',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize('file_path_is_relative', (False, True), ids=('file_path_is_absolute', 'file_path_is_relative'))
@pytest.mark.parametrize('content_path_is_relative', (False, True), ids=('content_path_is_absolute', 'content_path_is_relative'))
def test_get_relative_path(file_path, content_path, exp_result,
                           file_path_is_relative, content_path_is_relative,
                           tmp_path, mocker):

    def write(path):
        path = pathlib.Path(path.format(tmp_path=str(tmp_path)))
        try:
            path.relative_to(tmp_path)
        except ValueError:
            print(':::  not creating:', path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix:
                print(':::  creating file:', path)
                path.write_bytes(b'content data')
            else:
                print(':::  creating directory:', path)
                path.mkdir(exist_ok=True)
        return path

    content_path = write(content_path)
    file_path = write(file_path)

    cwd = None
    orig_cwd = pathlib.Path(os.getcwd())
    if content_path_is_relative:
        cwd = content_path.parent.parent
        content_path = content_path.relative_to(cwd)
    if file_path_is_relative:
        if not cwd:
            cwd = file_path.parent.parent
        try:
            file_path = file_path.relative_to(cwd)
        except ValueError:
            pass

    print('___ content_path:', content_path)
    print('___ file_path:', file_path)
    print('___ cwd:', cwd)
    if cwd:
        if cwd.exists():
            os.chdir(cwd)
    try:
        tracker_jobs = make_TestTrackerJobs(
            content_path=str(content_path),
            common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
        )
        if isinstance(exp_result, Exception):
            exp_msg = type(exp_result)(str(exp_result).format(tmp_path=str(tmp_path)))
            with pytest.raises(type(exp_result), match=rf'^{exp_msg}$'):
                tracker_jobs.get_relative_file_path(str(file_path))
        else:
            relative_path = tracker_jobs.get_relative_file_path(str(file_path))
            assert relative_path == exp_result
    finally:
        if orig_cwd.exists():
            os.chdir(orig_cwd)


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
    argnames='screenshots, columns, horizontal_spacer, vertical_spacer, exp_bbcode',
    argvalues=(
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png')),
            1, ' | ', '\n-\n',
            (
                '[url=a.png][img]thumb_a.png[/img][/url]'
                '\n-\n'
                '[url=b.png][img]thumb_b.png[/img][/url]'
                '\n-\n'
                '[url=c.png][img]thumb_c.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png')),
            2, ' | ', '\n-\n',
            (
                '[url=a.png][img]thumb_a.png[/img][/url] | [url=b.png][img]thumb_b.png[/img][/url]'
                '\n-\n'
                '[url=c.png][img]thumb_c.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png')),
            3, '|', '-',
            (
                '[url=a.png][img]thumb_a.png[/img][/url]|[url=b.png][img]thumb_b.png[/img][/url]|[url=c.png][img]thumb_c.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png')),
            2, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url]'
                ':'
                '[url=c.png][img]thumb_c.png[/img][/url].[url=d.png][img]thumb_d.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png'), ImageUrl('e.png')),
            2, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url]'
                ':'
                '[url=c.png][img]thumb_c.png[/img][/url].[url=d.png][img]thumb_d.png[/img][/url]'
                ':'
                '[url=e.png][img]thumb_e.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png'), ImageUrl('e.png')),
            3, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url].[url=c.png][img]thumb_c.png[/img][/url]'
                ':'
                '[url=d.png][img]thumb_d.png[/img][/url].[url=e.png][img]thumb_e.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png'), ImageUrl('e.png'), ImageUrl('f.png')),
            2, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url]'
                ':'
                '[url=c.png][img]thumb_c.png[/img][/url].[url=d.png][img]thumb_d.png[/img][/url]'
                ':'
                '[url=e.png][img]thumb_e.png[/img][/url].[url=f.png][img]thumb_f.png[/img][/url]'
            ),
        ),
        (
            (ImageUrl('a.png'), ImageUrl('b.png'), ImageUrl('c.png'), ImageUrl('d.png'), ImageUrl('e.png'), ImageUrl('f.png')),
            3, '.', ':',
            (
                '[url=a.png][img]thumb_a.png[/img][/url].[url=b.png][img]thumb_b.png[/img][/url].[url=c.png][img]thumb_c.png[/img][/url]'
                ':'
                '[url=d.png][img]thumb_d.png[/img][/url].[url=e.png][img]thumb_e.png[/img][/url].[url=f.png][img]thumb_f.png[/img][/url]'
            ),
        ),
    ),
)
def test_make_screenshots_grid(screenshots, columns, horizontal_spacer, vertical_spacer, exp_bbcode, mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    bbcode = tracker_jobs.make_screenshots_grid(
        screenshots,
        columns=columns,
        horizontal_spacer=horizontal_spacer,
        vertical_spacer=vertical_spacer,
    )
    assert bbcode == exp_bbcode

def test_make_screenshots_grid_without_thumbnail_url(mocker):
    tracker_jobs = make_TestTrackerJobs(
        content_path='path/to/content',
        common_job_args={'home_directory': 'path/to/home', 'ignore_cache': 'mock bool'},
    )
    screenshots = (ImageUrl('a.png'), ImageUrl('b.png', thumbnail=False), ImageUrl('c.png'))
    with pytest.raises(RuntimeError, match=r'^No thumbnail for b\.png$'):
        tracker_jobs.make_screenshots_grid(screenshots)
