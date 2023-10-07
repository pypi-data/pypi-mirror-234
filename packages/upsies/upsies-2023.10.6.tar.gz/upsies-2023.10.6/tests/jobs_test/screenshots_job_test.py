import itertools
import queue
import re
from unittest.mock import DEFAULT, AsyncMock, Mock, PropertyMock, call

import pytest

from upsies import errors
from upsies.jobs import screenshots
from upsies.utils.daemon import MsgType


@pytest.fixture
def job(tmp_path, mocker):
    DaemonProcess_mock = Mock(
        return_value=Mock(
            join=AsyncMock(),
        ),
    )
    mocker.patch('upsies.utils.daemon.DaemonProcess', DaemonProcess_mock)
    return screenshots.ScreenshotsJob(
        home_directory=tmp_path,
        cache_directory=tmp_path,
        ignore_cache=False,
        content_path='some/path',
        exclude_files=('exclude', 'these', 'files'),
        timestamps=(120,),
        count=2,
    )


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_cache_id(tmp_path):
    job = screenshots.ScreenshotsJob(
        home_directory=tmp_path,
        cache_directory=tmp_path,
        content_path='some/path',
    )
    assert job.cache_id is None


@pytest.mark.parametrize('from_all_videos', (True, False), ids=['from all videos', 'from first video'])
@pytest.mark.parametrize('optimize', (True, False), ids=['optimize', 'no optimize'])
def test_ScreenshotsJob_initialize(from_all_videos, optimize, tmp_path):
    job = screenshots.ScreenshotsJob(
        home_directory=tmp_path,
        cache_directory=tmp_path,
        ignore_cache=False,
        content_path='some/path',
        exclude_files=['foo', 'bar', 'baz'],
        timestamps=(120,),
        count=2,
        from_all_videos=from_all_videos,
        optimize=optimize,
    )
    assert job._content_path == 'some/path'
    assert job._exclude_files == ['foo', 'bar', 'baz']
    assert job._screenshots_created == 0
    assert job._screenshots_total == -1
    assert job._timestamps == (120,)
    assert job._count == 2
    assert job._from_all_videos is from_all_videos
    assert job._optimize is optimize
    assert job._screenshots_process is None
    assert job._optimize_process is None
    assert 'screenshots_total' in job.signal.signals

    assert job.output == ()
    assert job.errors == ()
    assert not job.is_finished
    assert job.exit_code is None


@pytest.mark.parametrize(
    argnames='optimize, exp_calls',
    argvalues=(
        (None, [call._execute_screenshots_process()]),
        ('none', [call._execute_screenshots_process()]),
        (0, [call._execute_screenshots_process(), call._execute_optimize_process()]),
        (1, [call._execute_screenshots_process(), call._execute_optimize_process()]),
        ('0', [call._execute_screenshots_process(), call._execute_optimize_process()]),
        ('1', [call._execute_screenshots_process(), call._execute_optimize_process()]),
    ),
    ids=lambda v: repr(v),
)
def test_ScreenshotsJob_execute(optimize, exp_calls, job, mocker):
    mocks = Mock()
    mocker.patch.object(type(job), '_optimize', PropertyMock(return_value=optimize), create=True)
    mocks.attach_mock(
        mocker.patch.object(job, '_execute_screenshots_process'),
        '_execute_screenshots_process',
    )
    mocks.attach_mock(
        mocker.patch.object(job, '_execute_optimize_process'),
        '_execute_optimize_process',
    )

    job.execute()

    assert mocks.mock_calls == exp_calls


def test_ScreenshotsJob__execute_screenshots_process(job, mocker):
    DaemonProcess_mock = mocker.patch('upsies.utils.daemon.DaemonProcess')
    job._execute_screenshots_process()
    assert job._screenshots_process is DaemonProcess_mock.return_value
    assert DaemonProcess_mock.call_args_list == [call(
        name='_screenshots_process',
        target=screenshots._screenshots_process,
        kwargs={
            'content_path': job._content_path,
            'exclude_files': job._exclude_files,
            'timestamps': job._timestamps,
            'count': job._count,
            'from_all_videos': job._from_all_videos,
            'output_dir': job.home_directory,
            'overwrite': job.ignore_cache,
        },
        info_callback=job._handle_info,
        error_callback=job._handle_error,
    )]
    assert job._screenshots_process.start.call_args_list == [call()]


