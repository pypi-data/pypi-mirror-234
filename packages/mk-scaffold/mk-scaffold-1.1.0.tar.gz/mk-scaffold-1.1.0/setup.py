#!/usr/bin/env python3
# pylint: disable=redefined-outer-name
#
import shutil
import tempfile

from setuptools import setup


class AutoRestoreFile:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __enter__(self):
        shutil.copyfile(self.src, self.dst)

    def __exit__(self, _exc_type, _exc_value, _exc_traceback):
        shutil.copyfile(self.dst, self.src)


def load_requirements():
    with open("requirements.txt", encoding="UTF-8") as fd:
        requirements = fd.read().splitlines()
        requirements = [x for x in requirements if x and not x.startswith("--")]
    return requirements


def save_requirements(requirements):
    with open("requirements.txt", mode="w", encoding="UTF-8") as fd:
        fd.writelines([f"{x}\n" for x in requirements])


with tempfile.NamedTemporaryFile() as tmpfile:
    with AutoRestoreFile("requirements.txt", tmpfile.name):
        requirements = load_requirements()
        save_requirements(requirements)
        # Call setup with pyproject.toml configuration values
        setup()
