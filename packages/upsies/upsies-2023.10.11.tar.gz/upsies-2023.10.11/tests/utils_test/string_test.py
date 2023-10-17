import errno
import re
from unittest.mock import Mock, call

import pytest

from upsies import errors
from upsies.utils import string


@pytest.mark.parametrize(
    argnames='group, exp_string, exp_error',
    argvalues=(
        ('digits', '0123456789', None),
        ('foo', None, "No such character group: 'foo'"),
    ),
)
def test_group(group, exp_string, exp_error):
    if exp_error:
        with pytest.raises(ValueError, match=rf'^{re.escape(exp_error)}$'):
            string.group(group)
    else:
        assert string.group(group) == exp_string


max_nfo_size = 100

@pytest.fixture
def read_nfo_mocks(mocker):
    mocks = Mock()
    mocker.patch('upsies.utils.string._max_nfo_size', max_nfo_size)
    mocks.attach_mock(mocker.patch('upsies.utils.fs.file_list'), 'file_list')

    def mock_getsize(nfo_filepath):
        return max_nfo_size

    mocks.attach_mock(mocker.patch('os.path.getsize', side_effect=mock_getsize), 'getsize')

    def mock_open(nfo_filepath, mode):
        return Mock(
            __enter__=Mock(
                return_value=Mock(
                    read=Mock(return_value=f'content of {nfo_filepath}'.encode('utf-8')),
                ),
            ),
            __exit__=Mock(return_value=False),
        )

    mocks.attach_mock(mocker.patch('builtins.open', side_effect=mock_open), 'open')

    def mock_decode_nfo(bytes):
        return 'decoded ' + bytes.decode('utf-8')

    mocks.attach_mock(mocker.patch('upsies.utils.string.decode_nfo', side_effect=mock_decode_nfo), 'decode_nfo')

    return mocks

def test_read_nfo__no_nfos_found(read_nfo_mocks, mocker):
    mocks = read_nfo_mocks
    directory = 'path/to'

    mocks.file_list.return_value = []

    return_value = string.read_nfo(directory)
    assert return_value is None
    assert mocks.mock_calls == [
        call.file_list('path/to', extensions=('nfo', 'NFO')),
    ]

def test_read_nfo__getsize_does_not_raise(read_nfo_mocks, mocker):
    mocks = read_nfo_mocks
    directory = 'path/to'

    mocks.file_list.return_value = [
        'path/to/unreadable.nfo',
        'path/to/toobig.nfo',
        'path/to/good.nfo',
        'path/to/surplus.nfo',
    ]

    def mock_getsize(nfo_filepath):
        if 'unreadable' in nfo_filepath:
            raise OSError(errno.EACCES, 'Permission denied')
        elif 'toobig' in nfo_filepath:
            return max_nfo_size + 1
        else:
            return max_nfo_size

    mocks.getsize.side_effect = mock_getsize

    return_value = string.read_nfo(directory)
    assert return_value == 'decoded content of path/to/good.nfo'
    assert mocks.mock_calls == [
        call.file_list('path/to', extensions=('nfo', 'NFO')),
        call.getsize('path/to/unreadable.nfo'),
        call.getsize('path/to/toobig.nfo'),
        call.getsize('path/to/good.nfo'),
        call.open('path/to/good.nfo', 'rb'),
        call.decode_nfo(b'content of path/to/good.nfo'),
    ]

def test_read_nfo__getsize_raises(read_nfo_mocks, mocker):
    mocks = read_nfo_mocks
    directory = 'path/to'

    mocks.file_list.return_value = [
        'path/to/unreadable.nfo',
        'path/to/toobig.nfo',
    ]

    def mock_getsize(nfo_filepath):
        if 'unreadable' in nfo_filepath:
            raise OSError(errno.EACCES, 'Permission denied')
        elif 'toobig' in nfo_filepath:
            return max_nfo_size + 1
        else:
            return max_nfo_size

    mocks.getsize.side_effect = mock_getsize

    with pytest.raises(errors.ContentError, match=r'^Failed to read nfo: Permission denied$'):
        string.read_nfo(directory)

    assert mocks.mock_calls == [
        call.file_list('path/to', extensions=('nfo', 'NFO')),
        call.getsize('path/to/unreadable.nfo'),
        call.getsize('path/to/toobig.nfo'),
    ]

def test_read_nfo__open_does_not_raise(read_nfo_mocks, mocker):
    mocks = read_nfo_mocks
    directory = 'path/to'

    mocks.file_list.return_value = [
        'path/to/unreadable.nfo',
        'path/to/good.nfo',
        'path/to/surplus.nfo',
    ]

    def mock_open(nfo_filepath, mode):
        if 'unreadable' in nfo_filepath:
            raise OSError(errno.EACCES, 'Permission denied')
        else:
            return Mock(
                __enter__=Mock(
                    return_value=Mock(
                        read=Mock(return_value=f'content of {nfo_filepath}'.encode('utf-8')),
                    ),
                ),
                __exit__=Mock(return_value=False),
            )

    mocks.open.side_effect = mock_open

    return_value = string.read_nfo(directory)
    assert return_value == 'decoded content of path/to/good.nfo'
    assert mocks.mock_calls == [
        call.file_list('path/to', extensions=('nfo', 'NFO')),
        call.getsize('path/to/unreadable.nfo'),
        call.open('path/to/unreadable.nfo', 'rb'),
        call.getsize('path/to/good.nfo'),
        call.open('path/to/good.nfo', 'rb'),
        call.decode_nfo(b'content of path/to/good.nfo'),
    ]


