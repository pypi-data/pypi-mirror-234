from __future__ import annotations

import importlib
import os
import pathlib

VERSION = importlib.metadata.version('texutils')
COMMANDS = ('extract-refs',)

COLORS = {
    'red': '\033[41m',
    'green': '\033[42m',
    'yellow': '\033[43;30m',
    'turquoise': '\033[46;30m',
    'subtle': '\033[2m',
    'normal': '\033[m'
}

DESCRIPTION = """\
texutils is a collection of utilities for working with LaTeX files.

The following commands are available:
    - `extract-refs`: Extract the references from a LaTeX file and save them in various formats.
"""

CWD = pathlib.Path(os.getcwd())
