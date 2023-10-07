# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Callable
from typing import TypeAlias, TypeVar

from no_vtf.image import ImageDataTypes, ImageWithRawData

_I_co = TypeVar("_I_co", bound=ImageDataTypes, covariant=True)

ImageDecoder: TypeAlias = Callable[[bytes, int, int], ImageWithRawData[_I_co]]
