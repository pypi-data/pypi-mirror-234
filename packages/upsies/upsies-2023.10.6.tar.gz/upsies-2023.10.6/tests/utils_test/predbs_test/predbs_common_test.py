import os
import re

import pytest

from upsies import errors
from upsies.utils.predbs import common
from upsies.utils.types import ReleaseType

abbreviated_file_name_test_cases = (
    ('group-thetitle.1080p.bluray.x264.mkv', True),
    ('group-the.title.2016.720p.bluray.x264.mkv', True),
    ('group-thetitle720.mkv', True),
    ('group-the-title-720p.mkv', True),
    ('group-thetitle-720p.mkv', True),
    ('group-ttl-s02e01-720p.mkv', True),
    ('group-the.title.1984.720p.mkv', True),
    ('group-the.title.720p.mkv', True),
    ('group-ttl.720p.mkv', True),
    ('group-title.mkv', True),
    ('title-1080p-group.mkv', True),
    ('group-the_title_x264_bluray.mkv', True),
    ('ttl.720p-group.mkv', True),
    ('GR0up1080pAsDf.mkv', True),
    ('grpthetitle.mkv', True),
    ('title.2017.720p.bluray.x264-group.mkv', False),
)

@pytest.mark.parametrize('path', ('path/to', ''))
@pytest.mark.parametrize(
    argnames='filename, exp_is_abbreviated',
    argvalues=abbreviated_file_name_test_cases,
)
def test_is_abbreviated_filename(path, filename, exp_is_abbreviated):
    filepath = os.path.join(path, filename)
    return_value = common.is_abbreviated_filename(filepath)
    assert return_value is exp_is_abbreviated

@pytest.mark.parametrize('path', ('path/to', ''))
@pytest.mark.parametrize(
    argnames='filename, exp_is_abbreviated',
    argvalues=abbreviated_file_name_test_cases,
)
def test_assert_not_abbreviated_filename(path, filename, exp_is_abbreviated):
    filepath = os.path.join(path, filename)
    exp_msg = f'Abbreviated scene file name is verboten: {filepath}'

    if exp_is_abbreviated:
        with pytest.raises(errors.SceneAbbreviatedFilenameError, match=rf'^{re.escape(exp_msg)}$'):
            common.assert_not_abbreviated_filename(filepath)
    else:
        common.assert_not_abbreviated_filename(filepath)


@pytest.mark.parametrize(
    argnames='source, irrelevant_keys',
    argvalues=(
        ('BluRay', ()),
        ('DVDRip', ('resolution')),
    ),
    ids=lambda v: str(v),
)
@pytest.mark.parametrize(
    argnames='release_info, exclude, exp_keys',
    argvalues=(
        (
            {'type': ReleaseType.movie},
            (),
            ('title', 'year', 'resolution', 'source', 'video_codec', 'group'),
        ),
        (
            {'type': ReleaseType.movie},
            ('year',),
            ('title', 'resolution', 'source', 'video_codec', 'group'),
        ),
        (
            {'type': ReleaseType.season},
            (),
            ('title', 'episodes', 'resolution', 'source', 'video_codec', 'group'),
        ),
        (
            {'type': ReleaseType.season},
            ('resolution',),
            ('title', 'episodes', 'source', 'video_codec', 'group'),
        ),
        (
            {'type': ReleaseType.episode},
            (),
            ('title', 'episodes', 'resolution', 'source', 'video_codec', 'group'),
        ),
        (
            {'type': ReleaseType.episode},
            ('group',),
            ('title', 'episodes', 'resolution', 'source', 'video_codec'),
        ),
        (
            {'type': None},
            (),
            (),
        ),
        (
            {'type': None},
            ('source',),
            (),
        ),
        (
            {'type': 'something weird'},
            (),
            (),
        ),
    ),
    ids=lambda v: str(v),
)
def test_get_needed_keys(release_info, exclude, exp_keys, source, irrelevant_keys):
    release_info['source'] = source
    exp_keys = tuple(k for k in exp_keys if k not in irrelevant_keys)
    needed_keys = common.get_needed_keys(release_info, exclude=exclude)
    assert needed_keys == exp_keys


