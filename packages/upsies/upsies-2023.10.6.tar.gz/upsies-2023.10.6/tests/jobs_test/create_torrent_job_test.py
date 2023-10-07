import multiprocessing
import os
import re
import time
from unittest.mock import AsyncMock, Mock, call, patch

import pytest

from upsies import errors
from upsies.jobs.torrent import CreateTorrentJob, _torrent_process
from upsies.utils import torrent
from upsies.utils.daemon import MsgType


@pytest.fixture
def tracker():
    tracker = Mock()
    tracker.configure_mock(
        name='AsdF',
        options={
            'source': 'AsdF',
            'randomize_infohash': 'maybe randomize infohash',
            'exclude': ('a', 'b'),
        },
        login=AsyncMock(),
        get_announce_url=AsyncMock(),
        logout=AsyncMock(),
        calculate_piece_size_=Mock(name='calculate_piece_size'),
        calculate_piece_size_min_max=Mock(name='calculate_piece_size_min_max'),
    )
    return tracker


def make_CreateTorrentProgress(**kwargs):
    kw = {
        'bytes_per_second': 'mock bytes_per_second',
        'filepath': 'mock filepath',
        'percent_done': 'mock percent_done',
        'piece_size': 'mock piece_size',
        'pieces_done': 'mock pieces_done',
        'pieces_total': 'mock pieces_total',
        'seconds_elapsed': 'mock seconds_elapsed',
        'seconds_remaining': 'mock seconds_remaining',
        'seconds_total': 'mock seconds_total',
        'time_finished': 'mock time_finished',
        'time_started': 'mock time_started',
        'total_size': 'mock total_size',
    }
    kw.update(kwargs)
    return torrent.CreateTorrentProgress(**kw)

def make_FindTorrentProgress(**kwargs):
    kw = {
        'exception': 'mock exception',
        'filepath': 'mock filepath',
        'files_done': 'mock files_done',
        'files_per_second': 'mock files_per_second',
        'files_total': 'mock files_total',
        'percent_done': 'mock percent_done',
        'seconds_elapsed': 'mock seconds_elapsed',
        'seconds_remaining': 'mock seconds_remaining',
        'seconds_total': 'mock seconds_total',
        'status': 'mock status',
        'time_finished': 'mock time_finished',
        'time_started': 'mock time_started',
    }
    kw.update(kwargs)
    return torrent.FindTorrentProgress(**kw)


def test_CreateTorrentJob_cache_id(tmp_path, tracker):
    job = CreateTorrentJob(
        home_directory=tmp_path,
        cache_directory=tmp_path,
        ignore_cache=False,
        content_path='path/to/foo',
        tracker=tracker,
    )
    assert job.cache_id is None


def test_CreateTorrentJob_initialize(tracker, tmp_path):
    job = CreateTorrentJob(
        home_directory=tmp_path,
        cache_directory=tmp_path,
        ignore_cache=False,
        content_path='path/to/foo',
        reuse_torrent_path='path/to/existing.torrent',
        tracker=tracker,
    )
    assert job._content_path == 'path/to/foo'
    assert job._torrent_path == f'{tmp_path / "foo"}.asdf.torrent'
    assert job._exclude_files == list(tracker.options['exclude'])
    assert job._reuse_torrent_path == 'path/to/existing.torrent'
    assert job.info == ''
    assert job._torrent_process is None


@pytest.mark.parametrize(
    argnames='exclude_defaults, exclude_files, exp_exclude_files',
    argvalues=(
        (
            [r'.*\.txt$'],
            ['*.jpg'],
            [r'.*\.txt$', '*.jpg'],
        ),
    ),
    ids=lambda v: repr(v),
)
def test_CreateTorrentJob_initialize_with_exclude_files(exclude_defaults, exclude_files, exp_exclude_files,
                                                        tracker, tmp_path, mocker):
    mocker.patch.dict(tracker.options, {'exclude': exclude_defaults})
    job = CreateTorrentJob(
        home_directory=tmp_path,
        cache_directory=tmp_path,
        ignore_cache=False,
        content_path='path/to/foo',
        tracker=tracker,
        exclude_files=exclude_files,
    )
    assert job._exclude_files == list(exp_exclude_files)


@pytest.fixture
def job(tmp_path, tracker):
    return CreateTorrentJob(
        home_directory=tmp_path,
        cache_directory=tmp_path,
        ignore_cache=False,
        content_path='path/to/foo',
        reuse_torrent_path='path/to/existing.torrent',
        tracker=tracker,
    )


