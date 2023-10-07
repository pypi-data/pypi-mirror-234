# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Generic, TypeVar

from no_vtf._typing import mypyc_attr

_T_contra = TypeVar("_T_contra", contravariant=True)


@mypyc_attr(allow_interpreted_subclasses=True)
class TextureNamer(Generic[_T_contra]):
    @abstractmethod
    def __call__(self, input_name: str, texture: _T_contra) -> str:
        ...
