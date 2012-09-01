#!/usr/bin/env python
# Copyright (c) Paul Tagliamonte <paultag@debian.org> under the terms and
# conditions of the Expat license.

from atlantic import __appname__, __version__
from setuptools import setup

long_description = open('README.md').read()

setup(
    name=__appname__,
    version=__version__,
    packages=['atlantic'],

    author="Paul Tagliamonte",
    author_email="paultag@debian.org",

    long_description=long_description,
    description='Debian stuff',
    license="Expat",
    url="http://pault.ag",

    platforms=['any']
)
