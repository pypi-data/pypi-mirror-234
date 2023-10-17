from unittest.mock import Mock, call

import pytest

from upsies.utils import predbs


def test_predbs(mocker):
    existing_predbs = (Mock(), Mock(), Mock())
    submodules_mock = mocker.patch('upsies.utils.submodules')
    subclasses_mock = mocker.patch('upsies.utils.subclasses', return_value=existing_predbs)
    assert predbs.predbs() == existing_predbs
    assert submodules_mock.call_args_list == [call('upsies.utils.predbs')]
    assert subclasses_mock.call_args_list == [call(predbs.PredbApiBase, submodules_mock.return_value)]


def test_predb_returns_ClientApiBase_instance(mocker):
    existing_predbs = (Mock(), Mock(), Mock())
    existing_predbs[0].configure_mock(name='foo')
    existing_predbs[1].configure_mock(name='bar')
    existing_predbs[2].configure_mock(name='baz')
    mocker.patch('upsies.utils.predbs.predbs', return_value=existing_predbs)
    assert predbs.predb('bar', config={'foo': 'bar'}) is existing_predbs[1].return_value
    assert existing_predbs[1].call_args_list == [call(config={'foo': 'bar'})]

def test_predb_fails_to_find_predb(mocker):
    existing_predbs = (Mock(), Mock(), Mock())
    existing_predbs[0].configure_mock(name='foo')
    existing_predbs[1].configure_mock(name='bar')
    existing_predbs[2].configure_mock(name='baz')
    mocker.patch('upsies.utils.predbs.predbs', return_value=existing_predbs)
    with pytest.raises(ValueError, match='^Unsupported scene release database: bam$'):
        predbs.predb('bam')
    for c in existing_predbs:
        assert c.call_args_list == []


def test_predb_names(mocker):
    existing_predbs = (Mock(), Mock(), Mock())
    existing_predbs[0].configure_mock(name='FOO')
    existing_predbs[1].configure_mock(name='bar')
    existing_predbs[2].configure_mock(name='Baz')
    mocker.patch('upsies.utils.predbs.predbs', return_value=existing_predbs)
    assert predbs.predb_names() == ['bar', 'Baz', 'FOO']
