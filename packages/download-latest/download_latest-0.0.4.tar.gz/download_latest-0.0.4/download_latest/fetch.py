from __future__ import annotations

import http.client
import io
import os
import logging
import shlex
import shutil
import socket
import subprocess
import urllib.parse
import urllib.request
from typing import List, Sequence

from .meta import DEFAULT_LOGGER
from .task import SubProcessTask, Task
from .util import truncate

__all__ = [
    "DEFAULT_CURL_PATH",
    "DEFAULT_FETCH_BACKEND",
    "FETCH_BACKENDS",
    "CurlDownloadTask",
    "CurlHeadTask",
    "Fetch",
    "FetchException",
    "FetchMeter",
    "FetchParseException",
    "FetchResponse",
    "FetchSubProcessError",
    "FetchSubProcessTask",
    "PythonDownloadTask",
    "PythonHeadTask",
]

DEFAULT_CURL_PATH: str = "curl"
DEFAULT_FETCH_BACKEND: str = "auto"
FETCH_BACKENDS: list[str] = ["auto", "curl", "python"]


class FetchException(http.client.HTTPException):
    """Exception from Fetch."""

    pass


class FetchParseException(FetchException):
    """HTTP parse exception from Fetch."""

    pass


class FetchSubProcessError(FetchException):
    """Subprocess error from Fetch."""

    def __init__(self, process: subprocess.CompletedProcess) -> None:
        self.process = process
        if process.stderr:
            msg = process.stderr.decode("utf-8", errors="ignore").strip()
        else:
            program = process.args[0] if process.args else ""
            msg = f"{program} exited {process.returncode}"
        super().__init__(msg)


class FetchMeter:
    """
    An abstract class that can be used with Fetch to provide a progress meter.
    """

    def period(self) -> float | int:
        """Return the time in seconds per iteration."""
        return 0.1

    def begin(self) -> None:
        """Called at the beginning of the loop."""
        pass

    def step(self, index: int) -> None:
        """
        Called with each loop iteration.

        The index argument will provide a running count, starting at 0.
        """
        pass

    def end(self) -> None:
        """Called at the end of the loop."""
        pass


class FetchResponse:
    """A useful subset of an HTTPResponse."""

    def __init__(
        self,
        url: str,
        headers: http.client.HTTPMessage,
        status: int,
        reason: str,
    ):
        self.url = url
        self.headers = headers
        self.status = status
        self.reason = reason

    @classmethod
    def make_from_http_response(
        cls, response: http.client.HTTPResponse
    ) -> FetchResponse:
        return cls(
            url=response.url,  # type: ignore
            headers=response.headers,
            status=response.status,
            reason=response.reason,
        )

    @classmethod
    def make_from_raw_headers(cls, url: str, raw_headers: bytes) -> FetchResponse:
        """
        The HTTPResponse initializer patched to support bytes instead of a
        socket argument.
        """

        class FakeSocket(socket.socket):
            def __init__(self, fp: io.IOBase) -> None:
                self.fp = fp

            def makefile(self, *args, **kwargs) -> io.IOBase:  # type: ignore
                return self.fp

        raw_headers = cls._patch_raw_headers(raw_headers)
        raw_stream = io.BytesIO(raw_headers)
        sock = FakeSocket(raw_stream)

        try:
            response = http.client.HTTPResponse(sock, method="HEAD", url=url)
            response.begin()
        except (http.client.HTTPException, ValueError):
            raise FetchParseException("cannot parse")

        return cls(
            url=url,
            headers=response.headers,
            status=response.status,
            reason=response.reason,
        )

    @classmethod
    def make_from_raw_multiple_headers(
        cls,
        url: str,
        raw_multiple_headers: bytes,
    ) -> list[FetchResponse]:
        """
        Return a list of FetchResponses from the raw bytes of one or more HEAD
        requests.
        """
        responses = []
        for raw_headers in raw_multiple_headers.strip().split(b"\r\n\r\n"):
            response = cls.make_from_raw_headers(url=url, raw_headers=raw_headers)
            responses.append(response)
            location = response.headers["location"]
            if location:
                url = urllib.parse.urljoin(url, location)
        return responses

    @classmethod
    def _patch_raw_headers(cls, raw_headers: bytes) -> bytes:
        """
        Replace HTTP/x with HTTP/1.1 in a raw response so HTTPResponse.begin()
        doesn't throw an exception. Also, add a fake HTTP status line if we
        don't find one to handle non-HTTP protocols.
        """
        raw_lines = raw_headers.strip().split(b"\r\n")
        parts = raw_lines[0].split(None, 1) if raw_lines else []
        if parts and parts[0].startswith(b"HTTP"):
            raw_lines[0] = b" ".join([b"HTTP/1.1"] + parts[1:])
        else:
            raw_lines.insert(0, b"HTTP/1.1 200 OK")
        return b"\r\n".join(raw_lines + [])