def test_read_nfo__open_raises(read_nfo_mocks, mocker):
    mocks = read_nfo_mocks
    directory = 'path/to'

    mocks.file_list.return_value = [
        'path/to/unreadable.nfo',
    ]

    def mock_open(nfo_filepath, mode):
        if 'unreadable' in nfo_filepath:
            raise OSError(errno.EACCES, 'Permission denied')
        else:
            return Mock(
                __enter__=Mock(
                    return_value=Mock(
                        read=Mock(return_value=f'content of {nfo_filepath}'.encode('utf-8')),
                    ),
                ),
                __exit__=Mock(return_value=False),
            )

    mocks.open.side_effect = mock_open

    with pytest.raises(errors.ContentError, match=r'^Failed to read nfo: Permission denied$'):
        string.read_nfo(directory)

    assert mocks.mock_calls == [
        call.file_list('path/to', extensions=('nfo', 'NFO')),
        call.getsize('path/to/unreadable.nfo'),
        call.open('path/to/unreadable.nfo', 'rb'),
    ]


@pytest.mark.parametrize(
    argnames='bytes, exp_string',
    argvalues=(
        (b'M\x94\x94', 'Möö'),  # CP437
        (b'M\xC3\xB6\xC3\xB6', 'Möö'),  # UTF-8
    ),
)
def test_decode_nfo(bytes, exp_string):
    assert string.decode_nfo(bytes) == exp_string


@pytest.mark.parametrize(
    argnames='text, exp_text',
    argvalues=(
        ('THIS is a sTRING', 'This Is A String'),
        ("this is jeremy's string", "This Is Jeremy's String"),
        (' this\tstring  has   weird    spacing  ', ' This\tString  Has   Weird    Spacing  '),
    ),
)
def test_capitalize(text, exp_text):
    assert string.capitalize(text) == exp_text


@pytest.mark.parametrize(
    argnames='ratings, exp_string',
    argvalues=(
        ((-0.0, -0.1, -10.5), '☆☆☆☆☆☆☆☆☆☆'),
        ((0, 0.1, 0.2, 0.3), '☆☆☆☆☆☆☆☆☆☆'), ((0.4, 0.5, 0.6), '⯪☆☆☆☆☆☆☆☆☆'), ((0.7, 0.8, 0.9), '★☆☆☆☆☆☆☆☆☆'),
        ((1, 1.1, 1.2, 1.3), '★☆☆☆☆☆☆☆☆☆'), ((1.4, 1.5, 1.6), '★⯪☆☆☆☆☆☆☆☆'), ((1.7, 1.8, 1.9), '★★☆☆☆☆☆☆☆☆'),
        ((2, 2.1, 2.2, 2.3), '★★☆☆☆☆☆☆☆☆'), ((2.4, 2.5, 2.6), '★★⯪☆☆☆☆☆☆☆'), ((2.7, 2.8, 2.9), '★★★☆☆☆☆☆☆☆'),
        ((3, 3.1, 3.2, 3.3), '★★★☆☆☆☆☆☆☆'), ((3.4, 3.5, 3.6), '★★★⯪☆☆☆☆☆☆'), ((3.7, 3.8, 3.9), '★★★★☆☆☆☆☆☆'),
        ((4, 4.1, 4.2, 4.3), '★★★★☆☆☆☆☆☆'), ((4.4, 4.5, 4.6), '★★★★⯪☆☆☆☆☆'), ((4.7, 4.8, 4.9), '★★★★★☆☆☆☆☆'),
        ((5, 5.1, 5.2, 5.3), '★★★★★☆☆☆☆☆'), ((5.4, 5.5, 5.6), '★★★★★⯪☆☆☆☆'), ((5.7, 5.8, 5.9), '★★★★★★☆☆☆☆'),
        ((6, 6.1, 6.2, 6.3), '★★★★★★☆☆☆☆'), ((6.4, 6.5, 6.6), '★★★★★★⯪☆☆☆'), ((6.7, 6.8, 6.9), '★★★★★★★☆☆☆'),
        ((7, 7.1, 7.2, 7.3), '★★★★★★★☆☆☆'), ((7.4, 7.5, 7.6), '★★★★★★★⯪☆☆'), ((7.7, 7.8, 7.9), '★★★★★★★★☆☆'),
        ((8, 8.1, 8.2, 8.3), '★★★★★★★★☆☆'), ((8.4, 8.5, 8.6), '★★★★★★★★⯪☆'), ((8.7, 8.8, 8.9), '★★★★★★★★★☆'),
        ((9, 9.1, 9.2, 9.3), '★★★★★★★★★☆'), ((9.4, 9.5, 9.6), '★★★★★★★★★⯪'), ((9.7, 9.8, 9.9), '★★★★★★★★★★'),
        ((10, 10.1, 10.5, 12), '★★★★★★★★★★'),
    ),
)
def test_star_rating(ratings, exp_string):
    for rating in ratings:
        assert string.star_rating(rating) == exp_string


def test_remove_prefix():
    assert string.remove_prefix('com.domain.www', 'com.') == 'domain.www'
    assert string.remove_prefix('com.domain.www', 'moc.') == 'com.domain.www'


def test_remove_suffix():
    assert string.remove_suffix('www.domain.com', '.com') == 'www.domain'
    assert string.remove_suffix('www.domain.com', '.moc') == 'www.domain.com'


@pytest.mark.parametrize(
    argnames='fstring, local_objects, exp_result',
    argvalues=(
        ('foo {add(1, 2, 3) * 2} bar', {'add': lambda *n: sum(n)}, 'foo 12 bar'),
        ('foo {add(1, 2, 3) * 2} bar', {}, NameError("name 'add' is not defined")),
    ),
)
def test_evaluate_fstring(fstring, local_objects, exp_result):
    locals().update(local_objects)

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            string.evaluate_fstring(fstring)
    else:
        assert string.evaluate_fstring(fstring) == exp_result
