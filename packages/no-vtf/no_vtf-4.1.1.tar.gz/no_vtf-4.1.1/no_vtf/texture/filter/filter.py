# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from collections.abc import Sequence
from typing import Final, Generic, TypeVar

from no_vtf._typing import mypyc_attr

_T = TypeVar("_T")


@mypyc_attr(allow_interpreted_subclasses=True)
class TextureFilter(Generic[_T]):
    @abstractmethod
    def __call__(self, textures: Sequence[_T]) -> Sequence[_T]:
        ...


@mypyc_attr(allow_interpreted_subclasses=True)
class TextureCombinedFilter(TextureFilter[_T]):
    def __init__(self, filters: Sequence[TextureFilter[_T]]) -> None:
        self.filters: Final = filters

    def __call__(self, textures: Sequence[_T]) -> Sequence[_T]:
        for texture_filter in self.filters:
            textures = texture_filter(textures)

        return textures
