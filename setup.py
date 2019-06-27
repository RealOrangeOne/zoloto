from setuptools import setup

setup(
    name="zoloto",
    version="0.0.0",
    url="https://github.com/realorangeone/zoloto",
    author="Jake Howard",
    description="A fiducial marker system powered by OpenCV - Supports ArUco and April",
    packages=["zoloto"],
    python_requires=">=3.5",
    install_requires=[
        "opencv-contrib-python-headless==4.1.0.25",
        "cached-property==1.5.1",
        "coordinates==0.3.0",
        "fastcache==1.1.0",
        "ujson==1.35",
    ],
    project_urls={"GitHub: Issues": "https://github.com/realorangeone/zoloto/issues"},
    extras_require={"rpi": ["picamera[array]"]},
    entry_points={"console_scripts": ["zoloto-calibrate=zoloto.cli.calibrate:main"]},
)
