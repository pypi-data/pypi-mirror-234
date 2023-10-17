import os
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, PropertyMock, call

import pytest

from upsies import errors
from upsies.jobs.poster import PosterJob


def test_cache_id():
    job = PosterJob(webdb=None, webdb_id=None, autostart=False)
    assert job.cache_id is None


@pytest.mark.parametrize(
    argnames='init_kwargs, start_kwargs, exp_work_kwargs',
    argvalues=(
        (
            {'webdb': None, 'webdb_id': None},
            {'webdb': 'start webdb', 'webdb_id': 'start id'},
            {'webdb': 'start webdb', 'webdb_id': 'start id', 'season': None},
        ),
        (
            {'webdb': 'init webdb', 'webdb_id': 'init id'},
            {'webdb': 'start webdb', 'webdb_id': 'start id'},
            {'webdb': 'start webdb', 'webdb_id': 'start id', 'season': None},
        ),
        (
            {'webdb': 'init webdb', 'webdb_id': 'init id', 'season': 'init season'},
            {'webdb': 'start webdb', 'webdb_id': 'start id'},
            {'webdb': 'start webdb', 'webdb_id': 'start id', 'season': 'init season'},
        ),
        (
            {'webdb': 'init webdb', 'webdb_id': 'init id', 'season': 'init season'},
            {'webdb': 'start webdb', 'webdb_id': None, 'season': 'start season'},
            {'webdb': 'start webdb', 'webdb_id': 'init id', 'season': 'start season'},
        ),
        (
            {'webdb': 'init webdb', 'webdb_id': 'init id', 'season': None},
            {'webdb': None, 'webdb_id': 'start id', 'season': 'start season'},
            {'webdb': 'init webdb', 'webdb_id': 'start id', 'season': 'start season'},
        ),
    ),
    ids=lambda v: repr(v),
)
def test_start(init_kwargs, start_kwargs, exp_work_kwargs, mocker):
    mocks = Mock()
    mocker.patch('upsies.jobs.base.JobBase.start', mocks.start)
    mocker.patch('upsies.jobs.poster.PosterJob.attach_task', mocks.attach_task)
    mocker.patch('upsies.jobs.poster.PosterJob._work', mocks._work)

    job = PosterJob(autostart=False, **init_kwargs)

    assert mocks.mock_calls == []
    job.start(**start_kwargs)
    assert mocks.mock_calls == [
        call.start(),
        call._work(**exp_work_kwargs),
        call.attach_task(coro=mocks._work.return_value, finish_when_done=True),
    ]


@pytest.mark.parametrize(
    argnames=(
        'webdb, webdb_id, season, '
        '_get_poster_filepath, _get_poster_url, _download_poster, '
        '_resize_poster, _imghost, _upload_poster, exp_calls'
    ),
    argvalues=(
        (
            'mock webdb',
            'tt123',
            'S03',
            Mock(return_value='downloaded/poster.jpg'),
            AsyncMock(return_value=None),
            AsyncMock(return_value=None),
            Mock(return_value=None),
            None,
            AsyncMock(return_value=None),
            [
                call._get_poster_url('mock webdb', 'tt123', 'S03'),
            ],
        ),
        (
            'mock webdb',
            'tt123',
            'S03',
            Mock(return_value='downloaded/poster.jpg'),
            AsyncMock(return_value='http://original/url.jpg'),
            AsyncMock(return_value=None),
            Mock(return_value=None),
            None,
            AsyncMock(return_value=None),
            [
                call._get_poster_url('mock webdb', 'tt123', 'S03'),
                call._get_poster_filepath('mock webdb', 'tt123', 'S03', 'http://original/url.jpg'),
                call._download_poster('http://original/url.jpg', 'downloaded/poster.jpg'),
            ],
        ),
        (
            'mock webdb',
            'tt123',
            'S03',
            Mock(return_value='downloaded/poster.jpg'),
            AsyncMock(return_value='http://original/url.jpg'),
            AsyncMock(return_value='path/to/original.jpg'),
            Mock(return_value=None),
            None,
            AsyncMock(return_value=None),
            [
                call._get_poster_url('mock webdb', 'tt123', 'S03'),
                call._get_poster_filepath('mock webdb', 'tt123', 'S03', 'http://original/url.jpg'),
                call._download_poster('http://original/url.jpg', 'downloaded/poster.jpg'),
                call._resize_poster('path/to/original.jpg'),
            ],
        ),
        (
            'mock webdb',
            'tt123',
            'S03',
            Mock(return_value='downloaded/poster.jpg'),
            AsyncMock(return_value='http://original/url.jpg'),
            AsyncMock(return_value='path/to/original.jpg'),
            Mock(return_value='path/to/resized.jpg'),
            None,
            AsyncMock(return_value=None),
            [
                call._get_poster_url('mock webdb', 'tt123', 'S03'),
                call._get_poster_filepath('mock webdb', 'tt123', 'S03', 'http://original/url.jpg'),
                call._download_poster('http://original/url.jpg', 'downloaded/poster.jpg'),
                call._resize_poster('path/to/original.jpg'),
                call.send('path/to/resized.jpg'),
            ],
        ),
        (
            'mock webdb',
            'tt123',
            'S03',
            Mock(return_value='downloaded/poster.jpg'),
            AsyncMock(return_value='http://original/url.jpg'),
            AsyncMock(return_value='path/to/original.jpg'),
            Mock(return_value='path/to/resized.jpg'),
            'mock imghost',
            AsyncMock(return_value='http://resized/url.jpg'),
            [
                call._get_poster_url('mock webdb', 'tt123', 'S03'),
                call._get_poster_filepath('mock webdb', 'tt123', 'S03', 'http://original/url.jpg'),
                call._download_poster('http://original/url.jpg', 'downloaded/poster.jpg'),
                call._resize_poster('path/to/original.jpg'),
                call._upload_poster('path/to/resized.jpg'),
                call.send('http://resized/url.jpg'),
            ],
        ),
    ),
)
@pytest.mark.asyncio
async def test_work(webdb, webdb_id, season,
                    _get_poster_filepath, _get_poster_url, _download_poster, _resize_poster, _imghost, _upload_poster,
                    exp_calls, mocker):
    job = PosterJob(autostart=False, webdb=None, webdb_id=None)

    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(job, '_get_poster_filepath', _get_poster_filepath), '_get_poster_filepath')
    mocks.attach_mock(mocker.patch.object(job, '_get_poster_url', _get_poster_url), '_get_poster_url')
    mocks.attach_mock(mocker.patch.object(job, '_download_poster', _download_poster), '_download_poster')
    mocks.attach_mock(mocker.patch.object(job, '_resize_poster', _resize_poster), '_resize_poster')
    job._imghost = _imghost
    mocks.attach_mock(mocker.patch.object(job, '_upload_poster', _upload_poster), '_upload_poster')
    mocks.attach_mock(mocker.patch.object(job, 'send'), 'send')

    await job._work(webdb, webdb_id, season)
    assert mocks.mock_calls == exp_calls


