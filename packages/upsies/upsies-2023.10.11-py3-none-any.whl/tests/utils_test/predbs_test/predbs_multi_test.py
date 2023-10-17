import asyncio
import re
from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies import errors
from upsies.utils.predbs import SceneCheckResult, multi


def test_with_custom_predbs(mocker):
    predb_mock = mocker.patch('upsies.utils.predbs.predb')
    predbs = (Mock(), Mock(), Mock())
    multipredb = multi.MultiPredbApi(predbs)
    assert multipredb._predbs == predbs
    assert predb_mock.call_args_list == []

def test_with_default_predbs(mocker):
    exp_predbs = [
        Mock(name=name)
        for name in multi.MultiPredbApi.DEFAULT_PREDB_NAMES
    ]
    predb_mock = mocker.patch('upsies.utils.predbs.predb', side_effect=exp_predbs)
    multipredb = multi.MultiPredbApi()
    assert multipredb._predbs == exp_predbs
    assert predb_mock.call_args_list == [
        call('srrdb'),
        # call('corruptnet'),
        # call('predbovh'),
        # call('predbclub'),
        call('predbde'),
    ]


@pytest.fixture
def multipredb():
    predbs = [Mock(), Mock(), Mock()]
    predbs[0].configure_mock(name='foo')
    predbs[1].configure_mock(name='bar')
    predbs[2].configure_mock(name='baz')
    return multi.MultiPredbApi(predbs=predbs)


def test_predbs(multipredb, mocker):
    mocker.patch.object(multipredb, '_predbs', ['mock predb 1', 'mock predb 2'])
    assert multipredb.predbs == ('mock predb 1', 'mock predb 2')


@pytest.mark.asyncio
async def test_call(multipredb, mocker):
    predb = Mock(my_method=AsyncMock(return_value='my response'))

    return_value = await multipredb._call(predb, 'my_method', 123, this='that')
    assert return_value == 'my response'
    assert predb.my_method.call_args_list == [call(123, this='that')]


@pytest.mark.parametrize(
    argnames='exceptions, method_name, exp_exception',
    argvalues=(
        (
            [],
            'my_method',
            NotImplementedError('foo|bar|baz.my_method'),
        ),
        (
            [errors.RequestError('only error')],
            'my_method',
            errors.RequestError('only error'),
        ),
        (
            [errors.RequestError('error one'), errors.RequestError('error two')],
            'my_method',
            errors.RequestError('All queries failed: error one, error two'),
        ),
    ),
    ids=lambda v: repr(v),
)
def test_raise(exceptions, method_name, exp_exception, multipredb, mocker):
    with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
        multipredb._raise(exceptions, method_name)


class MockPredb(str):
    def __init__(self, name):
        self.name = name

