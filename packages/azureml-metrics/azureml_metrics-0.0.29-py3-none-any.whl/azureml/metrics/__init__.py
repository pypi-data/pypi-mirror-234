# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contains metrics computation classes for Azure Machine Learning."""
import sys

from ._score import compute_metrics, score
from ._score import list_metrics, list_tasks

__all__ = [
    "compute_metrics",
    "score",
    "list_metrics",
    "list_tasks",
]

# TODO copy this file as part of setup in runtime package
__path__ = __import__('pkgutil').extend_path(__path__, __name__)  # type: ignore

try:
    from ._version import ver as VERSION, selfver as SELFVERSION

    __version__ = VERSION
except ImportError:
    VERSION = '0.0.0+dev'
    SELFVERSION = VERSION
    __version__ = VERSION

module = sys.modules[__name__]
