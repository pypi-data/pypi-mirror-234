# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

import typing

from typing import Final, Generic, Literal, TypeAlias, TypeGuard, TypeVar, Union

import numpy as np
import numpy.typing as npt

from no_vtf._typing import mypyc_attr
from no_vtf.deferred import Deferred

ImageDataTypesLDR: TypeAlias = np.uint8 | np.uint16
ImageDataTypesHDR: TypeAlias = np.float16 | np.float32

ImageDataTypes: TypeAlias = Union[ImageDataTypesLDR, ImageDataTypesHDR]

ImageData: TypeAlias = npt.NDArray[ImageDataTypes]

ImageChannels = Literal["rgb", "rgba", "l", "la", "a"]
ImageDynamicRange = Literal["ldr", "hdr"]

_I_co = TypeVar("_I_co", bound=ImageDataTypes, covariant=True)


@mypyc_attr(allow_interpreted_subclasses=True)
class Image(Generic[_I_co]):
    def __init__(
        self,
        *,
        data: Deferred[npt.NDArray[_I_co]],
        dtype: np.dtype[_I_co],
        channels: ImageChannels,
    ):
        self.data: Final = data
        self.dtype: Final = dtype
        self.channels: Final[ImageChannels] = channels

    @property
    def dynamic_range(self) -> ImageDynamicRange:
        ldr = _is_ldr(self.dtype)
        hdr = _is_hdr(self.dtype)
        assert ldr != hdr, "_is_ldr() and _is_hdr() must be mutually exclusive"

        return "hdr" if hdr else "ldr"

    @staticmethod
    def is_ldr(image: Image[_I_co]) -> TypeGuard[Image[ImageDataTypesLDR]]:
        return image.dynamic_range == "ldr"

    @staticmethod
    def is_hdr(image: Image[_I_co]) -> TypeGuard[Image[ImageDataTypesHDR]]:
        return image.dynamic_range == "hdr"


@mypyc_attr(allow_interpreted_subclasses=True)
class ImageWithRawData(Image[_I_co]):
    def __init__(
        self,
        *,
        raw: bytes,
        data: Deferred[npt.NDArray[_I_co]],
        dtype: np.dtype[_I_co],
        channels: ImageChannels,
    ):
        super().__init__(data=data, dtype=dtype, channels=channels)

        self.raw: Final = raw


def _is_ldr(dtype: npt.DTypeLike) -> bool:
    ldr_dtypes = typing.get_args(ImageDataTypesLDR)
    return any(np.issubdtype(dtype, ldr_dtype) for ldr_dtype in ldr_dtypes)


def _is_hdr(dtype: npt.DTypeLike) -> bool:
    hdr_dtypes = typing.get_args(ImageDataTypesHDR)
    return any(np.issubdtype(dtype, hdr_dtype) for hdr_dtype in hdr_dtypes)
