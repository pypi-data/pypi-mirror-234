from __future__ import annotations

import dataclasses
import enum
import logging
import os
from pathlib import Path
import time
from typing import Sequence

from .cache import Cache
from .fetch import Fetch, FetchMeter, FetchResponse
from .meta import DEFAULT_LOGGER
from .util import (
    deduce_filename_from_url,
    get_file_md5,
    get_file_modified,
    get_file_size,
    get_human_file_size,
    get_human_time,
    parse_header_accept_ranges,
    parse_header_content_length,
    parse_header_content_md5,
    parse_header_etag,
    parse_header_last_modified,
    rm_f,
    truncate,
)


__all__ = [
    "Decision",
    "DownloadLatest",
    "DownloadLatestException",
    "FileData",
]


class DownloadLatestException(Exception):
    """Exception raised by DownloadLatest."""

    pass


@dataclasses.dataclass
class FileData:
    """Local or Remote attributes for DownloadLatest."""

    etag: str | None = None
    md5: str | None = None
    modified: int | None = None
    resume: bool = False
    size: int | None = None


@dataclasses.dataclass
class Decision:
    """Decision parameters for DownloadLatest."""

    action: str = "downloading"
    download: bool = True
    local: FileData = dataclasses.field(default_factory=FileData)
    remote: FileData = dataclasses.field(default_factory=FileData)
    restart: bool = False
    resume: bool = False
    resume_restart_reason: str | None = None
    resume_start_at: int | None = None


class State(enum.Enum):
    """State for DownloadLatest."""

    HEAD_READY = 1
    HEAD_BEGIN = 2
    HEAD_OK = 3
    HEAD_ERROR = 4
    DOWNLOAD_READY = 5
    DOWNLOAD_ABORTED = 6
    DOWNLOAD_PASS = 7
    DOWNLOAD_BEGIN = 8
    DOWNLOAD_ERROR = 9
    DOWNLOAD_OK = 10


