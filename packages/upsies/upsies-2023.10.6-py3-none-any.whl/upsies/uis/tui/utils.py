import sys

import logging  # isort:skip
_log = logging.getLogger(__name__)


def is_tty():
    """Whether we live in a terminal and can interacte with the user"""
    # As long as we have input and output, we have user interaction. sys.stdout
    # may be redirected, but prompt-toolkit will print to sys.stderr instead.
    if not sys.stdin or (not sys.stdout and not sys.stderr):
        return False
    else:
        if sys.stdin.isatty():
            if sys.stdout and sys.stdout.isatty():
                return True
            elif sys.stderr and sys.stderr.isatty():
                return True
        return False