class Fetch:
    """HTTP request handlers with cURL and Python backends."""

    backend: str
    logger: logging.Logger
    meter: FetchMeter | None

    def __init__(
        self,
        backend: str | None = None,
        logger: logging.Logger | None = None,
        meter: FetchMeter | None = None,
    ) -> None:
        """Create a Fetch instance."""

        if backend is None:
            backend = DEFAULT_FETCH_BACKEND
        if logger is None:
            logger = DEFAULT_LOGGER

        self.backend = backend
        self.logger = logger
        self.meter = meter

    def download(
        self,
        url: str,
        path: os.PathLike | str,
        resume: bool = False,
    ) -> bool:
        """Download url to path and return success."""

        task_type = self._get_download_task_type()
        task = task_type(url=url, path=path, resume=resume, logger=self.logger)
        self._run(task)
        return task.check()

    def head(self, url: str) -> list[FetchResponse]:
        """Make HEAD requests to url and return the responses."""

        task_type = self._get_head_task_type()
        task = task_type(url=url, logger=self.logger)
        self._run(task)
        return task.check()

    def resolve_backend(self):
        """Return the actual backend used (sans auto)."""
        if self.backend == "auto":
            if shutil.which(DEFAULT_CURL_PATH):
                return "curl"
            else:
                return "python"
        else:
            return self.backend

    # Private

    def _get_download_task_type(
        self,
    ) -> type[CurlDownloadTask] | type[PythonDownloadTask]:
        """Return the Task type for download."""

        if self.resolve_backend() == "curl":
            return CurlDownloadTask
        else:  # python
            return PythonDownloadTask

    def _get_head_task_type(self) -> type[CurlHeadTask] | type[PythonHeadTask]:
        """Return the Task type for head."""

        if self.resolve_backend() == "curl":
            return CurlHeadTask
        else:  # python
            return PythonHeadTask

    def _run(self, task) -> None:
        """Run the task, calling the meter if specified."""

        task.begin()
        if self.meter:
            self.meter.begin()
            for index in task.loop(period=self.meter.period()):
                self.meter.step(index)
            self.meter.end()
        else:
            task.wait()
        task.end()


class FetchSubProcessTask(SubProcessTask):
    """A concurrent subprocess runner with logging."""

    args: Sequence[str]

    def __init__(self, args: Sequence[str], logger: logging.Logger):
        """Create a subprocess Task."""

        super().__init__(args)
        self.logger = logger

    def begin(self) -> None:
        """Log some data."""
        cmd = " ".join(shlex.quote(arg) for arg in self.args)
        self.logger.debug(f"    exec: {cmd}")

    def check_process(self) -> subprocess.CompletedProcess:
        """
        Return the CompletedProcess.

        Raise a FetchSubProcessError if the subprocess exited in error.
        """
        process = self.get()
        if process.returncode == 0:
            return process
        else:
            raise FetchSubProcessError(process)

    def end(self) -> None:
        """Log some more data."""
        process = self.get()
        self.logger.debug(
            truncate(
                f"    exec: code={process.returncode} "
                + f"out={process.stdout!r} err={process.stderr!r}",
                80,
            )
        )


