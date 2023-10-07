import re
from unittest.mock import Mock, call

import pytest

from upsies.utils import subtitle


@pytest.mark.parametrize('forced, exp_forced', (
    (True, True),
    (False, False),
    ('', False),
    (1, True),
))
@pytest.mark.parametrize('format, exp_format', (
    ('SRT', 'SRT'),
    ('', ''),
    (None, ''),
))
@pytest.mark.parametrize(
    argnames='language, exp_language, exp_attributes, exp_exception',
    argvalues=(
        ('foo-mx-Latn', None, None, ValueError("Invalid language: 'foo-mx-Latn'")),

        ('pt', 'pt', {'language': 'pt', 'territory': ''}, None),
        ('PT', 'pt', {'language': 'pt', 'territory': ''}, None),
        ('por', 'pt', {'language': 'pt', 'territory': ''}, None),

        ('Pt-bR', 'pt-BR', {'language': 'pt', 'territory': 'BR'}, None),
        ('spa-419', 'es-419', {'language': 'es', 'territory': '419'}, None),
        ('zh-HANS', 'zh-Hans', {'language': 'zh', 'territory': ''}, None),
        ('gsw-u-sd-chzh', 'gsw-u-sd-chzh', {'language': 'gsw', 'territory': ''}, None),
    ),
)
def test_Subtitle(language, exp_language, exp_attributes, exp_exception,
                  format, exp_format,
                  forced, exp_forced):
    if exp_exception:
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            subtitle.Subtitle(language=language, forced=forced, format=format)
    else:
        sub = subtitle.Subtitle(language=language, forced=forced, format=format)
        assert sub.language == exp_attributes['language']
        assert sub.territory == exp_attributes['territory']
        assert sub.forced == exp_forced
        assert sub.format == exp_format

        assert repr(sub) == (
            'Subtitle('
            + repr(exp_language)
            + f', forced={exp_forced!r}'
            + f', format={exp_format!r}'
            + ')'
        )


@pytest.mark.parametrize(
    argnames='a, b, exp_equal',
    argvalues=(
        (
            subtitle.Subtitle(language='foo', forced=False, format=None),
            subtitle.Subtitle(language='FOO', forced=False, format=None),
            True,
        ),
        (
            subtitle.Subtitle(language='foo', forced=False, format=None),
            subtitle.Subtitle(language='bar', forced=False, format=None),
            False,
        ),
        (
            subtitle.Subtitle(language='foo', forced=False, format=None),
            subtitle.Subtitle(language='foo', forced=0, format=None),
            True,
        ),
        (
            subtitle.Subtitle(language='foo', forced=False, format=None),
            subtitle.Subtitle(language='foo', forced=1, format=None),
            False,
        ),
        (
            subtitle.Subtitle(language='foo', forced=False, format=None),
            subtitle.Subtitle(language='foo', forced=False, format=''),
            True,
        ),
        (
            subtitle.Subtitle(language='foo', forced=False, format='FMT'),
            subtitle.Subtitle(language='foo', forced=False, format='FMT2'),
            False,
        ),
    ),
)
def test_Subtitle___eq__(a, b, exp_equal):
    equal = a == b
    assert equal is exp_equal


@pytest.mark.parametrize(
    argnames='kwargs, exp_return_value',
    argvalues=(
        ({'language': 'en', 'forced': False, 'format': 'FMT'}, subtitle.Subtitle(language='en', forced=False, format='FMT')),
        ({'language': 'invalidcode', 'forced': False, 'format': 'FMT'}, None),
    ),
    ids=lambda v: repr(v),
)
def test_Subtitle_or_none(kwargs, exp_return_value):
    return_value = subtitle.Subtitle.or_none(**kwargs)
    assert return_value == exp_return_value


def test_get_subtitles(mocker):
    mocks = Mock()
    for funcname in dir(subtitle):
        if funcname.startswith('get_subtitles_from_'):
            mocks.attach_mock(
                mocker.patch(f'upsies.utils.subtitle.{funcname}', return_value={funcname, 'return', 'values'}),
                funcname,
            )

    content_path = 'path/to/content'
    subtitles = subtitle.get_subtitles(content_path)
    assert subtitles == {
        'get_subtitles_from_mediainfo',
        'get_subtitles_from_filenames',
        'get_subtitles_from_idx_files',
        'get_subtitles_from_dvd_tree',
        'return', 'values',
    }

    assert mocks.mock_calls == [
        call.get_subtitles_from_mediainfo(content_path),
        call.get_subtitles_from_filenames(content_path),
        call.get_subtitles_from_idx_files(content_path),
        call.get_subtitles_from_dvd_tree(content_path),
    ]