@pytest.mark.asyncio
async def test_CreateTorrentJob_activity_property(job, mocker):
    mock_activity = Mock()
    mocker.patch.object(job, '_activity', mock_activity)
    assert job.activity is mock_activity


@pytest.mark.asyncio
async def test_CreateTorrentJob_execute(job, mocker):
    mocker.patch.object(job, '_get_announce_url', AsyncMock())
    mocker.patch.object(job, '_handle_torrent_created', Mock())
    mocker.patch.object(job, '_start_torrent_creation_process', Mock())

    job.execute()
    await job._get_announce_url_task

    assert job._get_announce_url.call_args_list == [call()]
    assert job._handle_torrent_created.call_args_list == []
    assert job._start_torrent_creation_process.call_args_list == [call(job._get_announce_url.return_value)]
    assert not job.is_finished


@pytest.mark.asyncio
async def test_CreateTorrentJob_get_announce_url(job, mocker):
    mocks = AsyncMock(
        get_announce_url=AsyncMock(return_value='http://announce.url'),
        announce_url_callback=Mock(),
    )
    mocker.patch.object(job._tracker, 'get_announce_url', mocks.get_announce_url)

    def check_activity(*args, **kwargs):
        assert job.activity == 'announce_url'

    mocks.announce_url_callback.side_effect = check_activity
    job.signal.register('announce_url', mocks.announce_url_callback)

    assert job.activity == ''
    announce_url = await job._get_announce_url()
    assert announce_url == mocks.get_announce_url.return_value
    assert mocks.mock_calls == [
        call.announce_url_callback(Ellipsis),
        call.get_announce_url(),
        call.announce_url_callback('http://announce.url'),
    ]
    assert job.activity == ''

@pytest.mark.asyncio
async def test_CreateTorrentJob_get_announce_url_catches_RequestError_from_get_announce_url(job, mocker):
    mocks = AsyncMock(
        get_announce_url=AsyncMock(side_effect=errors.RequestError('no url found')),
        announce_url_callback=Mock(),
    )
    mocker.patch.object(job._tracker, 'get_announce_url', mocks.get_announce_url)
    job.signal.register('announce_url', mocks.announce_url_callback)

    assert job.activity == ''
    announce_url = await job._get_announce_url()
    assert announce_url is None
    assert mocks.mock_calls == [
        call.announce_url_callback(Ellipsis),
        call.get_announce_url(),
    ]
    assert job.errors == (errors.RequestError('no url found'),)
    assert job.is_finished
    assert job.activity == ''


def test_CreateTorrentJob_start_torrent_creation_process(job, mocker):
    DaemonProcess_mock = mocker.patch('upsies.utils.daemon.DaemonProcess', Mock(
        return_value=Mock(join=AsyncMock()),
    ))
    announce_url = 'http:/foo/announce'
    job._start_torrent_creation_process(announce_url)
    assert DaemonProcess_mock.call_args_list == [call(
        name=job.name,
        target=_torrent_process,
        kwargs={
            'content_path': 'path/to/foo',
            'announce': announce_url,
            'source': job._tracker.options['source'],
            'torrent_path': os.path.join(
                job.home_directory,
                f'foo.{job._tracker.options["source"].lower()}.torrent',
            ),
            'exclude': job._exclude_files,
            'use_cache': not job.ignore_cache,
            'reuse_torrent_path': job._reuse_torrent_path,
            'randomize_infohash': job._tracker.options['randomize_infohash'],
            'piece_size_calculator': job._tracker.calculate_piece_size,
            'piece_size_min_max_calculator': job._tracker.calculate_piece_size_min_max,
        },
        init_callback=job._handle_files,
        info_callback=job._handle_info_update,
        error_callback=job._handle_error,
        result_callback=job._handle_torrent_created,
        finished_callback=job.finish,
    )]
    assert job._torrent_process.start.call_args_list == [call()]


@pytest.mark.parametrize('torrent_process', (None, Mock()))
def test_CreateTorrentJob_finish(torrent_process, job):
    job._torrent_process = torrent_process
    assert not job.is_finished
    job.finish()
    assert job.is_finished
    if torrent_process:
        assert job._torrent_process.stop.call_args_list == [call()]
    else:
        assert job._torrent_process is None


