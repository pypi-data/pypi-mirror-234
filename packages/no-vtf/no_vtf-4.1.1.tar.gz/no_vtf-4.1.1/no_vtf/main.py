# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import contextlib
import functools
import inspect
import itertools
import os
import pathlib
import re
import sys
import traceback

from collections.abc import Callable, Iterator, Sequence
from contextlib import AbstractContextManager
from typing import Final, Generic, Optional, Protocol, TextIO, TypeVar, Union, cast

import alive_progress
import alive_progress.animations.bars
import alive_progress.animations.spinner_compiler
import alive_progress.animations.spinners
import alive_progress.animations.utils
import alive_progress.styles.internal
import alive_progress.utils.cells
import click
import click_option_group

from typing_extensions import ParamSpec

import no_vtf

from no_vtf.filesystem import InputPaths, OutputDirectories
from no_vtf.image import ImageDynamicRange
from no_vtf.pipeline import Pipeline, Receipt
from no_vtf.task_runner import ParallelRunner, SequentialRunner, TaskRunner
from no_vtf.texture.decoder.vtf import VtfDecoder
from no_vtf.texture.extractor.vtf import VtfExtractor
from no_vtf.texture.filter import TextureCombinedFilter, TextureFilter
from no_vtf.texture.filter.vtf import (
    VtfFaceFilter,
    VtfFrameFilter,
    VtfMipmapFilter,
    VtfResolutionFilter,
    VtfSliceFilter,
)
from no_vtf.texture.namer.vtf import Vtf2TgaLikeNamer
from no_vtf.texture.vtf import VtfTexture

_P = ParamSpec("_P")
_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)


class _HelpFormatter(click.HelpFormatter):
    def write_usage(self, prog: str, args: str = "", prefix: Optional[str] = None) -> None:
        prog = click.style(prog, fg=127, bold=True)
        args = click.style(args, bold=True)
        super().write_usage(prog, args, prefix)

    def write_heading(self, heading: str) -> None:
        heading = click.style(heading, underline=True)
        super().write_heading(heading)


class _OptionGroup(click_option_group.OptionGroup):
    def get_help_record(self, ctx: click.Context) -> Optional[tuple[str, str]]:
        help_record = super().get_help_record(ctx)
        if not help_record:
            return None

        name, help_ = help_record
        name = click.style(name, fg=172, bold=True)
        return name, help_


class _GroupedOption(click_option_group.GroupedOption):
    _dim_pattern: Final[re.Pattern[str]] = re.compile(r"(?<=\s)\[[^\[\]\s]+\]", re.ASCII)

    def get_help_record(self, ctx: click.Context) -> Optional[tuple[str, str]]:
        help_record = super().get_help_record(ctx)
        if help_record is None:
            return None

        def dim_repl(match: re.Match[str]) -> str:
            return click.style(match.group(), dim=True)

        opts, opt_help = help_record
        opt_help = self._dim_pattern.sub(dim_repl, opt_help)
        return opts, opt_help


