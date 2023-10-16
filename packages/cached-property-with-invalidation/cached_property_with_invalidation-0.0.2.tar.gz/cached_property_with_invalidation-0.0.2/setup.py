from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.2"
DESCRIPTION = "Decorator to create cached_property that can be invalidated when invalidation variable is updated"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cached_property_with_invalidation",
    version=VERSION,
    author="Tyler Lum",
    author_email="tylergwlum@gmail.com",
    url="https://github.com/tylerlum/cached_property_with_invalidation",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "cached_property", "cached", "property", "invalidation"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