@pytest.mark.parametrize(
    argnames='optimize, exp_ignore_dependency_error',
    argvalues=(
        ('default', True),
        ('custom', False),
    ),
    ids=lambda v: repr(v),
)
def test_ScreenshotsJob__execute_optimize_process(optimize, exp_ignore_dependency_error, job, mocker):
    mocker.patch.object(job, '_optimize', optimize)
    DaemonProcess_mock = mocker.patch('upsies.utils.daemon.DaemonProcess')
    job._execute_optimize_process()
    assert job._optimize_process is DaemonProcess_mock.return_value
    assert DaemonProcess_mock.call_args_list == [call(
        name='_optimize_process',
        target=screenshots._optimize_process,
        kwargs={
            'level': job._optimize,
            'ignore_dependency_error': exp_ignore_dependency_error,
        },
        info_callback=job._handle_info,
        error_callback=job._handle_error,
    )]
    assert job._optimize_process.start.call_args_list == [call()]


@pytest.mark.parametrize('is_finished', (False, True))
@pytest.mark.parametrize('all_screenshots_created', (False, True))
@pytest.mark.parametrize(
    argnames='optimize, info, exp_attributes, exp_calls',
    argvalues=(
        (
            False,
            {'screenshots_total': 12},
            {
                '_screenshots_total': 12,
            },
            [
                call.emit('screenshots_total', 12),
            ],
        ),
        (
            False,
            {'screenshot_path': 'path/to/screenshot.png', 'video_path': 'path/to/video.mkv'},
            {
                '_screenshots_by_file': {'path/to/video.mkv': ['path/to/screenshot.png']},
                '_screenshots_created': 1,
            },
            [
                call.job_send('path/to/screenshot.png'),
            ],
        ),
        (
            True,
            {'screenshot_path': 'path/to/screenshot.png', 'video_path': 'path/to/video.mkv'},
            {
                '_screenshots_by_file': {'path/to/video.mkv': ['path/to/screenshot.png']},
                '_screenshots_created': 0,
            },
            [
                call.optimize_process_send(MsgType.info, 'path/to/screenshot.png'),
            ],
        ),
        (
            True,
            {'optimized_screenshot_path': 'path/to/screenshot.png'},
            {
                '_screenshots_by_file': {},
                '_screenshots_created': 1,
            },
            [
                call.job_send('path/to/screenshot.png'),
            ],
        ),
    ),
    ids=lambda v: repr(v),
)
def test_ScreenshotsJob__handle_info(is_finished,
                                     optimize, info, exp_attributes, exp_calls,
                                     all_screenshots_created,
                                     job, mocker):
    mocker.patch('upsies.utils.fs.file_size', return_value=123)
    mocks = Mock()
    mocker.patch.object(type(job), 'is_finished', PropertyMock(return_value=is_finished))
    if optimize:
        mocks.attach_mock(mocker.patch.object(job, '_optimize_process').send, 'optimize_process_send')
    else:
        mocker.patch.object(job, '_optimize_process', None)
    mocks.attach_mock(mocker.patch.object(job, 'send'), 'job_send')
    mocks.attach_mock(mocker.patch.object(job.signal, 'emit'), 'emit')
    mocks.attach_mock(mocker.patch.object(job, 'finish'), 'finish')

    if all_screenshots_created:
        mocker.patch.object(type(job), 'screenshots_created', PropertyMock(return_value=123))
        mocker.patch.object(type(job), 'screenshots_total', PropertyMock(return_value=123))
        exp_calls.append(call.finish())

    job._handle_info(info)

    if is_finished:
        assert mocks.mock_calls == []

    else:
        assert mocks.mock_calls == exp_calls
        for attr, exp_value in exp_attributes.items():
            assert getattr(job, attr) == exp_value


def test_ScreenshotsJob_handle_error_with_exception(job):
    assert job.raised is None
    assert job.errors == ()
    job._handle_error(errors.ScreenshotError('Foo!'))
    assert job.raised == errors.ScreenshotError('Foo!')
    assert job.errors == ()
    assert job.is_finished

def test_ScreenshotsJob_handle_error_with_string(job):
    assert job.errors == ()
    job._handle_error('Foo!')
    assert job.errors == ('Foo!',)
    assert job.is_finished