def _show_credits(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    credits = """
    no_vtf - Valve Texture Format Converter
    Copyright (C) b5327157

    https://sr.ht/~b5327157/no_vtf/
    https://pypi.org/project/no-vtf/
    https://developer.valvesoftware.com/wiki/no_vtf

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see <https://www.gnu.org/licenses/>.
    """

    click.echo(inspect.cleandoc(credits))
    ctx.exit()


def _show_version(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return

    click.echo(no_vtf.__version__)
    ctx.exit()


class _Slice(click.ParamType):
    name: Final = "slice"

    def get_metavar(self, param: click.Parameter) -> str:
        return "INDEX|[START]:[STOP][:STEP]"

    def convert(
        self,
        value: Union[str, slice],
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> slice:
        if isinstance(value, slice):
            return value

        slice_indices = self._to_slice_indices(value, param, ctx)

        start = slice_indices[0]
        if len(slice_indices) == 1:
            if start is None:
                self.fail("Index is empty.", param, ctx)
            if start >= 0:
                return slice(start, start + 1)
            else:
                stop = start + 1 if start != -1 else None
                return slice(start, stop)

        stop = slice_indices[1]
        if len(slice_indices) == 2:
            return slice(start, stop)

        step = slice_indices[2]
        if len(slice_indices) == 3:
            if step == 0:
                self.fail("Slice step cannot be zero.", param, ctx)
            return slice(start, stop, step)

        self.fail(f"Too many values in {value!r}.", param, ctx)

    def _to_slice_indices(
        self, value: str, param: Optional[click.Parameter], ctx: Optional[click.Context]
    ) -> list[Optional[int]]:
        slice_indices: list[Optional[int]] = []
        for slice_index in value.split(":"):
            if not slice_index:
                slice_indices.append(None)
            else:
                try:
                    slice_indices.append(int(slice_index))
                except ValueError:
                    self.fail(f"{slice_index!r} is not a valid integer.", param, ctx)
        return slice_indices


click.Context.formatter_class = _HelpFormatter


@click.command(name="no_vtf", no_args_is_help=True)
@click.argument(
    "paths",
    metavar="[--] PATH...",
    type=click.Path(path_type=pathlib.Path, exists=True),
    required=True,
    nargs=-1,
)
@click_option_group.optgroup("Conversion mode", cls=_OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--animate/--no-animate",
    cls=_GroupedOption,
    help="Output animated image file (default) / output each frame individually",
    type=bool,
    default=True,
)
@click_option_group.optgroup.option(
    "--raw",
    cls=_GroupedOption,
    help="Extract image data as-is (without decoding)",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup("\n  Extraction", cls=_OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--mipmaps",
    "-m",
    cls=_GroupedOption,
    help="Extract all mipmaps",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup.option(
    "--low-res-img",
    cls=_GroupedOption,
    help="Extract low resolution image",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup.option(
    "--min-resolution",
    cls=_GroupedOption,
    help="Minimum mipmap resolution",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click_option_group.optgroup.option(
    "--max-resolution",
    cls=_GroupedOption,
    help="Maximum mipmap resolution",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click_option_group.optgroup.option(
    "--closest-resolution",
    cls=_GroupedOption,
    help="Fallback to the closest resolution if no exact match",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup.option(
    "--frames",
    cls=_GroupedOption,
    help="Frames to extract",
    type=_Slice(),
)
@click_option_group.optgroup.option(
    "--faces",
    cls=_GroupedOption,
    help="Faces to extract",
    type=_Slice(),
)
@click_option_group.optgroup.option(
    "--slices",
    cls=_GroupedOption,
    help="Slices to extract",
    type=_Slice(),
)
@click_option_group.optgroup(
    "\n  Image decoding (not used with --raw)",
    cls=_OptionGroup,
)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--dynamic-range",
    cls=_GroupedOption,
    help="Override LDR/HDR auto-detection",
    type=click.Choice(["ldr", "hdr"], case_sensitive=False),
)
@click_option_group.optgroup.option(
    "--overbright-factor",
    cls=_GroupedOption,
    help="Multiplicative factor used for decoding compressed HDR textures",
    show_default=True,
    type=float,
    default=16.0,
)
@click_option_group.optgroup(
    "\n  Image postprocessing (not used with --raw)",
    cls=_OptionGroup,
)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--hdr-to-ldr",
    cls=_GroupedOption,
    help="Convert HDR from linear sRGB to sRGB and output as clipped LDR",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup.option(
    "--separate-channels",
    cls=_GroupedOption,
    help="Output the RGB/L and A channels separately",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup(
    "\n  Image output (not used with --raw)",
    cls=_OptionGroup,
)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--ldr-format",
    "-f",
    cls=_GroupedOption,
    help="LDR output format",
    metavar="SINGLE[|MULTI]",
    show_default=True,
    type=str,
    default="tiff|apng",
)
@click_option_group.optgroup.option(
    "--hdr-format",
    "-F",
    cls=_GroupedOption,
    help="HDR output format",
    metavar="SINGLE[|MULTI]",
    show_default=True,
    type=str,
    default="exr",
)
@click_option_group.optgroup.option(
    "--fps",
    cls=_GroupedOption,
    help="Frame rate used for animated image files",
    show_default=True,
    type=int,
    default=5,
)
@click_option_group.optgroup.option(
    "--compress/--no-compress",
    cls=_GroupedOption,
    help="Control lossless compression",
    type=bool,
    default=None,
)
@click_option_group.optgroup("\n  Read/write control", cls=_OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "write",
    "--always-write/--no-write",
    cls=_GroupedOption,
    help="Write images",
    type=bool,
    default=None,
)
@click_option_group.optgroup.option(
    "readback",
    "--readback/--no-readback",
    cls=_GroupedOption,
    help="Readback images",
    type=bool,
    default=False,
)
@click_option_group.optgroup("\n  Output destination", cls=_OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--output-dir",
    "-o",
    "output_directory",
    cls=_GroupedOption,
    help="Output directory",
    metavar="PATH",
    type=click.Path(path_type=pathlib.Path, exists=True, file_okay=False, dir_okay=True),
)
@click_option_group.optgroup.option(
    "--output-file",
    "-O",
    cls=_GroupedOption,
    help="Output file",
    metavar="PATH",
    type=click.Path(path_type=pathlib.Path, file_okay=True, dir_okay=False),
)
@click_option_group.optgroup("\n  Miscellaneous", cls=_OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.option(
    "--num-workers",
    cls=_GroupedOption,
    help="Number of workers for parallel conversion",
    metavar="INTEGER",
    type=click.IntRange(min=1),
)
@click_option_group.optgroup.option(
    "--no-progress",
    cls=_GroupedOption,
    help="Do not show the progress bar",
    type=bool,
    is_flag=True,
)
@click_option_group.optgroup("\n  Info", cls=_OptionGroup)  # type: ignore[misc]
@click_option_group.optgroup.help_option("--help", "-h", cls=_GroupedOption)
@click_option_group.optgroup.option(
    "--version",
    cls=_GroupedOption,
    help="Show the version and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_version,
)
@click_option_group.optgroup.option(
    "--credits",
    cls=_GroupedOption,
    help="Show the credits and exit.",
    type=bool,
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=_show_credits,
)
def main_command(
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path],
    output_file: Optional[pathlib.Path],
    ldr_format: str,
    hdr_format: str,
    dynamic_range: Optional[ImageDynamicRange],
    mipmaps: bool,
    min_resolution: Optional[int],
    max_resolution: Optional[int],
    closest_resolution: bool,
    frames: Optional[slice],
    faces: Optional[slice],
    slices: Optional[slice],
    animate: bool,
    fps: int,
    separate_channels: bool,
    overbright_factor: float,
    hdr_to_ldr: bool,
    low_res_img: bool,
    compress: Optional[bool],
    raw: bool,
    write: Optional[bool],
    readback: bool,
    num_workers: Optional[int],
    no_progress: bool,
) -> None:
    """
    Convert Valve Texture Format files into standard image files.

    PATH can be either file, or directory (in which case it is recursively searched
    for .vtf files, symbolic links are not followed). Multiple paths may be provided.

    As the output path, it is possible to specify either file or directory.

    Specifying the output file is useful mostly for single-file conversions,
    with filters to ensure the output file will be written only once.

    If the output directory is not specified, images are output into the source directories
    (in-place conversion). Otherwise, directory tree for any found files will be reconstructed
    in the chosen directory.

    Output LDR/HDR format is selected by its common file name extension. It is recommended selecting
    one of the specifically supported image formats (PNG, APNG, TGA, TIFF, EXR). Other image formats
    have not been validated to work, but can be still selected. A secondary format specifically used
    to output animated image files can be selected after '|' (see default LDR format as an example).
    The "skip" format can be used to skip the write step entirely.

    For the specifically supported image formats, compression is configurable when saving the image.
    Lossless compression is enabled by default. Lossy compression is not used.

    The BGRA8888 format can store both LDR and compressed HDR images.
    The specific type is either auto-detected by looking at the input file name
    (roughly, if it contains "hdr" near the end), or can be set manually.

    It is possible to filter images to convert by min/max resolution (width & height),
    and by frames/faces/slices. The former supports exact or closest match. The latter
    supports selection by single index or via Python slicing:
    https://python-reference.readthedocs.io/en/latest/docs/brackets/slicing.html

    Face index mapping: right (0), left, back, front, up, down, sphere map (6).

    After applying filters, only the highest-resolution mipmap is converted by default.
    Alternatively, all mipmaps of the high-resolution image can be converted.

    Animated textures are converted into an animated multi-frame image file by default.
    Alternatively, they can also be converted into single-frame images with animation disabled.

    The RGB/L and A channels are packed into one file by default.
    When output separately, resulting file names will be suffixed with "_rgb", "_l" or "_a".

    By default, image files are only written if they do not exist already.
    Alternatively, they can be overwritten, or writing can be disabled entirely.

    Images can also be read back to verify they have been written properly.
    Readback will error if data to be written do not match what is in the file.

    Worker is spawned for each logical core to run the conversion in parallel.
    Number of workers can be overridden. If set to 1, conversion is sequential.
    Sequential conversion enables more verbose errors to be printed.

    Exit status: Zero if all went successfully, non-zero if there was an error.
    Upon a recoverable error, conversion will proceed with the next file.
    """

    main(
        paths=paths,
        output_directory=output_directory,
        output_file=output_file,
        ldr_format=ldr_format,
        hdr_format=hdr_format,
        dynamic_range=dynamic_range,
        mipmaps=mipmaps,
        min_resolution=min_resolution,
        max_resolution=max_resolution,
        closest_resolution=closest_resolution,
        frames=frames,
        faces=faces,
        slices=slices,
        animate=animate,
        fps=fps,
        separate_channels=separate_channels,
        overbright_factor=overbright_factor,
        hdr_to_ldr=hdr_to_ldr,
        low_res_img=low_res_img,
        compress=compress,
        raw=raw,
        write=write,
        readback=readback,
        num_workers=num_workers,
        no_progress=no_progress,
    )


def main(  # noqa: C901
    *,
    paths: Sequence[pathlib.Path],
    output_directory: Optional[pathlib.Path] = None,
    output_file: Optional[pathlib.Path] = None,
    ldr_format: Optional[str] = None,
    hdr_format: Optional[str] = None,
    dynamic_range: Optional[ImageDynamicRange] = None,
    mipmaps: Optional[bool] = None,
    min_resolution: Optional[int] = None,
    max_resolution: Optional[int] = None,
    closest_resolution: Optional[bool] = None,
    frames: Optional[slice] = None,
    faces: Optional[slice] = None,
    slices: Optional[slice] = None,
    animate: Optional[bool] = None,
    fps: Optional[int] = None,
    separate_channels: Optional[bool] = None,
    overbright_factor: Optional[float] = None,
    hdr_to_ldr: Optional[bool] = None,
    low_res_img: Optional[bool] = None,
    compress: Optional[bool] = None,
    raw: Optional[bool] = None,
    write: Optional[bool] = None,
    readback: Optional[bool] = None,
    num_workers: Optional[int] = None,
    no_progress: Optional[bool] = None,
) -> None:
    if output_file and output_directory:
        raise ValueError("Output file and directory is mutually exclusive")

    params = main_command.params
    if ldr_format is None:
        ldr_format = _get_param_default(params, "ldr_format", str)
    if hdr_format is None:
        hdr_format = _get_param_default(params, "hdr_format", str)
    if mipmaps is None:
        mipmaps = _get_param_default(params, "mipmaps", bool)
    if closest_resolution is None:
        closest_resolution = _get_param_default(params, "closest_resolution", bool)
    if animate is None:
        animate = _get_param_default(params, "animate", bool)
    if fps is None:
        fps = _get_param_default(params, "fps", int)
    if separate_channels is None:
        separate_channels = _get_param_default(params, "separate_channels", bool)
    if overbright_factor is None:
        overbright_factor = _get_param_default(params, "overbright_factor", float)
    if hdr_to_ldr is None:
        hdr_to_ldr = _get_param_default(params, "hdr_to_ldr", bool)
    if low_res_img is None:
        low_res_img = _get_param_default(params, "low_res_img", bool)
    if raw is None:
        raw = _get_param_default(params, "raw", bool)
    if readback is None:
        readback = _get_param_default(params, "readback", bool)
    if no_progress is None:
        no_progress = _get_param_default(params, "no_progress", bool)

    vtf_extension_pattern = re.compile(r"\.vtf$", re.ASCII | re.IGNORECASE)

    texture_filters = _get_filters(
        mipmaps=mipmaps,
        min_resolution=min_resolution,
        max_resolution=max_resolution,
        closest_resolution=closest_resolution,
        frames=frames,
        faces=faces,
        slices=slices,
    )

    texture_extractor = VtfExtractor(low_res_img=low_res_img)
    texture_filter = TextureCombinedFilter(texture_filters)
    texture_decoder = VtfDecoder(dynamic_range=dynamic_range, overbright_factor=overbright_factor)
    texture_namer = Vtf2TgaLikeNamer(include_mipmap_level=mipmaps, include_frame=(not animate))

    formats = ldr_format.split("|") + hdr_format.split("|")
    pipeline_initializer = functools.partial(Pipeline.initialize, formats)
    pipeline_initializer()

    pipeline = Pipeline(
        input_extension_pattern=vtf_extension_pattern,
        ldr_format=ldr_format,
        hdr_format=hdr_format,
        animate=animate,
        fps=fps,
        separate_channels=separate_channels,
        hdr_to_ldr=hdr_to_ldr,
        compress=compress,
        raw=raw,
        write=write,
        readback=readback,
        extractor=texture_extractor,
        filter=texture_filter,
        decoder=texture_decoder,
        namer=texture_namer,
    )

    input_paths = InputPaths(paths)
    if input_paths.has_directories():
        _resolve_directories(input_paths, not no_progress)

    task_runner: TaskRunner
    if num_workers is None or num_workers > 1:
        task_runner = ParallelRunner(max_workers=num_workers, initializer=pipeline_initializer)
    else:
        task_runner = SequentialRunner()

    if output_file:
        tasks = _get_tasks(pipeline, input_paths, output_file=output_file)
    else:
        tasks = _get_tasks(pipeline, input_paths, output_directory=output_directory)
    exit_status = _process_tasks(task_runner, tasks, not no_progress)
    sys.exit(exit_status)


def _get_param_default(
    params: Sequence[click.core.Parameter], param_name: str, param_type: type[_T]
) -> _T:
    for param in params:
        if param.name == param_name:
            default = param.default
            if callable(default):
                default = default()

            assert isinstance(default, param_type)
            return default

    raise RuntimeError(f"No such parameter: {param_name}")


def _get_filters(
    *,
    mipmaps: bool,
    min_resolution: Optional[int],
    max_resolution: Optional[int],
    closest_resolution: bool,
    frames: Optional[slice],
    faces: Optional[slice],
    slices: Optional[slice],
) -> Sequence[TextureFilter[VtfTexture]]:
    texture_filters: list[TextureFilter[VtfTexture]] = []

    if frames:
        texture_filters.append(VtfFrameFilter(frames=frames))
    if faces:
        texture_filters.append(VtfFaceFilter(faces=faces))
    if slices:
        texture_filters.append(VtfSliceFilter(slices=slices))
    if min_resolution is not None or max_resolution is not None:
        texture_filters.append(
            VtfResolutionFilter(
                min=min_resolution, max=max_resolution, closest_as_fallback=closest_resolution
            )
        )
    if not mipmaps:
        texture_filters.append(VtfMipmapFilter(mipmap_levels=slice(-1, None), last="filtered"))

    return texture_filters


def _resolve_directories(input_paths: InputPaths, show_progress: bool) -> None:
    progress_bar_manager = _alive_bar(receipt=False) if show_progress else None
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for file in input_paths.search_in_directories("*.[vV][tT][fF]", add_results=True):
            if progress_bar:
                progress_bar.text = _posix_tty_style(file.name, io=sys.stderr, bold=True)
                progress_bar()
        input_paths.remove_directories()


def _get_tasks(
    pipeline: Pipeline[_T],
    input_paths: InputPaths,
    *,
    output_directory: Optional[pathlib.Path] = None,
    output_file: Optional[pathlib.Path] = None,
) -> Sequence[_Task[_T]]:
    output_directories = OutputDirectories(output_directory)

    tasks: list[_Task[_T]] = []
    for input_file, input_base_directory in input_paths:
        if output_file:
            assert not output_directory, "output_file and output_directory are mutually exclusive"
            task = _Task(pipeline=pipeline, input_file=input_file, output_file=output_file)
        else:
            output_directory = output_directories(input_file, input_base_directory)
            task = _Task(
                pipeline=pipeline, input_file=input_file, output_directory=output_directory
            )
        tasks.append(task)
    return tasks


def _process_tasks(
    task_runner: TaskRunner,
    tasks: Sequence[_Task[object]],
    show_progress: bool,
) -> int:
    exit_status = 0

    num_files = len(tasks)
    progress_bar_manager = _alive_bar(num_files) if show_progress else None
    with progress_bar_manager or contextlib.nullcontext() as progress_bar:
        for task, result in task_runner(tasks):
            task = cast(_Task[object], task)
            if isinstance(result, Receipt):
                if progress_bar:
                    skipped = not result.io_done
                    progress_bar(skipped=skipped)
                    progress_bar.text = _posix_tty_style(
                        str(task.input_file.name), io=sys.stderr, bold=True
                    )
            else:
                exit_status = 1

                exception: Exception = result
                formatted_exception = "".join(traceback.format_exception(exception))
                message = (
                    click.style("Error", fg="red")
                    + " while processing "
                    + click.style(repr(task), bold=True)
                    + f": {formatted_exception}"
                )
                click.echo(message, file=sys.stderr)

    return exit_status


class _Task(Generic[_T_co]):
    def __init__(
        self,
        *,
        pipeline: Pipeline[_T_co],
        input_file: pathlib.Path,
        output_directory: Optional[pathlib.Path] = None,
        output_file: Optional[pathlib.Path] = None,
    ) -> None:
        assert not (
            output_file and output_directory
        ), "output_file and output_directory are mutually exclusive"

        self.pipeline: Final = pipeline
        self.input_file: Final = input_file

        self._output_directory: Final = output_directory
        self._output_file: Final = output_file

    def __call__(self) -> Receipt:
        if self._output_file:
            return self.pipeline(self.input_file, output_file=self._output_file)
        else:
            assert self._output_directory, "either output_file or output_directory must be set"
            return self.pipeline(self.input_file, output_directory=self._output_directory)

    def __str__(self) -> str:
        return f"{self.input_file}"

    def __repr__(self) -> str:
        return f"{str(self.input_file)!r}"


class _AliveBar(Protocol):
    text: str

    def __call__(self, *, skipped: bool = False) -> None:
        ...


def _alive_bar(
    total: Optional[int] = None, *, receipt: bool = True
) -> AbstractContextManager[_AliveBar]:
    style = functools.partial(_posix_tty_style, io=sys.stderr)

    classic = _bar_factory(
        style("=", fg=127, bold=True),
        tip=style(">", fg=127, bold=True),
        background=" ",
        borders=(
            style("[", fg=172, bold=True),
            style("]", fg=172, bold=True),
        ),
        underflow=style("!", fg="red", bold=True),
        overflow=style("x", fg="red", bold=True),
    )

    brackets = _bouncing_spinner_factory(
        style(">" * 10, fg=127, bold=True), style("<" * 10, fg=127, bold=True)
    )

    alive_progress.styles.internal.BARS["no_vtf"] = classic
    alive_progress.styles.internal.SPINNERS["no_vtf"] = brackets

    return cast(
        AbstractContextManager[_AliveBar],
        alive_progress.alive_bar(
            total,
            length=40,
            spinner=None,
            bar="no_vtf",
            unknown="no_vtf",
            file=sys.stderr,
            enrich_print=False,
            receipt=receipt,
        ),
    )


def _bouncing_spinner_factory(chars_1: str, chars_2: str, *, right: bool = True) -> object:
    scroll_1 = _scrolling_spinner_factory(chars_1, right=right)
    scroll_2 = _scrolling_spinner_factory(chars_2, right=not right)
    return alive_progress.animations.spinners.sequential_spinner_factory(scroll_1, scroll_2)


def _scrolling_spinner_factory(chars: str, *, right: bool = True) -> object:
    num_cells = len(alive_progress.utils.cells.to_cells(click.unstyle(chars)))
    natural = num_cells * 2

    @alive_progress.animations.spinner_compiler.spinner_controller(
        natural=natural,
    )  # type: ignore[misc]
    def inner_spinner_factory(actual_length: Optional[int] = None) -> object:
        def frame_data() -> Iterator[str]:
            assert isinstance(inner_spinner_factory.natural, int)
            nonlocal actual_length
            actual_length = actual_length or inner_spinner_factory.natural

            start = 0
            stop = actual_length - num_cells + 1
            frame_iterator: Sequence[int] = list(range(start, stop))
            if not right:
                frame_iterator = list(reversed(frame_iterator))

            for i in frame_iterator:
                yield " " * i + chars + " " * (actual_length - i - num_cells)

        return (frame_data(),)

    return inner_spinner_factory


def _bar_factory(  # noqa: C901
    base: str,
    *,
    tip: str,
    background: str,
    underflow: str,
    overflow: str,
    borders: Optional[tuple[str, str]] = None,
) -> object:
    @alive_progress.animations.bars.bar_controller  # type: ignore[misc]
    def inner_bar_factory(
        length: int, spinner_factory: Optional[Callable[[int], object]] = None
    ) -> object:
        @_bordered(borders, "||")
        def draw_known(
            running: bool, percent: float
        ) -> tuple[tuple[str, ...], Optional[tuple[str]]]:
            percent = max(0, percent)

            base_length = round(percent * (length + 1))
            tip_length = 0

            if base_length > 0:
                if base_length <= length:
                    tip_length += 1

                base_length = min(length, base_length - 1)

            underflow_length = 0
            underflow_border = False
            if not running and percent < 1:
                if base_length + tip_length < length:
                    underflow_length = 1
                else:
                    underflow_border = True

            background_length = length - (base_length + tip_length + underflow_length)

            rendered_base = base_length * (base,)
            rendered_tip = tip_length * (tip,)
            rendered_underflow = underflow_length * (underflow,)
            rendered_background = background_length * (background,)

            right_border = None
            if percent > 1:
                right_border = (overflow,)
            if underflow_border:
                right_border = (underflow,)

            return (
                rendered_base + rendered_tip + rendered_underflow + rendered_background,
                right_border,
            )

        if spinner_factory:
            player = alive_progress.animations.utils.spinner_player(spinner_factory(length))

            @_bordered(borders, "||")
            def draw_unknown(percent: float) -> tuple[tuple[str, ...], Optional[tuple[str]]]:
                return next(player), None

            return draw_known, True, False, draw_unknown
        else:
            return draw_known, True, False, None

    return inner_bar_factory


def _bordered(
    borders: Optional[Sequence[str]], default: Sequence[str]
) -> Callable[
    [Callable[_P, tuple[tuple[str, ...], Optional[tuple[str]]]]],
    Callable[_P, tuple[str, ...]],
]:
    def wrapper(
        fn: Callable[_P, tuple[tuple[str, ...], Optional[tuple[str]]]]
    ) -> Callable[_P, tuple[str, ...]]:
        @functools.wraps(fn)
        def inner_bordered(*args: _P.args, **kwargs: _P.kwargs) -> tuple[str, ...]:
            content, right = fn(*args, **kwargs)
            return tuple(itertools.chain(left_border, content, right or right_border))

        return inner_bordered

    left_border = tuple((borders or default)[0:1] or default[0:1])
    right_border = tuple((borders or default)[1:2] or default[1:2])
    return wrapper


def _posix_tty_style(
    text: str,
    *,
    io: TextIO,
    fg: Optional[Union[int, tuple[int, int, int], str]] = None,
    bg: Optional[Union[int, tuple[int, int, int], str]] = None,
    bold: Optional[bool] = None,
    dim: Optional[bool] = None,
    underline: Optional[bool] = None,
    overline: Optional[bool] = None,
    italic: Optional[bool] = None,
    blink: Optional[bool] = None,
    reverse: Optional[bool] = None,
    strikethrough: Optional[bool] = None,
    reset: bool = True,
) -> str:
    if os.name == "posix" and io.isatty():
        return click.style(
            text,
            fg=fg,
            bg=bg,
            bold=bold,
            dim=dim,
            underline=underline,
            overline=overline,
            italic=italic,
            blink=blink,
            reverse=reverse,
            strikethrough=strikethrough,
            reset=reset,
        )

    return text
