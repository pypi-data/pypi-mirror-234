from __future__ import annotations

import subprocess
import threading
from typing import ClassVar, Generic, Iterable, Sequence, TypeVar
import time


T = TypeVar("T")


class TaskTimeout(Exception):
    """Exception for Task.wait() when timeout is specified."""

    def __init__(self, timeout: float | int) -> None:
        super().__init__(f"{timeout}s elapsed")


class Task(Generic[T]):
    """
    A concurrent task runner using threading.Thread.

    Example:

    >>> class TimeConsumingTask(Task[float]):
    ...     def __init__(self, a: int, b: int, duration: float) -> None:
    ...         super().__init__()
    ...         self.a, self.b, self.duration = a, b, duration
    ...
    ...     def run(self) -> float:
    ...         try:
    ...             time.sleep(self.duration)
    ...             return float(self.a / self.b)
    ...         except Exception:
    ...             return float("NaN")
    ...
    >>> task = TimeConsumingTask(3, 2, 0.7)
    >>> for i in task.loop(period=0.2):
    ...     print(i)
    0
    1
    2
    3
    >>> task.get()
    1.5
    """

    MAX_SLEEP: ClassVar[float] = 1 / 60

    _lock: threading.Lock
    _result: T | None
    _thread: threading.Thread | None

    def __init__(self) -> None:
        """Create the task."""
        self._result = None
        self._result_ready = threading.Event()
        self._thread = None

    def get(self, timeout: float | int | None = None) -> T:
        """
        Return the task's result.

        If the task wasn't already started, it will be started.

        If timeout is specified, then block at most timeout seconds. If the task
        hasn't finished, then raise a TaskTimeout exception.

        If timeout is not specified, then block until the task finishes.
        """
        self.start()

        if not self._result_ready.wait(timeout):
            raise TaskTimeout(timeout or 0)
        elif self._result is None:  # pragma: no cover
            raise RuntimeError("expected result to not be None")
        else:
            return self._result

    def loop(self, period: float | int | None = None) -> Iterable[int]:
        """
        Return an iterator of integers starting at 0, ending when the task
        finishes.

        If period is specified, this will not iterate more than once every
        period seconds.

        This is guaranteed to iterate at least once, even if the task has
        finished before the loop starts.
        """
        index = 0
        period_time = period if period is not None and period > 0 else 0
        start_time = time.time()

        self.start()

        while index == 0 or self.running():
            yield index
            index += 1
            while True:
                wait_time = (period_time * index) + start_time - time.time()
                if wait_time <= 0 or not self.running():
                    break
                time.sleep(min(wait_time, self.MAX_SLEEP))

    def poll(self) -> T | None:
        """Return the task's result or None."""

        if self._thread:
            try:
                return self.get(0)
            except TaskTimeout:
                return None
        else:
            return None

    def run(self) -> T:
        """The task activity. Subclasses should override this method."""

        raise NotImplementedError()  # pragma: no cover

    def running(self) -> bool:
        """Return whether or not the task is running."""

        return bool(self._thread) and self.poll() is None

    def start(self) -> None:
        """Start the task if it hasn't already been started."""

        if not self._thread:

            def target() -> None:
                try:
                    self._result = self.run()
                finally:
                    self._result_ready.set()

            self._thread = threading.Thread(target=target, daemon=True)
            self._thread.start()

    def wait(self, timeout: float | int | None = None) -> None:
        """
        Wait for the task to finish.

        Has the arguments and functionality as get() except it doesn't return
        anything.
        """
        self.get(timeout)


class SubProcessTask(Task[subprocess.CompletedProcess]):
    """
    A concurrent subprocess runner.

    Example:

    >>> task = SubProcessTask("sleep 0.5; echo -n hi")
    >>> for i in task.loop(period=0.2):
    ...     print(i)
    ...
    0
    1
    2
    >>> task.get().stdout
    b'hi'
    """

    def __init__(self, args: Sequence[str] | str | bytes):
        """Create a subprocess Task."""

        super().__init__()
        self.args = args

    def run(self) -> subprocess.CompletedProcess:
        """Run a subprocess of args and return a CompletedProcess."""
        try:
            return subprocess.run(
                self.args,
                capture_output=True,
                shell=isinstance(self.args, (str, bytes)),
            )
        except Exception as e:
            return subprocess.CompletedProcess(
                args=self.args,
                returncode=-255,
                stdout=b"",
                stderr=str(e).encode("utf-8", errors="ignore"),
            )
