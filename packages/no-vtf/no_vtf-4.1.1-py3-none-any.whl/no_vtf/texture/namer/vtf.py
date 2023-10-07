# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Final

from no_vtf._typing import mypyc_attr
from no_vtf.texture.namer import TextureNamer
from no_vtf.texture.vtf import VtfTexture


@mypyc_attr(allow_interpreted_subclasses=True)
class Vtf2TgaLikeNamer(TextureNamer[VtfTexture]):
    def __init__(self, *, include_mipmap_level: bool, include_frame: bool = True) -> None:
        self.include_mipmap_level: Final = include_mipmap_level
        self.include_frame: Final = include_frame

    def __call__(self, input_name: str, texture: VtfTexture) -> str:
        output_name = input_name

        if texture.is_cubemap:
            face_names = ("rt", "lf", "bk", "ft", "up", "dn", "sph")
            output_name += face_names[texture.face_index]

        if self.include_frame and texture.num_frames > 1:
            output_name += f"{texture.frame_index:03d}"

        if self.include_mipmap_level and texture.num_mipmaps > 1:
            mipmap_level = texture.num_mipmaps - texture.mipmap_index - 1
            output_name += f"_mip{mipmap_level}"

        if texture.num_slices > 1:
            output_name += f"_z{texture.slice_index:03d}"

        return output_name
