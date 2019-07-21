from setuptools import setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="zoloto",
    version="0.1.0",
    url="https://github.com/realorangeone/zoloto",
    author="Jake Howard",
    description="A fiducial marker system powered by OpenCV - Supports ArUco and April",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="BSD",
    packages=["zoloto"],
    python_requires=">=3.5",
    install_requires=[
        "opencv-contrib-python-headless>=4,<5",
        "cached-property",
        "coordinates",
        "fastcache",
        "ujson",
    ],
    project_urls={"GitHub: Issues": "https://github.com/realorangeone/zoloto/issues"},
    extras_require={"rpi": ["picamera[array]"]},
    entry_points={
        "console_scripts": [
            "zoloto-calibrate=zoloto.cli.calibrate:main",
            "zoloto-preview=zoloto.cli.preview:main",
        ]
    },
    keywords="opencv cv fiducial marker aruco april",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development",
    ],
)
