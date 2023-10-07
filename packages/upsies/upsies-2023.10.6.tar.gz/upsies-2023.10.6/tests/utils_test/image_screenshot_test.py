import os
import re
from unittest.mock import call

import pytest

from upsies import errors
from upsies.utils import image, video

VF_FLAGS = (
    'full_chroma_int',
    'full_chroma_inp',
    'accurate_rnd',
    'spline',
)

@pytest.mark.parametrize(
    argnames='video_file, timestamp, screenshot_file, color_matrix, exp_args',
    argvalues=(
        pytest.param(
            'video.mkv', 123, 'foo%.png', 'BT.2020',
            (
                '-y', '-hide_banner', '-loglevel', 'error',
                '-ss', '123',
                '-i', 'ffmpeg_input:video.mkv',
                '-vf', ':'.join((
                    'scale=in_h_chr_pos=0',
                    'in_v_chr_pos=0',
                    'in_color_matrix=bt2020',
                    'flags=' + '+'.join(VF_FLAGS),
                )),
                '-pix_fmt', 'rgb24', '-vframes', '1',
                'file:foo%%.png',
            ),
            id='BT.2020',
        ),
        pytest.param(
            'video.mkv', 123, 'foo%.png', 'BT.709',
            (
                '-y', '-hide_banner', '-loglevel', 'error',
                '-ss', '123',
                '-i', 'ffmpeg_input:video.mkv',
                '-vf', ':'.join((
                    "scale='max(sar,1)*iw':'max(1/sar,1)*ih'",
                    'in_h_chr_pos=0',
                    'in_v_chr_pos=128',
                    'in_color_matrix=bt709',
                    'flags=' + '+'.join(VF_FLAGS),
                )),
                '-pix_fmt', 'rgb24', '-vframes', '1',
                'file:foo%%.png',
            ),
            id='BT.709',
        ),
        pytest.param(
            'video.mkv', 123, 'foo%.png', 'BT.601',
            (
                '-y', '-hide_banner', '-loglevel', 'error',
                '-ss', '123',
                '-i', 'ffmpeg_input:video.mkv',
                '-vf', ':'.join((
                    "scale='max(sar,1)*iw':'max(1/sar,1)*ih'",
                    'in_h_chr_pos=0',
                    'in_v_chr_pos=128',
                    'in_color_matrix=bt601',
                    'flags=' + '+'.join(VF_FLAGS),
                )),
                '-pix_fmt', 'rgb24', '-vframes', '1',
                'file:foo%%.png',
            ),
            id='BT.601',
        ),
        pytest.param(
            'video.mkv', 123, 'foo%.png', 'BT.foo',
            (
                '-y', '-hide_banner', '-loglevel', 'error',
                '-ss', '123',
                '-i', 'ffmpeg_input:video.mkv',
                '-vf', ':'.join((
                    "scale='max(sar,1)*iw':'max(1/sar,1)*ih'",
                    'flags=' + '+'.join(VF_FLAGS),
                )),
                '-pix_fmt', 'rgb24', '-vframes', '1',
                'file:foo%%.png',
            ),
            id='No color matrix',
        ),
    ),
    ids=lambda v: str(v),
)
def test_make_screenshot_cmd(video_file, timestamp, screenshot_file, color_matrix, exp_args, mocker):
    mocker.patch('upsies.utils.image._ffmpeg_executable', return_value='ffmpeg.executable')
    mocker.patch('upsies.utils.video.make_ffmpeg_input', side_effect=lambda path: f'ffmpeg_input:{path}')
    mocker.patch('upsies.utils.video.is_bt601', return_value=color_matrix == 'BT.601')
    mocker.patch('upsies.utils.video.is_bt709', return_value=color_matrix == 'BT.709')
    mocker.patch('upsies.utils.video.is_bt2020', return_value=color_matrix == 'BT.2020')

    cmd = image._make_screenshot_cmd(video_file, timestamp, screenshot_file)
    assert cmd == ('ffmpeg.executable',) + exp_args


def test_nonexisting_video_file(mocker):
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable',
                                             side_effect=errors.ContentError('Foo you'))
    sanitize_path_mock = mocker.patch('upsies.utils.fs.sanitize_path', return_value='sanitized path')
    run_mock = mocker.patch('upsies.utils.subproc.run')
    mock_file = 'path/to/foo.mkv'

    with pytest.raises(errors.ScreenshotError, match=r'^Foo you$'):
        image.screenshot(mock_file, 123, 'image.png')
    assert assert_file_readable_mock.call_args_list == [call(mock_file)]
    assert sanitize_path_mock.call_args_list == []
    assert run_mock.call_args_list == []