@pytest.mark.parametrize('activity', ('', 'searching', 'hashing'))
@pytest.mark.parametrize('torrent_process', (None, 'mock torrent_process'), ids=lambda v: repr(v))
def test_CreateTorrentJob_cancel_search(torrent_process, activity, job, mocker):
    mocker.patch.object(job, '_torrent_process', (Mock() if torrent_process else None))
    mocker.patch.object(job, '_activity', activity)
    job.cancel_search()
    if activity == 'searching' and torrent_process:
        assert job._torrent_process.send.call_args_list == [call(MsgType.terminate, torrent.SKIP_SEARCHING)]
    elif torrent_process:
        assert job._torrent_process.send.call_args_list == []


def test_CreateTorrentJob_handle_files(job, mocker):
    mocks = Mock()
    job.signal.register('file_tree', mocks.tree)
    job.signal.register('file_list', mocks.list)
    mock_files = Mock(tree='mock tree', list='mock list')
    job._handle_files(mock_files)
    assert mocks.mock_calls == [
        call.tree('mock tree'),
        call.list('mock list'),
    ]


@pytest.mark.parametrize(
    argnames='progress, exp_exception, exp_activity',
    argvalues=(
        (make_CreateTorrentProgress(), None, 'hashing'),
        (make_FindTorrentProgress(status='verifying'), None, 'verifying'),
        (make_FindTorrentProgress(status='hit'), None, ''),
        (make_FindTorrentProgress(status='<anything else>'), None, 'searching'),
        (
            'invalid progress object',
            RuntimeError('Unexpected info update: {info!r}'),
            '',
        ),
    ),
    ids=lambda v: type(v).__name__,
)
def test_CreateTorrentJob_handle_info_update(progress, exp_exception, exp_activity, job, mocker):
    mocker.patch.object(job.signal, 'emit')
    assert job.activity == ''
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            job._handle_info_update(progress)
        assert job.signal.emit.call_args_list == []
    else:
        job._handle_info_update(progress)
        assert job.signal.emit.call_args_list == [call('progress_update', progress)]
    assert job.activity == exp_activity


@pytest.mark.parametrize(
    argnames='torrent_path, exp_output',
    argvalues=(
        (None, ()),
        ('', ()),
        ('foo/bar.torrent', ('foo/bar.torrent',),),
    ),
)
def test_CreateTorrentJob_handle_torrent_created(torrent_path, exp_output, job):
    assert job.output == ()
    job._handle_torrent_created(torrent_path)
    assert job.output == exp_output


def test_CreateTorrentJob_handle_error(job, mocker):
    mocker.patch.object(job, 'exception')
    mocker.patch.object(job, 'error')
    job._handle_error('message')
    assert job.error.call_args_list == [call('message')]
    job._handle_error(errors.RequestError('message'))
    assert job.exception.call_args_list == [call(errors.RequestError('message'))]


class Callable:
    def __eq__(self, other):
        return callable(other)


@pytest.fixture
def queues():
    queues = Mock(
        output=multiprocessing.Queue(),
        input=multiprocessing.Queue(),
    )
    yield queues
    # Prevent BrokenPipeError tracebacks on stderr
    # https://bugs.python.org/issue35844
    time.sleep(0.1)
    queues.output.cancel_join_thread()
    queues.input.cancel_join_thread()


@patch('upsies.utils.torrent.create')
def test_torrent_process_creates_torrent(create_mock, queues):
    create_mock.return_value = 'path/to/foo.mkv.torrent'
    _torrent_process(queues.output, queues.input, some='argument', another='one')
    assert queues.output.get() == (MsgType.result, 'path/to/foo.mkv.torrent')
    assert queues.output.empty()
    assert queues.input.empty()
    assert create_mock.call_args_list == [call(
        some='argument',
        another='one',
        init_callback=Callable(),
        progress_callback=Callable(),
    )]


@patch('upsies.utils.torrent.create')
def test_torrent_process_catches_TorrentCreateError(create_mock, queues):
    create_mock.side_effect = errors.TorrentCreateError('Argh')
    _torrent_process(queues.output, queues.input, some='argument')
    assert queues.output.get() == (MsgType.error, 'Argh')
    assert queues.output.empty()
    assert queues.input.empty()


def test_torrent_process_initializes_with_file_tree(mocker, queues):
    def create_mock(init_callback, **kwargs):
        init_callback('this is not a file tree')

    mocker.patch('upsies.utils.torrent.create', create_mock)
    _torrent_process(queues.output, queues.input, some='argument')
    assert queues.output.get() == (MsgType.init, 'this is not a file tree')


