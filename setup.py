#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='arbalet_apps',
    version='3.2.0',
    license="GNU General Public License 3",
    description="Python API for development with Arbalet LED tables (ARduino-BAsed LEd Table)",
    url='http://github.com/arbalet-project',
    author="Yoan Mollard",
    author_email="contact@arbalet-project.org",
    long_description=open('README.md').read(),

    install_requires= ["pygame", "configparser", "bottle", "zmq", "python-xlib", "numpy", "tornado", "petname"], # "python-midi", "Pillow", # These packages are not Raspi-friendly
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
                ('arbalet/apps/lightshero/songs/Feelings', ['arbalet/apps/lightshero/songs/Feelings/guitar.ogg']),
                ('arbalet/apps/lightshero/songs/Feelings', ['arbalet/apps/lightshero/songs/Feelings/notes.mid']),
                ('arbalet/apps/lightshero/songs/Feelings', ['arbalet/apps/lightshero/songs/Feelings/song.ini']),
                ('arbalet/apps/lightshero/songs/Feelings', ['arbalet/apps/lightshero/songs/Feelings/song.ogg']),
                ('arbalet/tools/sequencer/sequences', ['arbalet/tools/sequencer/sequences/default.json']),
                ('arbalet/tools/snap/xml', ['arbalet/tools/snap/xml/arbalet.xml']),
                ('arbalet/tools/snap/templates', ['arbalet/tools/snap/templates/admin.html']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap.css']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap.css.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap-grid.css']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap-grid.css.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap-grid.min.css']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap-grid.min.css.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap.min.css']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap.min.css.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap-reboot.css']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap-reboot.css.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap-reboot.min.css']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/css', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/css/bootstrap-reboot.min.css.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/js', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/js/bootstrap.bundle.js']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/js', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/js/bootstrap.bundle.js.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/js', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/js/bootstrap.bundle.min.js']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/js', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/js/bootstrap.bundle.min.js.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/js', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/js/bootstrap.js']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/js', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/js/bootstrap.js.map']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/js', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/js/bootstrap.min.js']),
                ('arbalet/tools/snap/static/bootstrap-4.1.3-dist/js', ['arbalet/tools/snap/static/bootstrap-4.1.3-dist/js/bootstrap.min.js.map']),
                ('arbalet/tools/snap/static/css/', ['arbalet/tools/snap/static/css/admin.css']),
                ('arbalet/tools/snap/static/images/', ['arbalet/tools/snap/static/images/background.jpg']),
                ('arbalet/tools/snap/static/images/', ['arbalet/tools/snap/static/images/header.png']),
                ('arbalet/tools/snap/static/js/', ['arbalet/tools/snap/static/js/admin.js']),
                ('arbalet/tools/snap/static/js/lib', ['arbalet/tools/snap/static/js/lib/jquery-3.2.1.js']),
    ],
)
