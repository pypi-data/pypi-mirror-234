import os
import random
import re
from unittest.mock import Mock, call, patch

import pytest

from upsies import constants, errors
from upsies.utils import video


@pytest.fixture(autouse=True)
def clear_all_lru_caches():
    for name in dir(video):
        attr = getattr(video, name)
        if hasattr(attr, 'cache_clear'):
            print(f'Calling {name}.cache_clear()')
            attr.cache_clear()


def generate_mediainfo(complete_name, unique_id):
    return (
        'General\n'
        + (
            ''
            if unique_id is None else
            f'Unique ID                                : {unique_id}\n'
        )
        + f'Complete name                            : {complete_name}\n'
    )


def test_run_mediainfo_gets_unreadable_file(mocker):
    run_mock = mocker.patch('upsies.utils.subproc.run')
    assert_file_readable_mock = mocker.patch(
        'upsies.utils.fs.assert_file_readable',
        side_effect=errors.ContentError("Can't read this, yo"),
    )
    with pytest.raises(errors.ContentError, match=r"^Can't read this, yo$"):
        video._run_mediainfo('some/path')
    assert assert_file_readable_mock.call_args_list == [
        call('some/path'),
    ]
    assert run_mock.call_args_list == []

def test_run_mediainfo_passes_positional_args_to_mediainfo_command(mocker):
    run_mock = mocker.patch('upsies.utils.subproc.run')
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable')
    args = ('--foo', '--bar=baz')
    assert video._run_mediainfo('some/path', *args) == run_mock.return_value
    assert assert_file_readable_mock.call_args_list == [
        call('some/path'),
    ]
    assert run_mock.call_args_list == [
        call((video._mediainfo_executable, 'some/path') + args, cache=True),
    ]

def test_run_mediainfo_catches_DependencyError(mocker):
    run_mock = mocker.patch(
        'upsies.utils.subproc.run',
        side_effect=errors.DependencyError('Missing dependency: your mom'),
    )
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable')
    with pytest.raises(errors.ContentError, match=r'^Missing dependency: your mom$'):
        video._run_mediainfo('some/path')
    assert assert_file_readable_mock.call_args_list == [
        call('some/path'),
    ]
    assert run_mock.call_args_list == [
        call((video._mediainfo_executable, 'some/path'), cache=True),
    ]

def test_run_mediainfo_does_not_catch_ProcessError(mocker):
    run_mock = mocker.patch(
        'upsies.utils.subproc.run',
        side_effect=errors.ProcessError('Bogus command'),
    )
    assert_file_readable_mock = mocker.patch('upsies.utils.fs.assert_file_readable')
    with pytest.raises(errors.ProcessError, match=r'^Bogus command$'):
        video._run_mediainfo('some/path')
    assert assert_file_readable_mock.call_args_list == [
        call('some/path'),
    ]
    assert run_mock.call_args_list == [
        call((video._mediainfo_executable, 'some/path'),
             cache=True),
    ]


@pytest.mark.parametrize('has_unique_id', (True, False), ids=('unique_id_included', 'unique_id_missing'))
@pytest.mark.parametrize('file_extension', ('mkv', 'txt'))
@pytest.mark.parametrize('only_first', (True, False))
def test_mediainfo_for_file_ignoring_extension(file_extension, only_first, has_unique_id, tmp_path, mocker):
    rel_path = f'My Content/foo.{file_extension}'
    full_path = tmp_path / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_bytes(b'my data')

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.find_videos'),
        'find_videos',
    )
    mocks.attach_mock(
        mocker.patch(
            'upsies.utils.video._run_mediainfo',
            side_effect=lambda file: generate_mediainfo(
                complete_name=file,
                unique_id='123456789 (0x1234ABCD)' if has_unique_id else None,
            )),
        '_run_mediainfo',
    )

    return_value = video.mediainfo(full_path, only_first=only_first)
    assert return_value == generate_mediainfo(
        complete_name=f'foo.{file_extension}',
        unique_id='123456789 (0x1234ABCD)' if has_unique_id else '0 (0x0)',
    )

    assert mocks.mock_calls == [
        call._run_mediainfo(full_path)
    ]

@pytest.mark.parametrize('has_unique_id', (True, False), ids=('unique_id_included', 'unique_id_missing'))
def test_mediainfo_for_first_video(has_unique_id, tmp_path, mocker):
    rel_path = 'My Content'
    full_path = tmp_path / rel_path
    full_path.mkdir(parents=True, exist_ok=True)

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.find_videos', return_value=(
            os.path.join(full_path, 'foo.mkv'),
            os.path.join(full_path, 'bar.mkv'),
            os.path.join(full_path, 'baz.mkv'),
        )),
        'find_videos',
    )
    mocks.attach_mock(
        mocker.patch(
            'upsies.utils.video._run_mediainfo',
            side_effect=lambda file: generate_mediainfo(
                complete_name=file,
                unique_id=('123456789 (0x1234ABCD)' if has_unique_id else None),
            )),
        '_run_mediainfo',
    )

    return_value = video.mediainfo(full_path, only_first=True)
    assert return_value == generate_mediainfo(
        complete_name=os.path.join(rel_path, 'foo.mkv'),
        unique_id=(
            '123456789 (0x1234ABCD)'
            if has_unique_id else
            '0 (0x0)'
        ),
    )

    assert mocks.mock_calls == [
        call.find_videos(full_path),
        call._run_mediainfo(os.path.join(full_path, 'foo.mkv')),
    ]

@pytest.mark.parametrize('has_unique_id', (True, False), ids=('unique_id_included', 'unique_id_missing'))
def test_mediainfo_for_all_videos(has_unique_id, tmp_path, mocker):
    rel_path = 'My Content'
    full_path = tmp_path / rel_path
    full_path.mkdir(parents=True, exist_ok=True)

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.find_videos', return_value=(
            os.path.join(full_path, 'foo.mkv'),
            os.path.join(full_path, 'bar.mkv'),
            os.path.join(full_path, 'baz.mkv'),
        )),
        'find_videos',
    )
    mocks.attach_mock(
        mocker.patch(
            'upsies.utils.video._run_mediainfo',
            side_effect=lambda file: generate_mediainfo(
                complete_name=file,
                unique_id='123456789 (0x1234ABCD)' if has_unique_id else None,
            )),
        '_run_mediainfo',
    )

    return_value = video.mediainfo(full_path, only_first=False)
    exp_unique_id = (
        '123456789 (0x1234ABCD)'
        if has_unique_id else
        '0 (0x0)'
    )
    assert return_value == [
        generate_mediainfo(
            complete_name=os.path.join(rel_path, 'foo.mkv'),
            unique_id=exp_unique_id,
        ),
        generate_mediainfo(
            complete_name=os.path.join(rel_path, 'bar.mkv'),
            unique_id=exp_unique_id,
        ),
        generate_mediainfo(
            complete_name=os.path.join(rel_path, 'baz.mkv'),
            unique_id=exp_unique_id,
        ),
    ]

    assert mocks.mock_calls == [
        call.find_videos(full_path),
        call._run_mediainfo(os.path.join(full_path, 'foo.mkv')),
        call._run_mediainfo(os.path.join(full_path, 'bar.mkv')),
        call._run_mediainfo(os.path.join(full_path, 'baz.mkv')),
    ]

@pytest.mark.parametrize('has_unique_id', (True, False), ids=('unique_id_included', 'unique_id_missing'))
def test_mediainfo_for_file_without_parent_directory(has_unique_id, tmp_path, mocker):
    rel_path = 'My Content/foo.mkv'
    full_path = tmp_path / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_bytes(b'my data')

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.find_videos', return_value=(
            os.path.join(full_path, 'foo.mkv'),
            os.path.join(full_path, 'bar.mkv'),
            os.path.join(full_path, 'baz.mkv'),
        )),
        'find_videos',
    )
    mocks.attach_mock(
        mocker.patch(
            'upsies.utils.video._run_mediainfo',
            side_effect=lambda file: generate_mediainfo(
                complete_name=file,
                unique_id='123456789 (0x1234ABCD)' if has_unique_id else None,
            )),
        '_run_mediainfo',
    )

    return_value = video.mediainfo('foo.mkv', only_first=True)
    assert return_value == generate_mediainfo(
        complete_name='foo.mkv',
        unique_id='123456789 (0x1234ABCD)' if has_unique_id else '0 (0x0)',
    )

    assert mocks.mock_calls == [
        call._run_mediainfo('foo.mkv')
    ]


@pytest.mark.parametrize(
    argnames='path_exists, duration, default',
    argvalues=(
        (True, 123.0, video.NO_DEFAULT_VALUE),
        (True, 123.0, 'default value'),
        (True, 123.0, None),
        (False, 123.0, video.NO_DEFAULT_VALUE),
        (False, 123.0, 'default value'),
        (False, 123.0, None),
    ),
)
def test_duration(path_exists, duration, default, mocker, tmp_path):
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.find_videos', return_value=(
            'some/path/to/foo.mkv',
            'some/path/to/bar.mkv',
            'some/path/to/baz.mkv',
        )),
        'find_videos',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video._duration', return_value=duration),
        '_duration',
    )

    path = tmp_path / 'foo.mkv'
    if path_exists:
        path.write_bytes(b'mock data')

    return_value = video.duration(path, default=default)
    if not path_exists and default is not video.NO_DEFAULT_VALUE:
        assert return_value is default
        assert mocks.mock_calls == []
    else:
        assert return_value is mocks._duration.return_value
        assert mocks.mock_calls == [
            call.find_videos(path),
            call._duration(mocks.find_videos.return_value[0]),
        ]

def test__duration_gets_duration_from_ffprobe(mocker):
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video._duration_from_ffprobe', return_value=123.0),
        '_duration_from_ffprobe',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video._duration_from_mediainfo', return_value=456.0),
        '_duration_from_mediainfo',
    )
    return_value = video._duration('some/path')
    assert return_value == mocks._duration_from_ffprobe.return_value
    assert mocks.mock_calls == [
        call._duration_from_ffprobe('some/path'),
    ]

