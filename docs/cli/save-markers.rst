Save markers
============

The ``save-markers`` tool outputs the images of all the fiducial markers in a given type.

Each marker is surrounded by a white boarder, which is not considered part of the marker (it's not counted when working out the marker's size).

When `--raw` is passed, Markers are output as PNG files, at their smallest possible format. They can then be resized as necessary without losing quality.

Without `--raw`, images are saved 500px, plus a border with text identifying which marker is being used.
