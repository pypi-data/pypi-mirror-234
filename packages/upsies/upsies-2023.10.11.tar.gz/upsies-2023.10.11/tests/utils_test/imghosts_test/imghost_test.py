from unittest.mock import Mock, call

import pytest

from upsies.utils import imghosts


def test_imghosts(mocker):
    existing_imghosts = (Mock(), Mock(), Mock())
    submodules_mock = mocker.patch('upsies.utils.imghosts.submodules')
    subclasses_mock = mocker.patch('upsies.utils.imghosts.subclasses', return_value=existing_imghosts)
    assert imghosts.imghosts() == existing_imghosts
    assert submodules_mock.call_args_list == [call('upsies.utils.imghosts')]
    assert subclasses_mock.call_args_list == [call(imghosts.base.ImageHostBase, submodules_mock.return_value)]


@pytest.mark.parametrize('name', ('foo', 'bar', 'baz'))
@pytest.mark.parametrize(
    argnames='options, cache_directory, exp_calls',
    argvalues=(
        (None, None, [call(options=None, cache_directory=None)]),
        ({'this': 'that'}, None, [call(options={'this': 'that'}, cache_directory=None)]),
        (None, 'path/to/cache', [call(options=None, cache_directory='path/to/cache')]),
        ({'this': 'that'}, 'path/to/cache', [call(options={'this': 'that'}, cache_directory='path/to/cache')]),
    ),
)
def test_imghost_returns_ImageHostBase_instance(name, options, cache_directory, exp_calls, mocker):
    existing_imghosts = {
        'foo': Mock(),
        'bar': Mock(),
        'baz': Mock(),
    }
    existing_imghosts['foo'].configure_mock(name='foo')
    existing_imghosts['bar'].configure_mock(name='bar')
    existing_imghosts['baz'].configure_mock(name='baz')
    mocker.patch('upsies.utils.imghosts.imghosts', return_value=existing_imghosts.values())

    kwargs = {}
    if options:
        kwargs['options'] = options
    if cache_directory:
        kwargs['cache_directory'] = cache_directory
    return_value = imghosts.imghost(name, **kwargs)
    assert return_value == existing_imghosts[name].return_value
    assert existing_imghosts[name].call_args_list == exp_calls

def test_imghost_fails_to_find_imghost(mocker):
    existing_imghosts = (Mock(), Mock(), Mock())
    existing_imghosts[0].configure_mock(name='foo')
    existing_imghosts[1].configure_mock(name='bar')
    existing_imghosts[2].configure_mock(name='baz')
    mocker.patch('upsies.utils.imghosts.imghosts', return_value=existing_imghosts)
    with pytest.raises(ValueError, match='^Unsupported image hosting service: bam$'):
        imghosts.imghost('bam')
    for ih in existing_imghosts:
        assert ih.call_args_list == []


def test_imghost_names(mocker):
    existing_imghosts = (Mock(), Mock(), Mock())
    existing_imghosts[0].configure_mock(name='FOO')
    existing_imghosts[1].configure_mock(name='bar')
    existing_imghosts[2].configure_mock(name='Baz')
    mocker.patch('upsies.utils.imghosts.imghosts', return_value=existing_imghosts)
    assert imghosts.imghost_names() == ['bar', 'Baz', 'FOO']
