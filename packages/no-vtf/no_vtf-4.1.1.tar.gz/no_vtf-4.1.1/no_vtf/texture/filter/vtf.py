# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from collections.abc import Sequence
from typing import Final, Literal, Optional, Union

from no_vtf._typing import mypyc_attr
from no_vtf.texture.filter import TextureFilter
from no_vtf.texture.vtf import VtfTexture


@mypyc_attr(allow_interpreted_subclasses=True)
class VtfMipmapFilter(TextureFilter[VtfTexture]):
    def __init__(
        self,
        *,
        mipmap_levels: slice,
        last: Union[Literal["original"], Literal["filtered"]] = "original",
    ) -> None:
        self.mipmap_levels: Final = mipmap_levels
        self.last: Final = last

    def __call__(self, textures: Sequence[VtfTexture]) -> Sequence[VtfTexture]:
        if not textures:
            return []

        length: int
        if self.last == "original":
            assert (
                len(set(map(lambda texture: texture.num_mipmaps, textures))) == 1
            ), "num_mipmaps must be the same for all filtered textures"
            length = textures[0].num_mipmaps
        else:
            length = max(map(lambda texture: texture.mipmap_index, textures)) + 1

        indices = range(*self.mipmap_levels.indices(length))

        textures_filtered: list[VtfTexture] = []
        for index in indices:
            textures_filtered.extend(
                filter(lambda texture: texture.mipmap_index == index, textures)
            )
        return textures_filtered


@mypyc_attr(allow_interpreted_subclasses=True)
class VtfResolutionFilter(TextureFilter[VtfTexture]):
    def __init__(
        self,
        *,
        min: Optional[int] = None,  # noqa: A002
        max: Optional[int] = None,  # noqa: A002
        closest_as_fallback: bool = False,
    ) -> None:
        if min is not None and max is not None and min > max:
            raise RuntimeError(f"Unordered resolutions: {min = } <= {max = }")

        self.closest_as_fallback: Final = closest_as_fallback

        self._min: Final = min
        self._max: Final = max

    def __call__(self, textures: Sequence[VtfTexture]) -> Sequence[VtfTexture]:
        if self._min is None and self._max is None:
            return textures

        def resolution_filter(texture: VtfTexture) -> bool:
            if self._min is not None:
                if not all(
                    resolution >= self._min
                    for resolution in (texture.image.logical_width, texture.image.logical_height)
                ):
                    return False

            if self._max is not None:
                if not all(
                    resolution <= self._max
                    for resolution in (texture.image.logical_width, texture.image.logical_height)
                ):
                    return False

            return True

        exact_matches = list(filter(resolution_filter, textures))
        if exact_matches or not self.closest_as_fallback:
            return exact_matches

        assert (
            self._min is not None or self._max is not None
        ), "either min or max resolution must be set"
        num_pixels = (self._min or self._max or 0) * (self._max or self._min or 0)

        close_matches = {
            abs(num_pixels - texture.image.logical_width * texture.image.logical_height): texture
            for texture in textures
        }
        close_matches = dict(sorted(close_matches.items()))

        closest_match = list(close_matches.values())[0:1]
        return closest_match


@mypyc_attr(allow_interpreted_subclasses=True)
class VtfFrameFilter(TextureFilter[VtfTexture]):
    def __init__(self, *, frames: slice) -> None:
        self.frames: Final = frames

    def __call__(self, textures: Sequence[VtfTexture]) -> Sequence[VtfTexture]:
        if not textures:
            return []

        assert (
            len(set(map(lambda texture: texture.num_frames, textures))) == 1
        ), "num_frames must be the same for all filtered textures"
        indices = range(*self.frames.indices(textures[0].num_frames))

        textures_filtered: list[VtfTexture] = []
        for index in indices:
            textures_filtered.extend(filter(lambda texture: texture.frame_index == index, textures))
        return textures_filtered


@mypyc_attr(allow_interpreted_subclasses=True)
class VtfFaceFilter(TextureFilter[VtfTexture]):
    def __init__(self, *, faces: slice) -> None:
        self.faces: Final = faces

    def __call__(self, textures: Sequence[VtfTexture]) -> Sequence[VtfTexture]:
        if not textures:
            return []

        assert (
            len(set(map(lambda texture: texture.num_faces, textures))) == 1
        ), "num_faces must be the same for all filtered textures"
        indices = range(*self.faces.indices(textures[0].num_faces))

        textures_filtered: list[VtfTexture] = []
        for index in indices:
            textures_filtered.extend(filter(lambda texture: texture.face_index == index, textures))
        return textures_filtered


@mypyc_attr(allow_interpreted_subclasses=True)
class VtfSliceFilter(TextureFilter[VtfTexture]):
    def __init__(self, *, slices: slice) -> None:
        self.slices: Final = slices

    def __call__(self, textures: Sequence[VtfTexture]) -> Sequence[VtfTexture]:
        if not textures:
            return []

        assert (
            len(set(map(lambda texture: texture.num_slices, textures))) == 1
        ), "num_slices must be the same for all filtered textures"
        indices = range(*self.slices.indices(textures[0].num_slices))

        textures_filtered: list[VtfTexture] = []
        for index in indices:
            textures_filtered.extend(filter(lambda texture: texture.slice_index == index, textures))
        return textures_filtered
