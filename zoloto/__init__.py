import pkg_resources

__version__ = pkg_resources.require("zoloto")[0].version


def has_gui_components():
    try:
        pkg_resources.require("opencv-contrib-python")
        return True
    except pkg_resources.DistributionNotFound:
        return False
