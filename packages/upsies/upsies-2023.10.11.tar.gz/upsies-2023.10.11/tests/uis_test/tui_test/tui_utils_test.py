from unittest.mock import Mock

import pytest

from upsies.uis.tui import utils


@pytest.mark.parametrize(
    argnames='stdin_isatty, stdout_isatty, stderr_isatty',
    argvalues=(
        (False, False, False),
        (False, False, True),
        (False, True, False),
        (False, True, True),
        (True, False, False),
        (True, False, True),
        (True, True, False),
        (True, True, True),
    ),
)
@pytest.mark.parametrize(
    argnames='stdin, stdout, stderr',
    argvalues=(
        (None, None, None),
        (None, None, Mock()),
        (None, None, Mock()),
        (None, Mock(), None),
        (None, Mock(), Mock()),
        (Mock(), None, None),
        (Mock(), None, Mock()),
        (Mock(), Mock(), None),
        (Mock(), Mock(), Mock()),
    ),
)
def test_is_tty(stdin, stdout, stderr, stdin_isatty, stdout_isatty, stderr_isatty, mocker):
    if stdin:
        stdin.isatty = lambda: stdin_isatty
    if stdout:
        stdout.isatty = lambda: stdout_isatty
    if stderr:
        stderr.isatty = lambda: stderr_isatty
    mocker.patch('sys.stdin', stdin)
    mocker.patch('sys.stdout', stdout)
    mocker.patch('sys.stderr', stderr)

    if not stdin or not stdin.isatty():
        exp_is_tty = False
    elif (stdout and stdout.isatty()) or (stderr and stderr.isatty()):
        exp_is_tty = True
    else:
        exp_is_tty = False

    assert utils.is_tty() is exp_is_tty
