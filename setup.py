#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='arbalet_apps',
    version='1.0.0',
    license="GNU General Public License 3",
    description="Python API for development with Arbalet LED tables (ARduino-BAsed LEd Table)",
    url='http://github.com/arbalet-project',
    author="Yoan Mollard",
    author_email="contact@konqi.fr",
    long_description=open('README.md').read(),

    install_requires= ["pygame", "bottle", "pyalsaaudio", "zmq", "python-xlib", "Pillow", "numpy"], # "python-midi"
    include_package_data=True,
    zip_safe=False,  # contains data files

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
    ],

    packages=find_packages(),
    namespace_packages = ['arbalet'],

    data_files=[('arbalet/apps/tetris/music', ['arbalet/apps/tetris/music/Cailloux_-_tetris.ogg']),
                ('arbalet/apps/tetris/music', ['arbalet/apps/tetris/music/ExDeath_-_Another_Tetris_Remix.ogg']),
                ('arbalet/apps/tetris/music', ['arbalet/apps/tetris/music/Mic_-_Mic_music_tetris__.ogg']),
    ],
)
