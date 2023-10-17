from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies import errors
from upsies.jobs.scene import SceneSearchJob


@pytest.fixture
async def make_SceneSearchJob(tmp_path):
    def make_SceneSearchJob(content_path=tmp_path, ignore_cache=False):
        return SceneSearchJob(
            home_directory=tmp_path,
            cache_directory=tmp_path,
            ignore_cache=ignore_cache,
            content_path=content_path,
            predb=Mock(search=AsyncMock()),
        )
    return make_SceneSearchJob


def test_cache_id(make_SceneSearchJob):
    job = make_SceneSearchJob(content_path='path/to/Foo/')
    assert job.cache_id is None


def test_initialize_with_default_predb(mocker):
    MultiPredbApi_mock = mocker.patch('upsies.utils.predbs.MultiPredbApi')
    job = SceneSearchJob(content_path='path/to/Foo/')
    assert job._predb is MultiPredbApi_mock.return_value
    assert MultiPredbApi_mock.call_args_list == [call()]

def test_initialize_with_custom_predb(mocker):
    MultiPredbApi_mock = mocker.patch('upsies.utils.predbs.MultiPredbApi')
    custom_predb = Mock()
    job = SceneSearchJob(content_path='path/to/Foo/', predb=custom_predb)
    assert job._predb is custom_predb
    assert MultiPredbApi_mock.call_args_list == []


@pytest.mark.asyncio
async def test_execute(make_SceneSearchJob, mocker):
    job = make_SceneSearchJob()
    mocker.patch.object(job, 'attach_task', Mock())
    mocker.patch.object(job, '_search', Mock())
    job.execute()
    assert job._search.call_args_list == [call()]
    assert job.attach_task.call_args_list == [call(job._search.return_value, finish_when_done=True)]


@pytest.mark.parametrize(
    argnames='exception',
    argvalues=(
        errors.SceneError('no'),
        errors.RequestError('no interwebs'),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_search_handles_exception_from_search(exception, make_SceneSearchJob, mocker):
    job = make_SceneSearchJob()
    cb = Mock()
    job.signal.register('search_results', cb)
    job._predb.search.side_effect = exception
    await job._search()
    assert job._predb.search.call_args_list == [call(
        query=job._content_path,
        only_existing_releases=False,
    )]
    assert job.output == ()
    assert job.errors == (exception,)
    assert job.exit_code == 1
    assert job.is_finished
    assert cb.call_args_list == []

@pytest.mark.asyncio
async def test_search_handles_no_results(make_SceneSearchJob, mocker):
    job = make_SceneSearchJob()
    cb = Mock()
    job.signal.register('search_results', cb)
    job._predb.search.return_value = []
    await job._search()
    assert job._predb.search.call_args_list == [call(
        query=job._content_path,
        only_existing_releases=False,
    )]
    assert job.output == ()
    assert job.errors == ('No results',)
    assert job.exit_code == 1
    assert job.is_finished
    assert cb.call_args_list == [call([])]

@pytest.mark.asyncio
async def test_search_handles_results(make_SceneSearchJob, mocker):
    job = make_SceneSearchJob()
    cb = Mock()
    job.signal.register('search_results', cb)
    job._predb.search.return_value = ['foo', 'bar', 'baz']
    await job._search()
    assert job._predb.search.call_args_list == [call(
        query=job._content_path,
        only_existing_releases=False,
    )]
    assert job.output == ('foo', 'bar', 'baz')
    assert job.errors == ()
    assert job.exit_code == 0
    assert job.is_finished
    assert cb.call_args_list == [call(['foo', 'bar', 'baz'])]