@pytest.mark.parametrize(
    argnames='screenshots_process, exp_screenshots_process_stopped',
    argvalues=(
        (None, False),
        (Mock(name='screenshots_process'), True),
    ),
)
@pytest.mark.parametrize(
    argnames='optimize_process, exp_optimize_process_stopped',
    argvalues=(
        (None, False),
        (Mock(name='optimize_process'), True),
    ),
)
def test_ScreenshotsJob_finish(screenshots_process, exp_screenshots_process_stopped,
                               optimize_process, exp_optimize_process_stopped,
                               job, mocker):
    job.execute()

    mocker.patch.object(job, '_screenshots_process', screenshots_process)
    mocker.patch.object(job, '_optimize_process', optimize_process)
    mocks = Mock()
    if job._screenshots_process:
        mocks.attach_mock(job._screenshots_process.stop, '_screenshots_process_stop')
    if job._optimize_process:
        mocks.attach_mock(job._optimize_process.stop, '_optimize_process_stop')

    job.finish()

    exp_mock_calls = []
    if exp_screenshots_process_stopped:
        exp_mock_calls.append(call._screenshots_process_stop())
    if exp_optimize_process_stopped:
        exp_mock_calls.append(call._optimize_process_stop())
    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize(
    argnames=('screenshots_total', 'output', 'exp_exit_code'),
    argvalues=(
        (-1, ('a.jpg', 'b.jpg', 'c.jpg'), 0),
        (-1, (), 1),
        (0, (), 0),
        (1, (), 1),
        (3, (), 1),
        (3, ('a.jpg',), 1),
        (3, ('a.jpg', 'b.jpg'), 1),
        (3, ('a.jpg', 'b.jpg', 'c.jpg'), 0),
    ),
)
@pytest.mark.asyncio
async def test_exit_code(screenshots_total, output, exp_exit_code, job):
    assert job.exit_code is None
    for o in output:
        job.send(o)
    job._screenshots_total = screenshots_total
    job.finish()
    await job.wait()
    assert job.is_finished
    assert job.exit_code == exp_exit_code


def test_content_path(job, mocker):
    mock_content_path = Mock()
    job.content_path = mock_content_path
    assert job.content_path is mock_content_path

    mocker.patch.object(type(job), 'is_started', PropertyMock(return_value=True))
    with pytest.raises(RuntimeError, match=r'^Cannot set content_path after job has been started$'):
        job.content_path = Mock()
    assert job.content_path is mock_content_path


def test_exclude_files(job, mocker):
    mock_exclude_files = Mock()
    job.exclude_files = mock_exclude_files
    assert job.exclude_files is mock_exclude_files

    mocker.patch.object(type(job), 'is_started', PropertyMock(return_value=True))
    with pytest.raises(RuntimeError, match=r'^Cannot set exclude_files after job has been started$'):
        job.exclude_files = Mock()
    assert job.exclude_files is mock_exclude_files


def test_from_all_videos(job, mocker):
    mock_from_all_videos = Mock()
    job.from_all_videos = mock_from_all_videos
    assert job.from_all_videos is mock_from_all_videos

    mocker.patch.object(type(job), 'is_started', PropertyMock(return_value=True))
    with pytest.raises(RuntimeError, match=r'^Cannot set from_all_videos after job has been started$'):
        job.from_all_videos = Mock()
    assert job.from_all_videos is mock_from_all_videos


def test_count(job, mocker):
    mock_count = Mock()
    job.count = mock_count
    assert job.count is mock_count

    mocker.patch.object(type(job), 'is_started', PropertyMock(return_value=True))
    with pytest.raises(RuntimeError, match=r'^Cannot set count after job has been started$'):
        job.count = Mock()
    assert job.count is mock_count


def test_timestamps(job, mocker):
    mock_timestamps = Mock()
    job.timestamps = mock_timestamps
    assert job.timestamps is mock_timestamps

    mocker.patch.object(type(job), 'is_started', PropertyMock(return_value=True))
    with pytest.raises(RuntimeError, match=r'^Cannot set timestamps after job has been started$'):
        job.timestamps = Mock()
    assert job.timestamps is mock_timestamps


def test_screenshots_total(job):
    assert job.screenshots_total is job._screenshots_total


def test_screenshots_created(job):
    assert job.screenshots_created is job._screenshots_created


def test_screenshots_by_file(job):
    job._screenshots_by_file = {
        'path/to/foo.mkv': ['screenshot1', 'screenshot2'],
    }

    screenshots_by_file = job.screenshots_by_file
    assert screenshots_by_file == {
        'path/to/foo.mkv': ('screenshot1', 'screenshot2'),
    }

    screenshots_by_file['path/to/foo.mkv'] = 'screenshot4'
    assert job.screenshots_by_file == {
        'path/to/foo.mkv': ('screenshot1', 'screenshot2'),
    }

    screenshots_by_file['path/to/bar.mkv'] = 'screenshot5'
    assert job.screenshots_by_file == {
        'path/to/foo.mkv': ('screenshot1', 'screenshot2'),
    }

    del screenshots_by_file['path/to/foo.mkv']
    assert job.screenshots_by_file == {
        'path/to/foo.mkv': ('screenshot1', 'screenshot2'),
    }


