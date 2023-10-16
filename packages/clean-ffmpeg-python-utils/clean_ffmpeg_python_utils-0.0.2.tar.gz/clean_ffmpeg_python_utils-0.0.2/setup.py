from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.2"
DESCRIPTION = "Easy-to-use ffmpeg python utils with simpler arguments"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="clean_ffmpeg_python_utils",
    version=VERSION,
    author="Tyler Lum",
    author_email="tylergwlum@gmail.com",
    url="https://github.com/tylerlum/clean_ffmpeg_python_utils",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["ffmpeg-python", "typed-argument-parser"],
    keywords=["python", "ffmpeg", "video", "audio"],
    entry_points={
        "console_scripts": [
            "clean_ffmpeg_python_utils=clean_ffmpeg_python_utils.clean_ffmpeg_python_utils:main",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
