from . import _version
from .core import (Image, ImageAddon)

__version__ = _version.get_versions()['version']

__all__ = [
    'Image',
    'ImageAddon'
]