@pytest.mark.parametrize(
    argnames='ffprobe_exception',
    argvalues=(
        RuntimeError('foo'),
        errors.DependencyError('bar'),
        errors.ProcessError('baz'),
    ),
    ids=lambda v: repr(v),
)
def test__duration_gets_duration_from_mediainfo(ffprobe_exception, mocker):
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video._duration_from_ffprobe', side_effect=ffprobe_exception),
        '_duration_from_ffprobe',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video._duration_from_mediainfo', return_value=456.0),
        '_duration_from_mediainfo',
    )
    return_value = video._duration('some/path')
    assert return_value == mocks._duration_from_mediainfo.return_value
    assert mocks.mock_calls == [
        call._duration_from_ffprobe('some/path'),
        call._duration_from_mediainfo('some/path'),
    ]


def test__duration_from_ffprobe_succeeds(mocker):
    make_ffmpeg_input_mock = mocker.patch('upsies.utils.video.make_ffmpeg_input', return_value='path/to/foo.mkv')
    run_mock = mocker.patch('upsies.utils.subproc.run', return_value=' 123.4 \n')
    assert video._duration_from_ffprobe('foo') == 123.4
    assert make_ffmpeg_input_mock.call_args_list == [call('foo')]
    assert run_mock.call_args_list == [call(
        (video._ffprobe_executable,
         '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1',
         make_ffmpeg_input_mock.return_value),
        ignore_errors=True,
    )]

def test__duration_from_ffprobe_fails(mocker):
    make_ffmpeg_input_mock = mocker.patch('upsies.utils.video.make_ffmpeg_input', return_value='path/to/foo.mkv')
    run_mock = mocker.patch('upsies.utils.subproc.run', return_value='arf!')
    exp_error = (
        'Unexpected output from '
        f"({video._ffprobe_executable!r}, "
        "'-v', 'error', '-show_entries', 'format=duration', "
        "'-of', 'default=noprint_wrappers=1:nokey=1', "
        f"{make_ffmpeg_input_mock.return_value!r}): 'arf!'"
    )
    with pytest.raises(RuntimeError, match=rf'^{re.escape(exp_error)}$'):
        video._duration_from_ffprobe('foo')
    assert make_ffmpeg_input_mock.call_args_list == [call('foo')]
    assert run_mock.call_args_list == [call(
        (video._ffprobe_executable,
         '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1',
         make_ffmpeg_input_mock.return_value),
        ignore_errors=True,
    )]


def test__duration_from_mediainfo_succeeds(mocker):
    tracks_mock = mocker.patch('upsies.utils.video._tracks', return_value={
        'General': [{'@type': 'General', 'Duration': '123.4'}],
    })
    assert video._duration_from_mediainfo('some/path') == 123.4
    assert tracks_mock.call_args_list == [call('some/path')]

@pytest.mark.parametrize(
    argnames='track',
    argvalues=(
        {'@type': 'General', 'Duration': 'foo'},
        {'@type': 'General'},
    ),
)
def test__duration_from_mediainfo_fails(track, mocker):
    tracks_mock = mocker.patch('upsies.utils.video._tracks', return_value={
        'General': [track],
    })
    with pytest.raises(RuntimeError, match=rf'^Unexpected tracks from some/path: {re.escape(str(tracks_mock.return_value))}$'):
        video._duration_from_mediainfo('some/path')
    assert tracks_mock.call_args_list == [call('some/path')]


@pytest.mark.parametrize(
    argnames='path_exists, default, found_videos_or_exception',
    argvalues=(
        (True, video.NO_DEFAULT_VALUE, ['foo.mkv', 'bar.mkv']),
        (True, video.NO_DEFAULT_VALUE, errors.ContentError('No video file found')),
        (True, 'default value', ['foo.mkv', 'bar.mkv']),
        (True, 'default value', errors.ContentError('No video file found')),
        (True, None, ['foo.mkv', 'bar.mkv']),
        (True, None, errors.ContentError('No video file found')),
        (False, video.NO_DEFAULT_VALUE, ['foo.mkv', 'bar.mkv']),
        (False, video.NO_DEFAULT_VALUE, errors.ContentError('No video file found')),
        (False, 'default value', ['foo.mkv', 'bar.mkv']),
        (False, 'default value', errors.ContentError('No video file found')),
        (False, None, ['foo.mkv', 'bar.mkv']),
        (False, None, errors.ContentError('No video file found')),
    ),
    ids=lambda v: repr(v),
)
def test_tracks(path_exists, default, found_videos_or_exception, mocker, tmp_path):
    mocks = Mock()
    if isinstance(found_videos_or_exception, Exception):
        mocks.attach_mock(
            mocker.patch('upsies.utils.video.find_videos', side_effect=found_videos_or_exception),
            'find_videos',
        )
    else:
        mocks.attach_mock(
            mocker.patch('upsies.utils.video.find_videos', return_value=found_videos_or_exception),
            'find_videos',
        )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video._tracks', return_value={'mediainfo': 'tracks'}),
        '_tracks',
    )

    path = tmp_path / 'content'
    if path_exists:
        path.mkdir(parents=True, exist_ok=True)

    return_value = video.tracks(path, default=default)
    if not path_exists and default is not video.NO_DEFAULT_VALUE:
        assert return_value is default
        assert mocks.mock_calls == []
    else:
        assert return_value is mocks._tracks.return_value
        if isinstance(found_videos_or_exception, Exception):
            assert mocks.mock_calls == [
                call.find_videos(path),
                call._tracks(path),
            ]
        else:
            assert mocks.mock_calls == [
                call.find_videos(path),
                call._tracks(found_videos_or_exception[0]),
            ]


def test__tracks_returns_expected_structure(mocker):
    run_mediainfo_mock = mocker.patch('upsies.utils.video._run_mediainfo', return_value=(
        '{"media": {"track": ['
        '{"@type": "Video", "foo": "bar"}, '
        '{"@type": "Audio", "bar": "baz"}, '
        '{"@type": "Audio", "also": "this"}]}}'
    ))
    tracks = video.tracks('foo/bar.mkv')
    assert run_mediainfo_mock.call_args_list == [call('foo/bar.mkv', '--Output=JSON')]
    assert tracks == {'Video': [{'@type': 'Video', 'foo': 'bar'}],
                      'Audio': [{'@type': 'Audio', 'bar': 'baz'},
                                {'@type': 'Audio', 'also': 'this'}]}

def test__tracks_gets_unexpected_output_from_mediainfo(mocker):
    run_mediainfo_mock = mocker.patch('upsies.utils.video._run_mediainfo', return_value=(
        'this is not JSON'
    ))
    with pytest.raises(RuntimeError, match=(r'^foo/bar.mkv: Unexpected mediainfo output: '
                                            r'this is not JSON: Expecting value: line 1 column 1 \(char 0\)$')):
        video.tracks('foo/bar.mkv')

    run_mediainfo_mock.return_value = '{"this": ["is", "unexpected", "json"]}'
    with pytest.raises(RuntimeError, match=(r'^foo/bar.mkv: Unexpected mediainfo output: '
                                            r'\{"this": \["is", "unexpected", "json"\]\}: '
                                            r"Missing field: 'media'$")):
        video.tracks('foo/bar.mkv')


