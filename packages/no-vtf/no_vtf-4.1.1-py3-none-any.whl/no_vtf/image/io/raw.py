# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from collections.abc import Sequence

from no_vtf._typing import mypyc_attr
from no_vtf.image import ImageDataTypes, ImageWithRawData
from no_vtf.image.io.io import IO


@mypyc_attr(allow_interpreted_subclasses=True)
class RawIO(IO[ImageWithRawData[ImageDataTypes]]):
    def write_sequence(
        self, path: pathlib.Path, sequence: Sequence[ImageWithRawData[ImageDataTypes]]
    ) -> None:
        with open(path, "wb") as file:
            for image in sequence:
                data = image.raw
                file.write(data)

    def readback_sequence(
        self, path: pathlib.Path, sequence: Sequence[ImageWithRawData[ImageDataTypes]]
    ) -> None:
        with open(path, "rb") as file:
            for image in sequence:
                data = image.raw

                read_data = file.read(len(data))
                if data != read_data:
                    raise RuntimeError(f"{path!r}: Data differs from what is in the file")

            if file.read():
                raise RuntimeError(f"{path!r}: Data differs from what is in the file")