@pytest.fixture
def screenshots_process_mocks(mocker):
    args = {
        'output_queue': Mock(),
        'input_queue': Mock(),
        'content_path': 'path/to/videos',
        'exclude_files': ('files', 'to', 'exclude'),
        'timestamps': ['1:00:00', '2:00:00', '3:00:00'],
        'count': 123,
        'from_all_videos': False,
        'output_dir': 'path/to/my/screenshots',
        'overwrite': 'my overwrite value',
    }
    mocks = Mock()
    mocks.attach_mock(args['output_queue'].put, 'output_queue_put')
    mocks.attach_mock(mocker.patch('upsies.jobs.screenshots._get_video_files'), '_get_video_files')
    mocks.attach_mock(mocker.patch('upsies.jobs.screenshots._map_timestamps'), '_map_timestamps')
    mocks.attach_mock(mocker.patch('upsies.jobs.screenshots._screenshot_video_files'), '_screenshot_video_files')
    return args, mocks

def test__screenshots_process__no_videos_found(screenshots_process_mocks):
    args, mocks = screenshots_process_mocks
    mocks._get_video_files.return_value = []

    return_value = screenshots._screenshots_process(
        args['output_queue'], args['input_queue'],
        content_path=args['content_path'],
        exclude_files=args['exclude_files'],
        timestamps=args['timestamps'],
        count=args['count'],
        from_all_videos=args['from_all_videos'],
        output_dir=args['output_dir'],
        overwrite=args['overwrite'],
    )
    assert return_value is None

    assert mocks.mock_calls == [
        call._get_video_files(
            args['output_queue'],
            content_path=args['content_path'],
            exclude_files=args['exclude_files'],
        ),
        call.output_queue_put((MsgType.error, 'No videos found')),
    ]

@pytest.mark.parametrize('termination_indicated', (False, True), ids=['not terminated', 'terminated'])
@pytest.mark.parametrize('from_all_videos', (False, True), ids=['from_first_video', 'from_all_videos'])
def test__screenshots_process(from_all_videos, termination_indicated, screenshots_process_mocks):
    args, mocks = screenshots_process_mocks
    args['from_all_videos'] = from_all_videos
    mocks._get_video_files.return_value = ('foo.mkv', 'bar.mp4', 'baz.web')
    mocks._map_timestamps.return_value = {
        'foo.mkv': [10, 20, 30],
        'bar.mp4': [10, 20, 29],
        'baz.web': [10, 20, 27],
    }
    if termination_indicated:
        mocks._screenshot_video_files.side_effect = SystemExit('terminated')

    return_value = screenshots._screenshots_process(
        args['output_queue'], args['input_queue'],
        content_path=args['content_path'],
        exclude_files=args['exclude_files'],
        timestamps=args['timestamps'],
        count=args['count'],
        from_all_videos=args['from_all_videos'],
        output_dir=args['output_dir'],
        overwrite=args['overwrite'],
    )
    assert return_value is None

    if from_all_videos:
        exp_video_files = ['foo.mkv', 'bar.mp4', 'baz.web']
    else:
        exp_video_files = ['foo.mkv']

    assert mocks.mock_calls == [
        call._get_video_files(
            args['output_queue'],
            content_path=args['content_path'],
            exclude_files=args['exclude_files'],
        ),
        call._map_timestamps(
            video_files=exp_video_files,
            timestamps=args['timestamps'],
            count=args['count'],
        ),
        call.output_queue_put((MsgType.info, {'screenshots_total': 9})),
        call._screenshot_video_files(
            args['output_queue'], args['input_queue'],
            timestamps_map=mocks._map_timestamps.return_value,
            output_dir=args['output_dir'],
            overwrite=args['overwrite'],
        ),
    ]


