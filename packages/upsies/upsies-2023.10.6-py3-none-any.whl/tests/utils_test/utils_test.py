import asyncio
import re
from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies import errors, utils


def test_submodules_finds_modules_and_packages(mocker):
    mocker.patch('os.listdir', return_value=(
        '_this_is_private',
        'this_is_a_package',
        'this_is_a_module.py',
        'this_is_something_else.foo',
    ))
    import_mock = mocker.patch('importlib.import_module', side_effect=(1, 2, 3, 4, 5))
    assert set(utils.submodules('asdf')) == {1, 2}
    assert import_mock.call_args_list == [
        call(name='.this_is_a_package', package='asdf'),
        call(name='.this_is_a_module', package='asdf'),
    ]


def test_subclasses():
    from aiobtclientapi.clients import APIBase, deluge, qbittorrent, rtorrent, transmission
    subclses = utils.subclasses(
        basecls=APIBase,
        modules={deluge, qbittorrent, rtorrent, transmission},
    )
    assert subclses == {
        deluge.DelugeAPI,
        qbittorrent.QbittorrentAPI,
        rtorrent.RtorrentAPI,
        transmission.TransmissionAPI,
    }


def test_closest_number():
    assert utils.closest_number(5, ()) == 0
    assert utils.closest_number(5, (), default=123) == 123

    numbers = (10, 20, 30)

    for n in (-10, 0, 9, 10, 11, 14):
        assert utils.closest_number(n, numbers) == 10
    for n in (16, 19, 20, 21, 24):
        assert utils.closest_number(n, numbers) == 20
    for n in range(26, 50):
        assert utils.closest_number(n, numbers) == 30

    for n in range(0, 50):
        with pytest.raises(ValueError, match=r'^No number equal to or below 9: \(10, 20, 30\)$'):
            utils.closest_number(n, numbers, max=9)

    for n in range(0, 50):
        assert utils.closest_number(n, numbers, max=10) == 10

    for n in range(0, 16):
        assert utils.closest_number(n, numbers, max=20) == 10
    for n in range(16, 50):
        assert utils.closest_number(n, numbers, max=20) == 20


def test_CaseInsensitiveString_equality():
    assert utils.CaseInsensitiveString('Foo') == 'foo'
    assert utils.CaseInsensitiveString('fOo') == 'FOO'
    assert utils.CaseInsensitiveString('foO') == 'foo'
    assert utils.CaseInsensitiveString('foo') != 'fooo'

def test_CaseInsensitiveString_identity():
    assert utils.CaseInsensitiveString('Foo') in ('foo', 'bar', 'baz')
    assert utils.CaseInsensitiveString('fOo') in ('FOO', 'BAR', 'BAZ')
    assert utils.CaseInsensitiveString('foO') not in ('fooo', 'bar', 'baz')

def test_CaseInsensitiveString_lt():
    assert utils.CaseInsensitiveString('foo') < 'Fooo'

def test_CaseInsensitiveString_le():
    assert utils.CaseInsensitiveString('foo') <= 'Foo'

def test_CaseInsensitiveString_gt():
    assert utils.CaseInsensitiveString('Fooo') > 'foo'

def test_CaseInsensitiveString_ge():
    assert utils.CaseInsensitiveString('Foo') >= 'foo'


def test_MonitoredList_getitem():
    lst = utils.MonitoredList((1, 2, 3), callback=Mock())
    assert lst[0] == 1
    assert lst[1] == 2
    assert lst[2] == 3

def test_MonitoredList_setitem():
    cb = Mock()
    lst = utils.MonitoredList((1, 2, 3), callback=cb)
    assert cb.call_args_list == []
    lst[0] = 100
    assert cb.call_args_list == [call(lst)]
    assert lst == [100, 2, 3]

def test_MonitoredList_delitem():
    cb = Mock()
    lst = utils.MonitoredList((1, 2, 3), callback=cb)
    assert cb.call_args_list == []
    del lst[1]
    assert cb.call_args_list == [call(lst)]
    assert lst == [1, 3]

