import re

import pytest

from upsies import errors


def error_classes():
    clses = []
    for name in dir(errors):
        if not name.startswith('_'):
            cls = getattr(errors, name)
            if isinstance(cls, type) and issubclass(cls, Exception):
                clses.append(cls)
    return clses


@pytest.mark.parametrize(
    argnames='cls',
    argvalues=error_classes(),
)
def test_equality(cls):
    try:
        assert cls('foo') == cls('foo')
        assert cls('foo') != cls('bar')
        assert cls('foo') != ValueError('foo')
    # Some exceptions require more arguments
    except TypeError:
        pass


def test_RequestError_url():
    e = errors.RequestError('foo', url='http://foo')
    assert e.url == 'http://foo'

def test_RequestError_headers():
    e = errors.RequestError('foo', headers={'a': 1, 'b': 2})
    assert e.headers == {'a': 1, 'b': 2}

def test_RequestError_status_code():
    e = errors.RequestError('foo', status_code=123)
    assert e.status_code == 123

def test_RequestError_text():
    e = errors.RequestError('foo', text='Error 404')
    assert e.text == 'Error 404'

@pytest.mark.parametrize(
    argnames='text, default, exp_result',
    argvalues=(
        ('foo', errors._NO_DEFAULT_VALUE, errors.RequestError('Malformed JSON: foo: Expecting value: line 1 column 1 (char 0)')),
        ('foo', None, None),
        ('foo', 'asdf', 'asdf'),
        ('"foo"', None, 'foo'),
        ('["foo", "bar"]', 'asdf', ['foo', 'bar']),
        ('["foo", "bar", baz]', 'asdf', 'asdf'),
    ),
)
def test_RequestError_json(text, default, exp_result):
    e = errors.RequestError('foo', text=text)
    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            e.json(default=default)
    else:
        assert e.json(default=default) == exp_result


def test_SubprocessError():
    e = TypeError('foo')
    traceback = 'mock traceback'
    subproc_e = errors.SubprocessError(e, traceback)
    assert subproc_e.original_traceback == 'Subprocess traceback:\nmock traceback'


def test_SceneRenamedError_name_attributes():
    e = errors.SceneRenamedError(original_name='foo', existing_name='bar')
    assert e.original_name == 'foo'
    assert e.existing_name == 'bar'


def test_SceneFileSizeError():
    e = errors.SceneFileSizeError(
        filename='foo',
        original_size=123,
        existing_size=124,
    )
    assert e.filename == 'foo'
    assert e.original_size == 123
    assert e.existing_size == 124


def test_SceneMissingInfoError():
    e = errors.SceneMissingInfoError('foo.mkv')
    assert str(e) == 'Missing information: foo.mkv'


@pytest.mark.parametrize(
    argnames='files, exp_msg',
    argvalues=(
        (
            [],
            (
                'Potential duplicate files found'
            ),
        ),
        (
            ['a.mkv'],
            (
                '1 potential duplicate file found:\n'
                ' - a.mkv'
            ),
        ),
        (
            ['a.mkv', 'b.mkv'],
            (
                '2 potential duplicate files found:\n'
                ' - a.mkv\n'
                ' - b.mkv'
            ),
        ),
    ),
    ids=lambda v: repr(v),
)
def test_FoundDupeError(files, exp_msg):
    e = errors.FoundDupeError(files)
    assert str(e) == exp_msg


def test_AnnounceUrlNotsetError():
    tracker = 'mock tracker'
    e = errors.AnnounceUrlNotSetError(tracker=tracker)
    assert str(e) == 'Announce URL is not set'
    assert e.tracker is tracker