@pytest.mark.parametrize(
    argnames='method_name, args, kwargs, predbs, call_side_effects, exp_result, exp_mock_calls',
    argvalues=(
        pytest.param(
            'mymethod', ('foo',), {'this': 'that'},
            [MockPredb('predb1'), MockPredb('predb2'), MockPredb('predb3'), MockPredb('predb4')],
            [
                NotImplementedError('this is not implemented'),
                errors.RequestError('Service is down'),
                'here is your response',
                NotImplementedError('that is not implemented'),
            ],
            'here is your response',
            [
                call('predb1', 'mymethod', 'foo', this='that'),
                call('predb2', 'mymethod', 'foo', this='that'),
                call('predb3', 'mymethod', 'foo', this='that'),
            ],
            id='First good response is returned',
        ),

        pytest.param(
            'mymethod', ('foo',), {'bar': 'baz'},
            [MockPredb('predb1'), MockPredb('predb2'), MockPredb('predb3'), MockPredb('predb4')],
            [
                NotImplementedError('This is not implemented'),
                errors.RequestError('Service is down'),
                NotImplementedError('This is also not implemented'),
                NotImplementedError('That is not implemented'),
            ],
            errors.RequestError(
                'All queries failed: '
                'This is not implemented, '
                'Service is down, '
                'This is also not implemented, '
                'That is not implemented'
            ),
            [
                call('predb1', 'mymethod', 'foo', bar='baz'),
                call('predb2', 'mymethod', 'foo', bar='baz'),
                call('predb3', 'mymethod', 'foo', bar='baz'),
                call('predb4', 'mymethod', 'foo', bar='baz'),
            ],
            id='All raise',
        ),
    ),
)
@pytest.mark.asyncio
async def test_for_each_predb(method_name, args, kwargs, predbs, call_side_effects, exp_result, exp_mock_calls, multipredb, mocker):
    mocker.patch.object(multipredb, '_call', side_effect=call_side_effects)
    mocker.patch.object(multipredb, '_predbs', predbs)

    if isinstance(exp_result, Exception):
        with pytest.raises(type(exp_result), match=rf'^{re.escape(str(exp_result))}$'):
            await multipredb._for_each_predb(method_name, *args, **kwargs)
    else:
        return_value = await multipredb._for_each_predb(method_name, *args, **kwargs)
        assert return_value == exp_result

    assert multipredb._call.call_args_list == exp_mock_calls


@pytest.mark.asyncio
async def test_for_all_predbs(multipredb, mocker):
    predbs = [MockPredb(name) for name in 'abcde']
    mocker.patch.object(multipredb, '_predbs', predbs)

    async def call_side_effect(predb, method_name, *args, **kwargs):
        if predb.name == 'a':
            await asyncio.sleep(0.3)
            raise errors.RequestError('4: a')
        elif predb.name == 'b':
            await asyncio.sleep(0.0)
            raise NotImplementedError('1: b')
        elif predb.name == 'c':
            await asyncio.sleep(0.2)
            return '3: c: result'
        elif predb.name == 'd':
            await asyncio.sleep(0.4)
            return '5: d: result'
        elif predb.name == 'e':
            await asyncio.sleep(0.1)
            return '2: e: result'
        else:
            raise RuntimeError(f'Unexpected predb: {predb.name}')

    mocker.patch.object(multipredb, '_call', side_effect=call_side_effect)

    method_name = 'mymethod'
    args = ('foo',)
    kwargs = {'bar': 'baz'}

    exp_results = [
        NotImplementedError('1: b'),
        '2: e: result',
        '3: c: result',
        errors.RequestError('4: a'),
        '5: d: result',
    ]

    async for result in multipredb._for_all_predbs(method_name, *args, **kwargs):
        exp_result = exp_results.pop(0)
        assert str(result) == str(exp_result)

    assert multipredb._call.call_args_list == [
        call(predbs[0], method_name, *args, **kwargs),
        call(predbs[1], method_name, *args, **kwargs),
        call(predbs[2], method_name, *args, **kwargs),
        call(predbs[3], method_name, *args, **kwargs),
        call(predbs[4], method_name, *args, **kwargs),
    ]


@pytest.fixture
def multipredb_for_verify_release(multipredb, mocker):
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(multipredb, 'search'), 'search')
    mocks.attach_mock(mocker.patch.object(multipredb, '_verify_release'), '_verify_release')
    mocks.attach_mock(mocker.patch.object(multipredb, '_verify_release_per_file'), '_verify_release_per_file')
    return multipredb, mocks

@pytest.mark.asyncio
async def test_verify_release_gets_release_name(multipredb_for_verify_release):
    multipredb, mocks = multipredb_for_verify_release
    content_path = 'path/to/Mock.Release'
    release_name = 'Mock.Release'

    return_value = await multipredb.verify_release(content_path, release_name)
    assert return_value is mocks._verify_release.return_value

    assert mocks.mock_calls == [
        call._verify_release(content_path, release_name),
    ]