def test_MonitoredList_insert():
    cb = Mock()
    lst = utils.MonitoredList((1, 2, 3), callback=cb)
    assert cb.call_args_list == []
    lst.insert(1, 1.5)
    assert cb.call_args_list == [call(lst)]
    assert lst == [1, 1.5, 2, 3]

def test_MonitoredList_len():
    lst = utils.MonitoredList((1, 2, 3), callback=Mock())
    assert len(lst) == 3

def test_MonitoredList_equality():
    lst = utils.MonitoredList((1, 2, 3), callback=Mock())
    assert lst == [1, 2, 3]
    assert lst != [1, 2, 4]
    assert lst == utils.MonitoredList([1, 2, 3], callback=Mock())
    assert lst != utils.MonitoredList([1, 3, 2], callback=Mock())

def test_MonitoredList_repr():
    cb = Mock()
    lst = utils.MonitoredList((1, 2, 3), callback=cb)
    assert repr(lst) == f'MonitoredList([1, 2, 3], callback={cb!r})'


@pytest.mark.parametrize(
    argnames=('args, kwargs, exp_mapping'),
    argvalues=(
        (({'foo': 'bar'},), {}, {'foo': 'bar'}),
        (({('f', 'o', 'o'): 'bar'},), {}, {('f', 'o', 'o'): 'bar'}),
        (({'foo': ['b', 'a', 'r']},), {}, {'foo': ('b', 'a', 'r')}),
        (({'foo': ['b', 'a', 'r', {1: 2}]},), {}, {'foo': ('b', 'a', 'r', frozenset(((1, 2))))}),
        (({'foo': {1: 'b', 2: ['a', 'r']}},), {}, {'foo': frozenset(((1, 'b'), (2, ('a', 'r'))))}),
    ),
    ids=lambda v: str(v),
)
def test_ImmutableMapping(args, kwargs, exp_mapping):
    mapping = utils.ImmutableMapping(*args, **kwargs)
    assert mapping == exp_mapping


def test_is_sequence():
    assert utils.is_sequence((1, 2, 3))
    assert utils.is_sequence([1, 2, 3])
    assert not utils.is_sequence('123')


@pytest.mark.parametrize(
    argnames=('a', 'b', 'merged'),
    argvalues=(
        ({1: 10}, {1: 20}, {1: 20}),
        ({1: 10}, {2: 20}, {1: 10, 2: 20}),
        ({1: 10}, {1: 20, 2: 2000}, {1: 20, 2: 2000}),
        ({1: 10, 2: 2000}, {1: 20}, {1: 20, 2: 2000}),
        ({1: {2: 20}}, {1: {2: 2000}}, {1: {2: 2000}}),
        ({1: {2: 20}}, {1: {2: {3: 30}}}, {1: {2: {3: 30}}}),
        ({1: {2: 20, 3: {5: 50}}}, {1: {3: {4: 40, 5: 5000}}}, {1: {2: 20, 3: {4: 40, 5: 5000}}}),
    ),
    ids=lambda v: str(v),
)
def test_merge_dicts(a, b, merged):
    assert utils.merge_dicts(a, b) == merged
    assert id(a) != id(merged)
    assert id(b) != id(merged)


def test_deduplicate_deduplicates():
    assert utils.deduplicate([1, 2, 1, 3, 1, 4, 3, 5]) == [1, 2, 3, 4, 5]

def test_deduplicate_maintains_order():
    assert utils.deduplicate([3, 2, 1, 1, 4, 5, 1, 3]) == [3, 2, 1, 4, 5]

def test_deduplicate_deduplicates_unhashable_items():
    items = [
        {'a': 1, 'b': 2},
        {'a': 2, 'b': 2},
        {'a': 3, 'b': 1},
        {'a': 4, 'b': 3},
        {'a': 5, 'b': 1},
        {'a': 6, 'b': 4},
    ]
    assert utils.deduplicate(items, key=lambda item: item['b']) == [
        {'a': 1, 'b': 2},
        {'a': 3, 'b': 1},
        {'a': 4, 'b': 3},
        {'a': 6, 'b': 4},
    ]


