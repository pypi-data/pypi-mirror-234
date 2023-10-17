import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, PropertyMock, call, patch

import pytest
from prompt_toolkit.application import Application
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.output import DummyOutput

from upsies.uis.tui.tui import TUI


@pytest.fixture(autouse='module')
def mock_app(mocker):
    app = Application(
        input=create_pipe_input(),
        output=DummyOutput(),
    )
    mocker.patch('upsies.uis.tui.tui.TUI._make_app', Mock(return_value=app))
    mocker.patch('upsies.uis.tui.tui.TUI._jobs_container', Mock(children=[]), create=True)
    mocker.patch('upsies.uis.tui.tui.TUI._layout', create=True)

@pytest.fixture(autouse='module')
def mock_JobWidget(mocker):
    job_widget = Mock(
        __pt_container__=Mock(return_value=(Window())),
        is_interactive=None,
        job=Mock(wait=AsyncMock()),
    )
    mocker.patch('upsies.uis.tui.jobwidgets.JobWidget', Mock(return_value=job_widget))

class MockJob(Mock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get('name') is not None:
            self.configure_mock(name=kwargs['name'])

        if 'prejobs' not in kwargs:
            self.configure_mock(prejobs=())


def test_add_jobs(mocker):
    jobs = (
        MockJob(name='a', prejobs=(),),
        MockJob(name='b', prejobs=(
            MockJob(name='b.1', prejobs=()),
            MockJob(name='b.2', prejobs=(
                MockJob(name='b.2.x', prejobs=()),
            )),
        )),
        MockJob(name='c', prejobs=(
            MockJob(name='c.1', prejobs=(
                MockJob(name='c.1.x', prejobs=()),
                MockJob(name='c.1.y', prejobs=()),
            )),
            MockJob(name='c.2', prejobs=()),
        )),
    )

    def find_job(name, jobs):
        for job in jobs:
            if job.name == name:
                return job
            prejob = find_job(name, job.prejobs)
            if prejob:
                return prejob

    ui = TUI()
    mocks = Mock()
    mocks.attach_mock(mocker.patch.object(ui, '_add_job'), '_add_job')
    mocks.attach_mock(mocker.patch.object(ui, '_update_jobs_container'), '_update_jobs_container')
    mocks.attach_mock(mocker.patch.object(ui, '_connect_jobs'), '_connect_jobs')
    mocks.attach_mock(mocker.patch.object(ui, '_start_jobs'), '_start_jobs')

    ui.add_jobs(*jobs)

    assert mocks.mock_calls == [
        call._add_job(find_job('a', jobs)),
        call._add_job(find_job('b', jobs)),
        call._add_job(find_job('c', jobs)),
        call._update_jobs_container(),
        call._connect_jobs(find_job('a', jobs), find_job('b', jobs), find_job('c', jobs)),
        call._start_jobs(find_job('a', jobs), find_job('b', jobs), find_job('c', jobs)),
    ]


def test_add_job_detects_job_name_duplicate(mocker):
    mocker.patch('upsies.uis.tui.jobwidgets.JobWidget')
    mocker.patch('upsies.uis.tui.tui.to_container')
    ui = TUI()
    ui._add_job(MockJob(name='a'))
    ui._add_job(MockJob(name='b'))
    with pytest.raises(RuntimeError, match=r'^Conflicting job name: b$'):
        ui._add_job(MockJob(name='b'))


def test_add_job_gracefully_ignores_adding_exact_job_duplicate(mocker):
    mocker.patch('upsies.uis.tui.jobwidgets.JobWidget')
    mocker.patch('upsies.uis.tui.tui.to_container')
    ui = TUI()
    ui._add_job(MockJob(name='a'))
    b_job = MockJob(name='b')
    ui._add_job(b_job)
    ui._add_job(MockJob(name='c'))
    ui._add_job(b_job)
    ui._add_job(MockJob(name='d'))
    assert list(ui._jobs) == ['a', 'b', 'c', 'd']


def test_add_job_creates_JobWidget_and_Container(mocker):
    JobWidget_mock = mocker.patch('upsies.uis.tui.jobwidgets.JobWidget')
    to_container_mock = mocker.patch('upsies.uis.tui.tui.to_container')
    ui = TUI()
    job = MockJob(name='a')
    ui._add_job(job)
    assert tuple(ui._jobs) == (job.name,)
    assert ui._jobs[job.name].widget == JobWidget_mock.return_value
    assert ui._jobs[job.name].container == to_container_mock.return_value
    assert JobWidget_mock.call_args_list == [call(job, ui._app)]
    assert to_container_mock.call_args_list == [call(JobWidget_mock.return_value)]


class JobInfo:
    def __init__(self, *, job, widget, container):
        self.job = job
        self.widget = widget
        self.container = container

    def __repr__(self):
        return f'<{type(self).__name__} {self.job.name!r}>'

class Job:
    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f'<{type(self).__name__} {self.name!r}>'

def test_update_jobs_container_only_adds_first_unfinished_job_and_focuses_it_if_no_job_has_errors(mocker):
    ui = TUI()
    mocker.patch.object(ui, '_update_focus')
    ui._jobs = {
        'an': JobInfo(job=Job('a', is_enabled=False, is_started=False, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='aw')),

        'bi': JobInfo(job=Job('b', is_enabled=False, is_started=False, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='bw')),
        'cn': JobInfo(job=Job('c', is_enabled=False, is_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='cw')),
        'dn': JobInfo(job=Job('d', is_enabled=True, is_started=False, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='dw')),

        'ei': JobInfo(job=Job('e', is_enabled=False, is_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='ew')),
        'fi': JobInfo(job=Job('f', is_enabled=True, is_started=False, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='fw')),
        'gn': JobInfo(job=Job('g', is_enabled=True, is_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='gw')),

        'hi': JobInfo(job=Job('h', is_enabled=True, is_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='hw')),

        'xi': JobInfo(job=Job('x', is_enabled=True, is_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='xw')),
        'yn': JobInfo(job=Job('y', is_enabled=True, is_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=False), container=Mock(name='yw')),
        'zi': JobInfo(job=Job('z', is_enabled=True, is_started=True, is_finished=False, errors=()), widget=Mock(is_interactive=True), container=Mock(name='zw')),
    }
    ui._layout = Mock()
    jobs_container_id = id(ui._jobs_container)

    def assert_jobs_container(*keys, focused):
        ui._update_jobs_container()
        assert id(ui._jobs_container) == jobs_container_id
        exp_children = [ui._jobs[k].container for k in keys]
        assert ui._jobs_container.children == exp_children
        if focused:
            assert ui._update_focus.call_args_list == [
                call(ui._jobs[f])
                for f in focused
            ]
        else:
            assert ui._update_focus.call_args_list == []
        ui._update_focus.reset_mock()
        print('#######################################################')

    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['an'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['bi'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['cn'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['dn'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['ei'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['fi'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['gn'].job.is_finished = True
    assert_jobs_container('hi', 'gn', 'yn', focused=['hi'])

    ui._jobs['hi'].job.is_finished = True
    assert_jobs_container('hi', 'xi', 'gn', 'yn', focused=['xi'])

    ui._jobs['xi'].job.errors = ('Error message',)
    assert_jobs_container('hi', 'xi', 'zi', 'gn', 'yn', focused=['xi', 'zi'])


@pytest.mark.parametrize('raised', (None, ValueError('whatever')))
def test_update_focus(raised, mocker):
    ui = TUI()
    mocker.patch.object(ui._layout, 'focus', side_effect=raised)
    jobinfo = Mock()
    ui._update_focus(jobinfo)
    assert ui._layout.focus.call_args_list == [call(jobinfo.container)]


def test_connect_jobs():
    ui = TUI()
    mocks = Mock()
    jobs = [
        mocks.foo,
        mocks.bar,
        mocks.baz,
    ]
    ui._connect_jobs(*jobs)
    assert mocks.mock_calls == [
        call.foo.signal.register('finished', ui._handle_job_finished),
        call.foo.signal.register('refresh_job_list', ui._refresh_jobs),
        call.bar.signal.register('finished', ui._handle_job_finished),
        call.bar.signal.register('refresh_job_list', ui._refresh_jobs),
        call.baz.signal.register('finished', ui._handle_job_finished),
        call.baz.signal.register('refresh_job_list', ui._refresh_jobs),
    ]


@pytest.mark.parametrize(
    argnames='finished_job, enabled_jobs, exp_mock_calls',
    argvalues=(
        pytest.param(
            Mock(exit_code=1),
            [SimpleNamespace(name='foo', is_finished=False)],
            [call._exit()],
            id='Finished job failed',
        ),
        pytest.param(
            Mock(exit_code=0),
            [SimpleNamespace(name='foo', is_finished=False)],
            [call._refresh_jobs()],
            id='Finished job succeeded, only other job is not finished',
        ),
        pytest.param(
            Mock(exit_code=0),
            [SimpleNamespace(name='foo', is_finished=True)],
            [call._exit()],
            id='Finished job succeeded, only other job is finished',
        ),
        pytest.param(
            Mock(exit_code=0),
            [
                SimpleNamespace(name='foo', is_finished=True),
                SimpleNamespace(name='bar', is_finished=True),
                SimpleNamespace(name='baz', is_finished=True),
            ],
            [call._exit()],
            id='Finished job succeeded, all other jobs are finished',
        ),
        pytest.param(
            Mock(exit_code=0),
            [
                SimpleNamespace(name='foo', is_finished=True),
                SimpleNamespace(name='bar', is_finished=False),
                SimpleNamespace(name='baz', is_finished=True),
            ],
            [call._refresh_jobs()],
            id='Finished job succeeded, one other job is not finished',
        ),
    ),
)
def test_handle_job_finished(finished_job, enabled_jobs, exp_mock_calls, mocker):
    ui = TUI()

    mocks = Mock()
    mocker.patch.object(type(ui), '_enabled_jobs', PropertyMock(return_value=[
        Mock(job=job) for job in enabled_jobs
    ]))
    mocks.attach_mock(mocker.patch.object(ui, '_exit'), '_exit')
    mocks.attach_mock(mocker.patch.object(ui, '_refresh_jobs'), '_refresh_jobs')

    ui._handle_job_finished(finished_job)

    assert mocks.mock_calls == exp_mock_calls


@pytest.mark.parametrize('app_terminated', (True, False))
def test_refresh_jobs(app_terminated, mocker):
    ui = TUI()

    enabled_jobs = [
        Mock(name='foo'),
        Mock(name='bar'),
        Mock(name='baz'),
    ]

    mocks = Mock()
    mocker.patch.object(type(ui), '_enabled_jobs', PropertyMock(return_value=[
        SimpleNamespace(job=job) for job in enabled_jobs
    ]))
    mocker.patch.object(ui, '_app_terminated', app_terminated)
    mocks.attach_mock(mocker.patch.object(ui, '_start_jobs'), '_start_jobs')
    mocks.attach_mock(mocker.patch.object(ui, '_update_jobs_container'), '_update_jobs_container')
    mocks.attach_mock(mocker.patch.object(ui._app, 'invalidate'), 'invalidate')

    ui._refresh_jobs()

    if app_terminated:
        assert mocks.mock_calls == []
    else:
        assert mocks.mock_calls == [
            call._start_jobs(*enabled_jobs),
            call._update_jobs_container(),
            call.invalidate(),
        ]


def test_start_jobs():
    ui = TUI()
    mocks = Mock()
    jobs = (
        Mock(is_started=False, autostart=False, start=mocks.start_0),
        Mock(is_started=False, autostart=True, start=mocks.start_1),
        Mock(is_started=True, autostart=False, start=mocks.start_2),
        Mock(is_started=True, autostart=True, start=mocks.start_3),
        Mock(is_started=True, autostart=True, start=mocks.start_4),
        Mock(is_started=True, autostart=False, start=mocks.start_5),
        Mock(is_started=False, autostart=True, start=mocks.start_6),
        Mock(is_started=False, autostart=False, start=mocks.start_7),
    )

    ui._start_jobs(*jobs)

    assert mocks.mock_calls == [
        call.start_1(),
        call.start_6(),
    ]


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_run_calls_add_jobs(mocker):
    ui = TUI()
    mocker.patch.object(ui, 'add_jobs')
    mocker.patch.object(ui._app, 'run')
    ui.run(('a', 'b', 'c'))
    assert ui.add_jobs.call_args_list == [call('a', 'b', 'c')]

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_run_runs_application(mocker):
    ui = TUI()
    mocker.patch.object(ui, 'add_jobs')
    mocker.patch.object(ui._app, 'run')
    ui.run(('a', 'b', 'c'))
    assert ui._app.run.call_args_list == [call(set_exception_handler=False)]

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_run_raises_stored_exception(mocker):
    ui = TUI()
    mocker.patch.object(ui, 'add_jobs')
    mocker.patch.object(ui._app, 'run')
    mocker.patch.object(ui, '_get_exception', Mock(return_value=ValueError('foo')))
    with pytest.raises(ValueError, match=r'^foo$'):
        ui.run(('a', 'b', 'c'))

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_run_returns_first_nonzero_job_exit_code(mocker):
    ui = TUI()
    ui._jobs = {
        'a': SimpleNamespace(job=Mock(exit_code=0)),
        'b': SimpleNamespace(job=Mock(exit_code=1)),
        'c': SimpleNamespace(job=Mock(exit_code=2)),
        'd': SimpleNamespace(job=Mock(exit_code=3)),
    }
    mocker.patch.object(ui, 'add_jobs')
    mocker.patch.object(ui._app, 'run')
    mocker.patch.object(ui, '_get_exception', Mock(return_value=None))
    exit_code = ui.run(('a', 'b', 'c'))
    assert exit_code == 1

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_run_returns_zero_if_all_jobs_finished_successfully(mocker):
    ui = TUI()
    ui._jobs = {
        'a': SimpleNamespace(job=Mock(exit_code=0)),
        'b': SimpleNamespace(job=Mock(exit_code=0)),
        'c': SimpleNamespace(job=Mock(exit_code=0)),
        'd': SimpleNamespace(job=Mock(exit_code=0)),
    }
    mocker.patch.object(ui, 'add_jobs')
    mocker.patch.object(ui._app, 'run')
    mocker.patch.object(ui, '_get_exception', Mock(return_value=None))
    exit_code = ui.run(('a', 'b', 'c'))
    assert exit_code == 0


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_exit_does_nothing_if_already_exited(mocker):
    ui = TUI()
    ui._app_terminated = True
    mocker.patch.object(ui, '_terminate_jobs', AsyncMock())
    ui._exit()
    assert ui._terminate_jobs.call_args_list == []
    assert ui._app_terminated is True

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_exit_waits_for_application_to_run(mocker, event_loop):
    ui = TUI()
    mocker.patch.object(ui, '_terminate_jobs', AsyncMock())
    mocker.patch.object(type(ui._app), 'is_running', PropertyMock(return_value=False))
    mocker.patch.object(type(ui._app), 'is_done', PropertyMock(return_value=False))
    # If asycnio.call_soon() is still mocked when the test is finished, pytest
    # just hangs. pytest.mark.asyncio seems to depend on it.
    with patch.object(event_loop, 'call_soon'):
        ui._exit()
        assert event_loop.call_soon.call_args_list == [call(ui._exit)]
    assert ui._terminate_jobs.call_args_list == []
    assert ui._app_terminated is False

@pytest.mark.asyncio
async def test_exit_calls_terminate_jobs(mocker):
    ui = TUI()
    mocker.patch.object(type(ui._app), 'is_running', PropertyMock(return_value=True))
    mocker.patch.object(type(ui._app), 'is_done', PropertyMock(return_value=False))
    mocker.patch.object(type(ui._app), 'exit', Mock())
    mocker.patch.object(ui, '_update_jobs_container', Mock())
    ui._exit()
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    assert ui._app_terminated is True
    assert ui._app.exit.call_args_list == [call()]
    assert ui._update_jobs_container.call_args_list == [call()]

@pytest.mark.asyncio
async def test_exit_handles_exception_from_terminate_jobs(mocker):
    ui = TUI()
    mocker.patch.object(type(ui._app), 'is_running', PropertyMock(return_value=True))
    mocker.patch.object(type(ui._app), 'is_done', PropertyMock(return_value=False))
    mocker.patch.object(type(ui._app), 'exit', Mock())
    mocker.patch.object(ui, '_update_jobs_container', Mock())
    mocker.patch.object(ui, '_terminate_jobs', AsyncMock(side_effect=RuntimeError('foo!')))
    ui._exit()
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    await asyncio.sleep(0)
    assert ui._app_terminated is True
    assert ui._app.exit.call_args_list == [call()]
    assert str(ui._exception) == 'foo!'
    assert isinstance(ui._exception, RuntimeError)
    assert ui._update_jobs_container.call_args_list == [call()]


@pytest.mark.asyncio
async def test_terminate_jobs(mocker):
    ui = TUI()
    ui._jobs = {
        'a': SimpleNamespace(job=Mock(is_started=False, is_finished=False, is_enabled=False, wait=AsyncMock())),
        'b': SimpleNamespace(job=Mock(is_started=False, is_finished=False, is_enabled=True, wait=AsyncMock())),
        'c': SimpleNamespace(job=Mock(is_started=False, is_finished=True, is_enabled=False, wait=AsyncMock())),
        'd': SimpleNamespace(job=Mock(is_started=False, is_finished=True, is_enabled=True, wait=AsyncMock())),
        'e': SimpleNamespace(job=Mock(is_started=True, is_finished=False, is_enabled=False, wait=AsyncMock())),
        'f': SimpleNamespace(job=Mock(is_started=True, is_finished=False, is_enabled=True, wait=AsyncMock())),
        'g': SimpleNamespace(job=Mock(is_started=True, is_finished=True, is_enabled=False, wait=AsyncMock())),
        'h': SimpleNamespace(job=Mock(is_started=True, is_finished=True, is_enabled=True, wait=AsyncMock())),
    }
    mocker.patch.object(ui, '_finish_jobs', Mock())
    await ui._terminate_jobs()
    assert ui._finish_jobs.call_args_list == [call([jobinfo.job for jobinfo in ui._jobs.values()])]
    assert ui._jobs['a'].job.wait.call_args_list == []
    assert ui._jobs['b'].job.wait.call_args_list == []
    assert ui._jobs['c'].job.wait.call_args_list == []
    assert ui._jobs['d'].job.wait.call_args_list == []
    assert ui._jobs['e'].job.wait.call_args_list == [call()]
    assert ui._jobs['f'].job.wait.call_args_list == [call()]
    assert ui._jobs['g'].job.wait.call_args_list == []
    assert ui._jobs['h'].job.wait.call_args_list == []


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_finish_jobs():
    ui = TUI()
    jobs = [
        Mock(is_finished=False, is_enabled=False),
        Mock(is_finished=True, is_enabled=False),
        Mock(is_finished=False, is_enabled=True),
        Mock(is_finished=True, is_enabled=True),
    ]
    ui._finish_jobs(jobs)
    assert jobs[0].finish.call_args_list == [call()]
    assert jobs[1].finish.call_args_list == []
    assert jobs[2].finish.call_args_list == [call()]
    assert jobs[3].finish.call_args_list == []


@pytest.mark.asyncio  # Ensure aioloop exists
async def test_get_exception_from_loop_exception_handler():
    ui = TUI()
    ui._exception = ValueError('asdf')
    ui._jobs = {
        'a': SimpleNamespace(job=Mock(raised=ValueError('foo'), is_enabled=False)),
        'b': SimpleNamespace(job=Mock(raised=None, is_enabled=False)),
        'c': SimpleNamespace(job=Mock(raised=ValueError('bar'), is_enabled=True)),
        'd': SimpleNamespace(job=Mock(raised=None, is_enabled=True)),
    }
    exc = ui._get_exception()
    assert isinstance(exc, ValueError)
    assert str(exc) == 'asdf'

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_get_exception_from_first_failed_enabled_job():
    ui = TUI()
    ui._exception = None
    ui._jobs = {
        'a': SimpleNamespace(job=Mock(raised=ValueError('foo'), is_enabled=False)),
        'b': SimpleNamespace(job=Mock(raised=None, is_enabled=False)),
        'c': SimpleNamespace(job=Mock(raised=ValueError('bar'), is_enabled=True)),
        'd': SimpleNamespace(job=Mock(raised=None, is_enabled=True)),
    }
    exc = ui._get_exception()
    assert isinstance(exc, ValueError)
    assert str(exc) == 'bar'

@pytest.mark.asyncio  # Ensure aioloop exists
async def test_get_exception_returns_None_if_no_exception_raised():
    ui = TUI()
    ui._exception = None
    ui._jobs = {
        'a': SimpleNamespace(job=Mock(raised=None, is_enabled=False)),
        'b': SimpleNamespace(job=Mock(raised=None, is_enabled=False)),
        'c': SimpleNamespace(job=Mock(raised=None, is_enabled=True)),
        'd': SimpleNamespace(job=Mock(raised=None, is_enabled=True)),
    }
    assert ui._get_exception() is None
