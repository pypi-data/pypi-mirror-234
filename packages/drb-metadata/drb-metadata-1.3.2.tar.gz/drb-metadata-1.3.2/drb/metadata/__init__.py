from .core import DrbMetadata, MetadataAddon
from . import _version

__all__ = [
    'DrbMetadata',
    'MetadataAddon'
]
__version__ = _version.get_versions()['version']
