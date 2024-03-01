"""football-calendar setup."""

from setuptools import setup

with open("README.md", encoding="UTF-8") as fp:
    long_description = fp.read()

__version__ = "0.0.1"

setup(
    version=__version__,
    long_description=long_description,
)
