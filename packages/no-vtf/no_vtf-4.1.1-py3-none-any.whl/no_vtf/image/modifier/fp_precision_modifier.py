# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Final, Literal, Optional, TypeVar

import numpy as np

from no_vtf._typing import mypyc_attr
from no_vtf.image import Image, ImageDataTypes
from no_vtf.image.modifier import ImageModifier

FloatingPointNumBits = Literal[16, 32, 64]

_I_contra = TypeVar("_I_contra", bound=ImageDataTypes, contravariant=True)


@mypyc_attr(allow_interpreted_subclasses=True)
class FPPrecisionModifier(ImageModifier[_I_contra]):
    def __init__(
        self,
        *,
        min: Optional[FloatingPointNumBits] = None,  # noqa: A002
        max: Optional[FloatingPointNumBits] = None,  # noqa: A002
    ) -> None:
        if min is not None and max is not None and min > max:
            raise RuntimeError(f"Unordered precisions: {min = } <= {max = }")

        self._min: Final = min
        self._max: Final = max

    def __call__(self, image: Image[_I_contra]) -> Image[ImageDataTypes]:
        if not np.issubdtype(image.dtype, np.floating):
            return image

        fp_bits = np.dtype(image.dtype).itemsize * 8

        if self._min is not None and fp_bits < self._min:
            dtype = np.dtype(f"float{self._min}")
            data = image.data.map(lambda data: data.astype(dtype))
            return Image(data=data, dtype=dtype, channels=image.channels)

        if self._max is not None and fp_bits > self._max:
            dtype = np.dtype(f"float{self._max}")
            data = image.data.map(lambda data: data.astype(dtype))
            return Image(data=data, dtype=dtype, channels=image.channels)

        return image
