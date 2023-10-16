from __future__ import annotations

import logging

try:  # pragma: no cover
    from importlib.metadata import metadata  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    from importlib_metadata import metadata  # type: ignore

__all__ = [
    "DEFAULT_LOGGER",
    "__description__",
    "__program__",
    "__version__",
]

__package = __name__.split(".")[0]
__metadata = metadata(__package)

DEFAULT_LOGGER = logging.getLogger(__package)
__description__ = __metadata["Summary"]
__program__ = __metadata["Name"]
__version__ = __metadata["Version"]
