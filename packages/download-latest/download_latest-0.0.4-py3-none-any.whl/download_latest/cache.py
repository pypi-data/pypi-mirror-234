from __future__ import annotations

from contextlib import contextmanager
import json
import logging
import os
from pathlib import Path
import time
from typing import ClassVar, Generator, IO

from .meta import DEFAULT_LOGGER
from .util import get_user_cache_dir, rm_f

__all__ = ["Cache"]


class Cache:
    """A store of request and file metadata."""

    DEFAULT_LOCK_TIMEOUT: ClassVar[float] = 0.5  # seconds
    LOCK_SLEEP_INTERVAL: ClassVar[float] = 0.01  # seconds
    MAIN_CACHE_KEYS: ClassVar[set] = {"download", "output"}

    cache_dir: Path
    lock_timeout: int | float
    logger: logging.Logger
    data: dict

    def __init__(
        self,
        cache_dir: str | os.PathLike | None = None,
        lock_timeout: int | float | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        """
        Create the cache.

        If cache_dir is not specified, then use get_user_cache_dir().
        """
        if cache_dir is None:
            cache_dir = get_user_cache_dir()
        if lock_timeout is None:
            lock_timeout = self.DEFAULT_LOCK_TIMEOUT
        if logger is None:
            logger = DEFAULT_LOGGER

        self.cache_dir = Path(cache_dir)
        self.lock_timeout = lock_timeout
        self.logger = logger
        self.data = self._normalize({})

    @property
    def cache_path(self) -> Path:
        """Return the path to the cache file."""
        return self.cache_dir / "cache.json"

    @property
    def lock_path(self) -> Path:
        """Return the path to the lock file."""
        return self.cache_dir / "cache.lock"

    def load(self) -> dict:
        """Load the cache and return it."""
        with self.lock():
            new_data = self._read()
            if isinstance(new_data, dict):
                self.data = self._normalize(new_data)
            return self.data

    @contextmanager
    def lock(self) -> Generator:
        """
        Wait / block until lock_path is available. Release when lock_timeout is
        reached, logging a warning.
        """
        self._ensure_cache_dir()
        start = None
        while True:
            try:
                self._open_exclusive(self.lock_path)
                break
            except FileExistsError:
                pass
            except OSError as e:
                self.logger.warning(f"cache lock error: {str(e)}")
            if start is None:
                self.logger.debug("cache lock detected")
                start = time.time()
            elapsed = time.time() - start
            if elapsed > self.lock_timeout:
                self.logger.warning("cache lock timeout")
                break
            time.sleep(self.LOCK_SLEEP_INTERVAL)
        try:
            yield
        finally:
            rm_f(self.lock_path)

    @contextmanager
    def update(self) -> Generator:
        """
        Return the cache from the filesystem to a yield context. Then, save the
        result back to the filesystem.

        >>> with Cache().update() as data:
        ...     data['foo'] = bar
        """
        with self.lock():
            new_data = self._read()
            if isinstance(new_data, dict):
                self.data = self._normalize(new_data)
            yield self.data
            self._write(self.data)

    # Private

    def _ensure_cache_dir(self) -> None:
        """Make the cache directory if it does not exist."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _open_exclusive(self, path: Path, **kwargs) -> IO:
        """Open path exclusively, i.e., it must not exist."""
        return path.open(mode="x", **kwargs)

    def _normalize(self, data: dict) -> dict:
        """Normalize the cache dictionary."""
        for key in self.MAIN_CACHE_KEYS:
            value = data.get(key)
            if not isinstance(value, dict):
                data[key] = {}
        return data

    def _read(self) -> object:
        """Read the parsed JSON from the filesystem cache and return it."""
        try:
            return self._read_json(self.cache_path)
        except (FileNotFoundError, ValueError):
            pass
        except OSError as e:
            self.logger.warning(f"cache read error: {str(e)}")
        return None

    def _read_json(self, path: Path) -> object:
        """Read and parse JSON data from path."""
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: dict) -> None:
        """Write a dictionary to the filesystem cache as JSON."""
        try:
            self._write_json(self.cache_path, data)
        except OSError as e:
            self.logger.warning(f"cache write error: {str(e)}")

    def _write_json(self, path: Path, data: object) -> None:
        """Write data to path as JSON."""
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