class CurlDownloadTask(FetchSubProcessTask):
    """Download using cURL."""

    def __init__(
        self,
        url: str,
        path: os.PathLike | str,
        resume: bool,
        logger: logging.Logger,
    ):
        args = [
            DEFAULT_CURL_PATH,
            "--silent",
            "--show-error",
            "--fail",
            "--location",
            "--output",
            str(path),
            *(["--continue-at", "-"] if resume else []),
            "--",
            url,
        ]
        super().__init__(args=args, logger=logger)
        self.url = url
        self.path = path
        self.resume = resume

    def check(self) -> bool:
        """
        Return True.

        Raise a FetchSubProcessError if cURL exited in error.
        """
        return bool(super().check_process())


class CurlHeadTask(FetchSubProcessTask):
    """Make HEAD requests using cURL."""

    def __init__(
        self,
        url: str,
        logger: logging.Logger,
    ):
        args = [
            DEFAULT_CURL_PATH,
            "--silent",
            "--show-error",
            "--location",
            "--head",
            "--",
            url,
        ]
        super().__init__(args=args, logger=logger)
        self.url = url

    def check(self) -> list[FetchResponse]:
        """
        Return a list of FetchResponses.

        Raise a FetchSubProcessError if cURL exited in error.
        """
        process = super().check_process()
        responses = FetchResponse.make_from_raw_multiple_headers(
            url=self.url, raw_multiple_headers=process.stdout
        )
        if responses:
            return responses
        else:  # pragma: no cover
            raise RuntimeError("expected responses")


def convert_urllib_friendly_url(url: str) -> str:
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme == "":
        return "http://" + url
    else:
        return url


class PythonDownloadTask(Task[bool]):
    """Download using Python urllib."""

    request_url: str

    def __init__(
        self,
        url: str,
        path: os.PathLike | str,
        resume: bool,
        logger: logging.Logger,
    ):
        super().__init__()
        self.url = url
        self.path = path
        self.resume = resume
        self.logger = logger
        self.request_url = convert_urllib_friendly_url(url)

    def begin(self) -> None:
        self.logger.debug(f"  python: download {self.url} -> {str(self.path)}")

    def check(self) -> bool:
        """
        Return True.

        Raise a FetchException if download failed.
        """
        success = self.get()
        if success:
            return success
        else:
            raise FetchException("download failed")

    def end(self) -> None:
        self.logger.debug("  python: download finished")

    def run(self) -> bool:
        try:
            urllib.request.urlretrieve(self.request_url, filename=self.path)
            return True
        except urllib.error.ContentTooShortError:
            self.logger.warning("  python: size mismatch")
            return True
        except Exception as e:
            self.logger.error(f"  python: {str(e)}")
            return False


class PythonHeadTask(Task[List[FetchResponse]]):
    """Make HEAD requests using Python urllib."""

    request_url: str

    def __init__(self, url: str, logger: logging.Logger):
        """Create the task."""

        super().__init__()
        self.url = url
        self.logger = logger
        self.request_url = convert_urllib_friendly_url(url)

    def begin(self) -> None:
        self.logger.debug(f"  python: head {self.url}")

    def check(self) -> list[FetchResponse]:
        """
        Return a list of FetchResponses.

        Raise a FetchException if there were no responses.
        """
        responses = self.get()
        if responses:
            return responses
        else:
            raise FetchException("no responses")

    def end(self) -> None:
        self.logger.debug("  python: head finished")

    def run(self) -> list[FetchResponse]:
        """Make HEAD requests, following redirects, and return the responses."""

        url = self.url
        responses: list[FetchResponse] = []

        class PassHTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(
                self, *args, **kwargs
            ) -> urllib.request.Request | None:
                fp: http.client.HTTPResponse = args[1]
                if not responses:
                    fp.url = url  # type: ignore
                responses.append(FetchResponse.make_from_http_response(fp))
                return super().redirect_request(*args, **kwargs)

        try:
            opener = urllib.request.build_opener(PassHTTPRedirectHandler)
            request = urllib.request.Request(self.request_url, method="HEAD")
            try:
                response = opener.open(request)
            except urllib.error.HTTPError as e:
                response = e.fp
            responses.append(FetchResponse.make_from_http_response(response))

        finally:
            return responses
