Calibration
===========

To perform accurate pose estimation, each camera must be calibrated. To calibrate the camera, OpenCV ships with a tool_ to assist.

The resulting calibration file can be passed into a :class:`zoloto.cameras.camera.Camera`.

Note: Occasionally on Linux, the tool will fail to open the camera. This happens as it uses gstreamer backend by default, whereas Zoloto uses v4l2. To disable gstreamer, set the ``OPENCV_VIDEOIO_PRIORITY_GSTREAMER=0`` environment variable.

Calibration Parameters
----------------------
.. autoclass:: zoloto.calibration.CalibrationParameters
    :members:

.. _tool: https://docs.opencv.org/4.5.3/d7/d21/tutorial_interactive_calibration.html