@pytest.mark.parametrize(
    argnames='all_tracks, exp_subtitles',
    argvalues=(
        ({'Video': ..., 'Audio': ...}, set()),
        ({'Video': ..., 'Audio': ..., 'Text': []}, set()),
        ({'Video': ..., 'Audio': ..., 'Text': [{}]}, set()),
        ({'Video': ..., 'Audio': ..., 'Text': [{'Language': 'invalidcode'}]}, set()),
        (
            {'Video': ..., 'Audio': ..., 'Text': [{'Language': 'foo'}]},
            {subtitle.Subtitle(language='foo', forced=False, format=None)},
        ),
        (
            {'Video': ..., 'Audio': ..., 'Text': [{'Language': 'foo', 'Forced': 'No', 'CodecID': 'unknown'}]},
            {subtitle.Subtitle(language='foo', forced=False, format='')},
        ),
        (
            {'Video': ..., 'Audio': ..., 'Text': [{'Language': 'foo', 'Forced': 'Yes', 'CodecID': 'S_TEXT/ASS'}]},
            {subtitle.Subtitle(language='foo', forced=True, format='ASS')},
        ),
        (
            {'Video': ..., 'Audio': ..., 'Text': [
                {'Language': 'foo', 'Forced': 'No', 'CodecID': 'S_HDMV/PGS'},
                {'Language': 'bar', 'Forced': 'No', 'CodecID': 'S_TEXT/ASS'},
                {'Language': 'baz', 'Forced': 'Yes', 'CodecID': 'S_TEXT/UTF8'},
            ]},
            {
                subtitle.Subtitle(language='foo', forced=False, format='PGS'),
                subtitle.Subtitle(language='bar', forced=False, format='ASS'),
                subtitle.Subtitle(language='baz', forced=True, format='SRT'),
            },
        ),
    ),
    ids=lambda v: repr(v),
)
def test_get_subtitles_from_mediainfo(all_tracks, exp_subtitles, mocker):
    tracks_mock = mocker.patch('upsies.utils.video.tracks', return_value=all_tracks)

    content_path = 'path/to/content'
    subtitles = subtitle.get_subtitles_from_mediainfo(content_path)
    assert subtitles == exp_subtitles

    assert tracks_mock.call_args_list == [call(content_path)]


@pytest.mark.parametrize(
    argnames='file_list, exp_subtitles',
    argvalues=(
        ([], set()),
        (['path/to/foo.mkv', 'path/to/foo.jpg'], set()),
        (['path/to/foo.mkv', 'path/to/foo.srt', 'path/to/foo.ssa', 'path/to/foo.ass', 'path/to/foo.vtt'], set()),
        (['path/to/foo.mkv', 'path/to/foo.en.srt', 'path/to/foo.ssa', 'path/to/foo.ass', 'path/to/foo.vtt'], {
            subtitle.Subtitle(language='en', forced=False, format='SRT'),
        }),
        (['path/to/foo.mkv', 'path/to/foo.en.srt', 'path/to/foo.fre.ssa', 'path/to/foo.ass', 'path/to/foo.vtt'], {
            subtitle.Subtitle(language='en', forced=False, format='SRT'),
            subtitle.Subtitle(language='fre', forced=False, format='SSA'),
        }),
        (['path/to/foo.mkv', 'path/to/foo.en.srt', 'path/to/foo.fre.ssa', 'path/to/foo.invalidcode.ass', 'path/to/foo.vtt'], {
            subtitle.Subtitle(language='en', forced=False, format='SRT'),
            subtitle.Subtitle(language='fre', forced=False, format='SSA'),
        }),
        (['path/to/foo.mkv', 'path/to/foo.en.srt', 'path/to/foo.fre.ssa', 'path/to/foo.pt.ass', 'path/to/foo.vie.vtt'], {
            subtitle.Subtitle(language='en', forced=False, format='SRT'),
            subtitle.Subtitle(language='fre', forced=False, format='SSA'),
            subtitle.Subtitle(language='pt', forced=False, format='ASS'),
            subtitle.Subtitle(language='vie', forced=False, format='VTT'),
        }),
    ),
    ids=lambda v: repr(v),
)
def test_get_subtitles_from_filenames(file_list, exp_subtitles, mocker):
    file_list_mock = mocker.patch('upsies.utils.fs.file_list', return_value=file_list)

    content_path = 'path/to/content'
    subtitles = subtitle.get_subtitles_from_filenames(content_path)
    assert subtitles == exp_subtitles

    assert file_list_mock.call_args_list == [
        call(content_path, extensions=('srt', 'ssa', 'ass', 'vtt')),
    ]