def run_optimize_process_test(msgs, exp_calls, output_queue, input_queue, ignore_dependency_error, exp_raises, mocker):
    mocks = Mock()
    mocks.attach_mock(output_queue, 'output_queue')
    mocks.attach_mock(input_queue, 'input_queue')
    mocks.attach_mock(
        mocker.patch('upsies.jobs.screenshots._read_queue_until_empty', side_effect=msgs),
        '_read_queue_until_empty',
    )

    def optimize_mock(file_path, *args, **kwargs):
        if file_path.endswith('missing_dependency'):
            raise errors.DependencyError('Missing dependency')
        elif file_path.endswith('bad'):
            raise errors.ImageOptimizeError(f'bad image: {file_path}')
        else:
            return DEFAULT

    mocks.attach_mock(
        mocker.patch('upsies.utils.image.optimize', side_effect=optimize_mock),
        'optimize',
    )

    if isinstance(exp_raises, Exception):
        with pytest.raises(type(exp_raises), match=rf'^{re.escape(str(exp_raises))}$'):
            screenshots._optimize_process(
                output_queue=output_queue,
                input_queue=input_queue,
                level='my level',
                ignore_dependency_error=ignore_dependency_error,
            )
    else:
        return_value = screenshots._optimize_process(
            output_queue=output_queue,
            input_queue=input_queue,
            level='my level',
            ignore_dependency_error=ignore_dependency_error,
        )
        assert return_value is None

def test__optimize_process_terminates_normally(mocker):
    output_queue, input_queue = Mock(), Mock()
    msgs = (
        (
            (MsgType.info, '/path/to/1.png'),
        ),
        (), (),
        (
            (MsgType.info, '/path/to/2.png'),
            (MsgType.info, '/path/to/3.bad'),
            (MsgType.info, '/path/to/4.png'),
            (MsgType.info, 'missing_dependency'),
        ),
        (), (), (), (), (),
        (
            (MsgType.info, '/path/to/5.png'),
            (MsgType.terminate, 'foo'),
            (MsgType.info, '/path/to/6.png'),
            (MsgType.info, '/path/to/7.png'),
        ),
    )
    exp_calls = [
        call._read_queue_until_empty(input_queue=input_queue),
        call.optimize('/path/to/1.png', level='my level'),
        call.output_queue.put((MsgType.info, {'optimized_screenshot_path': '/path/to/1.png'})),
        call._read_queue_until_empty(input_queue=input_queue),
        call._read_queue_until_empty(input_queue=input_queue),
        call._read_queue_until_empty(input_queue=input_queue),
        call.optimize('/path/to/2.png', level='my level'),
        call.output_queue.put((MsgType.info, {'optimized_screenshot_path': '/path/to/2.png'})),
        call._read_queue_until_empty(input_queue=input_queue),
        call.optimize('/path/to/3.bad', level='my level'),
        call.output_queue.put((MsgType.error, 'bad image: /path/to/3.bad')),
        call._read_queue_until_empty(input_queue=input_queue),
        call.optimize('/path/to/4.png', level='my level'),
        call.output_queue.put((MsgType.info, {'optimized_screenshot_path': '/path/to/4.png'})),
        call._read_queue_until_empty(input_queue=input_queue),
        call._read_queue_until_empty(input_queue=input_queue),
        call._read_queue_until_empty(input_queue=input_queue),
        call._read_queue_until_empty(input_queue=input_queue),
    ]
    ignore_dependency_error = True
    exp_raises = None
    run_optimize_process_test(msgs, exp_calls, output_queue, input_queue, ignore_dependency_error, exp_raises, mocker)

def test__optimize_process_raises_dependency_error(mocker):
    output_queue, input_queue = Mock(), Mock()
    msgs = (
        (
            (MsgType.info, '/path/to/1.png'),
            (MsgType.info, 'missing_dependency'),
            (MsgType.info, '/path/to/2.png'),
        ),
        (),
        (
            (MsgType.info, '/path/to/3.png'),
            (MsgType.terminate, 'foo'),
            (MsgType.info, '/path/to/4.png'),
        ),
    )
    exp_calls = [
        call._read_queue_until_empty(input_queue=input_queue),
        call.optimize('/path/to/1.png', level='my level'),
        call.output_queue.put((MsgType.info, {'optimized_screenshot_path': '/path/to/1.png'})),
        call._read_queue_until_empty(input_queue=input_queue),
        call.optimize('missing_dependency', level='my level'),
        call.output_queue.put((MsgType.info, {'optimized_screenshot_path': '/path/to/2.png'})),
        call._read_queue_until_empty(input_queue=input_queue),
        call.optimize('/path/to/3.bad', level='my level'),
        call.output_queue.put((MsgType.error, 'bad image: /path/to/3.bad')),
        call._read_queue_until_empty(input_queue=input_queue),
        call.optimize('/path/to/4.png', level='my level'),
        call.output_queue.put((MsgType.info, {'optimized_screenshot_path': '/path/to/4.png'})),
        call._read_queue_until_empty(input_queue=input_queue),
        call._read_queue_until_empty(input_queue=input_queue),
        call._read_queue_until_empty(input_queue=input_queue),
        call._read_queue_until_empty(input_queue=input_queue),
    ]
    ignore_dependency_error = False
    exp_raises = errors.DependencyError('Missing dependency')
    run_optimize_process_test(msgs, exp_calls, output_queue, input_queue, ignore_dependency_error, exp_raises, mocker)