def test_torrent_process_sends_progress(mocker, queues):
    def create_mock(progress_callback, **kwargs):
        for progress in (10, 50, 100):
            progress_callback(progress)

    mocker.patch('upsies.utils.torrent.create', create_mock)
    _torrent_process(queues.output, queues.input, some='argument')
    assert queues.output.get() == (MsgType.info, 10)
    assert queues.output.get() == (MsgType.info, 50)
    assert queues.output.get() == (MsgType.info, 100)


@pytest.mark.parametrize(
    argnames='callback_name, callback_args, msgs, exp_output',
    argvalues=(
        pytest.param(
            'init_callback',
            [
                'mock file tree 1',
                'mock file tree 2',
                'mock file tree 3',
            ],
            [
                (None, None),
                (MsgType.terminate, 'ignored'),
                (None, None),
            ],
            [
                (MsgType.init, 'mock file tree 1'),
                (MsgType.result, 'cb returned: cancel'),
            ],
            id='init_callback provides file_tree and cancels',
        ),

        pytest.param(
            'progress_callback',
            [
                make_CreateTorrentProgress(percent_done=12),
                make_CreateTorrentProgress(percent_done=75),
                make_CreateTorrentProgress(percent_done=100),
            ],
            [
                (None, None),
                (None, None),
                (None, None),
            ],
            [
                (MsgType.info, make_CreateTorrentProgress(percent_done=12)),
                (MsgType.info, make_CreateTorrentProgress(percent_done=75)),
                (MsgType.info, make_CreateTorrentProgress(percent_done=100)),
                (MsgType.result, 'mock/path/to.torrent'),
            ],
            id='progress_callback gets CreateTorrentProgress until torrent is finished',
        ),

        pytest.param(
            'progress_callback',
            [
                make_CreateTorrentProgress(percent_done=12),
                make_CreateTorrentProgress(percent_done=75),
                make_CreateTorrentProgress(percent_done=100),
            ],
            [
                (None, None),
                (MsgType.terminate, None),
                (None, None),
            ],
            [
                (MsgType.info, make_CreateTorrentProgress(percent_done=12)),
                (MsgType.result, 'cb returned: cancel'),
            ],
            id='progress_callback gets CreateTorrentProgress and cancels torrent creation',
        ),

        pytest.param(
            'progress_callback',
            [
                make_CreateTorrentProgress(percent_done=12),
                make_CreateTorrentProgress(percent_done=75),
                make_CreateTorrentProgress(percent_done=100),
            ],
            [
                (None, None),
                (MsgType.terminate, torrent.SKIP_SEARCHING),
                (None, None),
            ],
            [
                (MsgType.info, make_CreateTorrentProgress(percent_done=12)),
                (MsgType.result, 'cb returned: cancel'),
            ],
            id='progress_callback gets CreateTorrentProgress and tries to skip searching',
        ),

        pytest.param(
            'progress_callback',
            [
                make_FindTorrentProgress(percent_done=12, status=False),
                make_FindTorrentProgress(percent_done=15, status=None),
                make_FindTorrentProgress(percent_done=100, status='never reached'),
            ],
            [
                (None, None),
                (None, None),
                (MsgType.terminate, torrent.SKIP_SEARCHING),
                (None, None),
            ],
            [
                (MsgType.info, make_FindTorrentProgress(percent_done=12, status=False)),
                (MsgType.info, make_FindTorrentProgress(percent_done=15, status=None)),
                (MsgType.result, f'cb returned: {torrent.SKIP_SEARCHING}'),
            ],
            id='progress_callback gets FindTorrentProgress and skips searching',
        ),
    ),
)
def test_torrent_process(callback_name, callback_args, msgs, exp_output, queues, mocker):
    def create_mock(**kwargs):
        callback = kwargs[callback_name]
        for typ, msg in msgs:
            print('### Sending', (typ, msg))
            queues.input.put((typ, msg))
            time.sleep(0.1)

            callback_return_value = callback(callback_args.pop(0))
            print('###', callback_name, 'returned', repr(callback_return_value))
            if callback_return_value:
                return f'cb returned: {callback_return_value}'

        return 'mock/path/to.torrent'

    mocker.patch('upsies.utils.torrent.create', create_mock)
    _torrent_process(queues.output, queues.input, some='argument')

    output = []
    print('### OUTPUT:')
    while True:
        try:
            output.append(queues.output.get(timeout=0.3))
            print('###', output[-1])
        except multiprocessing.queues.Empty:
            break

    assert output == exp_output