@pytest.mark.asyncio
async def test_verify_release_gets_no_release_name_and_finds_no_matching_scene_release(multipredb_for_verify_release):
    multipredb, mocks = multipredb_for_verify_release
    content_path = 'path/to/Mock.Release'
    mocks.search.return_value = ()

    return_value = await multipredb.verify_release(content_path)
    assert return_value == (SceneCheckResult.false, ())

    assert mocks.mock_calls == [
        call.search(content_path),
    ]

@pytest.mark.asyncio
async def test_verify_release_finds_valid_scene_release(multipredb_for_verify_release):
    multipredb, mocks = multipredb_for_verify_release
    content_path = 'path/to/Mock.Release'
    verify_release_results = {
        'The.Foo.2000.x264-AAA': (SceneCheckResult.false, ()),
        'The.Foo.2000.x264-BBB': (SceneCheckResult.unknown, ()),
        'The.Foo.2000.x264-CCC': (SceneCheckResult.true, (errors.SceneRenamedError(original_name='foo', existing_name='bar'),)),
        'The.Foo.2000.x264-DDD': (SceneCheckResult.true, ()),
        'The.Foo.2000.x264-EEE': (SceneCheckResult.true, (errors.SceneFileSizeError('foo', original_size=123, existing_size=456),)),
    }
    mocks.search.return_value = tuple(verify_release_results.keys())
    mocks._verify_release.side_effect = tuple(verify_release_results.values())

    return_value = await multipredb.verify_release(content_path)
    assert return_value == (SceneCheckResult.true, ())

    assert mocks.mock_calls == [
        call.search(content_path),
        call._verify_release(content_path, 'The.Foo.2000.x264-AAA'),
        call._verify_release(content_path, 'The.Foo.2000.x264-BBB'),
        call._verify_release(content_path, 'The.Foo.2000.x264-CCC'),
        call._verify_release(content_path, 'The.Foo.2000.x264-DDD'),
    ]

@pytest.mark.asyncio
async def test_verify_release_finds_only_nonscene_releases(multipredb_for_verify_release):
    multipredb, mocks = multipredb_for_verify_release
    content_path = 'path/to/Mock.Release'
    verify_release_results = {
        'The.Foo.2000.x264-AAA': (SceneCheckResult.false, ()),
        'The.Foo.2000.x264-BBB': (SceneCheckResult.unknown, ()),
    }
    mocks.search.return_value = tuple(verify_release_results.keys())
    mocks._verify_release.side_effect = tuple(verify_release_results.values())

    return_value = await multipredb.verify_release(content_path)
    assert return_value is mocks._verify_release_per_file.return_value

    assert mocks.mock_calls == [
        call.search(content_path),
        call._verify_release(content_path, 'The.Foo.2000.x264-AAA'),
        call._verify_release(content_path, 'The.Foo.2000.x264-BBB'),
        call._verify_release_per_file(content_path),
    ]

@pytest.mark.asyncio
async def test_verify_release_finds_only_scene_releases_with_exceptions(multipredb_for_verify_release):
    multipredb, mocks = multipredb_for_verify_release
    content_path = 'path/to/Mock.Release'
    verify_release_results = {
        'The.Foo.2000.x264-AAA': (SceneCheckResult.true, (errors.SceneRenamedError(original_name='foo', existing_name='bar'),)),
        'The.Foo.2000.x264-BBB': (SceneCheckResult.unknown, ()),
        'The.Foo.2000.x264-CCC': (SceneCheckResult.true, (errors.SceneFileSizeError('foo', original_size=123, existing_size=456),)),
    }
    mocks.search.return_value = tuple(verify_release_results.keys())
    mocks._verify_release.side_effect = tuple(verify_release_results.values())

    return_value = await multipredb.verify_release(content_path)
    assert return_value is mocks._verify_release_per_file.return_value

    assert mocks.mock_calls == [
        call.search(content_path),
        call._verify_release(content_path, 'The.Foo.2000.x264-AAA'),
        call._verify_release(content_path, 'The.Foo.2000.x264-BBB'),
        call._verify_release(content_path, 'The.Foo.2000.x264-CCC'),
        call._verify_release_per_file(content_path),
    ]


