# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools

import numpy as np
import numpy.typing as npt
import PIL.BlpImagePlugin
import PIL.Image

from no_vtf.deferred import Deferred
from no_vtf.image import ImageWithRawData
from no_vtf.image.ndarray import image_bytes_to_ndarray


def decode_rgb_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgb")


def decode_rgba_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def decode_argb_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (1, 2, 3, 0), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def decode_bgr_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (2, 1, 0), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgb")


def decode_bgra_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (2, 1, 0, 3), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def decode_abgr_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (3, 2, 1, 0), np.uint8)
    )
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="rgba")


def decode_rgba_uint16_be(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint16]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.uint16, ">")
    )
    return ImageWithRawData(
        raw=encoded_image, data=data, dtype=np.dtype(np.uint16), channels="rgba"
    )


def decode_rgba_uint16_le(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint16]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.uint16, "<")
    )
    return ImageWithRawData(
        raw=encoded_image, data=data, dtype=np.dtype(np.uint16), channels="rgba"
    )


def decode_rgba_float16_be(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.float16]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.float16, ">")
    )
    return ImageWithRawData(
        raw=encoded_image, data=data, dtype=np.dtype(np.float16), channels="rgba"
    )


def decode_rgba_float16_le(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.float16]:
    data = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1, 2, 3), np.float16, "<")
    )
    return ImageWithRawData(
        raw=encoded_image, data=data, dtype=np.dtype(np.float16), channels="rgba"
    )


def decode_l_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    data = Deferred(lambda: image_bytes_to_ndarray(encoded_image, width, height, (0,), np.uint8))
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="l")


def decode_a_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    data = Deferred(lambda: image_bytes_to_ndarray(encoded_image, width, height, (0,), np.uint8))
    return ImageWithRawData(raw=encoded_image, data=data, dtype=np.dtype(np.uint8), channels="a")


def decode_la_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    la_uint8 = Deferred(
        lambda: image_bytes_to_ndarray(encoded_image, width, height, (0, 1), np.uint8)
    )
    return ImageWithRawData(
        raw=encoded_image, data=la_uint8, dtype=np.dtype(np.uint8), channels="la"
    )


def decode_uv_uint8(encoded_image: bytes, width: int, height: int) -> ImageWithRawData[np.uint8]:
    def thunk() -> npt.NDArray[np.uint8]:
        rg_uint8 = image_bytes_to_ndarray(encoded_image, width, height, (0, 1), np.uint8)
        b_uint8: npt.NDArray[np.uint8] = np.zeros(rg_uint8.shape[:-1], dtype=np.uint8)
        rgb_uint8: npt.NDArray[np.uint8] = np.dstack((rg_uint8, b_uint8))
        return rgb_uint8

    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgb"
    )


def decode_bgra_uint4_le(
    encoded_image: bytes, width: int, height: int
) -> ImageWithRawData[np.uint8]:
    def thunk() -> npt.NDArray[np.uint8]:
        bgra_uint4 = image_bytes_to_ndarray(encoded_image, width, height, (0, 1), np.uint8)

        br_uint8 = np.bitwise_and(np.left_shift(bgra_uint4, 4), 0xF0)
        ga_uint8 = np.bitwise_and(bgra_uint4, 0xF0)

        r_uint8 = br_uint8[..., [1]]
        g_uint8 = ga_uint8[..., [0]]
        b_uint8 = br_uint8[..., [0]]
        a_uint8 = ga_uint8[..., [1]]

        rgba_uint8: npt.NDArray[np.uint8] = np.dstack((r_uint8, g_uint8, b_uint8, a_uint8))
        return rgba_uint8

    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgba"
    )


def decode_dxt1_rgb(
    encoded_image: bytes, logical_width: int, logical_height: int
) -> ImageWithRawData[np.uint8]:
    def thunk() -> npt.NDArray[np.uint8]:
        rgba_uint8 = _decode_dxt_generic(encoded_image, logical_width, logical_height, 1, "DXT1")
        rgb_uint8: npt.NDArray[np.uint8] = rgba_uint8[..., :3]
        return rgb_uint8

    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgb"
    )


def decode_dxt1_rgba(
    encoded_image: bytes, logical_width: int, logical_height: int
) -> ImageWithRawData[np.uint8]:
    thunk = functools.partial(
        _decode_dxt_generic, encoded_image, logical_width, logical_height, 1, "DXT1"
    )
    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgba"
    )


def decode_dxt3(
    encoded_image: bytes, logical_width: int, logical_height: int
) -> ImageWithRawData[np.uint8]:
    thunk = functools.partial(
        _decode_dxt_generic, encoded_image, logical_width, logical_height, 2, "DXT3"
    )
    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgba"
    )


def decode_dxt5(
    encoded_image: bytes, logical_width: int, logical_height: int
) -> ImageWithRawData[np.uint8]:
    thunk = functools.partial(
        _decode_dxt_generic, encoded_image, logical_width, logical_height, 3, "DXT5"
    )
    return ImageWithRawData(
        raw=encoded_image, data=Deferred(thunk), dtype=np.dtype(np.uint8), channels="rgba"
    )


def _decode_dxt_generic(
    encoded_image: bytes, logical_width: int, logical_height: int, n: int, pixel_format: str
) -> npt.NDArray[np.uint8]:
    physical_width, physical_height = _dxt_physical_dimensions(logical_width, logical_height)

    # reference for "n" and "pixel_format": Pillow/src/PIL/DdsImagePlugin.py
    pil_image = PIL.Image.frombytes(
        "RGBA", (physical_width, physical_height), encoded_image, "bcn", n, pixel_format
    )

    rgba_uint8: npt.NDArray[np.uint8] = np.array(pil_image)
    rgba_uint8 = rgba_uint8[:logical_height, :logical_width, :]
    return rgba_uint8


def _dxt_physical_dimensions(logical_width: int, logical_height: int) -> tuple[int, int]:
    physical_width = _dxt_physical_length(logical_width)
    physical_height = _dxt_physical_length(logical_height)
    return physical_width, physical_height


def _dxt_physical_length(logical_length: int) -> int:
    physical_length = (max(logical_length, 4) + 3) // 4 * 4
    return physical_length