@pytest.mark.parametrize(
    argnames='existing_files, file_list, exp_subtitles',
    argvalues=(
        ({}, [], set()),
        ({'foo.idx': 'junk\nmore junk\n'}, ['foo.idx'], set()),
        ({'foo.idx': 'junk\nid: invalidcode, index: 0\nmore junk\n'}, ['foo.idx'], set()),
        (
            {
                'foo.idx': 'junk\nid: de, index: 0\nmore junk\n',
                'bar.idx': 'junk\nid: en, index: 1\nmore junk\n',
                'baz.idx': 'junk\nid: ru, index: 123\nmore junk\n',
            },
            ['foo.idx', 'bar.idx', 'baz.idx', 'nosuchfile.idx'],
            {
                subtitle.Subtitle(language='de', forced=False, format=subtitle._subtitle_formats['idx']),
                subtitle.Subtitle(language='en', forced=False, format=subtitle._subtitle_formats['idx']),
                subtitle.Subtitle(language='ru', forced=False, format=subtitle._subtitle_formats['idx']),
            },
        ),
    ),
    ids=lambda v: repr(v),
)
def test_get_subtitles_from_idx_files(existing_files, file_list, exp_subtitles, tmp_path, mocker):
    content_path = tmp_path / 'content'
    content_path.mkdir(parents=True, exist_ok=True)
    for file, data in existing_files.items():
        (content_path / file).write_text(data)

    file_list_mock = mocker.patch('upsies.utils.fs.file_list', return_value=(
        str(content_path / file)
        for file in file_list
    ))

    subtitles = subtitle.get_subtitles_from_idx_files(content_path)
    assert subtitles == exp_subtitles

    assert file_list_mock.call_args_list == [
        call(content_path, extensions=('idx',)),
    ]


@pytest.mark.parametrize(
    argnames='found_videos, exp_subtitles',
    argvalues=(
        (
            {
                'a.mkv': {'Video': ..., 'Audio': ..., 'Text': [{'Language': 'a', 'Forced': 'Yes', 'CodecID': 'S_TEXT/UTF8'}]},
                'VTS_01_02.VOB': {'Video': ..., 'Audio': ..., 'Text': [
                    {'Language': 'xa'},
                    {'Language': 'xb'},
                ]},
                'VIDEO_TS.IFO': {},
                'b.jpg': {},
                'VTS_03_04.VOB': {'Video': ..., 'Audio': ..., 'Text': [
                    {'Language': 'ya'},
                    {'Language': 'yb'},
                ]},
            },
            set((
                subtitle.Subtitle(language='xa', forced=False, format='VobSub'),
                subtitle.Subtitle(language='xb', forced=False, format='VobSub'),
                subtitle.Subtitle(language='ya', forced=False, format='VobSub'),
                subtitle.Subtitle(language='yb', forced=False, format='VobSub'),
            )),
        ),
    ),
    ids=lambda v: repr(v),
)
def test_get_subtitles_from_dvd_tree(found_videos, exp_subtitles, tmp_path, mocker):
    content_path = 'path/to/content'

    find_videos_mock = mocker.patch('upsies.utils.video.find_videos', return_value=tuple(found_videos))
    tracks_mock = mocker.patch('upsies.utils.video.tracks', side_effect=(
        tracks
        for filename, tracks in found_videos.items()
        if filename.upper().endswith('VOB')
    ))

    subtitles = subtitle.get_subtitles_from_dvd_tree(content_path)
    assert subtitles == exp_subtitles

    assert find_videos_mock.call_args_list == [
        call(content_path),
    ]
    assert tracks_mock.call_args_list == [
        call(re.sub(r'\d+.VOB', '0.IFO', filename))
        for filename in found_videos.keys()
        if filename.upper().endswith('VOB')
    ]