@pytest.mark.parametrize('invalid_timestamp', ('anywhere', [1, 2, 3]))
def test_invalid_timestamp(invalid_timestamp, mocker):
    mocker.patch('upsies.utils.fs.assert_file_readable', return_value=True)
    sanitize_path_mock = mocker.patch('upsies.utils.fs.sanitize_path', return_value='sanitized path')
    run_mock = mocker.patch('upsies.utils.subproc.run')

    mock_file = 'path/to/foo.mkv'
    with pytest.raises(errors.ScreenshotError, match=rf"^Invalid timestamp: {re.escape(repr(invalid_timestamp))}$"):
        image.screenshot(mock_file, invalid_timestamp, 'image.png')
    assert sanitize_path_mock.call_args_list == []
    assert run_mock.call_args_list == []

@pytest.mark.parametrize(
    argnames='timestamp',
    argvalues=(
        '12',
        '01:24',
        '1:02:03',
        '01:02:03',
        '123:02:03',
        123,
    ),
)
def test_valid_timestamp(timestamp, mocker):
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable', return_value=True)
    sanitize_path_mock = mocker.patch('upsies.utils.fs.sanitize_path', return_value='sanitized path')
    path_exists_mock = mocker.patch('os.path.exists', side_effect=(False, True))
    duration_mock = mocker.patch('upsies.utils.video.duration', return_value=1e6)
    make_screenshot_cmd_mock = mocker.patch('upsies.utils.image._make_screenshot_cmd', return_value='mock cmd')
    run_mock = mocker.patch('upsies.utils.subproc.run')

    mock_file = 'path/to/foo.mkv'
    screenshot_path = image.screenshot(mock_file, timestamp, 'image.png')
    assert screenshot_path == 'sanitized path'
    assert assert_file_readable_mock.call_args_list == [call(mock_file)]
    assert sanitize_path_mock.call_args_list == [call('image.png')]
    assert path_exists_mock.call_args_list == [call('sanitized path'), call('sanitized path')]
    assert duration_mock.call_args_list == [call(mock_file)]
    assert make_screenshot_cmd_mock.call_args_list == [call(mock_file, timestamp, 'sanitized path')]
    assert run_mock.call_args_list == [call(
        'mock cmd',
        ignore_errors=True,
        join_stderr=True,
    )]


def test_timestamp_after_video_end(mocker):
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable', return_value=True)
    sanitize_path_mock = mocker.patch('upsies.utils.fs.sanitize_path', return_value='sanitized path')
    path_exists_mock = mocker.patch('os.path.exists', side_effect=(False, True))
    duration_mock = mocker.patch('upsies.utils.video.duration', return_value=600)
    make_screenshot_cmd_mock = mocker.patch('upsies.utils.image._make_screenshot_cmd', return_value='mock cmd')
    run_mock = mocker.patch('upsies.utils.subproc.run')

    mock_file = 'path/to/foo.mkv'
    timestamp = 601
    with pytest.raises(errors.ScreenshotError, match=r'^Timestamp is after video end \(0:10:00\): 0:10:01$'):
        image.screenshot(mock_file, timestamp, 'image.png')
    assert assert_file_readable_mock.call_args_list == [call(mock_file)]
    assert sanitize_path_mock.call_args_list == [call('image.png')]
    assert path_exists_mock.call_args_list == [call('sanitized path')]
    assert duration_mock.call_args_list == [call(mock_file)]
    assert make_screenshot_cmd_mock.call_args_list == []
    assert run_mock.call_args_list == []


def test_getting_duration_fails(mocker):
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable', return_value=True)
    sanitize_path_mock = mocker.patch('upsies.utils.fs.sanitize_path', return_value='sanitized path')
    path_exists_mock = mocker.patch('os.path.exists', side_effect=(False, True))
    duration_mock = mocker.patch('upsies.utils.video.duration', side_effect=errors.ContentError('not a video file'))
    make_screenshot_cmd_mock = mocker.patch('upsies.utils.image._make_screenshot_cmd', return_value='mock cmd')
    run_mock = mocker.patch('upsies.utils.subproc.run')

    mock_file = 'path/to/foo.mkv'
    with pytest.raises(errors.ScreenshotError, match=r'^not a video file$'):
        image.screenshot(mock_file, 123, 'image.png')
    assert assert_file_readable_mock.call_args_list == [call(mock_file)]
    assert sanitize_path_mock.call_args_list == [call('image.png')]
    assert path_exists_mock.call_args_list == [call('sanitized path')]
    assert duration_mock.call_args_list == [call(mock_file)]
    assert make_screenshot_cmd_mock.call_args_list == []
    assert run_mock.call_args_list == []


