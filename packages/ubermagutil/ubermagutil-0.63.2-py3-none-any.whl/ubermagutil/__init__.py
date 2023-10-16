"""Utilities used across Ubermag."""
import importlib.metadata

import pytest

from . import progress
from .basic_logging import setup_logging
from .inherit_docs import inherit_docs
from .tools import changedir, hysteresis_values

__version__ = importlib.metadata.version(__package__)


def test():
    """Run all package tests.

    Examples
    --------
    1. Run all tests.

    >>> import ubermagutil as uu
    ...
    >>> # uu.test()

    """
    return pytest.main(["-v", "--pyargs", "ubermagutil", "-l"])  # pragma: no cover
