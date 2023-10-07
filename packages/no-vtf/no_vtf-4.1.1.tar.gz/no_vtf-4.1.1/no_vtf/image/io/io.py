# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

import no_vtf.image.io  # noqa: F401  # define every IO for IO.initialize()

from no_vtf._typing import mypyc_attr

_T = TypeVar("_T")


@mypyc_attr(allow_interpreted_subclasses=True)
class IO(Generic[_T]):
    @classmethod
    def initialize(cls, *, _recursive: bool = True) -> None:
        if _recursive:
            for subclass in cls.__subclasses__():
                subclass.initialize()

    def write(self, path: pathlib.Path, data: _T, /) -> None:
        self.write_sequence(path, [data])

    def readback(self, path: pathlib.Path, data: _T, /) -> None:
        self.readback_sequence(path, [data])

    @abstractmethod
    def write_sequence(self, path: pathlib.Path, sequence: Sequence[_T], /) -> None:
        ...

    @abstractmethod
    def readback_sequence(self, path: pathlib.Path, sequence: Sequence[_T], /) -> None:
        ...