class DownloadLatest:
    r"""
    Download a file only if the remote file has changed.

    Example:

    >>> from download_latest import DownloadLatest
    >>> dl = DownloadLatest("fsf.org/robots.txt")
    >>> if dl.run(): dl.file.open().readline()
    ...
    '# robots.txt for http://www.fsf.org/\n'
    >>> if dl.run(): dl.file.open().readline()
    ...
    >>> # won't re-download if no changes
    """

    url: str
    file: Path
    backend: str
    dry_run: bool
    force: bool
    logger: logging.Logger

    local_output_path: Path
    local_download_path: Path
    local_new_path: Path

    state: State
    cache: Cache
    fetch: Fetch
    decision: Decision | None
    responses: Sequence[FetchResponse] | None

    def __init__(
        self,
        url: str,
        file: os.PathLike | str | None = None,
        backend: str | None = None,
        dry_run: bool = False,
        force: bool = False,
        logger: logging.Logger | None = None,
        meter: FetchMeter | None = None,
    ):
        """
        Create a new DownloadLatest instance.

        Deduce file if not specified. Raise a DownloadLatestException if it
        cannot not deduce file.

        Raise a DownloadLatestException if one of the paths is not writeable.
        """
        self.url = url
        if file is None:
            self.file = self._deduce_file(url)
        else:
            self.file = self._check_file(file)

        local_output_path = self.file.resolve()
        name = local_output_path.name
        self.local_output_path = local_output_path
        self.local_download_path = local_output_path.with_name(f"{name}.download")
        self.local_new_path = local_output_path.with_name(f"{name}.new")

        self._require_writeable(self.local_output_path)
        self._require_writeable(self.local_download_path)
        self._require_writeable(self.local_new_path)

        self.dry_run = dry_run
        self.force = force
        self.logger = DEFAULT_LOGGER if logger is None else logger

        self.cache = Cache(logger=logger)
        self.fetch = Fetch(backend=backend, logger=logger, meter=meter)
        self.decision = None
        self.responses = None
        self.state = State.HEAD_READY

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url!r}, {str(self.file)!r})"

    def run(self) -> bool:
        """
        Run the download steps in sequence and return whether or not the
        download occured.
        """
        self.log_paths()
        self.head()
        self.decide()
        self.log_decision()
        self.download()
        return self.state is State.DOWNLOAD_OK

    def log_paths(self) -> DownloadLatest:
        """Log the url, file and local paths."""

        self.logger.info(f"     url: {self.url}")
        self.logger.info(f"    file: {self.file}")

        def debug_path(name, path):
            suffix = " (exists)" if path.exists() else ""
            self.logger.debug(f"{name}: {path}{suffix}")

        debug_path("  output", self.local_output_path)
        debug_path("download", self.local_download_path)
        debug_path("     new", self.local_new_path)

        return self

    def head(self) -> DownloadLatest:
        """
        Make HEAD requests to url, following redirects, and set responses.

        Raise a DownloadLatestException if the server returned an error or no
        response was received.
        """
        self.state = State.HEAD_BEGIN

        try:
            responses = self.fetch.head(self.url)
        finally:
            self.state = State.HEAD_ERROR

        if not responses:
            raise DownloadLatestException("no response received")
        self.responses = responses

        for i, response in enumerate(responses):
            headn = f"head {i + 1}"
            self.logger.debug(f"{headn:>8}: [{response.status}] {response.url}")

        status = responses[-1].status
        if status < 200 or 299 < status:
            raise DownloadLatestException(f"server returned error: {status}")
        else:
            self.state = State.HEAD_OK
            return self

    def decide(self) -> DownloadLatest:
        """Make decision based on remote / local file metadata."""

        self._require_response()
        self.cache.load()

        d = Decision(
            local=self._get_local_data(),
            remote=self._get_remote_data(),
        )

        if not self.force and self.local_download_path.exists():
            dc = self.cache.data["download"].get(str(self.local_download_path))
            if not d.remote.resume:
                d.restart = True
                d.resume_restart_reason = "server resume not supported"
            elif (
                isinstance(dc, dict)
                and self.url == dc.get("url")
                and (
                    (d.remote.etag is not None and d.remote.etag == dc.get("etag"))
                    or (d.remote.md5 is not None and d.remote.md5 == dc.get("md5"))
                    or (
                        d.remote.modified is not None
                        and d.remote.size is not None
                        and d.remote.modified == dc.get("modified")
                        and d.remote.size == dc.get("size")
                    )
                )
            ):
                d.resume = True
                size = get_file_size(self.local_download_path) or 0
                d.resume_start_at = size
                d.resume_restart_reason = "cache match, resuming"
            else:
                d.restart = True
                d.resume_restart_reason = "cache mismatch, not resuming"

        if self.force:
            d.action = "downloading (force enabled)"
        elif d.restart:
            d.action = "restarting download"
        elif d.resume:
            d.action = (
                f"resuming download from {get_human_file_size(d.resume_start_at or 0)}"
            )
        elif not self.local_output_path.exists():
            d.action = "downloading"
        elif d.remote.md5 is not None and d.local.md5 is not None:
            if d.remote.md5 == d.local.md5:
                d.download = False
                d.action = "md5 match, not downloading"
            else:
                d.action = "md5 mismatch, downloading"
        elif d.remote.etag is not None and d.local.etag is not None:
            if d.remote.etag == d.local.etag:
                d.download = False
                d.action = "etag match, not downloading"
            else:
                d.action = "etag mismatch, downloading"
        elif (
            d.remote.size is not None
            and d.local.size is not None
            and d.remote.modified is not None
            and d.local.modified is not None
            and d.remote.size == d.local.size
            and d.remote.modified == d.local.modified
        ):
            d.download = False
            d.action = "size and modified match, not downloading"
        else:
            d.action = "local / remote mismatch, downloading"

        self.decision = d
        self.state = State.DOWNLOAD_READY
        return self

    def log_decision(self) -> DownloadLatest:
        """Log decision details."""

        d = self._require_decision()

        def v(where, key):
            value = getattr(getattr(d, where), key)
            if value is None:
                value = "-"
            else:
                if key == "size":
                    value = get_human_file_size(value)
                elif key == "modified":
                    value = get_human_time(value)
                elif key == "resume":
                    value = ("" if value else "un") + "supported"
            return truncate(value, 34)

        self.logger.debug(f"{'-'*23} local {'-'*28} remote {'-'*14}")
        for key in ("md5", "etag", "size", "modified", "resume"):
            self.logger.debug(f"{key:>8}: {v('local', key):<34} {v('remote',key)}")
        self.logger.debug("-" * 80)

        if d.resume_restart_reason:
            self.logger.info(f"  resume: {d.resume_restart_reason}")

        action = d.action
        if d.download and not d.resume:
            if d.remote.size is not None:
                action += " " + get_human_file_size(d.remote.size)
            else:
                action += " (unknown size)"

        self.logger.info(f"  action: {action}")

        return self

    def download(self) -> DownloadLatest:
        """Start the download."""

        self.state = State.DOWNLOAD_ABORTED

        response = self._require_response()
        decision = self._require_decision()

        if self.dry_run:
            self.logger.debug("  result: dry-run enabled, passing")
            self.state = State.DOWNLOAD_PASS
            return self

        rm_f(self.local_new_path)
        if not decision.download:
            rm_f(self.local_download_path)
            self.logger.debug("  result: no download needed")
            self.state = State.DOWNLOAD_PASS
            return self

        if decision.resume:
            start_size = decision.resume_start_at or 0
        else:
            start_size = 0

        with self.cache.update() as data:
            data["download"][str(self.local_download_path)] = {
                "url": self.url,
                "md5": decision.remote.md5,
                "etag": decision.remote.etag,
                "size": decision.remote.size,
                "modified": decision.remote.modified,
            }

        self.state = State.DOWNLOAD_BEGIN
        start = time.time()
        try:
            self.fetch.download(
                url=response.url,
                path=self.local_download_path,
                resume=decision.resume,
            )
        finally:
            self.state = State.DOWNLOAD_ERROR
        elapsed = time.time() - start

        download_md5 = get_file_md5(self.local_download_path)
        download_size = get_file_size(self.local_download_path) or 0
        transfered = download_size - start_size

        if decision.remote.md5 is not None and download_md5 != decision.remote.md5:
            self.logger.error("   error: md5 mismatch")
            return self

        if decision.remote.size is not None:
            human_comparison = (
                f"expected {get_human_file_size(decision.remote.size)}, "
                + f"actual {get_human_file_size(download_size)}"
            )
            if download_size > decision.remote.size:
                self.logger.warning(
                    f" warning: size mismatch {human_comparison}, probably okay"
                )
            elif download_size < decision.remote.size:
                self.logger.error(f"   error: size mismatch: {human_comparison}")

        with self.cache.update() as data:
            data["download"].pop(str(self.local_download_path), None)
            if decision.remote.etag:
                data["output"][str(self.local_output_path)] = {
                    "md5": download_md5,
                    "etag": decision.remote.etag,
                }
            else:
                data["output"].pop(str(self.local_output_path), None)

        rm_f(self.local_output_path)
        self.local_download_path.rename(self.local_output_path)

        modified = decision.remote.modified
        if modified is not None:
            os.utime(self.local_output_path, (modified, modified))

        self.local_new_path.open("a+")

        # HACK: the green color is determined by the first word being 'success'
        self.logger.info(
            f" success: transferred {get_human_file_size(transfered)}"
            + f" in {elapsed:.1f}s"
        )

        self.state = State.DOWNLOAD_OK
        return self

    # Private

    def _check_file(self, file: os.PathLike | str) -> Path:
        """
        Check the file to make sure it's not empty and return it.

        Raise a DownloadLatestException otherwise.
        """
        file = Path(file)
        resolved_name = file.resolve().name
        if resolved_name == "" or resolved_name == "..":
            raise DownloadLatestException(f"filename is empty: {str(file)!r}")
        return file

    def _deduce_file(self, url: str) -> Path:
        """
        Deduce a file from url.

        Raise DownloadLatestException if not possible.
        """
        filename = deduce_filename_from_url(url)
        if filename:
            return self._check_file(filename)
        else:
            raise DownloadLatestException("cannot deduce filename")

    def _get_local_data(self) -> FileData:
        """Return the local output file data."""
        md5 = self._get_local_md5()
        return FileData(
            etag=self._get_local_etag_from_cache(check_md5=md5),
            md5=md5,
            modified=self._get_local_modified(),
            resume=True,
            size=self._get_local_size(),
        )

    def _get_local_etag_from_cache(self, check_md5: str | None = None) -> str | None:
        """Return the local output etag stored in the cache."""
        output_cache = self.cache.data["output"]
        info = output_cache.get(str(self.local_output_path))

        if isinstance(info, dict) and check_md5 is not None:
            etag = info.get("etag")
            md5 = info.get("md5")

            if check_md5 == md5:
                return etag
            else:
                self.logger.warning("cached local etag: md5 mismatch")
        return None

    def _get_local_md5(self) -> str | None:
        """Return the local output md5."""
        return get_file_md5(self.local_output_path)

    def _get_local_modified(self) -> int | None:
        """Return the local output modified time."""
        return get_file_modified(self.local_output_path)

    def _get_local_size(self) -> int | None:
        """Return the local output file size."""
        return get_file_size(self.local_output_path)

    def _get_remote_data(self) -> FileData:
        """Return the remote file data."""
        return FileData(
            etag=self._get_remote_etag(),
            md5=self._get_remote_md5(),
            modified=self._get_remote_modified(),
            resume=self._get_remote_resume(),
            size=self._get_remote_size(),
        )

    def _get_remote_etag(self) -> str | None:
        """Return the remote etag."""
        headers = self._require_response().headers
        return parse_header_etag(headers)

    def _get_remote_md5(self) -> str | None:
        """Return the remote md5."""
        headers = self._require_response().headers
        return parse_header_content_md5(headers)

    def _get_remote_modified(self) -> int | None:
        """Return the remote modified time."""
        headers = self._require_response().headers
        return parse_header_last_modified(headers)

    def _get_remote_resume(self) -> bool:
        """Return whether the server supports resuming downloads."""
        headers = self._require_response().headers
        return parse_header_accept_ranges(headers)

    def _get_remote_size(self) -> int | None:
        """Return the remote file size."""
        headers = self._require_response().headers
        return parse_header_content_length(headers)

    def _require_decision(self) -> Decision:
        """Raise DownloadLatestException if no decision was made."""
        if self.decision:
            return self.decision
        else:
            raise DownloadLatestException("no decision made")

    def _require_response(self) -> FetchResponse:
        """Raise DownloadLatestException if no response was received."""
        if self.responses:
            return self.responses[-1]
        else:
            raise DownloadLatestException("no response received")

    def _require_writeable(self, path: Path) -> Path:
        """Raise DownloadLatestException if path is not writeable."""
        if not path.exists() or path.is_file():
            return path
        else:
            raise DownloadLatestException(f"file exists: {path}")
