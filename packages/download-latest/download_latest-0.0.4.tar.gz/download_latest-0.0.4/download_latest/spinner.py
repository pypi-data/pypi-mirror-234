from __future__ import annotations

import math


class Spinner:
    r"""
    A simple spinner.

    >>> spinner = Spinner(chars="/-\\|", width=15)
    >>> for i, s in enumerate(spinner):
    ...    if i >= 6:
    ...        break
    ...    else:
    ...        print(s)
    ...
    /-\|/-\|/-\|/-\
    -\|/-\|/-\|/-\|
    \|/-\|/-\|/-\|/
    |/-\|/-\|/-\|/-
    /-\|/-\|/-\|/-\
    -\|/-\|/-\|/-\|
    """

    def __init__(
        self,
        chars: str = "/-\\|",
        width: int = 4,
        index: int = 0,
    ) -> None:
        """Create the spinner."""
        self.chars = chars
        self.width = width
        self.index = index % len(chars)

    def __iter__(self) -> Spinner:
        """Return the iterator (self)."""
        return self

    def __next__(self) -> str:
        """Return the next iteration of the spinner."""
        index, width = self.index, self.width
        chars = self.chars * (math.ceil((2 * width) / len(self.chars)))
        result = chars[index : index + width]
        self.index = (index + 1) % len(self.chars)
        return result
