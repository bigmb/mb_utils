#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_namespace_packages, setup
import os

VERSION_FILE = os.path.join(os.path.dirname(__file__), "VERSION.txt")


def _read_requirements() -> list[str]:
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if not os.path.exists(req_path):
        return []

    requirements: list[str] = []
    with open(req_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-r") or line.startswith("--requirement"):
                raise ValueError(
                    "requirements.txt contains nested requirements (-r/--requirement); "
                    "declare install_requires explicitly or flatten requirements.txt"
                )
            requirements.append(line)
    return requirements


INSTALL_REQUIRES = _read_requirements()
setup(
    name="mb_utils",
    description="Extra mb python utilities",
    author=["Malav Bateriwala"],
    packages=find_namespace_packages(include=["mb.*"]),
    #packages=find_packages(),
    scripts=[],
    install_requires=INSTALL_REQUIRES,
    setup_requires=["setuptools-git-versioning<2"],
    python_requires='>=3.8',
    setuptools_git_versioning={
        "enabled": True,
        "version_file": VERSION_FILE,
        "count_commits_from_version_file": True,
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}+{branch}",
        "dirty_template": "{tag}.post{ccount}",
    },
)