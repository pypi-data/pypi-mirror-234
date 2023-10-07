import sys

if sys.version_info[:2] >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

from .classes import Model
from .decorators import expectation, model

__version__ = metadata.version(__package__ or 'bauplan')

del metadata

__all__ = [
    'Model',
    'model', 'expectation',
    '__version__',
]
