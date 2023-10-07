# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import functools
import itertools
import pathlib
import re

from collections.abc import Sequence
from typing import ClassVar, Final, Literal, Optional, Protocol, cast

import imageio.core.v3_plugin_api
import imageio.plugins.freeimage
import imageio.typing
import imageio.v3
import numpy as np
import numpy.typing as npt

from no_vtf._typing import mypyc_attr
from no_vtf.image import Image, ImageData, ImageDataTypes
from no_vtf.image.io.io import IO
from no_vtf.image.modifier import ImageModifier
from no_vtf.image.modifier.fp_precision_modifier import FPPrecisionModifier

_IMAGE_IO_FORMAT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"[a-z0-9]+", re.ASCII | re.IGNORECASE
)


@mypyc_attr(allow_interpreted_subclasses=True)
class ImageIO(IO[Image[ImageDataTypes]]):
    @classmethod
    def initialize(
        cls, formats: Optional[Sequence[str]] = None, *, _recursive: bool = True
    ) -> None:
        super().initialize(_recursive=False)

        if not formats:
            _ImageIOBackend.initialize()
        else:
            for backend_format in map(str.lower, formats):
                match backend_format:
                    case "apng":
                        _ImageIOApngBackend.initialize()
                    case "exr":
                        _ImageIOExrBackend.initialize()
                    case "png":
                        _ImageIOPngBackend.initialize()
                    case "targa" | "tga":
                        _ImageIOTgaBackend.initialize()
                    case "tiff":
                        _ImageIOTiffBackend.initialize()
                    case _:
                        pass

        if _recursive:
            for subclass in cls.__subclasses__():
                subclass.initialize(formats)

    def __init__(
        self,
        *,
        format: str,  # noqa: A002
        compress: Optional[bool] = None,
        fps: Optional[int] = None,
    ) -> None:
        if not _IMAGE_IO_FORMAT_PATTERN.fullmatch(format):
            raise RuntimeError(f"Invalid format: {format}")

        self._format: Final = format

        if compress is None:
            compress = True

        backend: _ImageIOBackend
        match format.lower():
            case "apng":
                backend = _ImageIOApngBackend(compress=compress, fps=fps)
            case "exr":
                backend = _ImageIOExrBackend(compress=compress)
            case "png":
                backend = _ImageIOPngBackend(compress=compress)
            case "targa" | "tga":
                backend = _ImageIOTgaBackend(compress=compress)
            case "tiff":
                backend = _ImageIOTiffBackend(compress=compress)
            case _:
                extension = f".{format}"
                backend = _ImageIOBackend(extension=extension)
        self._backend: Final = backend

    def write_sequence(self, path: pathlib.Path, sequence: Sequence[Image[ImageDataTypes]]) -> None:
        self._backend.write(path, sequence)

    def readback_sequence(
        self, path: pathlib.Path, sequence: Sequence[Image[ImageDataTypes]]
    ) -> None:
        self._backend.readback(path, sequence)

    @property
    def format(self) -> str:
        return self._format


@mypyc_attr(allow_interpreted_subclasses=True)
class _DummyImageIO(ImageIO):
    pass


class _Opener(Protocol):
    def __call__(
        self,
        uri: imageio.typing.ImageResource,
        io_mode: Literal["r", "w"],
        *,
        extension: Optional[str] = None,
        format_hint: Optional[str] = None,
    ) -> imageio.core.v3_plugin_api.PluginV3:
        ...


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOBackend:
    @classmethod
    def initialize(cls, *, _recursive: bool = True) -> None:
        if _recursive:
            for subclass in cls.__subclasses__():
                subclass.initialize()

    def __init__(self, *, extension: Optional[str] = None) -> None:
        self._extension: Final = extension

    def write(self, path: pathlib.Path, sequence: Sequence[Image[ImageDataTypes]]) -> None:
        opener = self._get_opener()
        with opener(path, "w", extension=self._extension) as image_resource:
            for image in sequence:
                kwargs = self._get_writer_kwargs(image)
                image = self._postprocess(image)
                data = self._get_data(image)

                image_resource.write(data, **kwargs)

    def readback(self, path: pathlib.Path, sequence: Sequence[Image[ImageDataTypes]]) -> None:
        opener = self._get_opener()
        with opener(path, "r", extension=self._extension) as image_resource:
            for image, read_data in itertools.zip_longest(sequence, image_resource.iter()):
                if image is None or read_data is None:
                    raise RuntimeError(
                        f"{path!r}: Number of frames differs from what is in the file"
                    )

                image = self._postprocess(image)
                data = self._get_data(image)

                if data.dtype != read_data.dtype:
                    raise RuntimeError(f"{path!r}: Data type differs from what is in the file")

                if not self._compare_data(data, read_data):
                    raise RuntimeError(f"{path!r}: Data differs from what is in the file")

    def _get_opener(self) -> _Opener:
        return cast(_Opener, imageio.v3.imopen)

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        return {}

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return image

    def _get_data(self, image: Image[ImageDataTypes]) -> ImageData:
        data = image.data()

        # write luminance into three channels when alpha is present
        if image.channels == "la":
            l_uint8: npt.NDArray[ImageDataTypes] = data[:, :, [0]]
            a_uint8: npt.NDArray[ImageDataTypes] = data[:, :, [1]]
            data = np.dstack((l_uint8, l_uint8, l_uint8, a_uint8))

        # remove last axis if its length is 1
        if data.shape[-1] == 1:
            data = data[..., 0]

        return data

    def _compare_data(self, data: ImageData, read_data: ImageData) -> bool:
        return np.array_equal(data, read_data)


