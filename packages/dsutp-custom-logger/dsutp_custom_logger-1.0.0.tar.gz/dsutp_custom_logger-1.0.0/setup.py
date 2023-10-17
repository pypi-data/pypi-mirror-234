#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: Nurtaza
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2023 Nurtaza
"""

version = '1.0.0'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dsutp_custom_logger',
    version=version,

    author='Nurtaza',
    author_email='nurik.kulikov@mail.ru',

    description=(
        u'Python module custom logging'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/Nurik121/dsutp_custom_logger',
    download_url='https://github.com/Nurik121/dsutp_custom_logger/archive/main.zip',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['dsutp_custom_logger'],
    install_requires=['requests']
)