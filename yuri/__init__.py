import pkg_resources

from .camera import Camera  # noqa: F401

__version__ = pkg_resources.require("yuri")[0].version