_FP_FORCE_32_BITS: Final[ImageModifier[ImageDataTypes]] = FPPrecisionModifier(min=32, max=32)


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOPillowBackend(_ImageIOBackend):
    def __init__(self, *, extension: Optional[str] = None) -> None:
        super().__init__(extension=extension)

    def _get_opener(self) -> _Opener:
        return functools.partial(
            imageio.v3.imopen, plugin="pillow"
        )  # pyright: ignore [reportGeneralTypeIssues] # imopen is incorrectly typed


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOPngBackend(_ImageIOPillowBackend):
    def __init__(self, *, compress: bool = True, extension: str = ".png") -> None:
        super().__init__(extension=extension)
        self.compress: Final = compress

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        kwargs = super()._get_writer_kwargs(image)
        if not self.compress:
            kwargs["compress_level"] = 0
        return kwargs


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOApngBackend(_ImageIOPngBackend):
    def __init__(self, *, compress: bool = True, fps: Optional[int] = None) -> None:
        super().__init__(compress=compress, extension=".apng")
        self.fps: Final = fps

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        kwargs = super()._get_writer_kwargs(image)
        if self.fps:
            kwargs["duration"] = 1000 / self.fps
        return kwargs


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOLegacyBackend(_ImageIOBackend):
    def __init__(
        self, *, imageio_format: Optional[str] = None, extension: Optional[str] = None
    ) -> None:
        super().__init__(extension=extension)
        self._imageio_format: Final = imageio_format

    def _get_opener(self) -> _Opener:
        return functools.partial(
            imageio.v3.imopen, legacy_mode=True, plugin=self._imageio_format
        )  # pyright: ignore [reportGeneralTypeIssues] # imopen is incorrectly typed


# IO_FLAGS is an implicit reexport
_FREEIMAGE_IO_FLAGS: Final[
    type[imageio.plugins.freeimage.IO_FLAGS]  # pyright: ignore [reportPrivateImportUsage]
] = imageio.plugins.freeimage.IO_FLAGS  # pyright: ignore [reportPrivateImportUsage]


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOFreeImageBackend(_ImageIOLegacyBackend):
    _freeimage_initialized: ClassVar[bool] = False

    @classmethod
    def initialize(cls, *, _recursive: bool = True) -> None:
        super().initialize(_recursive=False)

        if not _ImageIOFreeImageBackend._freeimage_initialized:
            # download() seems to be untyped because of implicit reexport
            imageio.plugins.freeimage.download()  # type: ignore[no-untyped-call]
            _ImageIOFreeImageBackend._freeimage_initialized = True

        if _recursive:
            for subclass in cls.__subclasses__():
                subclass.initialize()

    def __init__(self, *, imageio_format: str, extension: str) -> None:
        super().__init__(imageio_format=imageio_format, extension=extension)

        if not _ImageIOFreeImageBackend._freeimage_initialized:
            raise RuntimeError("ImageIO FreeImage backend was not initialized")

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        kwargs = super()._get_writer_kwargs(image)
        kwargs["flags"] = self._get_flags(image)
        return kwargs

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        return 0


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOExrBackend(_ImageIOFreeImageBackend):
    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="EXR-FI", extension=".exr")
        self.compress: Final = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = super()._get_flags(image)
        flags |= _FREEIMAGE_IO_FLAGS.EXR_ZIP if self.compress else _FREEIMAGE_IO_FLAGS.EXR_NONE
        if not np.issubdtype(image.data().dtype, np.float16):
            flags |= _FREEIMAGE_IO_FLAGS.EXR_FLOAT
        return flags

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return _FP_FORCE_32_BITS(image)


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOTgaBackend(_ImageIOFreeImageBackend):
    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="TARGA-FI", extension=".tga")
        self.compress: Final = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = super()._get_flags(image)
        flags |= (
            _FREEIMAGE_IO_FLAGS.TARGA_SAVE_RLE
            if self.compress
            else _FREEIMAGE_IO_FLAGS.TARGA_DEFAULT
        )
        return flags


@mypyc_attr(allow_interpreted_subclasses=True)
class _ImageIOTiffBackend(_ImageIOFreeImageBackend):
    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="TIFF-FI", extension=".tiff")
        self.compress: Final = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = super()._get_flags(image)
        flags |= (
            _FREEIMAGE_IO_FLAGS.TIFF_DEFAULT if self.compress else _FREEIMAGE_IO_FLAGS.TIFF_NONE
        )
        return flags

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return _FP_FORCE_32_BITS(image)
