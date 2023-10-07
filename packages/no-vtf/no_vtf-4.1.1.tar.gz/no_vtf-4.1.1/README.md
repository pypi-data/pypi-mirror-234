# no_vtf

Say no to [.vtf](https://developer.valvesoftware.com/wiki/Valve_Texture_Format) – convert it to one of the standard image formats.

![Badge showing supported Python versions](https://img.shields.io/pypi/pyversions/no_vtf?style=flat-square)
[![Badge showing package version on PyPI](https://img.shields.io/pypi/v/no_vtf?style=flat-square)](https://pypi.org/project/no-vtf/)
[![Badge showing number of monthly downloads from PyPI](https://img.shields.io/pypi/dm/no_vtf?style=flat-square)](https://pypistats.org/packages/no-vtf)
[![Badge showing source code repository hosted on SourceHut](https://img.shields.io/badge/sr.ht-repository-white?labelColor=212529&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjxzdmcKICAgdmlld0JveD0iMCAwIDUxMiA1MTIiCiAgIHZlcnNpb249IjEuMSIKICAgaWQ9InN2ZzUxIgogICBzb2RpcG9kaTpkb2NuYW1lPSJzb3VyY2VodXQtd2hpdGUuc3ZnIgogICBpbmtzY2FwZTp2ZXJzaW9uPSIxLjEgKGM2OGUyMmMzODcsIDIwMjEtMDUtMjMpIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxkZWZzCiAgICAgaWQ9ImRlZnM1NSIgLz4KICA8c29kaXBvZGk6bmFtZWR2aWV3CiAgICAgaWQ9Im5hbWVkdmlldzUzIgogICAgIHBhZ2Vjb2xvcj0iIzUwNTA1MCIKICAgICBib3JkZXJjb2xvcj0iI2ZmZmZmZiIKICAgICBib3JkZXJvcGFjaXR5PSIxIgogICAgIGlua3NjYXBlOnBhZ2VzaGFkb3c9IjAiCiAgICAgaW5rc2NhcGU6cGFnZW9wYWNpdHk9IjAiCiAgICAgaW5rc2NhcGU6cGFnZWNoZWNrZXJib2FyZD0iMSIKICAgICBzaG93Z3JpZD0iZmFsc2UiCiAgICAgaW5rc2NhcGU6em9vbT0iMS42NTQyOTY5IgogICAgIGlua3NjYXBlOmN4PSIyNTYiCiAgICAgaW5rc2NhcGU6Y3k9IjI1NiIKICAgICBpbmtzY2FwZTp3aW5kb3ctd2lkdGg9IjE5MjAiCiAgICAgaW5rc2NhcGU6d2luZG93LWhlaWdodD0iMTA1OSIKICAgICBpbmtzY2FwZTp3aW5kb3cteD0iMCIKICAgICBpbmtzY2FwZTp3aW5kb3cteT0iMCIKICAgICBpbmtzY2FwZTp3aW5kb3ctbWF4aW1pemVkPSIxIgogICAgIGlua3NjYXBlOmN1cnJlbnQtbGF5ZXI9InN2ZzUxIiAvPgogIDxwYXRoCiAgICAgZD0iTTI1NiA4QzExOSA4IDggMTE5IDggMjU2czExMSAyNDggMjQ4IDI0OCAyNDgtMTExIDI0OC0yNDhTMzkzIDggMjU2IDh6bTAgNDQ4Yy0xMTAuNSAwLTIwMC04OS41LTIwMC0yMDBTMTQ1LjUgNTYgMjU2IDU2czIwMCA4OS41IDIwMCAyMDAtODkuNSAyMDAtMjAwIDIwMHoiCiAgICAgaWQ9InBhdGg0OSIKICAgICBzdHlsZT0iZmlsbDojZmZmZmZmIiAvPgo8L3N2Zz4K)](https://sr.ht/~b5327157/no_vtf)
[![Badge showing builds.sr.ht status](https://builds.sr.ht/~b5327157/no_vtf.svg?search=tags:master)](https://builds.sr.ht/~b5327157/no_vtf?search=tags:master)
[![Badge showing REUSE compliance status](https://api.reuse.software/badge/git.sr.ht/~b5327157/no_vtf)](https://api.reuse.software/info/git.sr.ht/~b5327157/no_vtf)
[![Badge showing Nox as the chosen Python automation toolkit](https://img.shields.io/badge/🦊-Nox-D85E00.svg)](https://github.com/wntrblm/nox)

![Screencast showing conversion of sprays downloaded in Team Fortress 2 using no_vtf](https://git.sr.ht/~b5327157/no_vtf/blob/HEAD/resources/docs/screencast_v4.gif)

## Motivation

- cross-platform – runs on any machine where Python is supported
- console-only – runs without a graphical interface
- full HDR support (including [compressed HDR](https://developer.valvesoftware.com/wiki/Valve_Texture_Format#HDR_compression))
- parallel conversion – uses all available resources to speed up the process
- proper decoding of the `ARGB8888` format (VTFLib/VTFEdit handles the format [incorrectly](https://github.com/NeilJed/VTFLib/issues/13))
- formally described .vtf file format (via [Kaitai Struct](https://kaitai.io))
- regression suite against crafted .vtf files and reference output
- desktop environment integration via [no_vtf-desktop](https://git.sr.ht/~b5327157/no_vtf-desktop) (Linux-only)

## Installation

### Application bundle

For Linux and Windows running on x64, there are application bundles with the Python interpreter included. Below are links to the latest version.

- [no_vtf-linux_x64.tar.xz](https://b5327157.srht.site/no_vtf/release/no_vtf-linux_x64.tar.xz) (glibc 2.31 or newer required, i.e. Debian 11, Ubuntu 20.04 LTS, …)
- [no_vtf-windows_x64.zip](https://b5327157.srht.site/no_vtf/release/no_vtf-windows_x64.zip) (Windows 8.1 or newer required)

```
./no_vtf ...  # Linux
no_vtf.exe ...  %= Windows =%
```

Bundles are ready to be used offline – the FreeImage library is already included.

### Package

If you have Python 3.10 or newer, you can install the [package](https://pypi.org/project/no-vtf/) from PyPI directly. An optional desktop integration is available via the [no_vtf-desktop](https://pypi.org/project/no-vtf-desktop/) package.

Before the first conversion, the FreeImage library will be downloaded to support the process. Further conversions are supported offline.

As of PEP 668, it is recommended to install the package into a virtual environment.

#### Automated installation (via [pipx](https://pypa.github.io/pipx/))

```
pipx install no_vtf

no_vtf ...
```

#### Manual installation

```
python3 -m venv no_vtf-venv

source no_vtf-venv/bin/activate  # Linux
no_vtf-venv/scripts/activate  %= Windows =%

python3 -m pip install no_vtf

no_vtf ...
```

## Usage

#### General invocation

```
no_vtf [OPTIONS] PATH...
```

PATH can be either file or directory. Multiple paths may be provided.

Tip: With bundles, drag-and-drop files or folders to be converted onto the application launcher (the file with icon and no extension on Linux and the .exe file on Windows).

#### Change output directory

```
no_vtf --output-dir /tmp PATH...
```

#### Override LDR/HDR output format

```
no_vtf --ldr-format png --hdr-format tiff PATH...
```

#### Set FPS for animated textures

```
no_vtf --animate --fps 20 PATH...
```

#### LDR-only VTF2TGA-like conversion

```
no_vtf --no-animate --ldr-format tga --hdr-format skip PATH...
```

#### Further help

```
no_vtf --help
```

## Supported formats

### Input

All textures installed with many [Source Engine](https://developer.valvesoftware.com/wiki/Source) games, including [Team Fortress 2](https://store.steampowered.com/app/440/Team_Fortress_2/), [Source Filmmaker](https://store.steampowered.com/app/1840/Source_Filmmaker/) and [Portal 2](https://store.steampowered.com/app/620/Portal_2/), can be converted with the supported format set.

- `RGBA8888`
- `ABGR8888`
- `RGB888`
- `BGR888`
- `I8`
- `IA88`
- `A8`
- `RGB888_BLUESCREEN`
- `BGR888_BLUESCREEN`
- `ARGB8888`
- `BGRA8888`
- `DXT1`
- `DXT3`
- `DXT5`
- `BGRA4444`
- `DXT1_ONEBITALPHA`
- `UV88`
- `RGBA16161616F`
- `RGBA16161616`

All official VTF versions are supported (7.0-7.5).

### Output

The following formats were tested and optimized for use:

#### LDR

- PNG, APNG
- TGA
- TIFF (default)

#### HDR

- EXR (default)
- TIFF

It is also possible to select other [formats](https://imageio.readthedocs.io/en/stable/formats/index.html) supported by Imageio.

## Known issues

### Color space

Color space of LDR textures is inferred from the context in which the texture is used in-game. Since this context is not available when converting the .vtf files directly, color space metadata for the output images cannot be set.

Color space of HDR textures is always linear. It would make sense to set this metadata when converting into the TIFF format, but for technical reasons, this is not done.

### Bit-perfect compatibility with VTF2TGA

Some textures (notably those using DXT compression) have up to ±1 difference in R/G/B values compared to the output of VTF2TGA. This might be caused by rounding errors in either implementation.

## Benchmark

- Sample: 11 GiB of LDR .vtf files
- CPU: Intel Core i7-6500U

Size is the total disk usage consumed by the output.
Conversion was done without extraction of all mipmaps.

### Compressed PNG, parallel

Time is the wall clock time.

- 1 worker: 9.71 minutes
- 2 workers: 5.45 minutes
- 3 workers: 4.18 minutes
- 4 workers: 3.77 minutes

### Uncompressed, sequential

Time is the total CPU time spent in user and kernel mode.

- PNG: 10.35 minutes
- TGA: 2.69 minutes
- TIFF: 3.27 minutes

In all three cases, the size was 33 GiB.

### Compressed, sequential

Time is the total CPU time spent in user and kernel mode.

- PNG: 5.9 GiB, 12.56 minutes
- TGA: 14 GiB, 3.77 minutes
- TIFF: 6.9 GiB, 8.81 minutes

## Development

For more resources, check out the Nox sessions in `noxfile.py` and the build system in `builds/`.

### Linting

```
python3 -m pip install nox

python3 -m nox -R
python3 -m nox -R -- --fix
```

### Pre-build steps

```
# compile .ksy files (requires Kaitai Struct compiler)
# only necessary if a .ksy file was modified
ksy/compile.sh
```

## License

The package is licensed under [GNU LGPL v3.0 or later](https://spdx.org/licenses/LGPL-3.0-or-later.html), except of image IO done with the help of the [ImageIO FreeImage](https://github.com/imageio/imageio-freeimage) plugin. This makes the entire package effectively licensed under [GNU GPL v3.0 or later](https://spdx.org/licenses/GPL-3.0-or-later.html). If you make use of the image IO part (either directly or indirectly) when linking to no_vtf as a library, the combined work is licensed under the latter license.
