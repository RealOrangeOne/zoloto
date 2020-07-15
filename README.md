# Zoloto

[![Documentation Status](https://readthedocs.org/projects/zoloto/badge/?version=latest)](https://zoloto.readthedocs.io/en/latest/?badge=latest)
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

## Examples

```python
from pathlib import Path

from zoloto import MarkerType
from zoloto.cameras import ImageFileCamera


class MyCamera(ImageFileCamera):
    marker_type = MarkerType.DICT_6X6_50


with MyCamera(Path("my-image.png")) as camera:
    camera.save_frame("my-annotated-image.png", annotate=True)
    print("I saved an image with {} markers in.".format(len(camera.get_visible_markers())))
```

[More examples](./examples)

## Development setup

`./scripts/setup.sh` will create a virtual environment, and install all the required development dependencies into it.

There are some additional useful scripts to assist:

- `./scripts/test.sh`: Run the unit tests and linters
- `./scripts/fix.sh`: Automatically fix issues from `black` and `isort`
- `./scripts/benchmark.sh`: Run benchmarks (these can take a couple minutes depending on your hardware)
