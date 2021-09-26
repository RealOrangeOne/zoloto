# Zoloto

[![Documentation Status](https://readthedocs.org/projects/zoloto/badge/?version=stable)](https://zoloto.readthedocs.io/en/stable/?badge=stable)
![Tests Status](https://github.com/RealOrangeOne/zoloto/workflows/Tests/badge.svg)
![PyPI](https://img.shields.io/pypi/v/zoloto.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zoloto.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/zoloto.svg)
![PyPI - Status](https://img.shields.io/pypi/status/zoloto.svg)
![PyPI - License](https://img.shields.io/pypi/l/zoloto.svg)

A fiducial marker system powered by OpenCV - Supports ArUco and April

[Documentation](https://zoloto.readthedocs.io/)

## Installation

```text
pip install zoloto
```

### OpenCV

OpenCV should be installed manually, ideally through your system package manager. This makes it easier to customize your OpenCV installation for your system, or use the optimal settings for your OS / hardware. Note that you may need to install `opencv-contrib` as well as `opencv`.

If you'd rather have one installed automatically, install the extra `opencv`:

```text
pip install zoloto[opencv]
```

Note that this version lacks hardware acceleration. See [the README](https://github.com/opencv/opencv-python#readme) for more details.

For storage-constrained environments, there's also `opencv-contrib-python-headless`, which should be installed manually.

## Examples

```python
from pathlib import Path

from zoloto import MarkerType
from zoloto.cameras import ImageFileCamera


with ImageFileCamera(Path("my-image.png"), marker_type=MarkerType.ARUCO_6X6) as camera:
    camera.save_frame("my-annotated-image.png", annotate=True)
    print("I saved an image with {} markers in.".format(len(camera.get_visible_markers())))
```

[More examples](./zoloto/cli/)

Zoloto ships with a CLI (aptly named `zoloto`), which contains some helpful utils for working with Zoloto and fiducial markers.

## Development setup

`./scripts/setup.sh` will create a virtual environment, and install all the required development dependencies into it.

Note that this will not install a version of OpenCV for you. For that, run `./scripts/setup.sh opencv`.

There are some additional useful scripts to assist:

- `./scripts/test.sh`: Run the unit tests and linters
- `./scripts/fix.sh`: Automatically fix issues from `black` and `isort`
- `./scripts/benchmark.sh`: Run benchmarks (these can take a couple minutes depending on your hardware)
