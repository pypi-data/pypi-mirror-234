# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools

from typing import Final, Optional

from no_vtf._typing import mypyc_attr
from no_vtf.image import ImageDataTypes, ImageDynamicRange, ImageWithRawData
from no_vtf.image.decoder import ImageDecoder
from no_vtf.image.decoder.generic import (
    decode_a_uint8,
    decode_abgr_uint8,
    decode_argb_uint8,
    decode_bgr_uint8,
    decode_bgra_uint4_le,
    decode_bgra_uint8,
    decode_dxt1_rgb,
    decode_dxt1_rgba,
    decode_dxt3,
    decode_dxt5,
    decode_l_uint8,
    decode_la_uint8,
    decode_rgb_uint8,
    decode_rgba_float16_le,
    decode_rgba_uint8,
    decode_uv_uint8,
)
from no_vtf.image.decoder.vtf import (
    decode_bgr_uint8_bluescreen,
    decode_bgra_uint8_hdr,
    decode_rgb_uint8_bluescreen,
    decode_rgba_uint16_le_hdr,
)
from no_vtf.parser.generated.vtf import VtfImageFormat as VtfParserImageFormat
from no_vtf.texture.decoder import TextureDecoder
from no_vtf.texture.vtf import VtfTexture


@mypyc_attr(allow_interpreted_subclasses=True)
class VtfDecoder(TextureDecoder[VtfTexture, ImageDataTypes]):
    def __init__(
        self,
        *,
        dynamic_range: Optional[ImageDynamicRange] = None,
        overbright_factor: Optional[float] = None,
    ) -> None:
        self.dynamic_range: Final = dynamic_range
        self.overbright_factor: Final = overbright_factor

    def __call__(self, texture: VtfTexture) -> ImageWithRawData[ImageDataTypes]:
        encoded_image = texture.image.image_data
        logical_width = texture.image.logical_width
        logical_height = texture.image.logical_height

        decoder = self._get_decoder(texture)
        decoded_image = decoder(encoded_image, logical_width, logical_height)
        return decoded_image

    def _get_decoder(self, texture: VtfTexture) -> ImageDecoder[ImageDataTypes]:
        image_format = texture.image.image_format

        dynamic_range = (
            self.dynamic_range if self.dynamic_range is not None else texture.dynamic_range
        )

        decoder: Optional[ImageDecoder[ImageDataTypes]] = None
        match (image_format, dynamic_range):
            case VtfParserImageFormat.rgba8888, _:
                decoder = decode_rgba_uint8
            case VtfParserImageFormat.abgr8888, _:
                decoder = decode_abgr_uint8
            case VtfParserImageFormat.rgb888, _:
                decoder = decode_rgb_uint8
            case VtfParserImageFormat.bgr888, _:
                decoder = decode_bgr_uint8
            case VtfParserImageFormat.i8, _:
                decoder = decode_l_uint8
            case VtfParserImageFormat.ia88, _:
                decoder = decode_la_uint8
            case VtfParserImageFormat.a8, _:
                decoder = decode_a_uint8
            case VtfParserImageFormat.rgb888_bluescreen, _:
                decoder = decode_rgb_uint8_bluescreen
            case VtfParserImageFormat.bgr888_bluescreen, _:
                decoder = decode_bgr_uint8_bluescreen
            case VtfParserImageFormat.argb8888, _:
                # VTFLib/VTFEdit, Gimp VTF Plugin, and possibly others, decode this format
                # differently because of mismatched channels (verified against VTF2TGA).
                decoder = decode_argb_uint8
            case VtfParserImageFormat.bgra8888, None:
                raise RuntimeError("Dynamic range is set neither on VtfTexture nor VtfDecoder")
            case VtfParserImageFormat.bgra8888, "ldr":
                decoder = decode_bgra_uint8
            case VtfParserImageFormat.bgra8888, "hdr":
                decoder = functools.partial(
                    decode_bgra_uint8_hdr, overbright_factor=self.overbright_factor
                )
            case VtfParserImageFormat.dxt1, _:
                decoder = decode_dxt1_rgb
            case VtfParserImageFormat.dxt3, _:
                decoder = decode_dxt3
            case VtfParserImageFormat.dxt5, _:
                decoder = decode_dxt5
            case VtfParserImageFormat.bgra4444, _:
                decoder = decode_bgra_uint4_le
            case VtfParserImageFormat.dxt1_onebitalpha, _:
                decoder = decode_dxt1_rgba
            case VtfParserImageFormat.uv88, _:
                decoder = decode_uv_uint8
            case VtfParserImageFormat.rgba16161616f, _:
                decoder = decode_rgba_float16_le
            case VtfParserImageFormat.rgba16161616, _:
                decoder = decode_rgba_uint16_le_hdr

        if not decoder:
            raise RuntimeError(f"Unsupported Valve texture format: {image_format.name}")

        return decoder