@pytest.mark.parametrize(
    argnames=('items', 'group_sizes', 'exp_groups'),
    argvalues=(
        (range(18), [1], [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,), (16,), (17,)]),
        (range(18), [1, 2], [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15), (16, 17)]),
        (range(18), [1, 2, 3], [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17)]),
        (range(18), [1, 2, 3, 4], [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17)]),
        (range(18), [1, 2, 3, 4, 5, 6], [(0, 1, 2, 3, 4, 5), (6, 7, 8, 9, 10, 11), (12, 13, 14, 15, 16, 17)]),

        (range(17), [1], [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,), (16,)]),
        (range(17), [1, 2], [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,), (16,)]),
        (range(17), [1, 2, 3], [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,), (12,), (13,), (14,), (15,), (16,)]),
        (range(17), [2, 3, 4], [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, -1)]),
        (range(17), [3, 4], [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, -1)]),
        (range(17), [4], [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15), (16, -1, -1, -1)]),
        (range(17), [4, 5], [(0, 1, 2, 3, 4), (5, 6, 7, 8, 9), (10, 11, 12, 13, 14), (15, 16, -1, -1, -1)]),

        (range(16), [4], [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15)]),
        (range(16), [5, 4], [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15)]),
        (range(16), [4, 5, 3], [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15)]),
    ),
)
def test_as_groups(items, group_sizes, exp_groups):
    groups = tuple(utils.as_groups(items, group_sizes=group_sizes, default=-1))
    assert len(groups) == len(exp_groups)
    for a, b in zip(groups, exp_groups):
        assert a == b


@pytest.mark.parametrize(
    argnames='object, exp_return_value',
    argvalues=(
        ('foo', False),
        ((1, 2, 3), False),
        (re.compile(r'1, 2, 3'), True),
    ),
)
def test_is_regex_pattern(object, exp_return_value, mocker):
    assert utils.is_regex_pattern(object) is exp_return_value


@pytest.mark.parametrize(
    argnames='obj, exp_id',
    argvalues=(
        # Strings and other simple objects
        ('foo', b'foo'),
        (23, b'23'),
        (2.3, b'2.3'),

        # Iterables
        (['foo', 'bar', 'baz', 4], b'4barbazfoo'),
        (['foo', 'bar', 'baz', (4, 'five')], b'4fivebarbazfoo'),
        ([('foo', 'bar', 'baz'), {'hey': 'ho'}], b'barbazfooheyho'),
        ([('foo', 'bar', 'baz'), {'hey': ['h', 0]}], b'0hheybarbazfoo'),
        ([(1, 2, 3), ('5', 6.0), {7: ['eigh', 't']}], b'12356.07eight'),
        ([(1, 2, 3, (4.1, 4.2)), ('5', 6.0), {7: ['eigh', 't']}], b'1234.14.256.07eight'),

        # Mappings
        ({'a': 1, 'b': 2, 'c': 3}, b'1a2b3c'),
        ({('a', 'b'): 1, 'c': 2}, b'1ab2c'),
        ({('a', 'b', (1, 2)): 'what', 'c': 3}, b'12abwhat3c'),
        ({('a', 'b', (1, (2, 3))): 'what', 'c': 3}, b'123abwhat3c'),
        ({'what': ('a', 'b', (1, (2, 3))), 'c': 3}, b'123abwhat3c'),
    ),
    ids=lambda v: str(v),
)
def test_semantic_hash(obj, exp_id, mocker):
    sha256_mock = mocker.patch('hashlib.sha256')
    assert utils.semantic_hash(obj) == sha256_mock.return_value.hexdigest.return_value
    assert sha256_mock.call_args_list == [call(exp_id)]