def test_existing_screenshot_file(mocker):
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable', return_value=True)
    sanitize_path_mock = mocker.patch('upsies.utils.fs.sanitize_path', return_value='sanitized path')
    path_exists_mock = mocker.patch('os.path.exists', side_effect=(True, True))
    duration_mock = mocker.patch('upsies.utils.video.duration', return_value=1e6)
    make_screenshot_cmd_mock = mocker.patch('upsies.utils.image._make_screenshot_cmd', return_value='mock cmd')
    run_mock = mocker.patch('upsies.utils.subproc.run')

    mock_file = 'path/to/foo.mkv'
    screenshot_path = image.screenshot(mock_file, '1:02:03', 'image.png')
    assert screenshot_path == 'sanitized path'
    assert assert_file_readable_mock.call_args_list == [call(mock_file)]
    assert sanitize_path_mock.call_args_list == [call('image.png')]
    assert path_exists_mock.call_args_list == [call('sanitized path')]
    assert duration_mock.call_args_list == []
    assert make_screenshot_cmd_mock.call_args_list == []
    assert run_mock.call_args_list == []


def test_overwrite_existing_screenshot_file(mocker):
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable', return_value=True)
    sanitize_path_mock = mocker.patch('upsies.utils.fs.sanitize_path', return_value='sanitized path')
    path_exists_mock = mocker.patch('os.path.exists', side_effect=(True, True))
    duration_mock = mocker.patch('upsies.utils.video.duration', return_value=1e6)
    make_screenshot_cmd_mock = mocker.patch('upsies.utils.image._make_screenshot_cmd', return_value='mock cmd')
    run_mock = mocker.patch('upsies.utils.subproc.run')

    mock_file = 'path/to/foo.mkv'
    screenshot_path = image.screenshot(mock_file, '1:02:03', 'image.png', overwrite=True)
    assert screenshot_path == 'sanitized path'
    assert assert_file_readable_mock.call_args_list == [call(mock_file)]
    assert sanitize_path_mock.call_args_list == [call('image.png')]
    assert path_exists_mock.call_args_list == [call('sanitized path')]
    assert duration_mock.call_args_list == [call(mock_file)]
    assert make_screenshot_cmd_mock.call_args_list == [call(mock_file, '1:02:03', 'sanitized path')]
    assert run_mock.call_args_list == [call(
        'mock cmd',
        ignore_errors=True,
        join_stderr=True,
    )]


def test_screenshot_file_does_not_exist_for_some_reason(mocker):
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable', return_value=True)
    sanitize_path_mock = mocker.patch('upsies.utils.fs.sanitize_path', return_value='sanitized path')
    path_exists_mock = mocker.patch('os.path.exists', side_effect=(False, False))
    duration_mock = mocker.patch('upsies.utils.video.duration', return_value=1e6)
    make_screenshot_cmd_mock = mocker.patch('upsies.utils.image._make_screenshot_cmd', return_value='mock cmd')
    run_mock = mocker.patch('upsies.utils.subproc.run', return_value='ffmpeg output')

    mock_file = 'path/to/foo.mkv'
    with pytest.raises(errors.ScreenshotError, match=r'^path/to/foo.mkv: Failed to create screenshot at 601: ffmpeg output$'):
        image.screenshot(mock_file, 601, 'image.png')
    assert assert_file_readable_mock.call_args_list == [call(mock_file)]
    assert sanitize_path_mock.call_args_list == [call('image.png')]
    assert path_exists_mock.call_args_list == [call('sanitized path'), call('sanitized path')]
    assert duration_mock.call_args_list == [call(mock_file)]
    assert make_screenshot_cmd_mock.call_args_list == [call(mock_file, 601, 'sanitized path')]
    assert run_mock.call_args_list == [call(
        'mock cmd',
        ignore_errors=True,
        join_stderr=True,
    )]


def test_screenshot_has_display_aspect_ratio(data_dir, tmp_path):
    video_file = os.path.join(data_dir, 'video', 'aspect_ratio.mkv')
    screenshot_file = str(tmp_path / 'image.jpg')
    screenshot_path = image.screenshot(video_file, 0, screenshot_file)
    assert screenshot_path == screenshot_file
    tracks = video._tracks(screenshot_file)
    width = int(tracks['Image'][0]['Width'])
    height = int(tracks['Image'][0]['Height'])
    assert 1279 <= width <= 1280
    assert height == 534
