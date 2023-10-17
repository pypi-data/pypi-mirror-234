#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""PyTDI module."""

import importlib_metadata

from .core import TDICombination
from .core import LISATDICombination
from .core import LISAClockCorrection
from .interface import Data


try:
    __version__ = importlib_metadata.version('pytdi')
    metadata = importlib_metadata.metadata('pytdi').json
    __author__ = metadata['author']
    __email__ = metadata['author_email']
    __copyright__ = \
        '2021, Max Planck Institute for Gravitational Physics ' \
        '(Albert Einstein Institute) and California Institute of Technology'
except importlib_metadata.PackageNotFoundError:
    pass
