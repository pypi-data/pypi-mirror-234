# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from abc import abstractmethod
from typing import Generic, TypeVar

from no_vtf._typing import mypyc_attr
from no_vtf.image import Image, ImageDataTypes

_I_contra = TypeVar("_I_contra", bound=ImageDataTypes, contravariant=True)


@mypyc_attr(allow_interpreted_subclasses=True)
class ImageModifier(Generic[_I_contra]):
    @abstractmethod
    def __call__(self, image: Image[_I_contra], /) -> Image[ImageDataTypes]:
        ...