@pytest.mark.parametrize(
    argnames='release_name, exp_season_pack',
    argvalues=(
        ('X.S01.1080p.BluRay.x264-ASDF', 'X.S01.1080p.BluRay.x264-ASDF'),
        ('X.S01E01.1080p.BluRay.x264-ASDF', 'X.S01.1080p.BluRay.x264-ASDF'),
        ('X.S01E01.Episode.Title.1080p.BluRay.x264-ASDF', 'X.S01.1080p.BluRay.x264-ASDF'),
        ('X.S01E01.Episode.Title.1080i.BluRay.x264-ASDF', 'X.S01.1080i.BluRay.x264-ASDF'),
        ('X.S01E01.Episode.Title.DVDRip.x264-ASDF', 'X.S01.DVDRip.x264-ASDF'),
        ('X.S01E01.Episode.Title.REPACK.720p.BluRay.x264-ASDF', 'X.S01.REPACK.720p.BluRay.x264-ASDF'),
        ('X.S01E01.Episode.Title.PROPER.720p.BluRay.x264-ASDF', 'X.S01.PROPER.720p.BluRay.x264-ASDF'),
        ('X.S01E01.Episode.Title.DUTCH.DVDRip.x264-ASDF', 'X.S01.DUTCH.DVDRip.x264-ASDF'),
        ('X.S01E01.Episode.Title.iNTERNAL.DVDRip.x264-ASDF', 'X.S01.iNTERNAL.DVDRip.x264-ASDF'),
        ('X.S01E01.Episode.Title.REAL.DVDRip.x264-ASDF', 'X.S01.REAL.DVDRip.x264-ASDF'),
        ('X.S01E01.French.DVDRip.x264-ASDF', 'X.S01.French.DVDRip.x264-ASDF'),
        ('X.S01E01.Episode.Title.German.DL.DVDRip.x264-ASDF', 'X.S01.German.DL.DVDRip.x264-ASDF'),
        ('X.S01E01E02.Episode.Title.German.DL.DVDRip.x264-ASDF', 'X.S01.German.DL.DVDRip.x264-ASDF'),
        ('X.S01E03-E04.Episode.Title.German.DL.DVDRip.x264-ASDF', 'X.S01.German.DL.DVDRip.x264-ASDF'),
    ),
)
def test_get_season_pack_name(release_name, exp_season_pack):
    season_pack = common.get_season_pack_name(release_name)
    assert season_pack == exp_season_pack


@pytest.mark.parametrize(
    argnames='directory_name, files, exp_return_value',
    argvalues=(
        pytest.param(
            'Dellamorte.Dellamore.1994.1080p.BluRay.x264-LiViDiTY.mkv',
            (
                'Dellamorte.Dellamore.1994.1080p.BluRay.x264-LiViDiTY.mkv',
            ),
            False,
            id='Movie as file',
        ),

        pytest.param(
            'Dellamorte.Dellamore.1994.1080p.BluRay.x264-LiViDiTY',
            (
                'Dellamorte.Dellamore.1994.1080p.BluRay.x264-LiViDiTY/ly-dellmdm1080p.mkv',
            ),
            False,
            id='Movie in directory',
        ),

        pytest.param(
            'Fawlty.Towers.S01.720p.BluRay.x264-SHORTBREHD',
            (
                'Fawlty.Towers.S01.720p.BluRay.x264-SHORTBREHD/Fawlty.Towers.S01E01.720p.BluRay.x264-SHORTBREHD.mkv',
                'Fawlty.Towers.S01.720p.BluRay.x264-SHORTBREHD/Fawlty.Towers.S01E02.720p.BluRay.x264-SHORTBREHD.mkv',
                'Fawlty.Towers.S01.720p.BluRay.x264-SHORTBREHD/Fawlty.Towers.S01E03.720p.BluRay.x264-SHORTBREHD.mkv',
            ),
            False,
            id='Non-mixed season pack',
        ),

        pytest.param(
            'Drunk.History.S01.720p.HDTV.x264-MiXED',
            (
                'Drunk.History.S01.720p.HDTV.x264-MiXED/drunk.history.s01e01.720p.hdtv.x264-killers.mkv',
                'Drunk.History.S01.720p.HDTV.x264-MiXED/drunk.history.s01e02.720p.hdtv.x264-2hd.mkv',
                'Drunk.History.S01.720p.HDTV.x264-MiXED/drunk.history.s01e03.720p.hdtv.x264.mkv',
                'Drunk.History.S01.720p.HDTV.x264-MiXED/Drunk.History.S01E04.720p.HDTV.x264-EVOLVE.mkv',
            ),
            True,
            id='Season pack with 2 scene groups',
        ),

        pytest.param(
            'Drunk.History.S01.720p.HDTV.x264-MiXED',
            (
                'Drunk.History.S01.720p.HDTV.x264-MiXED/drunk.history.s01e01.720p.hdtv.x264-killers.mkv',
                'Drunk.History.S01.720p.HDTV.x264-MiXED/drunk.history.s01e02.720p.hdtv.x264-2hd.mkv',
                'Drunk.History.S01.720p.HDTV.x264-MiXED/drunk.history.s01e03.720p.hdtv.x264-2hd.mkv',
                'Drunk.History.S01.720p.HDTV.x264-MiXED/Drunk.History.S01E04.720p.HDTV.x264-EVO.mkv',
            ),
            True,
            id='Season pack with 2 scene groups and 1 non-scene group',
        ),

        pytest.param(
            'Drunk.History.S01.720p.HDTV.x264',
            (
                'Drunk.History.S01.720p.HDTV.x264/drunk.history.s01e01.720p.hdtv.x264-killers.mkv',
                'Drunk.History.S01.720p.HDTV.x264/drunk.history.s01e02.720p.hdtv.x264.mkv',
                'Drunk.History.S01.720p.HDTV.x264/Drunk.History.S01E04.720p.HDTV.x264-EVO.mkv',
            ),
            True,
            id='Season pack with 1 scene group and 1 non-scene group and 1 nogroup',
        ),
    ),
)
def test_is_mixed_scene_release(directory_name, files, exp_return_value, tmp_path):
    for filepath in files:
        filepath = tmp_path / filepath
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(f'this is {filepath}')

    directory_path = str(tmp_path / directory_name)
    return_value = common.is_mixed_season_pack(directory_path)
    assert return_value == exp_return_value
