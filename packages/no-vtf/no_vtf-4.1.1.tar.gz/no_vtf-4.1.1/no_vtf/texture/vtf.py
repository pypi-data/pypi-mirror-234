# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Final, Optional

from no_vtf._typing import mypyc_attr
from no_vtf.image import ImageDynamicRange
from no_vtf.parser.generated.vtf import VtfImage as VtfParserImage


@mypyc_attr(allow_interpreted_subclasses=True)
class VtfTexture:
    def __init__(
        self,
        *,
        dynamic_range: Optional[ImageDynamicRange],
        is_cubemap: bool,
        num_mipmaps: int,
        num_frames: int,
        num_faces: int,
        num_slices: int,
        mipmap_index: int,
        frame_index: int,
        face_index: int,
        slice_index: int,
        image: VtfParserImage,
    ) -> None:
        self.dynamic_range: Final = dynamic_range

        self.is_cubemap: Final = is_cubemap

        self.num_mipmaps: Final = num_mipmaps
        self.num_frames: Final = num_frames
        self.num_faces: Final = num_faces
        self.num_slices: Final = num_slices

        self.mipmap_index: Final = mipmap_index
        self.frame_index: Final = frame_index
        self.face_index: Final = face_index
        self.slice_index: Final = slice_index

        self.image: Final = image
