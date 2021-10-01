from setuptools import find_packages, setup

setup(
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
)