@pytest.mark.parametrize(
    argnames='tracks, default, exp_return_value, exp_exception',
    argvalues=(
        ({'Video': [{'video': 'track'}], 'Audio': [{'audio': 'track'}]}, video.NO_DEFAULT_VALUE, {'video': 'track'}, None),
        ({'Video': [{'video': 'track'}], 'Audio': [{'audio': 'track'}]}, 'default value', {'video': 'track'}, None),
        ({'Video': [{'video': 'track'}], 'Audio': [{'audio': 'track'}]}, None, {'video': 'track'}, None),
        ({}, video.NO_DEFAULT_VALUE, {'video': 'track'}, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        ({}, None, None, None),
    ),
)
def test_default_track_with_default_value(tracks, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if tracks:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.tracks', return_value=tracks)

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.default_track('video', path, default=default)
        else:
            assert video.default_track('video', path, default=default) is default
    else:
        assert video.default_track('video', path, default=default) == exp_return_value

@patch('upsies.utils.video.tracks')
def test_default_track_returns_track_with_default_tag(tracks_mock):
    tracks_mock.return_value = {
        'Video': [
            {'@type': 'Video', 'Some': 'video info'},
            {'@type': 'Video', 'Default': 'No'},
            {'@type': 'Video', 'Default': 'Yes'},
            {'@type': 'Video', 'Default': 'Yes', 'But too late': ':('},
        ],
        'Audio': [
            {'@type': 'Audio', 'Some': 'audio info'},
            {'@type': 'Audio', 'Default': 'No'},
            {'@type': 'Audio', 'Default': 'Yes'},
            {'@type': 'Audio', 'Default': 'Yes', 'But too late': ':('},
        ],
    }
    assert video.default_track('video', 'foo.mkv') == tracks_mock.return_value['Video'][-2]
    assert video.default_track('audio', 'foo.mkv') == tracks_mock.return_value['Audio'][-2]

@patch('upsies.utils.video.tracks')
def test_default_track_returns_first_track_if_no_default_tag_exists(tracks_mock):
    tracks_mock.return_value = {
        'Video': [
            {'@type': 'Video', 'Some': 'video info'},
            {'@type': 'Video', 'Default': 'No'},
        ],
        'Audio': [
            {'@type': 'Audio', 'Some': 'audio info'},
            {'@type': 'Audio', 'Default': 'No'},
        ],
    }
    assert video.default_track('video', 'foo.mkv') == tracks_mock.return_value['Video'][0]
    assert video.default_track('audio', 'foo.mkv') == tracks_mock.return_value['Audio'][0]

@pytest.mark.parametrize(
    argnames='path, tracks, track_type, default, exp_result',
    argvalues=(
        (
            'foo.mkv', {'foo': 'bar'}, 'video',
            video.NO_DEFAULT_VALUE,
            errors.ContentError("{path}: No video track found: {{'foo': 'bar'}}"),
        ),
        (
            'foo.mkv', {'foo': 'bar'}, 'video',
            None,
            None,
        ),
        (
            'foo.mkv', {'foo': 'bar'}, 'video',
            'my default',
            'my default',
        ),
    ),
)
def test_default_track_fails_to_find_any_track(path, tracks, track_type, default, exp_result, mocker, tmp_path):
    path = tmp_path / path
    path.write_bytes(b'data')
    path = str(path)

    tracks = {'foo': 'bar'}
    mocker.patch('upsies.utils.video.tracks', return_value=tracks)

    if isinstance(exp_result, Exception):
        msg = str(exp_result).format(path=path)
        with pytest.raises(type(exp_result), match=rf'^{re.escape(msg)}$'):
            video.default_track(track_type, path, default=default)
    else:
        return_value = video.default_track(track_type, path, default=default)
        assert return_value == exp_result


@pytest.mark.parametrize(
    argnames='video_track, exp_width, exp_exception',
    argvalues=(
        ({'@type': 'Video', 'Width': '1920'}, 1920, None),
        ({'@type': 'Video', 'Width': '1920', 'PixelAspectRatio': '1.0'}, 1920, None),
        ({'@type': 'Video', 'Width': '704', 'PixelAspectRatio': '1.455'}, 1024, None),
        ({'@type': 'Video', 'Width': '704', 'PixelAspectRatio': '0.888'}, 704, None),
        ({'@type': 'Video', 'Width': 'nan'}, None, errors.ContentError('Unable to determine video width')),
        ({'@type': 'Video', 'Width': ()}, None, errors.ContentError('Unable to determine video width')),
        ({'@type': 'Video'}, None, errors.ContentError('Unable to determine video width')),
        ({}, None, errors.ContentError('Unable to determine video width')),
        (errors.ContentError('Permission denied'), None, errors.ContentError('Permission denied')),
    ),
    ids=lambda v: str(v),
)
def test_width(video_track, exp_width, exp_exception, mocker):
    if isinstance(video_track, Exception):
        mocker.patch('upsies.utils.video.default_track', side_effect=video_track)
    else:
        mocker.patch('upsies.utils.video.default_track', return_value=video_track)

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            video.width('foo.mkv')
    else:
        assert video.width('foo.mkv') == exp_width

@pytest.mark.parametrize(
    argnames='video_track, default, exp_return_value, exp_exception',
    argvalues=(
        ({'@type': 'Video', 'Width': '1080'}, video.NO_DEFAULT_VALUE, 1080, None),
        ({'@type': 'Video', 'Width': '1080'}, 'default value', 1080, None),
        ({'@type': 'Video', 'Width': '1080'}, None, 1080, None),
        ({}, video.NO_DEFAULT_VALUE, True, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        ({}, None, None, None),
    ),
)
def test_width_with_default_value(video_track, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if video_track:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.default_track', return_value=video_track)

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.width(path, default=default)
        else:
            assert video.width(path, default=default) is default
    else:
        assert video.width(path, default=default) == exp_return_value


@pytest.mark.parametrize(
    argnames='video_track, exp_height, exp_exception',
    argvalues=(
        ({'@type': 'Video', 'Height': '1080'}, 1080, None),
        ({'@type': 'Video', 'Height': '1080', 'PixelAspectRatio': '1.0'}, 1080, None),
        ({'@type': 'Video', 'Height': '560', 'PixelAspectRatio': '1.455'}, 560, None),
        ({'@type': 'Video', 'Height': '480', 'PixelAspectRatio': '0.888'}, 540, None),
        ({'@type': 'Video', 'Height': 'nan'}, None, errors.ContentError('Unable to determine video height')),
        ({'@type': 'Video', 'Height': ()}, None, errors.ContentError('Unable to determine video height')),
        ({'@type': 'Video'}, None, errors.ContentError('Unable to determine video height')),
        ({}, None, errors.ContentError('Unable to determine video height')),
        (errors.ContentError('Permission denied'), None, errors.ContentError('Permission denied')),
    ),
    ids=lambda v: str(v),
)
def test_height(video_track, exp_height, exp_exception, mocker):
    if isinstance(video_track, Exception):
        mocker.patch('upsies.utils.video.default_track', side_effect=video_track)
    else:
        mocker.patch('upsies.utils.video.default_track', return_value=video_track)

    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            video.height('foo.mkv')
    else:
        assert video.height('foo.mkv') == exp_height

@pytest.mark.parametrize(
    argnames='video_track, default, exp_return_value, exp_exception',
    argvalues=(
        ({'@type': 'Video', 'Height': '1080'}, video.NO_DEFAULT_VALUE, 1080, None),
        ({'@type': 'Video', 'Height': '1080'}, 'default value', 1080, None),
        ({'@type': 'Video', 'Height': '1080'}, None, 1080, None),
        ({}, video.NO_DEFAULT_VALUE, True, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        ({}, None, None, None),
    ),
)
def test_height_with_default_value(video_track, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if video_track:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.default_track', return_value=video_track)

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.height(path, default=default)
        else:
            assert video.height(path, default=default) is default
    else:
        assert video.height(path, default=default) == exp_return_value


@pytest.mark.parametrize(
    argnames='scan_type, exp_scan_type',
    argvalues=(
        (None, 'p'),
        ('', 'p'),
        ('Progressive', 'p'),
        ('Interlaced', 'i'),
        ('MBAFF', 'i'),
        ('PAFF', 'i'),
    ),
)
@pytest.mark.parametrize(
    argnames='width, height, par, exp_resolution',
    argvalues=(
        ('7680', '4320', None, 4320),
        ('3840', '2160', None, 2160),
        ('1920', '1080', None, 1080),
        ('1920', '1044', None, 1080),
        ('1918', '1040', None, 1080),
        ('1920', '804', None, 1080),
        ('1392', '1080', None, 1080),
        ('1280', '534', None, 720),
        ('768', '720', None, 720),
        ('768', '576', None, 576),
        ('768', '576', None, 576),
        ('720', '540', None, 540),
        ('704', '400', None, 480),
        ('704', '572', '1.422', 576),  # mpv output: 704x572 => 1001x572
        ('704', '560', '1.455', 576),  # mpv output: 704x560 => 1024x560
        ('704', '480', '0.888', 540),  # mpv output: 704x480 => 704x540
        ('702', '478', '0.889', 540),  # mpv output: 702x478 => 702x537
        ('720', '428', '1.422', 576),  # mpv output: 720x428 => 1024x428
        ('716', '480', '1.185', 480),  # mpv output: 716x480 => 848x480
    ),
    ids=lambda value: str(value),
)
def test_resolution_and_resolution_int(width, height, par, exp_resolution, scan_type, exp_scan_type, mocker):
    default_track_mock = mocker.patch('upsies.utils.video.default_track', return_value={
        '@type': 'Video',
        'Width': width,
        'Height': height,
        'PixelAspectRatio': par,
        'ScanType': scan_type,
    })
    # Remove any None values
    for key in tuple(default_track_mock.return_value):
        if default_track_mock.return_value[key] is None:
            del default_track_mock.return_value[key]

    if exp_resolution:
        assert video.resolution_int('foo.mkv') == exp_resolution
        assert video.resolution('foo.mkv') == f'{exp_resolution}{exp_scan_type}'
    else:
        with pytest.raises(errors.ContentError, match=r'^Unable to determine video resolution$'):
            video.resolution('foo.mkv')

@pytest.mark.parametrize(
    argnames='video_track, exp_exception',
    argvalues=(
        ({'@type': 'Video', 'Height': 'nan', 'Width': '123'},
         errors.ContentError('Unable to determine video height')),
        ({'@type': 'Video', 'Height': '123', 'Width': 'nan'},
         errors.ContentError('Unable to determine video width')),
        ({'@type': 'Video', 'Width': '123'},
         errors.ContentError('Unable to determine video height')),
        ({'@type': 'Video', 'Height': '123'},
         errors.ContentError('Unable to determine video width')),
        ({},
         errors.ContentError('Unable to determine video width')),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.parametrize('function_name', ('resolution', 'resolution_int'))
def test_resolution_and_resolution_int_detection_fails(function_name, video_track, exp_exception, mocker):
    mocker.patch('upsies.utils.video.default_track', return_value=video_track)
    function = getattr(video, function_name)
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
        function('foo.mkv')

@pytest.mark.parametrize(
    argnames='video_track, default, exp_value, exp_exception',
    argvalues=(
        ({'@type': 'Video', 'Height': '1080', 'Width': '1920'}, video.NO_DEFAULT_VALUE, 1080, None),
        ({'@type': 'Video', 'Height': '1080', 'Width': '1920'}, 'default value', 1080, None),
        ({'@type': 'Video', 'Height': '1080', 'Width': '1920'}, None, 1080, None),
        ({}, video.NO_DEFAULT_VALUE, None, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        # ({}, None, None, None),
    ),
)
@pytest.mark.parametrize(
    argnames='function_name, exp_scan_type',
    argvalues=(
        ('resolution', 'p'),
        ('resolution_int', None),
    ),
)
def test_resolution_and_resolution_int_with_default_value(
        function_name, exp_scan_type,
        video_track, default,
        exp_value, exp_exception,
        mocker, tmp_path
):
    path = tmp_path / 'foo.mkv'
    if video_track:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.default_track', return_value=video_track)
    function = getattr(video, function_name)

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                function(path, default=default)
        else:
            assert function(path, default=default) is default
    else:
        if isinstance(exp_value, int):
            exp_return_value = (
                exp_value
                if function_name == 'resolution_int' else
                f'{exp_value}{exp_scan_type}'
            )
        else:
            exp_return_value = exp_value
        assert function(path, default=default) == exp_return_value

@pytest.mark.parametrize('function_name', ('resolution', 'resolution_int'))
def test_resolution_and_resolution_int_forwards_ContentError_from_default_track(function_name, mocker):
    mocker.patch('upsies.utils.video.default_track', side_effect=errors.ContentError('Something went wrong'))
    function = getattr(video, function_name)
    with pytest.raises(errors.ContentError, match=r'^Something went wrong$'):
        function('foo.mkv')

@pytest.mark.parametrize('function_name', ('resolution', 'resolution_int'))
def test_resolution_and_resolution_int_uses_display_aspect_ratio(function_name, data_dir):
    video_file = os.path.join(data_dir, 'video', 'aspect_ratio.mkv')
    function = getattr(video, function_name)
    if function_name == 'resolution':
        assert function(video_file) == '720p'
    elif function_name == 'resolution_int':
        assert function(video_file) == 720
    else:
        raise RuntimeError(f'Unexpected function_name: {function_name}')


@pytest.mark.parametrize(
    argnames='video_track, exp_frame_rate',
    argvalues=(
        ({'FrameRate': '25.000'}, 25.0),
        ({'FrameRate': '23.976'}, 23.976),
        ({'FrameRate': 'foo'}, 0.0),
        ({}, 0.0),
    ),
    ids=lambda v: str(v),
)
def test_frame_rate(video_track, exp_frame_rate, mocker):
    mocker.patch('upsies.utils.video.default_track', return_value=video_track)
    assert video.frame_rate('foo.mkv') == exp_frame_rate

@pytest.mark.parametrize(
    argnames='video_track, default, exp_return_value, exp_exception',
    argvalues=(
        ({'FrameRate': '25.000'}, video.NO_DEFAULT_VALUE, 25.0, None),
        ({'FrameRate': '25.000'}, 'default value', 25.0, None),
        ({'FrameRate': '25.000'}, None, 25.0, None),
        ({}, video.NO_DEFAULT_VALUE, True, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        ({}, None, None, None),
    ),
)
def test_frame_rate_with_default_value(video_track, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if video_track:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.default_track', return_value=video_track)

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.frame_rate(path, default=default)
        else:
            assert video.frame_rate(path, default=default) is default
    else:
        assert video.frame_rate(path, default=default) == exp_return_value

def test_frame_rate_forwards_ContentError_from_default_track(mocker):
    mocker.patch('upsies.utils.video.default_track', side_effect=errors.ContentError('Something went wrong'))
    with pytest.raises(errors.ContentError, match=r'^Something went wrong$'):
        video.frame_rate('foo.mkv')


@pytest.mark.parametrize(
    argnames='video_track, exp_bit_depth',
    argvalues=(
        ({'BitDepth': '8'}, 8),
        ({'BitDepth': '10'}, 10),
        ({'BitDepth': 'foo'}, 0),
        ({}, 0),
    ),
    ids=lambda v: str(v),
)
def test_bit_depth(video_track, exp_bit_depth, mocker):
    mocker.patch('upsies.utils.video.default_track', return_value=video_track)
    assert video.bit_depth('foo.mkv') == exp_bit_depth

@pytest.mark.parametrize(
    argnames='video_track, default, exp_return_value, exp_exception',
    argvalues=(
        ({'BitDepth': '10'}, video.NO_DEFAULT_VALUE, 10, None),
        ({'BitDepth': '10'}, 'default value', 10, None),
        ({'BitDepth': '10'}, None, 10, None),
        ({}, video.NO_DEFAULT_VALUE, True, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        ({}, None, None, None),
    ),
)
def test_bit_depth_with_default_value(video_track, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if video_track:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.default_track', return_value=video_track)

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.bit_depth(path, default=default)
        else:
            assert video.bit_depth(path, default=default) is default
    else:
        assert video.bit_depth(path, default=default) == exp_return_value

def test_bit_depth_forwards_ContentError_from_default_track(mocker):
    mocker.patch('upsies.utils.video.default_track', side_effect=errors.ContentError('Something went wrong'))
    with pytest.raises(errors.ContentError, match=r'^Something went wrong$'):
        video.bit_depth('foo.mkv')


@pytest.mark.parametrize(
    argnames='video_track, exp_return_value',
    argvalues=(
        ({}, ''),
        ({'HDR_Format': 'foo'}, ''),
        ({'HDR_Format': 'Dolby Vision'}, 'DV'),
        ({'HDR_Format': 'Dolby Vision / SMPTE ST 2086'}, 'DV'),
        ({'HDR_Format_Compatibility': 'HDR10+ Profile A'}, 'HDR10+'),
        ({'HDR_Format_Compatibility': 'HDR10+ Profile B'}, 'HDR10+'),
        ({'HDR_Format_Compatibility': 'HDR10'}, 'HDR10'),
        ({'HDR_Format_Compatibility': 'foo HDR bar'}, 'HDR'),
        ({'HDR_Format': 'foo HDR bar'}, 'HDR'),
        ({'colour_primaries': 'BT.2020'}, 'HDR10'),
    ),
    ids=lambda v: str(v),
)
def test_hdr_format(video_track, exp_return_value, mocker):
    mocker.patch('upsies.utils.video.default_track', return_value=video_track)
    assert video.hdr_format('foo.mkv') == exp_return_value

@pytest.mark.parametrize(
    argnames='video_track, default, exp_return_value, exp_exception',
    argvalues=(
        ({'HDR_Format_Compatibility': 'HDR10'}, video.NO_DEFAULT_VALUE, 'HDR10', None),
        ({'HDR_Format_Compatibility': 'HDR10'}, 'default value', 'HDR10', None),
        ({'HDR_Format_Compatibility': 'HDR10'}, None, 'HDR10', None),
        ({}, video.NO_DEFAULT_VALUE, True, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        ({}, None, None, None),
    ),
)
def test_hdr_format_with_default_value(video_track, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if video_track:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.default_track', return_value=video_track)

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.hdr_format(path, default=default)
        else:
            assert video.hdr_format(path, default=default) is default
    else:
        assert video.hdr_format(path, default=default) == exp_return_value

def test_hdr_format_forwards_ContentError_from_default_track(mocker):
    mocker.patch('upsies.utils.video.default_track', side_effect=errors.ContentError('Something went wrong'))
    with pytest.raises(errors.ContentError, match=r'^Something went wrong$'):
        video.hdr_format('foo.mkv')


@pytest.mark.parametrize(
    argnames='audio_tracks, exp_dual_audio',
    argvalues=(
        ([], False),
        ([{}, {}], False),
        ([{'Language': 'en'}], False),
        ([{'Language': 'fr'}], False),
        ([{'Language': 'fr'}, {'Language': 'en'}], True),
        ([{'Language': 'en'}, {'Language': 'fr'}], True),
        ([{'Language': 'da'}, {'Language': 'fr'}], True),
        ([{'Language': 'en-GB'}, {'Language': 'fr'}], True),
        ([{'Language': 'en-GB'}, {'Language': 'en-US'}], False),
        ([{'Language': 'en'}, {'Language': 'fr'}, {'Language': 'fr', 'Title': 'Commentary with Foo'}], True),
        ([{'Language': 'fr'}, {'Language': 'en', 'Title': 'Commentary with Foo'}], False),
        ([{'Language': 'fr'}, {'Language': 'en-GB', 'Title': 'Commentary with Foo'}], False),
    ),
    ids=lambda v: str(v),
)
def test_has_dual_audio(audio_tracks, exp_dual_audio, mocker):
    mocker.patch('upsies.utils.video.tracks', return_value={'Audio': audio_tracks})
    assert video.has_dual_audio('foo.mkv') == exp_dual_audio

@pytest.mark.parametrize(
    argnames='audio_tracks, default, exp_return_value, exp_exception',
    argvalues=(
        ([{'Language': 'fr'}, {'Language': 'en'}], video.NO_DEFAULT_VALUE, True, None),
        ([{'Language': 'fr'}, {'Language': 'en'}], 'default value', True, None),
        ([{'Language': 'fr'}, {'Language': 'en'}], None, True, None),
        ([], video.NO_DEFAULT_VALUE, True, errors.ContentError('{path}: No such file or directory')),
        ([], 'default value', 'default value', None),
        ([], None, None, None),
    ),
)
def test_has_dual_audio_with_default_value(audio_tracks, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if audio_tracks:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.tracks', return_value={'Audio': audio_tracks})

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.has_dual_audio(path, default=default)
        else:
            assert video.has_dual_audio(path, default=default) is default
    else:
        assert video.has_dual_audio(path, default=default) == exp_return_value

def test_has_dual_audio_forwards_ContentError_from_tracks(mocker):
    mocker.patch('upsies.utils.video.tracks', side_effect=errors.ContentError('Something went wrong'))
    with pytest.raises(errors.ContentError, match=r'^Something went wrong$'):
        video.has_dual_audio('foo.mkv')


def test_is_bt601_custom_default(tmp_path, mocker):
    mocker.patch('upsies.utils.video._get_color_matrix')
    mocker.patch('upsies.utils.video._get_closest_standard_resolution')
    assert video.is_bt601('foo.mkv', default='oh well') == 'oh well'

def test_is_bt601_with_color_matrix_bt601(tmp_path, mocker):
    mocker.patch('upsies.utils.video._get_color_matrix', side_effect=[True, False])
    mocker.patch('upsies.utils.video._get_closest_standard_resolution')
    assert video.is_bt601('foo.mkv') is True

def test_is_bt601_with_color_matrix_bt470(tmp_path, mocker):
    mocker.patch('upsies.utils.video._get_color_matrix', side_effect=[False, True])
    mocker.patch('upsies.utils.video._get_closest_standard_resolution')
    assert video.is_bt601('foo.mkv') is True

@pytest.mark.parametrize(
    argnames='standard_resolutions, exp_return_value, exp_mock_calls',
    argvalues=(
        ([719, 480], True, [
            call._get_color_matrix('foo.mkv', 'BT.601'),
            call._get_color_matrix('foo.mkv', 'BT.470 System B/G'),
            call.tracks('foo.mkv'),
            call._get_closest_standard_resolution('video track 1'),
            call._get_closest_standard_resolution('video track 2'),
        ]),
        ([480, 719], True, [
            call._get_color_matrix('foo.mkv', 'BT.601'),
            call._get_color_matrix('foo.mkv', 'BT.470 System B/G'),
            call.tracks('foo.mkv'),
            call._get_closest_standard_resolution('video track 1'),
            call._get_closest_standard_resolution('video track 2'),
        ]),
        ([720, 719], False, [
            call._get_color_matrix('foo.mkv', 'BT.601'),
            call._get_color_matrix('foo.mkv', 'BT.470 System B/G'),
            call.tracks('foo.mkv'),
            call._get_closest_standard_resolution('video track 1'),
        ]),
        ([719, 720], False, [
            call._get_color_matrix('foo.mkv', 'BT.601'),
            call._get_color_matrix('foo.mkv', 'BT.470 System B/G'),
            call.tracks('foo.mkv'),
            call._get_closest_standard_resolution('video track 1'),
            call._get_closest_standard_resolution('video track 2'),
        ]),
    ),
    ids=lambda v: str(v),
)
def test_is_bt601_with_sd_resolution(standard_resolutions, exp_return_value, exp_mock_calls, tmp_path, mocker):
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.video._get_color_matrix', return_value=False),
        '_get_color_matrix',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.tracks', return_value={'Video': [
            'video track 1',
            'video track 2',
        ]}),
        'tracks',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video._get_closest_standard_resolution', side_effect=standard_resolutions),
        '_get_closest_standard_resolution',
    )
    assert video.is_bt601('foo.mkv') == exp_return_value
    assert mocks.mock_calls == exp_mock_calls


def test_is_bt709(mocker):
    get_color_matrix_mock = mocker.patch('upsies.utils.video._get_color_matrix')
    path = Mock()
    default = Mock()
    assert video.is_bt709(path, default=default) is get_color_matrix_mock.return_value
    assert get_color_matrix_mock.call_args_list == [call(path, 'BT.709', default=default)]


def test_is_bt2020(mocker):
    get_color_matrix_mock = mocker.patch('upsies.utils.video._get_color_matrix')
    path = Mock()
    default = Mock()
    assert video.is_bt2020(path, default=default) is get_color_matrix_mock.return_value
    assert get_color_matrix_mock.call_args_list == [call(path, 'BT.2020', default=default)]


@pytest.mark.parametrize(
    argnames='default, path_exists, name, video_tracks, exp_return_value',
    argvalues=(
        (video.NO_DEFAULT_VALUE, True, 'BT.123', [{}, {'matrix_coefficients': 'BT.123'}, {}], True),
        (video.NO_DEFAULT_VALUE, True, 'BT.123', [{}, {'matrix_coefficients': 'BT.123 Foo'}, {}], True),
        (video.NO_DEFAULT_VALUE, True, 'BT.123', [{}, {'matrix_coefficients': 'BT.321'}, {}], False),
        (video.NO_DEFAULT_VALUE, True, 'BT.123', [{}, {}, {}], False),
        (video.NO_DEFAULT_VALUE, False, 'BT.123', [{}, {}, {}], False),
        ('oh well', False, 'BT.123', [{}, {}, {}], 'oh well'),
    ),
    ids=lambda v: str(v),
)
def test__get_color_matrix(default, path_exists, name, video_tracks, exp_return_value, tmp_path, mocker):
    path = tmp_path / 'foo.mkv'
    if path_exists:
        path.write_bytes(b'data')
    path = str(path)
    mocker.patch('upsies.utils.video.tracks', return_value={'Video': video_tracks})
    assert video._get_color_matrix(path, name, default=default) == exp_return_value


@pytest.mark.parametrize(
    argnames='tracks, exp_return_value',
    argvalues=(
        ({}, {}),
        ({'General': []}, {}),
        ({'Audio': [{}]}, {}),
        (
            {
                'Audio': [{'Language': 'ab'}, {}, {'Language': 'bc', 'Title': 'teh CoMmEnTaRy!'}],
                'Text': [{'Language': 'ab', 'Title': 'teh CoMmEnTaRy!'}, {'Language': 'cd'}, {}],
            },
            {'Audio': {'ab'}, 'Text': {'cd'}},
        ),
    ),
    ids=lambda v: str(v),
)
def test_languages(tracks, exp_return_value, mocker):
    mocker.patch('upsies.utils.video.tracks', return_value=tracks)
    return_value = video.languages('foo.mkv')
    assert return_value == exp_return_value

@pytest.mark.parametrize(
    argnames='tracks, exp_return_value',
    argvalues=(
        ({}, {}),
        ({'General': []}, {}),
        ({'Audio': [{}]}, {}),
        (
            {
                'Audio': [{'Language': 'ab'}, {}, {'Language': 'bc', 'Title': 'teh CoMmEnTaRy!'}],
                'Text': [{'Language': 'ab', 'Title': 'teh CoMmEnTaRy!'}, {'Language': 'cd'}, {}],
            },
            {'Audio': {'ab', 'bc'}, 'Text': {'ab', 'cd'}},
        ),
    ),
    ids=lambda v: str(v),
)
def test_languages_including_commentary(tracks, exp_return_value, mocker):
    mocker.patch('upsies.utils.video.tracks', return_value=tracks)
    return_value = video.languages('foo.mkv', exclude_commentary=False)
    assert return_value == exp_return_value

@pytest.mark.parametrize('default', (None, 'asdf'))
@pytest.mark.parametrize(
    argnames='tracks, exp_return_value',
    argvalues=(
        ({}, {}),
        ({'General': []}, {}),
        ({'Audio': [{}]}, {'Audio': {'<default>'}}),
        (
            {
                'Audio': [{'Language': 'ab'}, {}, {'Language': 'bc'}],
                'Text': [{'Language': 'ab'}, {'Language': 'cd'}, {}],
            },
            {'Audio': {'ab', '<default>', 'bc'}, 'Text': {'ab', 'cd', '<default>'}},
        ),
    ),
    ids=lambda v: str(v),
)
def test_languages_with_default(default, tracks, exp_return_value, mocker):
    mocker.patch('upsies.utils.video.tracks', return_value=tracks)
    return_value = video.languages('foo.mkv', default=default)
    assert return_value == {
        k: {
            default if v == '<default>' else v
            for v in v
        }
        for k, v in exp_return_value.items()
    }


@pytest.mark.parametrize(
    argnames='audio_tracks, exp_return_value',
    argvalues=(
        ([], False),
        ([{}, {}], False),
        ([{'Title': 'Shlommentary'}], False),
        ([{'Title': 'Commentary with Foo'}], True),
        ([{'Title': "Foo's commentary"}], True),
        ([{'Title': "THE FRICKIN' COMMENTARY, OMG"}], True),
        ([{'Title': "Director's Comments"}], True),
    ),
    ids=lambda v: str(v),
)
def test_has_commentary(exp_return_value, audio_tracks, mocker):
    mocker.patch('upsies.utils.video.tracks', return_value={'Audio': audio_tracks})
    assert video.has_commentary('foo.mkv') == exp_return_value

@pytest.mark.parametrize(
    argnames='audio_track, default, exp_return_value, exp_exception',
    argvalues=(
        ({'Title': 'Commentary with Foo'}, video.NO_DEFAULT_VALUE, True, None),
        ({'Title': 'Commentary with Foo'}, 'default value', True, None),
        ({'Title': 'Commentary with Foo'}, '', True, None),
        ({'Title': 'Commentary with Foo'}, None, True, None),
        ({}, video.NO_DEFAULT_VALUE, False, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        ({}, '', '', None),
        ({}, None, None, None),
    ),
)
def test_has_commentary_with_default_value(audio_track, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if audio_track:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.tracks', return_value={'Audio': [audio_track]})

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.has_commentary(path, default=default)
        else:
            assert video.has_commentary(path, default=default) is default
    else:
        assert video.has_commentary(path, default=default) == exp_return_value

def test_has_commentary_forwards_ContentError_from_tracks(mocker):
    mocker.patch('upsies.utils.video.tracks', side_effect=errors.ContentError('Something went wrong'))
    with pytest.raises(errors.ContentError, match=r'^Something went wrong$'):
        video.has_commentary('foo.mkv')


@pytest.mark.parametrize(
    argnames='audio_track, exp_audio_format',
    argvalues=(
        ({}, ''),
        ({'Format': 'AAC', 'Format_AdditionalFeatures': 'LC'}, 'AAC'),
        ({'Format': 'AC-3'}, 'DD'),
        ({'Format': 'E-AC-3'}, 'DDP'),
        ({'Format': 'E-AC-3', 'Format_Commercial_IfAny': 'Dolby Digital Plus with Dolby Atmos'}, 'DDP Atmos'),
        ({'Format': 'MLP FBA', 'Format_Commercial_IfAny': 'Dolby TrueHD'}, 'TrueHD'),
        ({'Format': 'MLP FBA', 'Format_Commercial_IfAny': 'Dolby TrueHD with Dolby Atmos'}, 'TrueHD Atmos'),
        ({'Format': 'DTS'}, 'DTS'),
        ({'Format': 'DTS', 'Format_Commercial_IfAny': 'DTS-ES Matrix'}, 'DTS-ES'),
        ({'Format': 'DTS', 'Format_Commercial_IfAny': 'DTS-ES Discrete'}, 'DTS-ES'),
        ({'Format': 'DTS', 'Format_Commercial_IfAny': 'DTS-HD High Resolution Audio', 'Format_AdditionalFeatures': 'XBR'}, 'DTS-HD'),
        ({'Format': 'DTS', 'Format_Commercial_IfAny': 'DTS-HD Master Audio', 'Format_AdditionalFeatures': 'XLL'}, 'DTS-HD MA'),
        ({'Format': 'DTS', 'Format_Commercial_IfAny': 'DTS-HD Master Audio', 'Format_AdditionalFeatures': 'XLL X'}, 'DTS:X'),
        ({'Format': 'FLAC'}, 'FLAC'),
        ({'Format': 'MPEG Audio'}, 'MP3'),
        ({'Format': 'Vorbis'}, 'Vorbis'),
        ({'Format': 'Opus'}, 'Opus'),
    ),
    ids=lambda v: str(v),
)
def test_audio_format(audio_track, exp_audio_format, mocker):
    mocker.patch('upsies.utils.video.default_track', return_value=audio_track)
    assert video.audio_format('foo.mkv') == exp_audio_format

@pytest.mark.parametrize(
    argnames='audio_track, path_exists, default, exp_result',
    argvalues=(
        (errors.ContentError('Nope'), True, video.NO_DEFAULT_VALUE, errors.ContentError('Nope')),
        (errors.ContentError('Nope'), True, 'default value', ''),
        (errors.ContentError('Nope'), True, None, ''),
        (errors.ContentError('Nope'), False, video.NO_DEFAULT_VALUE, errors.ContentError('Nope')),
        (errors.ContentError('Nope'), False, 'default value', 'default value'),
        (errors.ContentError('Nope'), False, None, None),

        ({'Format': 'FLAC'}, True, video.NO_DEFAULT_VALUE, 'FLAC'),
        ({'Format': 'FLAC'}, True, 'default value', 'FLAC'),
        ({'Format': 'FLAC'}, True, None, 'FLAC'),
        ({'Format': 'FLAC'}, False, video.NO_DEFAULT_VALUE, errors.ContentError('{path}: No such file or directory')),
        ({'Format': 'FLAC'}, False, 'default value', 'default value'),
        ({'Format': 'FLAC'}, False, None, None),

        ({'No audio': 'track'}, True, video.NO_DEFAULT_VALUE, ''),
        ({'No audio': 'track'}, True, 'default value', ''),
        ({'No audio': 'track'}, True, None, ''),
        ({'No audio': 'track'}, False, video.NO_DEFAULT_VALUE, errors.ContentError('{path}: No such file or directory')),
        ({'No audio': 'track'}, False, 'default value', 'default value'),
        ({'No audio': 'track'}, False, None, None),
    ),
    ids=lambda v: repr(v),
)
def test_audio_format_with_default_value(audio_track, path_exists, default, exp_result, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if path_exists:
        path.write_bytes(b'mock data')

    if isinstance(audio_track, Exception):
        mocker.patch('upsies.utils.video.default_track', side_effect=audio_track)
    elif path_exists:
        mocker.patch('upsies.utils.video.default_track', return_value=audio_track)
    else:
        mocker.patch('upsies.utils.video.default_track', side_effect=errors.ContentError(f'{path}: No such file or directory'))

    if isinstance(exp_result, Exception):
        msg = str(exp_result).format(path=path)
        with pytest.raises(type(exp_result), match=rf'^{re.escape(msg)}$'):
            print(repr(video.audio_format(path, default=default)))
    else:
        return_value = video.audio_format(path, default=default)
        assert return_value == exp_result


@pytest.mark.parametrize(
    argnames='audio_track, exp_audio_channels',
    argvalues=(
        ({}, ''),
        ({'Channels': '1'}, '1.0'),
        ({'Channels': '2'}, '2.0'),
        ({'Channels': '3'}, '2.0'),
        ({'Channels': '4'}, '2.0'),
        ({'Channels': '5'}, '2.0'),
        ({'Channels': '6'}, '5.1'),
        ({'Channels': '7'}, '5.1'),
        ({'Channels': '8'}, '7.1'),
    ),
    ids=lambda value: str(value),
)
def test_audio_channels(audio_track, exp_audio_channels, mocker):
    mocker.patch('upsies.utils.video.default_track', return_value=audio_track)
    assert video.audio_channels('foo.mkv') == exp_audio_channels

@pytest.mark.parametrize(
    argnames='audio_track, path_exists, default, exp_result',
    argvalues=(
        (errors.ContentError('Nope'), True, video.NO_DEFAULT_VALUE, errors.ContentError('Nope')),
        (errors.ContentError('Nope'), True, 'default value', ''),
        (errors.ContentError('Nope'), True, None, ''),
        (errors.ContentError('Nope'), False, video.NO_DEFAULT_VALUE, errors.ContentError('Nope')),
        (errors.ContentError('Nope'), False, 'default value', 'default value'),
        (errors.ContentError('Nope'), False, None, None),

        ({'Channels': '2'}, True, video.NO_DEFAULT_VALUE, '2.0'),
        ({'Channels': '2'}, True, 'default value', '2.0'),
        ({'Channels': '2'}, True, None, '2.0'),
        ({'Channels': '2'}, False, video.NO_DEFAULT_VALUE, errors.ContentError('{path}: No such file or directory')),
        ({'Channels': '2'}, False, 'default value', 'default value'),
        ({'Channels': '2'}, False, None, None),

        ({'No audio': 'track'}, True, video.NO_DEFAULT_VALUE, ''),
        ({'No audio': 'track'}, True, 'default value', ''),
        ({'No audio': 'track'}, True, None, ''),
        ({'No audio': 'track'}, False, video.NO_DEFAULT_VALUE, errors.ContentError('{path}: No such file or directory')),
        ({'No audio': 'track'}, False, 'default value', 'default value'),
        ({'No audio': 'track'}, False, None, None),
    ),
    ids=lambda v: repr(v),
)
def test_audio_channels_with_default_value(audio_track, path_exists, default, exp_result, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if path_exists:
        path.write_bytes(b'mock data')

    if isinstance(audio_track, Exception):
        mocker.patch('upsies.utils.video.default_track', side_effect=audio_track)
    elif path_exists:
        mocker.patch('upsies.utils.video.default_track', return_value=audio_track)
    else:
        mocker.patch('upsies.utils.video.default_track', side_effect=errors.ContentError(f'{path}: No such file or directory'))

    if isinstance(exp_result, Exception):
        msg = str(exp_result).format(path=path)
        with pytest.raises(type(exp_result), match=rf'^{re.escape(msg)}$'):
            print(repr(video.audio_channels(path, default=default)))
    else:
        return_value = video.audio_channels(path, default=default)
        assert return_value == exp_result


@pytest.mark.parametrize(
    argnames='video_track, exp_video_format',
    argvalues=(
        ({}, ''),
        ({'Encoded_Library_Name': 'XviD'}, 'XviD'),
        ({'Encoded_Library_Name': 'x264'}, 'x264'),
        ({'Encoded_Library_Name': 'x265'}, 'x265'),
        ({'Format': 'AVC'}, 'H.264'),
        ({'Format': 'HEVC'}, 'H.265'),
        ({'Format': 'VP9'}, 'VP9'),
        ({'Format': 'MPEG Video'}, 'MPEG-2'),
    ),
    ids=lambda value: str(value),
)
def test_video_format(video_track, exp_video_format, mocker):
    mocker.patch('upsies.utils.video.default_track', return_value=video_track)
    assert video.video_format('foo.mkv') == exp_video_format

@pytest.mark.parametrize(
    argnames='audio_track, default, exp_return_value, exp_exception',
    argvalues=(
        ({'Encoded_Library_Name': 'x264'}, video.NO_DEFAULT_VALUE, 'x264', None),
        ({'Encoded_Library_Name': 'x264'}, 'default value', 'x264', None),
        ({'Encoded_Library_Name': 'x264'}, None, 'x264', None),
        ({}, video.NO_DEFAULT_VALUE, None, errors.ContentError('{path}: No such file or directory')),
        ({}, 'default value', 'default value', None),
        ({}, None, None, None),
    ),
)
def test_video_format_with_default_value(audio_track, default, exp_return_value, exp_exception, mocker, tmp_path):
    path = tmp_path / 'foo.mkv'
    if audio_track:
        path.write_bytes(b'mock data')
        mocker.patch('upsies.utils.video.default_track', return_value=audio_track)

    if exp_exception:
        if default is video.NO_DEFAULT_VALUE:
            exp_error = str(exp_exception).format(path=path)
            with pytest.raises(type(exp_exception), match=rf'^{re.escape(exp_error)}$'):
                video.video_format(path, default=default)
        else:
            assert video.video_format(path, default=default) is default
    else:
        assert video.video_format(path, default=default) == exp_return_value

def test_video_format_catches_ContentError_from_default_track(mocker):
    mocker.patch('upsies.utils.video.default_track', side_effect=errors.ContentError('Something went wrong'))
    with pytest.raises(errors.ContentError, match=r'^Something went wrong$'):
        video.video_format('foo.mkv')


def test_find_videos_gets_bdmv(tmp_path, mocker):
    path = tmp_path / 'foo'
    (path / 'BDMV').mkdir(parents=True)
    return_value = video.find_videos(path)
    assert return_value == [str(path)]

@pytest.mark.parametrize(
    argnames='files, exp_result',
    argvalues=(
        (
            [
                ('xxx/VIDEO_TS/VIDEO_TS.BUP', 100), ('xxx/VIDEO_TS/VIDEO_TS.IFO', 100), ('xxx/VIDEO_TS/VIDEO_TS.VOB', 1000),

                ('foo/VIDEO_TS/VIDEO_TS.BUP', 100), ('foo/VIDEO_TS/VIDEO_TS.IFO', 100), ('foo/VIDEO_TS/VIDEO_TS.VOB', 1000),
                ('foo/VIDEO_TS/VTS_01_1.VOB', 6), ('foo/VIDEO_TS/VTS_01_2.VOB', 9), ('foo/VIDEO_TS/VTS_01_3.VOB', 12),
                ('foo/VIDEO_TS/VTS_02_1.VOB', 6), ('foo/VIDEO_TS/VTS_02_2.VOB', 24), ('foo/VIDEO_TS/VTS_02_3.VOB', 12),
                ('foo/VIDEO_TS/VTS_03_1.VOB', 12), ('foo/VIDEO_TS/VTS_03_2.VOB', 15), ('foo/VIDEO_TS/VTS_03_3.VOB', 9),

                ('bar/VIDEO_TS/VIDEO_TS.BUP', 100), ('bar/VIDEO_TS/VIDEO_TS.IFO', 100), ('bar/VIDEO_TS/VIDEO_TS.VOB', 1000),
                ('bar/VIDEO_TS/VTS_01_1.VOB', 10), ('bar/VIDEO_TS/VTS_01_2.VOB', 20), ('bar/VIDEO_TS/VTS_01_3.VOB', 30),
                ('bar/VIDEO_TS/VTS_02_1.VOB', 11), ('bar/VIDEO_TS/VTS_02_2.VOB', 21), ('bar/VIDEO_TS/VTS_02_3.VOB', 30),
                ('bar/VIDEO_TS/VTS_03_1.VOB', 31), ('bar/VIDEO_TS/VTS_03_2.VOB', 30), ('bar/VIDEO_TS/VTS_03_3.VOB', 30),

                ('baz/VIDEO_TS/VIDEO_TS.BUP', 100), ('baz/VIDEO_TS/VIDEO_TS.IFO', 100), ('baz/VIDEO_TS/VIDEO_TS.VOB', 1000),
                ('baz/VIDEO_TS/VTS_01_1.VOB', 100), ('baz/VIDEO_TS/VTS_01_2.VOB', 110), ('baz/VIDEO_TS/VTS_01_3.VOB', 120),
                ('baz/VIDEO_TS/VTS_02_1.VOB', 110), ('baz/VIDEO_TS/VTS_02_2.VOB', 101), ('baz/VIDEO_TS/VTS_02_3.VOB', 102),
                ('baz/VIDEO_TS/VTS_03_1.VOB', 103), ('baz/VIDEO_TS/VTS_03_2.VOB', 106), ('baz/VIDEO_TS/VTS_03_3.VOB', 100),
            ],
            ('bar/VIDEO_TS/VTS_03_1.VOB', 'baz/VIDEO_TS/VTS_01_3.VOB', 'foo/VIDEO_TS/VTS_02_2.VOB'),
        ),
        (
            [
                ('foo/VIDEO_TS', 100),
            ],
            errors.ContentError('{content_path}: No video file found'),
        ),
    ),
    ids=lambda v: repr(v),
)
def test_find_videos_gets_video_ts(files, exp_result, tmp_path, mocker):
    content_path = tmp_path / 'dvd'
    for filepath, filesize in files:
        (content_path / filepath).parent.mkdir(parents=True, exist_ok=True)
        with (content_path / filepath).open('wb') as f:
            f.truncate(filesize)  # Sparse file

    if isinstance(exp_result, Exception):
        exp_msg = str(exp_result).format(content_path=content_path)
        with pytest.raises(type(exp_result), match=rf'^{re.escape(exp_msg)}$'):
            video.find_videos(str(content_path))
    else:
        found_videos = video.find_videos(str(content_path))
        assert found_videos == [
            str(content_path / filepath)
            for filepath in exp_result
        ]

@pytest.mark.parametrize('separator', ('.', ' ', '-'))
@pytest.mark.parametrize('prefix', ('The Foo Show', ''))
@pytest.mark.parametrize('suffix', ('More Info', ''))
@pytest.mark.parametrize(
    argnames='filelist',
    argvalues=(
        (
            'some/path/{prefix} S01E01 {suffix}.mkv',
            'some/path/{prefix} S01E02 {suffix}.mkv',
            'some/path/{prefix} S01E03 {suffix}.mkv',
            'some/path/{prefix} foo {suffix}.mkv',
        ),
        (
            'some/path/{prefix} Season1 Episode1 {suffix}.mkv',
            'some/path/{prefix} Season1Episode2 {suffix}.mkv',
            'some/path/{prefix} Season 1 Episode 3 {suffix}.mkv',
            'some/path/{prefix} foo {suffix}.mkv',
        ),
    ),
    ids=lambda v: str(v),
)
def test_find_videos_gets_season_pack(filelist, separator, prefix, suffix, tmp_path, mocker):

    def real_file(file):
        return file.replace(' ', separator).format(prefix=prefix, suffix=suffix)

    filelist_shuffled = [
        real_file(file)
        for file in random.sample(filelist, k=len(filelist))
    ]
    file_list_mock = mocker.patch('upsies.utils.fs.file_list', return_value=filelist_shuffled)
    filter_main_videos_mock = mocker.patch('upsies.utils.video.filter_main_videos',
                                           return_value=['unexpected file list'])

    return_value = video.find_videos(tmp_path)
    expected_filelist = [real_file(f) for f in filelist if 'foo' not in f]
    assert return_value == expected_filelist

    assert file_list_mock.call_args_list == [
        call(tmp_path, extensions=constants.VIDEO_FILE_EXTENSIONS),
    ]
    assert filter_main_videos_mock.call_args_list == []

def test_find_videos_gets_video_file(tmp_path, mocker):
    file_list_mock = mocker.patch(
        'upsies.utils.fs.file_list',
        return_value=('some/path/foo.mkv',),
    )
    filter_main_videos_mock = mocker.patch(
        'upsies.utils.video.filter_main_videos',
        return_value=file_list_mock.return_value,
    )
    path = str(tmp_path / 'some/path/foo.mkv')
    return_value = video.find_videos(path)
    assert return_value == ['some/path/foo.mkv']

    assert file_list_mock.call_args_list == [
        call(path, extensions=constants.VIDEO_FILE_EXTENSIONS),
    ]
    assert filter_main_videos_mock.call_args_list == [
        call(file_list_mock.return_value),
    ]

def test_find_videos_finds_no_videos(tmp_path, mocker):
    file_list_mock = mocker.patch('upsies.utils.fs.file_list', return_value=())
    filter_main_videos_mock = mocker.patch('upsies.utils.video.filter_main_videos')
    with pytest.raises(errors.ContentError, match=rf'^{tmp_path}: No video file found$'):
        video.find_videos(tmp_path)
    assert file_list_mock.call_args_list == [
        call(tmp_path, extensions=constants.VIDEO_FILE_EXTENSIONS),
    ]
    assert filter_main_videos_mock.call_args_list == []


def test_filter_main_videos_gets_no_files(mocker):
    file_size_mock = mocker.patch('upsies.utils.fs.file_size', return_value=12345)
    assert video.filter_main_videos(()) == ()
    assert file_size_mock.call_args_list == []

def test_filter_main_videos_gets_single_file(mocker):
    file_size_mock = mocker.patch('upsies.utils.fs.file_size', return_value=12345)
    assert video.filter_main_videos(('foo.mkv',)) == ('foo.mkv',)
    assert file_size_mock.call_args_list == []

def test_filter_main_videos_gets_single_main_video_file(mocker):
    sizes = {
        'a.mkv': 50,
        'b.mp4': 500,
        'c.avi': None,
        'd.wmv': 100,
        'e.m2ts': 110,
        'f.mts': 0,
        'g.ts': 105,
        'h.mkv': 9000,
        'i.jpg': 10000,
        'j.txt': 12000,
    }
    file_size_mock = mocker.patch(
        'upsies.utils.fs.file_size',
        side_effect=tuple(sizes.values()),
    )
    assert video.filter_main_videos(sizes.keys()) == (
        'h.mkv',
    )
    assert file_size_mock.call_args_list == [
        call('a.mkv'),
        call('b.mp4'),
        call('c.avi'),
        call('d.wmv'),
        call('e.m2ts'),
        call('f.mts'),
        call('g.ts'),
        call('h.mkv'),
    ]

def test_filter_main_videos_gets_multiple_main_video_files(mocker):
    sizes = {
        'a.mkv': 50,
        'b.mp4': 500,
        'c.avi': None,
        'd.wmv': 10000,
        'e.m2ts': 11000,
        'f.mts': 0,
        'g.ts': 10500,
        'h.mkv': 9000,
        'i.jpg': 10000,
        'j.txt': 12000,
    }
    file_size_mock = mocker.patch(
        'upsies.utils.fs.file_size',
        side_effect=tuple(sizes.values()),
    )
    assert video.filter_main_videos(sizes.keys()) == (
        'd.wmv',
        'e.m2ts',
        'g.ts',
        'h.mkv',
    )
    assert file_size_mock.call_args_list == [
        call('a.mkv'),
        call('b.mp4'),
        call('c.avi'),
        call('d.wmv'),
        call('e.m2ts'),
        call('f.mts'),
        call('g.ts'),
        call('h.mkv'),
    ]

def test_filter_main_videos_gets_only_unsizable_files(mocker):
    sizes = {
        'a.mkv': None,
        'b.mkv': None,
        'c.mkv': None,
    }
    file_size_mock = mocker.patch(
        'upsies.utils.fs.file_size',
        side_effect=tuple(sizes.values()),
    )
    assert video.filter_main_videos(sizes.keys()) == ()
    assert file_size_mock.call_args_list == [
        call('a.mkv'),
        call('b.mkv'),
        call('c.mkv'),
    ]

def test_filter_main_videos_gets_video_ts_paths_from_dvd(mocker):
    file_size_mock = mocker.patch('upsies.utils.fs.file_size')
    filter_main_videos_dvd_mock = mocker.patch(
        'upsies.utils.video._filter_main_videos_dvd',
        return_value=['1.VOB', '2.VOB', '3.VOB'],
    )
    assert video.filter_main_videos(('mock', 'video', 'paths')) == ['1.VOB', '2.VOB', '3.VOB']
    assert file_size_mock.call_args_list == []
    assert filter_main_videos_dvd_mock.call_args_list == [
        call(('mock', 'video', 'paths')),
    ]


@pytest.mark.parametrize(
    argnames='video_ts_files, exp_main_vobs',
    argvalues=(
        pytest.param(
            [
                ('xxx/VIDEO_TS/VIDEO_TS.BUP', 100), ('xxx/VIDEO_TS/VIDEO_TS.IFO', 100), ('xxx/VIDEO_TS/VIDEO_TS.VOB', 1000),

                ('foo/VIDEO_TS/VIDEO_TS.BUP', 100), ('foo/VIDEO_TS/VIDEO_TS.IFO', 100), ('foo/VIDEO_TS/VIDEO_TS.VOB', 1000),
                ('foo/VIDEO_TS/VTS_01_1.VOB', 6), ('foo/VIDEO_TS/VTS_01_2.VOB', 9), ('foo/VIDEO_TS/VTS_01_3.VOB', 12),
                ('foo/VIDEO_TS/VTS_02_1.VOB', 6), ('foo/VIDEO_TS/VTS_02_2.VOB', 24), ('foo/VIDEO_TS/VTS_02_3.VOB', 12),
                ('foo/VIDEO_TS/VTS_03_1.VOB', 12), ('foo/VIDEO_TS/VTS_03_2.VOB', 15), ('foo/VIDEO_TS/VTS_03_3.VOB', 9),

                ('bar/VIDEO_TS/VIDEO_TS.BUP', 100), ('bar/VIDEO_TS/VIDEO_TS.IFO', 100), ('bar/VIDEO_TS/VIDEO_TS.VOB', 1000),
                ('bar/VIDEO_TS/VTS_01_1.VOB', 10), ('bar/VIDEO_TS/VTS_01_2.VOB', 20), ('bar/VIDEO_TS/VTS_01_3.VOB', 30),
                ('bar/VIDEO_TS/VTS_02_1.VOB', 11), ('bar/VIDEO_TS/VTS_02_2.VOB', 21), ('bar/VIDEO_TS/VTS_02_3.VOB', 30),
                ('bar/VIDEO_TS/VTS_03_1.VOB', 31), ('bar/VIDEO_TS/VTS_03_2.VOB', 30), ('bar/VIDEO_TS/VTS_03_3.VOB', 30),

                ('baz/VIDEO_TS/VIDEO_TS.BUP', 100), ('baz/VIDEO_TS/VIDEO_TS.IFO', 100), ('baz/VIDEO_TS/VIDEO_TS.VOB', 1000),
                ('baz/VIDEO_TS/VTS_01_1.VOB', 100), ('baz/VIDEO_TS/VTS_01_2.VOB', 110), ('baz/VIDEO_TS/VTS_01_3.VOB', 120),
                ('baz/VIDEO_TS/VTS_02_1.VOB', 110), ('baz/VIDEO_TS/VTS_02_2.VOB', 101), ('baz/VIDEO_TS/VTS_02_3.VOB', 102),
                ('baz/VIDEO_TS/VTS_03_1.VOB', 103), ('baz/VIDEO_TS/VTS_03_2.VOB', 106), ('baz/VIDEO_TS/VTS_03_3.VOB', 100),
            ],
            ('foo/VIDEO_TS/VTS_02_2.VOB', 'bar/VIDEO_TS/VTS_03_1.VOB', 'baz/VIDEO_TS/VTS_01_3.VOB'),
            id='Largest VOBs',
        ),
        pytest.param(
            [
                ('xxx/VIDEO_TS/VIDEO_TS.BUP', 100), ('xxx/VIDEO_TS/VIDEO_TS.IFO', 100),

                ('foo/VIDEO_TS/VIDEO_TS.BUP', 100), ('foo/VIDEO_TS/VIDEO_TS.IFO', 100),
                ('foo/VIDEO_TS/VTS_01_1.BUP', 6), ('foo/VIDEO_TS/VTS_01_2.IFO', 9),

                ('bar/VIDEO_TS/VIDEO_TS.BUP', 100), ('bar/VIDEO_TS/VIDEO_TS.IFO', 100),
                ('bar/VIDEO_TS/VTS_02_1.BUP', 6), ('bar/VIDEO_TS/VTS_02_2.IFO', 9),
            ],
            (),
            id='Only non-VOBs',
        ),
        pytest.param(
            (),
            (),
            id='No files',
        ),
    ),
    ids=lambda v: repr(v),
)
def test__filter_main_videos_dvd(video_ts_files, exp_main_vobs, tmp_path):
    base = tmp_path / 'dvd'
    for filepath, size in video_ts_files:
        (base / filepath).parent.mkdir(parents=True, exist_ok=True)
        (base / filepath).write_bytes(b'x' * size)

    exp_main_vobs = [
        str(base / filepath)
        for filepath in exp_main_vobs
    ]

    main_vobs = video._filter_main_videos_dvd([
        str(base / filepath)
        for filepath, size_ in video_ts_files
    ])
    assert main_vobs == exp_main_vobs


@pytest.mark.parametrize(
    argnames='video_ts_files, exp_main_vobs',
    argvalues=(
        (
            [
                ('VIDEO_TS/VIDEO_TS.BUP', 100), ('VIDEO_TS/VIDEO_TS.IFO', 100), ('VIDEO_TS/VIDEO_TS.VOB', 1000),
                ('VIDEO_TS/VTS_01_1.VOB', 6), ('VIDEO_TS/VTS_01_2.VOB', 9), ('VIDEO_TS/VTS_01_3.VOB', 12),
                ('VIDEO_TS/VTS_02_1.VOB', 6), ('VIDEO_TS/VTS_02_2.VOB', 24), ('VIDEO_TS/VTS_02_3.VOB', 12),
                ('VIDEO_TS/VTS_03_1.VOB', 12), ('VIDEO_TS/VTS_03_2.VOB', 15), ('VIDEO_TS/VTS_03_3.VOB', 9),
            ],
            ('VIDEO_TS/VTS_02_1.VOB', 'VIDEO_TS/VTS_02_2.VOB', 'VIDEO_TS/VTS_02_3.VOB'),
        ),
        (
            [
                ('VIDEO_TS/VIDEO_TS.BUP', 100), ('VIDEO_TS/VIDEO_TS.IFO', 100), ('VIDEO_TS/VIDEO_TS.VOB', 1000),
            ],
            [],
        ),
        (
            [],
            [],
        ),
    ),
    ids=lambda v: repr(v),
)
def test_find_main_vobs(video_ts_files, exp_main_vobs, tmp_path):
    base = tmp_path / 'dvd'
    for filepath, size in video_ts_files:
        (base / filepath).parent.mkdir(parents=True, exist_ok=True)
        (base / filepath).write_bytes(b'x' * size)

    exp_main_vobs = [
        str(base / filepath)
        for filepath in exp_main_vobs
    ]

    main_vobs = video.find_main_vobs([
        str(base / filepath)
        for filepath, size_ in video_ts_files
    ])
    assert main_vobs == exp_main_vobs


@pytest.mark.parametrize(
    argnames='found_main_vobs, exp_main_vob',
    argvalues=(
        (
            [('VIDEO_TS/VTS_02_1.VOB', 12), ('VIDEO_TS/VTS_02_2.VOB', 9), ('VIDEO_TS/VTS_02_3.VOB', 6),],
            'VIDEO_TS/VTS_02_1.VOB',
        ),
        (
            [('VIDEO_TS/VTS_02_1.VOB', 6), ('VIDEO_TS/VTS_02_2.VOB', 12), ('VIDEO_TS/VTS_02_3.VOB', 9),],
            'VIDEO_TS/VTS_02_2.VOB',
        ),
        (
            [('VIDEO_TS/VTS_02_1.VOB', 9), ('VIDEO_TS/VTS_02_2.VOB', 6), ('VIDEO_TS/VTS_02_3.VOB', 12),],
            'VIDEO_TS/VTS_02_3.VOB',
        ),
        (
            [],
            None,
        ),
    ),
    ids=lambda v: repr(v),
)
def test_find_main_vob(found_main_vobs, exp_main_vob, tmp_path, mocker):
    base = tmp_path / 'dvd'

    if exp_main_vob:
        exp_main_vob = str(base / exp_main_vob)

    found_main_vobs = [
        ((base / vob_path), size)
        for vob_path, size in found_main_vobs
    ]
    for vob_path, size in found_main_vobs:
        vob_path.parent.mkdir(parents=True, exist_ok=True)
        vob_path.write_bytes(b'x' * size)

    find_main_vobs_mock = mocker.patch('upsies.utils.video.find_main_vobs', return_value=[
        str(vob_path)
        for vob_path, size_ in found_main_vobs
    ])

    mock_video_ts_files = ['foo', 'bar', 'baz']
    main_set = video.find_main_vob(mock_video_ts_files)
    assert main_set == exp_main_vob
    assert find_main_vobs_mock.call_args_list == [call(mock_video_ts_files)]


@pytest.mark.parametrize(
    argnames='vob_path, exp_result',
    argvalues=(
        ('path/to/VIDEO_TS/VTS_01_1.VOB', 'path/to/VIDEO_TS/VTS_01_0.IFO'),
        ('path/to/VIDEO_TS//VTS_03_6.VOB', 'path/to/VIDEO_TS/VTS_03_0.IFO'),
        ('path/to/VIDEO_TS/VTS_01_1.N00B', ValueError('This does not look like a VOB file: path/to/VIDEO_TS/VTS_01_1.N00B')),
    ),
)
def test_vob2ifo(vob_path, exp_result):
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            video.vob2ifo(vob_path)
    else:
        result = video.vob2ifo(vob_path)
        assert result == exp_result


def test_for_each_video_ts(tmp_path):
    base = tmp_path / 'base'
    (base / 'VIDEO_TS').mkdir(parents=True)
    (base / 'foo' / 'VIDEO_TS').mkdir(parents=True)
    (base / 'bar').mkdir(parents=True)
    (base / 'bar' / 'VIDEO_TS').write_text('This is not a directory.')
    (base / 'foo' / 'baz').mkdir(parents=True)
    (base / 'foo' / 'baz' / 'VIDEO_TS').mkdir(parents=True)

    return_value = list(video.for_each_video_ts(str(base)))
    assert return_value == [
        str(base / 'VIDEO_TS'),
        str(base / 'foo' / 'VIDEO_TS'),
        str(base / 'foo' / 'baz' / 'VIDEO_TS'),
    ]


def test_make_ffmpeg_input_gets_bluray_directory(tmp_path):
    path = tmp_path / 'foo'
    (path / 'BDMV').mkdir(parents=True)
    exp_ffmpeg_input = f'bluray:{path}'
    assert video.make_ffmpeg_input(path) == exp_ffmpeg_input

@pytest.mark.parametrize(
    argnames='main_vobs, exp_vob',
    argvalues=(
        ([], None),
        (['1.VOB', '2.VOB', '3.VOB'], '1.VOB'),
    ),
    ids=lambda v: repr(v),
)
def test_make_ffmpeg_input_gets_dvd_directory(main_vobs, exp_vob, mocker, tmp_path):
    path = tmp_path / 'foo'
    (path / 'VIDEO_TS').mkdir(parents=True)

    mocks = Mock()
    mocks.attach_mock(
        mocker.patch('upsies.utils.fs.file_list'),
        'file_list',
    )
    mocks.attach_mock(
        mocker.patch('upsies.utils.video.filter_main_videos', return_value=[
            str(path / f'VIDEO_TS/{filename}')
            for filename in main_vobs
        ]),
        'filter_main_videos',
    )

    return_value = video.make_ffmpeg_input(path)
    if exp_vob is None:
        assert return_value == str(path)
    else:
        assert return_value == str(path / f'VIDEO_TS/{exp_vob}')

    assert mocks.mock_calls == [
        call.file_list(str(path / 'VIDEO_TS'), extensions=('VOB',)),
        call.filter_main_videos(mocks.file_list.return_value)
    ]

def test_make_ffmpeg_input_something_else(tmp_path):
    path = tmp_path / 'foo'
    assert video.make_ffmpeg_input(path) == str(path)
