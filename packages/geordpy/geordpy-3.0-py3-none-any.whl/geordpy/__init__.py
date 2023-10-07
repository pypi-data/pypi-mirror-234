from . import _version

__version__ = _version.get_versions()["version"]

from .geordpy import rdp_filter  # noqa: F401
