from unittest.mock import AsyncMock, Mock, call

import pytest

from upsies import errors
from upsies.jobs.torrent import AddTorrentJob


@pytest.fixture
def btclient():
    class MockBtClient():
        name = 'mocksy'
        label = 'Mocksy'
        add_torrent = AsyncMock()

        def __repr__(self):
            return '<BtClient instance>'

    return MockBtClient()


@pytest.fixture
async def make_AddTorrentJob(tmp_path, btclient):
    def make_AddTorrentJob(download_path=tmp_path, check_after_add='<check_after_add>', torrents=()):
        return AddTorrentJob(
            home_directory=tmp_path,
            cache_directory=tmp_path,
            ignore_cache=False,
            btclient=btclient,
            enqueue=torrents,
        )
    return make_AddTorrentJob


def test_cache_id(make_AddTorrentJob):
    job = make_AddTorrentJob()
    assert job.cache_id is None


@pytest.mark.parametrize(
    argnames='signal, args, exp_info',
    argvalues=(
        ('adding', ('path/to.torrent',), 'Adding to.torrent'),
        ('added', ('ignored argument',), ''),
        ('finished', ('ignored argument',), ''),
        ('error', ('ignored argument',), ''),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.asyncio
async def test_info_property_is_set(signal, args, exp_info, make_AddTorrentJob):
    job = make_AddTorrentJob()
    job.info = 'foo!'
    assert job.info == 'foo!'
    job.signal.emit(signal, *args)
    assert job.info == exp_info


@pytest.mark.parametrize(
    argnames='torrent_path, add_torrent_result, exp_calls',
    argvalues=(
        pytest.param(
            'my.torrent',
            errors.TorrentAddError('bad torrent'),
            [
                call.emit('adding', 'my.torrent'),
                call.add_torrent('my.torrent'),
                call.error(errors.TorrentAddError('bad torrent')),
            ],
            id='Adding fails',
        ),
        pytest.param(
            'my.torrent',
            'd34db33f',
            [
                call.emit('adding', 'my.torrent'),
                call.add_torrent('my.torrent'),
                call.send('d34db33f'),
                call.emit('added', 'd34db33f'),
            ],
            id='Adding succeeds',
        ),
    ),
)
@pytest.mark.asyncio
async def test_handle_input(torrent_path, add_torrent_result, exp_calls, make_AddTorrentJob, btclient, mocker):
    job = make_AddTorrentJob()

    mocks = Mock()
    mocks.attach_mock(
        (
            mocker.patch.object(job._btclient, 'add_torrent', side_effect=add_torrent_result)
            if isinstance(add_torrent_result, Exception) else
            mocker.patch.object(job._btclient, 'add_torrent', return_value=add_torrent_result)
        ),
        'add_torrent',
    )
    mocks.attach_mock(mocker.patch.object(job.signal, 'emit'), 'emit')
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')
    mocks.attach_mock(mocker.patch.object(job, 'send'), 'send')

    await job.handle_input(torrent_path)
    assert mocks.mock_calls == exp_calls