@pytest.mark.parametrize(
    argnames='webdb, webdb_id, season, exp_mock_calls, exp_return_value',
    argvalues=(
        (
            Mock(poster_url=AsyncMock(side_effect=errors.RequestError('No poster available'))),
            'tt123',
            None,
            [
                call.emit('finding_poster', 'tt123'),
                call.poster_url('tt123', season=None),
                call.error('Failed to find poster: No poster available'),
            ],
            None,
        ),
        (
            Mock(poster_url=AsyncMock(return_value='')),
            'tt123',
            'S06',
            [
                call.emit('finding_poster', 'tt123'),
                call.poster_url('tt123', season='S06'),
                call.error('Failed to find poster: There is no poster'),
            ],
            None,
        ),
        (
            Mock(poster_url=AsyncMock(return_value='http://poster/url.jpg')),
            'tt123',
            'S09',
            [
                call.emit('finding_poster', 'tt123'),
                call.poster_url('tt123', season='S09'),
                call.emit('found_poster', 'http://poster/url.jpg'),
            ],
            'http://poster/url.jpg',
        ),
    ),
)
@pytest.mark.asyncio
async def test_get_poster_url(webdb, webdb_id, season, exp_mock_calls, exp_return_value, mocker):
    job = PosterJob(webdb=None, webdb_id=None, autostart=False)

    mocks = Mock()
    mocks.attach_mock(webdb.poster_url, 'poster_url')
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')
    mocks.attach_mock(mocker.patch.object(job.signal, 'emit'), 'emit')

    return_value = await job._get_poster_url(webdb, webdb_id, season)
    assert mocks.mock_calls == exp_mock_calls
    assert return_value == exp_return_value


@pytest.mark.parametrize(
    argnames='webdb, webdb_id, season, url, exp_filename',
    argvalues=(
        (
            SimpleNamespace(name='mydb'),
            'tt123',
            None,
            'http://foo/bar',
            'mydb=tt123',
        ),
        (
            SimpleNamespace(name='mydb'),
            'tt123',
            '3',
            'http://foo/bar',
            'mydb=tt123.S03',
        ),
        (
            SimpleNamespace(name='mydb'),
            'tt123',
            '3',
            'http://foo/bar.jpg',
            'mydb=tt123.S03.jpg',
        ),
        (
            SimpleNamespace(name='mydb'),
            'tt123',
            None,
            'http://foo/bar.png',
            'mydb=tt123.png',
        ),
        (
            SimpleNamespace(name='mydb'),
            f'movie{os.sep}123',
            None,
            'http://foo/bar.png',
            'mydb=movie_123.png',
        ),
    ),
)
async def test_get_poster_filepath(webdb, webdb_id, season, url, exp_filename, mocker):
    job = PosterJob(webdb=None, webdb_id=None, autostart=False)

    return_value = job._get_poster_filepath(webdb, webdb_id, season, url)
    assert return_value == os.path.join(job.cache_directory, exp_filename)


