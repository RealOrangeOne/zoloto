from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

setup(
    name="zoloto",
    version="0.6.1",
    url="https://github.com/RealOrangeOne/zoloto",
    author="Jake Howard",
    description="A fiducial marker system powered by OpenCV - Supports ArUco and April",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="BSD",
    packages=find_packages(include="zoloto*"),
    package_data={"zoloto": ["py.typed"]},
    install_requires=[
        "cached-property>=1.5",
        "pyquaternion>=0.9.2",
        "numpy<1.21",  # Requires py3.8 for correct typing https://numpy.org/devdocs/reference/typing.html
    ],
    project_urls={
        "Changelog": "https://github.com/RealOrangeOne/zoloto/releases",
        "Documentation": "https://zoloto.readthedocs.io/en/stable/",
        "Issues": "https://github.com/RealOrangeOne/zoloto/issues",
    },
    entry_points={"console_scripts": ["zoloto=zoloto.cli:main"]},
    python_requires=">=3.6",
    extras_require={
        "rpi": ["picamera[array]>=1.13"],
        "opencv": ["opencv-contrib-python>=4.0,<4.6"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
)
