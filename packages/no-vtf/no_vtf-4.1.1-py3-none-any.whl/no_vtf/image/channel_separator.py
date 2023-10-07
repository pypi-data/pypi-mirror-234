# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Iterable
from typing import Optional, TypeVar

import numpy.typing as npt

from no_vtf._typing import mypyc_attr
from no_vtf.deferred import Deferred
from no_vtf.image import Image, ImageDataTypes

_I_contra = TypeVar("_I_contra", bound=ImageDataTypes, contravariant=True)


@mypyc_attr(allow_interpreted_subclasses=True)
class ChannelSeparator:
    def __call__(self, image: Image[_I_contra]) -> Iterable[Image[_I_contra]]:
        data_rgb: Optional[Deferred[npt.NDArray[_I_contra]]] = None
        data_l: Optional[Deferred[npt.NDArray[_I_contra]]] = None
        data_a: Optional[Deferred[npt.NDArray[_I_contra]]] = None

        match (image.channels):
            case "rgb":
                data_rgb = image.data
            case "rgba":
                data_rgb = image.data.map(lambda data: data[..., 0:3])
                data_a = image.data.map(lambda data: data[..., 3:4])
            case "l":
                data_l = image.data
            case "la":
                data_l = image.data.map(lambda data: data[..., 0:1])
                data_a = image.data.map(lambda data: data[..., 1:2])
            case "a":
                data_a = image.data

        if data_rgb is not None:
            yield Image(data=data_rgb, dtype=image.dtype, channels="rgb")

        if data_l is not None:
            yield Image(data=data_l, dtype=image.dtype, channels="l")

        if data_a is not None:
            yield Image(data=data_a, dtype=image.dtype, channels="a")
