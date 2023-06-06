#!/usr/bin/env python3

from setuptools import setup,find_packages,find_namespace_packages
from mb_utils.src.version import version

setup(
    name="mb_utils",
    version=version,
    description="Basic logger and utils package",
    author=["Malav Bateriwala"],
    #packages=find_namespace_packages(include=["mb_utils.*"]),
    packages=find_packages(),
    scripts=[],
    install_requires=[
        "numpy",
        "pandas",
        "colorama",
        "fastprogress",],
    python_requires='>=3.8',)
