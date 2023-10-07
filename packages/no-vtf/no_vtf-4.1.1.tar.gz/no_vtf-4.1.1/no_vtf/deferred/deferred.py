# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

from collections.abc import Callable
from typing import Final, Generic, Optional, Protocol, TypeVar, cast

from no_vtf._typing import mypyc_attr

_A = TypeVar("_A")
_A_contra = TypeVar("_A_contra", contravariant=True)
_B = TypeVar("_B")
_B_co = TypeVar("_B_co", covariant=True)


class _F(Protocol[_A_contra, _B_co]):
    def __call__(self, a: _A_contra, /) -> _B_co:
        ...


@mypyc_attr(allow_interpreted_subclasses=True)
class Deferred(Generic[_A]):
    @staticmethod
    def pure(a: _A, /) -> Deferred[_A]:
        return Deferred(lambda: a)

    @staticmethod
    def apply(f: Deferred[_F[_A_contra, _B_co]], a: Deferred[_A_contra], /) -> Deferred[_B_co]:
        return Deferred(lambda: f()(a()))

    @staticmethod
    def join(a: Deferred[Deferred[_A]], /) -> Deferred[_A]:
        return Deferred(lambda: a()())

    def __init__(self, thunk: Callable[[], _A], /) -> None:
        self._thunk: Final = thunk
        self._result: Optional[_A] = None
        self._result_valid = False

    def __call__(self) -> _A:
        if self._result_valid:
            return cast(_A, self._result)

        self._result = self._thunk()
        self._result_valid = True
        return self._result

    def map(self, f: Callable[[_A], _B], /) -> Deferred[_B]:
        return Deferred(lambda: f(self()))

    def bind(self, f: Callable[[_A], Deferred[_B]], /) -> Deferred[_B]:
        return Deferred(lambda: f(self())())