@pytest.fixture
def get_video_files_mocks(mocker):
    args = {
        'output_queue': Mock(),
        'content_path': 'path/to/videos',
        'exclude_files': ('files', 'to', 'exclude'),
    }
    mocks = Mock()
    mocks.attach_mock(args['output_queue'].put, 'output_queue_put')
    mocks.attach_mock(mocker.patch('upsies.utils.torrent.filter_files'), 'filter_files')
    mocks.attach_mock(mocker.patch('upsies.utils.video.filter_main_videos'), 'filter_main_videos')
    return args, mocks

@pytest.mark.parametrize(
    argnames='content_path, exclude_files, filter_files_result, filter_main_videos_result, exp_return_value, exp_mock_calls',
    argvalues=(
        (
            'path/to/something',
            ['exclude', 'these'],
            ['foo.mkv', 'bar.mp4', 'baz.webm'],
            ['foo.mkv', 'bar.mp4'],
            ['foo.mkv', 'bar.mp4'],
            [
                call.filter_files('path/to/something', exclude=['exclude', 'these']),
                call.filter_main_videos(['foo.mkv', 'bar.mp4', 'baz.webm']),
            ],
        ),
        (
            'path/to/something',
            ['exclude', 'these'],
            errors.ContentError('Failed to filter files'),
            ['foo.mkv', 'bar.mp4'],
            [],
            [
                call.filter_files('path/to/something', exclude=['exclude', 'these']),
                call.output_queue_put((MsgType.error, 'Failed to filter files')),
            ],
        ),
        (
            'path/to/something',
            ['exclude', 'these'],
            ['foo.mkv', 'bar.mp4', 'baz.webm'],
            errors.ContentError('Failed to filter main videos'),
            [],
            [
                call.filter_files('path/to/something', exclude=['exclude', 'these']),
                call.filter_main_videos(['foo.mkv', 'bar.mp4', 'baz.webm']),
                call.output_queue_put((MsgType.error, 'Failed to filter main videos')),
            ],
        ),
    ),
)
def test__get_video_files(content_path, exclude_files,
                          filter_files_result, filter_main_videos_result,
                          exp_return_value, exp_mock_calls, get_video_files_mocks):
    args, mocks = get_video_files_mocks
    args['content_path'] = 'path/to/something'
    args['exclude_files'] = ('bad', 'files')

    if isinstance(filter_files_result, Exception):
        mocks.filter_files.side_effect = filter_files_result
    else:
        mocks.filter_files.return_value = filter_files_result

    if isinstance(filter_main_videos_result, Exception):
        mocks.filter_main_videos.side_effect = filter_main_videos_result
    else:
        mocks.filter_main_videos.return_value = filter_main_videos_result

    return_value = screenshots._get_video_files(
        args['output_queue'],
        content_path=content_path,
        exclude_files=exclude_files,
    )
    assert return_value == exp_return_value

    assert mocks.mock_calls == exp_mock_calls


def test__screenshot_video_files(mocker):
    output_queue = Mock()
    input_queue = Mock()
    timestamps_map = {
        'path/to/foo.mkv': ['1:00:00', '2:00:00', '3:00:00'],
        'path/to/bar.mkv': ['1:00:01', '2:00:01', '3:00:01'],
        'path/to/baz.mkv': ['1:00:02', '2:00:02', '3:00:02'],
    }
    output_dir = 'path/to/my/screenshots'
    overwrite = 'my overwrite value'

    mocks = Mock()
    mocks.attach_mock(mocker.patch('upsies.jobs.screenshots._maybe_terminate'), '_maybe_terminate')
    mocks.attach_mock(mocker.patch('upsies.jobs.screenshots._screenshot_video_file'), '_screenshot_video_file')

    return_value = screenshots._screenshot_video_files(
        output_queue, input_queue,
        timestamps_map=timestamps_map,
        output_dir=output_dir,
        overwrite=overwrite,
    )
    assert return_value is None

    assert list(itertools.chain.from_iterable(
        [
            call._maybe_terminate(input_queue=input_queue),
            call._screenshot_video_file(
                output_queue, input_queue,
                video_file=video_file,
                timestamp=timestamps,
                output_dir=output_dir,
                overwrite=overwrite,
            )
        ]
        for video_file, timestamps in timestamps_map.items()
    ))


