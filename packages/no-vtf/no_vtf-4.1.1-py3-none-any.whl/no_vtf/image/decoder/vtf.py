# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Optional

import numpy as np
import numpy.typing as npt

from no_vtf.deferred import Deferred
from no_vtf.image import ImageWithRawData
from no_vtf.image.decoder.generic import (
    decode_bgr_uint8,
    decode_bgra_uint8,
    decode_rgb_uint8,
    decode_rgba_uint16_le,
)


def decode_rgb_uint8_bluescreen(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8]:
    image = decode_rgb_uint8(encoded_image, width, height)
    image = _decode_bluescreen(image)
    return image


def decode_bgr_uint8_bluescreen(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8]:
    image = decode_bgr_uint8(encoded_image, width, height)
    image = _decode_bluescreen(image)
    return image


def _decode_bluescreen(image: ImageWithRawData[np.uint8]) -> ImageWithRawData[np.uint8]:
    assert image.channels == "rgb", "_decode_bluescreen() must be called with rgb image channels"
    data = image.data.map(_decode_bluescreen_data)
    return ImageWithRawData(raw=image.raw, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def _decode_bluescreen_data(rgb_uint8: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    is_opaque: npt.NDArray[np.bool_] = rgb_uint8 != (0, 0, 255)
    is_opaque = is_opaque.any(axis=2)
    is_opaque = is_opaque[..., np.newaxis]

    rgb_uint8 *= is_opaque
    a_uint8: npt.NDArray[np.uint8] = np.multiply(is_opaque, 255, dtype=np.uint8)

    rgba_uint8: npt.NDArray[np.uint8] = np.dstack((rgb_uint8, a_uint8))
    return rgba_uint8


def decode_bgra_uint8_hdr(
    encoded_image: bytes, width: int, height: int, overbright_factor: Optional[float]
) -> ImageWithRawData[np.float32]:
    def thunk() -> npt.NDArray[np.float32]:
        nonlocal overbright_factor
        if overbright_factor is None:
            overbright_factor = 16

        rgba_uint8 = decode_bgra_uint8(encoded_image, width, height).data()

        rgba_float32: npt.NDArray[np.float32] = rgba_uint8.astype(np.float32) / 255.0
        rgba_float32[:, :, [0, 1, 2]] *= rgba_float32[:, :, [3]] * overbright_factor

        rgb_float32: npt.NDArray[np.float32] = rgba_float32[..., :3]
        return rgb_float32

    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.float32), channels="rgb"
    )


def decode_rgba_uint16_le_hdr(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.float32]:
    def thunk() -> npt.NDArray[np.float32]:
        rgba_uint16 = decode_rgba_uint16_le(encoded_image, width, height).data()
        # convert 4.12 fixed point stored as integer into floating point
        rgba_float32: npt.NDArray[np.float32] = rgba_uint16.astype(np.float32) / (1 << 12)
        return rgba_float32

    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.float32), channels="rgba"
    )