@pytest.mark.parametrize(
    argnames='obj',
    argvalues=(
        (i for i in range(10)),
    ),
    ids=lambda v: repr(v),
)
def test_semantic_hash_gets_unsupported_type(obj, mocker):
    sha256_mock = mocker.patch('hashlib.sha256')
    with pytest.raises(RuntimeError, match=rf'Unsupported type: {type(obj)!r}: {obj!r}'):
        utils.semantic_hash(obj)
    assert sha256_mock.call_args_list == []


@pytest.fixture
def unhandled_exception_handler(event_loop):
    original_exception_handler = event_loop.get_exception_handler()
    unhandled_exception_handler = Mock()
    event_loop.set_exception_handler(unhandled_exception_handler)
    yield unhandled_exception_handler
    event_loop.set_exception_handler(original_exception_handler)

def assert_unhandled_exception(handler, exception):
    if not exception:
        assert handler.call_args_list == []
    else:
        print(handler.call_args_list)
        assert len(handler.call_args_list) == 1
        assert len(handler.call_args_list[0].args) == 2
        assert len(handler.call_args_list[0].kwargs) == 0
        args = handler.call_args_list[0].args
        assert isinstance(args[0], asyncio.AbstractEventLoop)
        assert isinstance(args[1], dict)
        raised_exception = args[1].get('exception', 'NO EXCEPTION')
        assert raised_exception is exception

@pytest.mark.parametrize('callback', (None, Mock()))
@pytest.mark.asyncio
async def test_run_task__returned_task_returns_coro_return_value(callback, unhandled_exception_handler):
    coro = AsyncMock(return_value='foo')()
    task = utils.run_task(coro, callback=callback)

    return_value = await task
    assert return_value == 'foo'

    if callback:
        assert callback.call_args_list == [call(return_value)]

    assert_unhandled_exception(unhandled_exception_handler, None)

@pytest.mark.parametrize('callback', (None, Mock()))
@pytest.mark.asyncio
async def test_run_task__coro_raises_CancelledError(callback, unhandled_exception_handler):
    coro = AsyncMock(side_effect=asyncio.CancelledError())()
    task = utils.run_task(coro, callback=callback)

    return_value = await task
    assert return_value is None

    if callback:
        assert callback.call_args_list == [call(return_value)]

    assert_unhandled_exception(unhandled_exception_handler, None)

@pytest.mark.parametrize('callback', (None, Mock()))
@pytest.mark.asyncio
async def test_run_task__coro_raises_Exception(callback, unhandled_exception_handler):
    exception = errors.UpsiesError('my exception')
    coro = AsyncMock(side_effect=exception)()

    task = utils.run_task(coro, callback=callback)
    with pytest.raises(type(exception), match=rf'^{re.escape(str(exception))}$'):
        await task

    if callback:
        assert callback.call_args_list == [call(errors.UpsiesError('my exception'))]
        assert_unhandled_exception(unhandled_exception_handler, None)
    else:
        assert_unhandled_exception(unhandled_exception_handler, exception)

@pytest.mark.asyncio
async def test_run_task__callback_raises_Exception(unhandled_exception_handler, event_loop):
    exception = errors.UpsiesError('my exception')
    callback = Mock(side_effect=exception)
    coro = AsyncMock(return_value='foo')()

    task = utils.run_task(coro, callback=callback)
    return_value = await task
    assert return_value == 'foo'

    assert callback.call_args_list == [call('foo')]

    assert_unhandled_exception(unhandled_exception_handler, exception)

@pytest.mark.parametrize(
    argnames='args, kwargs',
    argvalues=(
        ((), {}),
        (('foo', 'bar'), {}),
        ((), {'baz': 123}),
        (('foo', 'bar'), {'baz': 123}),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_run_async(args, kwargs, event_loop):
    function = Mock()
    return_value = await utils.run_async(function, *args, **kwargs)
    assert return_value == function.return_value
    assert function.call_args_list == [call(*args, **kwargs)]
