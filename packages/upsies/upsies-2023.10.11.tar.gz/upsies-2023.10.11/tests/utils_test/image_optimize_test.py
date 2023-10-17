import re
from unittest.mock import call

import pytest

from upsies import errors
from upsies.utils import image


def test_optimization_levels():
    assert image.optimization_levels == (
        'low',
        'medium',
        'high',
        'placebo',
        'none',
        'default',
    )


@pytest.mark.parametrize(
    argnames='level, cmd_output, exp_cmd_called, exp_exception, exp_level',
    argvalues=(
        (None, '', False, None, None),
        ('none', '', False, None, None),
        ('default', '', True, None, '2'),
        ('low', '', True, None, '1'),
        ('medium', '', True, None, '2'),
        ('high', '', True, None, '4'),
        ('foo', '', False, errors.ImageOptimizeError('Invalid optimization level: foo'), None),
        ('default', 'Error message', True, errors.ImageOptimizeError('Failed to optimize: Error message'), '2'),
    ),
    ids=lambda v: repr(v),
)
def test_optimize(level, cmd_output, exp_cmd_called, exp_level, exp_exception, mocker):
    run_mock = mocker.patch('upsies.utils.subproc.run', return_value=cmd_output)

    image_file = 'path/to/image.png'

    if isinstance(exp_exception, Exception):
        with pytest.raises(type(exp_exception), match=rf'^{re.escape(str(exp_exception))}$'):
            image.optimize(image_file, level=level)
    else:
        image.optimize(image_file, level=level)

    if exp_cmd_called:
        assert run_mock.call_args_list == [call(
            [
                'oxipng', '--quiet', '--preserve',
                '--opt', str(exp_level),
                '--interlace', '0',
                '--strip', 'safe',
                image_file,
            ],
            join_stderr=True,
        )]
    else:
        assert run_mock.call_args_list == []