@pytest.fixture
def multipredb_for__verify_release(multipredb, mocker):
    mocks = Mock()
    mocks.attach_mock(
        mocker.patch.object(multipredb, 'is_scene_release'),
        'is_scene_release',
    )
    mocks.attach_mock(
        mocker.patch.object(multipredb, 'verify_release_name'),
        'verify_release_name',
    )
    mocks.attach_mock(
        mocker.patch.object(multipredb, 'verify_release_files'),
        'verify_release_files',
    )
    return multipredb, mocks

@pytest.mark.asyncio
async def test__verify_release_gets_nonscene_release_name(multipredb_for__verify_release):
    multipredb, mocks = multipredb_for__verify_release
    mocks.is_scene_release.return_value = SceneCheckResult.false

    is_scene, exceptions = await multipredb._verify_release('mock/path', 'Mock.Release')
    assert is_scene is SceneCheckResult.false
    assert exceptions == ()
    assert mocks.mock_calls == [
        call.is_scene_release('Mock.Release'),
    ]

@pytest.mark.asyncio
async def test__verify_release_gets_release_with_unknown_scene_status(multipredb_for__verify_release):
    multipredb, mocks = multipredb_for__verify_release
    mocks.is_scene_release.return_value = SceneCheckResult.unknown

    is_scene, exceptions = await multipredb._verify_release('mock/path', 'Mock.Release')
    assert is_scene is SceneCheckResult.unknown
    assert exceptions == ()
    assert mocks.mock_calls == [
        call.is_scene_release('Mock.Release'),
    ]

@pytest.mark.asyncio
async def test__verify_release_gets_wrong_release_name(multipredb_for__verify_release):
    multipredb, mocks = multipredb_for__verify_release
    mocks.is_scene_release.return_value = SceneCheckResult.true
    mocks.verify_release_name.side_effect = errors.SceneRenamedError(original_name='foo', existing_name='bar')
    mocks.verify_release_files.return_value = ()

    is_scene, exceptions = await multipredb._verify_release('mock/path', 'Mock.Release')
    assert is_scene is SceneCheckResult.true
    assert exceptions == (errors.SceneRenamedError(original_name='foo', existing_name='bar'),)
    assert mocks.mock_calls == [
        call.is_scene_release('Mock.Release'),
        call.verify_release_name('mock/path', 'Mock.Release'),
        call.verify_release_files('mock/path', 'Mock.Release'),
    ]

@pytest.mark.asyncio
async def test__verify_release_gets_wrong_release_files(multipredb_for__verify_release):
    multipredb, mocks = multipredb_for__verify_release
    mocks.is_scene_release.return_value = SceneCheckResult.true
    mocks.verify_release_files.return_value = (
        errors.SceneFileSizeError('foo', original_size=123, existing_size=456),
        errors.SceneFileSizeError('bar', original_size=100, existing_size=200),
    )

    is_scene, exceptions = await multipredb._verify_release('mock/path', 'Mock.Release')
    assert is_scene is SceneCheckResult.true
    assert exceptions == (
        errors.SceneFileSizeError('foo', original_size=123, existing_size=456),
        errors.SceneFileSizeError('bar', original_size=100, existing_size=200),
    )
    assert mocks.mock_calls == [
        call.is_scene_release('Mock.Release'),
        call.verify_release_name('mock/path', 'Mock.Release'),
        call.verify_release_files('mock/path', 'Mock.Release'),
    ]

