# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from abc import abstractmethod
from collections.abc import Sequence
from typing import BinaryIO, Generic, TypeVar, Union

from no_vtf._typing import mypyc_attr

_T_co = TypeVar("_T_co", covariant=True)


@mypyc_attr(allow_interpreted_subclasses=True)
class TextureExtractor(Generic[_T_co]):
    @abstractmethod
    def __call__(self, path_or_io: Union[pathlib.Path, BinaryIO], /) -> Sequence[_T_co]:
        ...
