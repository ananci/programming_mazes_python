#!/usr/bin/env python

"""Copyright 2020 Anna Eilering."""

import os
from setuptools import setup, find_namespace_packages
import sys


def get_long_description():
    """
    Get Long Description text for Mazes.
    :return: 'Stuff'
    :rtype: String
    """
    # TODO - Add better description here.
    return "Stuff"


def get_license():
    """
    Get License text for Mazes.
    :return: 'Stuff'
    :rtype: String
    """
    # TODO - Set up a license for this
    return "license"

setup(
    name='mazes',
    version='0.0.1',
    description='Implementation of mazes code from Programming Mazes book',
    author='Anna Eilering',
    author_email='nahkki@gmail.com',
    url='https://github.com/ananci/programming_mazes_python',
    install_requires=[],
    package_dir = {'': 'mazes'},
    packages=find_namespace_packages('mazes'),
    license=get_license(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Students',
        'Natural Language :: English',
        'License :: Freely Distributable',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities'],
    )