def test__screenshot_video_file(mocker):
    output_queue = Mock()
    input_queue = Mock()
    video_file = 'path/to/foo.mkv'
    timestamps = ['1:00:00', '2:00:00', '3:00:00']
    output_dir = 'path/to/my/screenshots'
    overwrite = 'my overwrite value'

    mocks = Mock()
    mocks.attach_mock(mocker.patch('upsies.jobs.screenshots._maybe_terminate'), '_maybe_terminate')
    mocks.attach_mock(mocker.patch('upsies.jobs.screenshots._make_screenshot'), '_make_screenshot')

    return_value = screenshots._screenshot_video_file(
        output_queue, input_queue,
        video_file=video_file,
        timestamps=timestamps,
        output_dir=output_dir,
        overwrite=overwrite,
    )
    assert return_value is None

    assert mocks.mock_calls == list(itertools.chain.from_iterable(
        [
            call._maybe_terminate(input_queue=input_queue),
            call._make_screenshot(
                output_queue,
                video_file=video_file,
                timestamp=ts,
                output_dir=output_dir,
                overwrite=overwrite,
            )
        ]
        for ts in timestamps
    ))


@pytest.mark.parametrize(
    argnames='video_file, screenshot_result, exp_output_queue_put_calls',
    argvalues=(
        (
            'path/to/foo.mkv',
            'path/to/actual_screenshots.jpg',
            [
                call((MsgType.info, {
                    'video_path': 'path/to/foo.mkv',
                    'screenshot_path': 'path/to/actual_screenshots.jpg',
                })),
            ],
        ),
        (
            'path/to/foo.mkv',
            errors.ScreenshotError('Failed to make screenshot'),
            [
                call((MsgType.error, 'Failed to make screenshot')),
            ],
        ),
    ),
    ids=lambda v: repr(v),
)
def test__make_screenshot(video_file, screenshot_result, exp_output_queue_put_calls, mocker):
    if isinstance(screenshot_result, Exception):
        screenshot_mock = mocker.patch('upsies.utils.image.screenshot', side_effect=screenshot_result)
    else:
        screenshot_mock = mocker.patch('upsies.utils.image.screenshot', return_value=screenshot_result)

    output_queue = Mock()
    timestamp = '01:23:45'
    output_dir = 'my/screenshots'
    overwrite = 'my overwrite value'

    return_value = screenshots._make_screenshot(
        output_queue,
        video_file=video_file,
        timestamp=timestamp,
        output_dir=output_dir,
        overwrite=overwrite,
    )
    assert return_value is None

    assert screenshot_mock.call_args_list == [call(
        video_file=video_file,
        screenshot_file='my/screenshots/foo.mkv.01:23:45.png',
        timestamp=timestamp,
        overwrite=overwrite,
    )]
    assert output_queue.put.call_args_list == exp_output_queue_put_calls


def test__map_timestamps(mocker):
    video_files = [
        'path/to/foo.mkv',
        'path/to/bar.mkv',
        'path/to/baz.mkv',
    ]
    timestamps = [10, 30, '90:00']
    count = 123

    def _validate_timestamps(*args, **kwargs):
        return ', '.join(
            itertools.chain(
                (repr(arg) for arg in args),
                (f'{k}={v!r}' for k, v in kwargs.items()),
            ))

    validate_timestamps_mock = mocker.patch('upsies.jobs.screenshots._validate_timestamps',
                                            side_effect=_validate_timestamps)
    return_value = screenshots._map_timestamps(
        video_files=video_files,
        timestamps=timestamps,
        count=count,
    )
    assert return_value == {
        'path/to/foo.mkv': "video_file='path/to/foo.mkv', timestamps=[10, 30, '90:00'], count=123",
        'path/to/bar.mkv': "video_file='path/to/bar.mkv', timestamps=[10, 30, '90:00'], count=123",
        'path/to/baz.mkv': "video_file='path/to/baz.mkv', timestamps=[10, 30, '90:00'], count=123",
    }
    assert validate_timestamps_mock.call_args_list == [
        call(
            video_file=video_file,
            timestamps=timestamps,
            count=count,
        )
        for video_file in video_files
    ]