@pytest.mark.parametrize(
    argnames='url, filepath, download, exp_mock_calls, exp_return_value',
    argvalues=(
        (
            'http://localhost.org:123/img.jpg',
            'path/to/downloaded/img.jpg',
            AsyncMock(return_value='path/to/sanitized/img.jpg'),
            [
                call.emit('downloading_poster', 'http://localhost.org:123/img.jpg'),
                call.download('http://localhost.org:123/img.jpg', 'path/to/downloaded/img.jpg', cache=True),
                call.emit('downloaded_poster', 'path/to/sanitized/img.jpg'),
            ],
            'path/to/sanitized/img.jpg',
        ),
        (
            'http://localhost.org:123/img.jpg',
            'path/to/downloaded/img.jpg',
            AsyncMock(side_effect=errors.RequestError('Teh internet has broked!')),
            [
                call.emit('downloading_poster', 'http://localhost.org:123/img.jpg'),
                call.download('http://localhost.org:123/img.jpg', 'path/to/downloaded/img.jpg', cache=True),
                call.error('Failed to download poster: Teh internet has broked!'),
            ],
            None,
        ),
    ),
)
@pytest.mark.asyncio
async def test_download_poster(url, filepath, download, exp_mock_calls, exp_return_value, mocker):
    job = PosterJob(autostart=False, webdb=None, webdb_id=None)

    mocks = Mock()
    mocks.attach_mock(mocker.patch('upsies.utils.http.download', download), 'download')
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')
    mocks.attach_mock(mocker.patch.object(job.signal, 'emit'), 'emit')

    return_value = await job._download_poster(url, filepath)
    assert mocks.mock_calls == exp_mock_calls
    assert return_value == exp_return_value


@pytest.mark.parametrize(
    argnames='filepath, home_directory, width, height, resize, exp_mock_calls, exp_return_value',
    argvalues=(
        (
            'path/to/original.jpg',
            'path/to/home',
            123,
            456,
            Mock(side_effect=errors.ImageResizeError('Your image is stooopid!')),
            [
                call.emit('resizing_poster', 'path/to/original.jpg'),
                call.resize(
                    'path/to/original.jpg',
                    target_directory='path/to/home',
                    target_filename='original.123x456.jpg',
                    width=123,
                    height=456,
                ),
                call.error('Failed to resize poster: Your image is stooopid!'),
            ],
            None,
        ),
        (
            'path/to/original.jpg',
            'path/to/home',
            123,
            456,
            Mock(return_value='path/to/resized.jpg'),
            [
                call.emit('resizing_poster', 'path/to/original.jpg'),
                call.resize(
                    'path/to/original.jpg',
                    target_directory='path/to/home',
                    target_filename='original.123x456.jpg',
                    width=123,
                    height=456,
                ),
                call.emit('resized_poster', 'path/to/resized.jpg'),
            ],
            'path/to/resized.jpg',
        ),
    ),
)
def test_resize_poster(filepath, home_directory, width, height, resize, exp_mock_calls, exp_return_value, mocker):
    job = PosterJob(autostart=False, webdb=None, webdb_id=None, width=width, height=height)

    mocks = Mock()
    mocks.attach_mock(mocker.patch('upsies.utils.image.resize', resize), 'resize')
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')
    mocks.attach_mock(mocker.patch.object(job.signal, 'emit'), 'emit')
    mocker.patch.object(type(job), 'home_directory', PropertyMock(return_value=home_directory))

    return_value = job._resize_poster(filepath)
    assert mocks.mock_calls == exp_mock_calls
    assert return_value == exp_return_value


@pytest.mark.parametrize(
    argnames='filepath, imghost, exp_mock_calls, exp_return_value',
    argvalues=(
        (
            'path/to/file.jpg',
            Mock(upload=AsyncMock(side_effect=errors.RequestError('Nu-uh!'))),
            [
                call.emit('uploading_poster', 'path/to/file.jpg'),
                call.upload('path/to/file.jpg'),
                call.error('Failed to upload poster: Nu-uh!'),
            ],
            None,
        ),
        (
            'path/to/file.jpg',
            Mock(upload=AsyncMock(return_value='http://localhost:123/uploaded.jpg')),
            [
                call.emit('uploading_poster', 'path/to/file.jpg'),
                call.upload('path/to/file.jpg'),
                call.emit('uploaded_poster', 'http://localhost:123/uploaded.jpg'),
            ],
            'http://localhost:123/uploaded.jpg',
        ),
    ),
)
@pytest.mark.asyncio
async def test_upload_poster(filepath, imghost, exp_mock_calls, exp_return_value, mocker):
    job = PosterJob(autostart=False, webdb=None, webdb_id=None, imghost=imghost)

    mocks = Mock()
    mocks.attach_mock(imghost.upload, 'upload')
    mocks.attach_mock(mocker.patch.object(job, 'error'), 'error')
    mocks.attach_mock(mocker.patch.object(job.signal, 'emit'), 'emit')

    return_value = await job._upload_poster(filepath)
    assert mocks.mock_calls == exp_mock_calls
    assert return_value == exp_return_value

    async def _upload_poster(self, filepath):
        try:
            resized_url = await self._imghost.upload(filepath)
        except errors.RequestError as e:
            self.error(f'Failed to upload poster: {e}')
        else:
            self.signal.emit('uploaded_poster', resized_url)
            return resized_url
