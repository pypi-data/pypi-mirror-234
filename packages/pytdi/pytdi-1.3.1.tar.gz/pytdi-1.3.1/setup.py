#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable='missing-module-docstring,exec-used

import setuptools


with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()


setuptools.setup(
    name='pytdi',
    use_scm_version=True,
    author='Martin Staab, Jean-Baptiste Bayle',
    author_email='martin.staab@aei.mpg.de, j2b.bayle@gmail.com',
    description="Python implementation of time-delay interferometry algorithms.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.in2p3.fr/LISA/LDPG/wg6_inrep/pytdi',
    license='BSD-3-Clause',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'h5py',
        'packaging',
        'importlib_metadata',
    ],
    setup_requires=['setuptools_scm'],
    tests_require=['pytest'],
    python_requires='>=3.6',
)