@pytest.mark.parametrize(
    argnames='duration, count, timestamps, exp_timestamps',
    argvalues=(
        # Invalid duration
        (-1, 0, [], []),
        (0, 0, [], []),
        (1, 0, [], []),
        (59, 0, [], []),
        (70, 0, [], ['0:00:30', '0:00:45']),
        # Default
        (300, 0, [], ['0:02:25', '0:03:37']),
        # Specific count
        (300, 1, [], ['0:02:25']),
        (300, 2, [], ['0:02:25', '0:03:37']),
        (300, 3, [], ['0:01:12', '0:02:25', '0:03:37']),
        (300, 4, [], ['0:01:12', '0:02:25', '0:03:37', '0:04:13']),
        # Specific timestamps
        (300, 0, [60], ['0:01:00']),
        (300, 0, [60, 60], ['0:01:00']),
        (300, 0, [60, '180'], ['0:01:00', '0:03:00']),
        (300, 0, [60, '180', '0:181'], ['0:01:00', '0:03:00', '0:03:01']),
        (300, 0, [60, '180', '002:01:181'], ['0:01:00', '0:03:00', '0:04:50']),
        (86400, 0, [60, '180', '002:01:181'], ['0:01:00', '0:03:00', '2:04:01']),
        # Specific timestamps and specific count
        (300, 3, [0], ['0:00:00', '0:02:25', '0:03:37']),
        (300, 3, [300], ['0:02:25', '0:03:37', '0:04:50']),
        (300, 3, [0, 301], ['0:00:00', '0:02:25', '0:04:50']),
        (300, 1, [60], ['0:01:00']),
        (300, 2, [60], ['0:01:00', '0:02:55']),
        (300, 3, [60], ['0:01:00', '0:02:55', '0:03:52']),
        (300, 3, [60, 180], ['0:01:00', '0:02:00', '0:03:00']),
        # Timestamps are returned sorted
        (300, 3, [60, 180, 120, 90], ['0:01:00', '0:01:30', '0:02:00', '0:03:00']),
        # Timestamps are deduplicated
        (300, 4, [60, '0:60', 90, '1:00'], ['0:01:00', '0:01:30', '0:03:10', '0:04:00']),
    ),
    ids=lambda v: repr(v),
)
def test__validate_timestamps(duration, count, timestamps, exp_timestamps, mocker):
    duration_mock = mocker.patch('upsies.utils.video.duration', return_value=duration)
    return_value = screenshots._validate_timestamps(
        video_file='foo.mkv',
        timestamps=timestamps,
        count=count,
    )
    assert return_value == exp_timestamps
    assert duration_mock.call_args_list == [call('foo.mkv')]


@pytest.mark.parametrize(
    argnames='get_nowait, exp_exception',
    argvalues=(
        (
            Mock(side_effect=queue.Empty()),
            None,
        ),
        (
            Mock(return_value=(MsgType.info, 'for your consideration')),
            None,
        ),
        (
            Mock(return_value=(MsgType.terminate, 'please stop')),
            SystemExit('Terminated'),
        ),
    ),
    ids=lambda v: repr(v),
)
def test__maybe_terminate(get_nowait, exp_exception):
    input_queue = Mock(get_nowait=get_nowait)
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            screenshots._maybe_terminate(input_queue=input_queue)
    else:
        return_value = screenshots._maybe_terminate(input_queue=input_queue)
        assert return_value is None


@pytest.mark.parametrize(
    argnames='queued_items, exp_return_value',
    argvalues=(
        (
            [queue.Empty('queue is empty')],
            [],
        ),
        (
            [
                ('typ1', 'msg1'),
                ('typ2', 'msg2'),
                ('typ3', 'msg3'),
                queue.Empty('queue is empty'),
            ],
            [
                ('typ1', 'msg1'),
                ('typ2', 'msg2'),
                ('typ3', 'msg3'),
            ],
        ),
        (
            [
                ('typ1', 'msg1'),
                ('typ2', 'msg2'),
                ('typ3', 'msg3'),
                queue.Empty('queue is empty'),
                ('typ4', 'msg4'),
                ('typ5', 'msg5'),
                ('typ6', 'msg6'),
            ],
            [
                ('typ1', 'msg1'),
                ('typ2', 'msg2'),
                ('typ3', 'msg3'),
            ],
        ),
    ),
    ids=lambda v: repr(v),
)
def test__read_queue_until_empty(queued_items, exp_return_value):
    input_queue = Mock(get=Mock(side_effect=queued_items))
    return_value = screenshots._read_queue_until_empty(input_queue=input_queue)
    assert return_value == exp_return_value

    exp_get_call_count = 0
    for item in queued_items:
        exp_get_call_count += 1
        if isinstance(item, queue.Empty):
            break

    assert input_queue.get.call_args_list == [
        call(timeout=0.01)
        for _ in range(exp_get_call_count)
    ]