@pytest.mark.asyncio
async def test__verify_release_gets_wrong_release_name_and_wrong_files(multipredb_for__verify_release):
    multipredb, mocks = multipredb_for__verify_release
    mocks.is_scene_release.return_value = SceneCheckResult.true
    mocks.verify_release_name.side_effect = errors.SceneRenamedError(original_name='foo', existing_name='bar')
    mocks.verify_release_files.return_value = (
        errors.SceneFileSizeError('foo', original_size=123, existing_size=456),
        errors.SceneFileSizeError('bar', original_size=100, existing_size=200),
    )

    is_scene, exceptions = await multipredb._verify_release('mock/path', 'Mock.Release')
    assert is_scene is SceneCheckResult.true
    assert exceptions == (
        errors.SceneRenamedError(original_name='foo', existing_name='bar'),
        errors.SceneFileSizeError('foo', original_size=123, existing_size=456),
        errors.SceneFileSizeError('bar', original_size=100, existing_size=200),
    )
    assert mocks.mock_calls == [
        call.is_scene_release('Mock.Release'),
        call.verify_release_name('mock/path', 'Mock.Release'),
        call.verify_release_files('mock/path', 'Mock.Release'),
    ]


@pytest.mark.parametrize(
    argnames='content_path, mock_data, exp_mock_calls, exp_is_scene_release, exp_exceptions',
    argvalues=(
        pytest.param(
            'path/to/content',
            {
                'foo.mkv': (
                    {'release_name': 'Foo-AAA', 'is_scene_release': SceneCheckResult.false, 'exceptions': ()},
                    {'release_name': 'Foo-BBB', 'is_scene_release': SceneCheckResult.true, 'exceptions': ()},
                ),
                'bar.mp4': (
                    {'release_name': 'Bar-AAA', 'is_scene_release': SceneCheckResult.true, 'exceptions': ()},
                    {'release_name': 'Bar-BBB', 'is_scene_release': SceneCheckResult.true,
                     'exceptions': (errors.SceneError('never found'),)},
                ),
            },
            [
                call.search('foo.mkv'),
                call._verify_release('foo.mkv', 'Foo-AAA'),
                call._verify_release('foo.mkv', 'Foo-BBB'),
                call.search('bar.mp4'),
                call._verify_release('bar.mp4', 'Bar-AAA'),
            ],
            SceneCheckResult.true,
            (),
            id='Verification is stopped after first match is found',
        ),

        pytest.param(
            'path/to/content',
            {
                'foo.mkv': (
                    {'release_name': 'Foo-AAA', 'is_scene_release': SceneCheckResult.false, 'exceptions': ()},
                    {'release_name': 'Foo-BBB', 'is_scene_release': SceneCheckResult.unknown, 'exceptions': ()},
                ),
                'bar.mp4': (
                    {'release_name': 'Bar-AAA', 'is_scene_release': SceneCheckResult.true, 'exceptions': ()},
                    {'release_name': 'Bar-BBB', 'is_scene_release': SceneCheckResult.true,
                     'exceptions': (errors.SceneError('never found'),)},
                ),
            },
            [
                call.search('foo.mkv'),
                call._verify_release('foo.mkv', 'Foo-AAA'),
                call._verify_release('foo.mkv', 'Foo-BBB'),
                call.search('bar.mp4'),
                call._verify_release('bar.mp4', 'Bar-AAA'),
            ],
            SceneCheckResult.unknown,
            (),
            id='One scene check is unknown',
        ),

        pytest.param(
            'path/to/content',
            {
                'foo.mkv': (
                    {'release_name': 'Foo-AAA', 'is_scene_release': SceneCheckResult.false, 'exceptions': ()},
                    {'release_name': 'Foo-BBB', 'is_scene_release': SceneCheckResult.false, 'exceptions': ()},
                ),
                'bar.mp4': (
                    {'release_name': 'Bar-AAA', 'is_scene_release': SceneCheckResult.false, 'exceptions': ()},
                    {'release_name': 'Bar-BBB', 'is_scene_release': SceneCheckResult.false, 'exceptions': ()},
                ),
            },
            [
                call.search('foo.mkv'),
                call._verify_release('foo.mkv', 'Foo-AAA'),
                call._verify_release('foo.mkv', 'Foo-BBB'),
                call.search('bar.mp4'),
                call._verify_release('bar.mp4', 'Bar-AAA'),
                call._verify_release('bar.mp4', 'Bar-BBB'),
            ],
            SceneCheckResult.false,
            (),
            id='All scene checks are false',
        ),

        pytest.param(
            'path/to/content',
            {
                'foo.mkv': (
                    {'release_name': 'Foo-AAA', 'is_scene_release': SceneCheckResult.true, 'exceptions': (errors.SceneError('foo!'),)},
                    {'release_name': 'Foo-BBB', 'is_scene_release': SceneCheckResult.true, 'exceptions': ()},
                ),
                'bar.mp4': (
                    {'release_name': 'Bar-AAA', 'is_scene_release': SceneCheckResult.true, 'exceptions': ()},
                    {'release_name': 'Bar-BBB', 'is_scene_release': SceneCheckResult.true, 'exceptions': ()},
                ),
            },
            [
                call.search('foo.mkv'),
                call._verify_release('foo.mkv', 'Foo-AAA'),
                call._verify_release('foo.mkv', 'Foo-BBB'),
                call.search('bar.mp4'),
                call._verify_release('bar.mp4', 'Bar-AAA'),
            ],
            SceneCheckResult.true,
            (errors.SceneError('foo!'),),
            id='One scene check returns exceptions',
        ),

        pytest.param(
            'path/to/content',
            {
                'foo.mkv': (
                    {'release_name': 'Foo-AAA', 'is_scene_release': SceneCheckResult.true, 'exceptions': (errors.SceneError('foo!'),)},
                    {'release_name': 'Foo-BBB', 'is_scene_release': SceneCheckResult.true, 'exceptions': ()},
                ),
                'bar.mp4': (
                    {'release_name': 'Bar-AAA', 'is_scene_release': SceneCheckResult.false, 'exceptions': ()},
                    {'release_name': 'Bar-BBB', 'is_scene_release': SceneCheckResult.true, 'exceptions': (errors.SceneError('bar!'),)},
                ),
            },
            [
                call.search('foo.mkv'),
                call._verify_release('foo.mkv', 'Foo-AAA'),
                call._verify_release('foo.mkv', 'Foo-BBB'),
                call.search('bar.mp4'),
                call._verify_release('bar.mp4', 'Bar-AAA'),
                call._verify_release('bar.mp4', 'Bar-BBB'),
            ],
            SceneCheckResult.true,
            (errors.SceneError('foo!'), errors.SceneError('bar!'), ),
            id='Multiple scene checks return exceptions',
        ),
    ),
)
@pytest.mark.asyncio
async def test_verify_release_per_file(content_path, mock_data, exp_mock_calls, exp_is_scene_release, exp_exceptions, multipredb, mocker):
    mocks = Mock()

    mocker.patch('upsies.utils.fs.file_list', Mock(
        return_value=mock_data.keys(),
    ))
    mocks.attach_mock(
        mocker.patch.object(multipredb, 'search', AsyncMock(side_effect=(
            tuple(data['release_name'] for data in datas)
            for datas in mock_data.values()
        ))),
        'search',
    )
    mocks.attach_mock(
        mocker.patch.object(multipredb, '_verify_release', AsyncMock(side_effect=tuple(
            (data['is_scene_release'], data['exceptions'])
            for datas in mock_data.values()
            for data in datas
        ))),
        '_verify_release',
    )

    is_scene_release, exceptions = await multipredb._verify_release_per_file(content_path)
    assert is_scene_release == exp_is_scene_release
    assert exceptions == exp_exceptions
    assert mocks.mock_calls == exp_mock_calls
