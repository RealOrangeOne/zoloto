from setuptools import setup

setup(
    name="yuri",
    version="0.0.0",
    url="https://github.com/realorangeone/yuri",
    author="Jake Howard",
    description="A fiducial marker system powered by OpenCV - Supports ArUco and April",
    packages=["yuri"],
    pathon_requires=">=3.6",
    install_requires=[
        "opencv-contrib-python-headless==4.1.0.25",
        "cached-property==1.5.1",
        "coordinates==0.3.0",
    ],
    project_urls={"GitHub: Issues": "https://github.com/realorangeone/yuri/issues"},
)
