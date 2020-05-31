#!/usr/bin/env python3

"""Copyright 2020 Anna Eilering."""

from distutils.core import setup

setup(
    name='mazes',
    version='0.0.3',
    author='Anna Eilering',
    author_email='nahkki@gmail.com',
    url='https://github.com/ananci/programming_mazes_python',
    license='LICENSE',
    description='Implementation of mazes code from Programming Mazes book',
    long_description=open('README.md').read(),
    install_requires=['cairosvg'],
)
