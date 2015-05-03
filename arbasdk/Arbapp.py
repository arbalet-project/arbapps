#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Arbapp - Arbalet Application

    All Application for Arbalet should inherit from this class.
    Wanna create an awesome Arbalet application? Start here.

    Copyright (C) 2015 Yoan Mollard <yoan@konqifr.fr>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from Arbalet import Arbalet
from Arbamodel import Arbamodel
import argparse

__all__ = ['Arbapp']

class Arbapp(object):
    app_declared = False  # True when an Arbapp has been instanciated

    def __init__(self, argparser=None):
        if Arbapp.app_declared:
            raise RuntimeError('Arbapp can be instanciated only once')

        Arbapp.app_declared = True
        self._default_config = 'config150.cfg'
        self.read_args(argparser)

        self.arbalet = Arbalet(not self.args.no_gui, self.args.hardware, self.args.server, self.args.brightness,
                               self.args.factor_sim, self.args.config)

        self.width = self.arbalet.width
        self.height = self.arbalet.height

        self.model = Arbamodel(self.width, self.height, 'black')
        self.set_model(self.model)
        self.hardware, self.simulation = False, True


    def read_args(self, argparser):
        if argparser:
            parser = argparser
        else:
            parser = argparse.ArgumentParser(description='This script runs on Arbalet and allows the following arguments:')

        parser.add_argument('-w', '--hardware',
                            action='store_const',
                            const=True,
                            default=False,
                            help='The program must connect directly to Arbalet hardware')
        parser.add_argument('-ng', '--no-gui',
                            action='store_const',
                            const=True,
                            default=False,
                            help='The program must not be simulated on the workstation in a 2D window')
        parser.add_argument('-s', '--server',
                            type=str,
                            default='',
                            help='Address and port of the Arbaserver sharing hardware (ex: myserver.local:33400, 192.168.0.15, ...)')
        parser.add_argument('-c', '--config',
                            type=str,
                            default=self._default_config,
                            help='Name of the config file describing the table (.cfg file)')
        parser.add_argument('-b', '--brightness',
                            type=float,
                            default=1,
                            help='Brightness, intensity of hardware LEDs between 0.0 (all LEDs off) and 1.0 (all LEDs at full brightness)')
        parser.add_argument('-f', '--factor_sim',
                            type=int,
                            default=40,
                            help='Size of the simulated pixels')
        self.args = parser.parse_args()

    def set_model(self, model):
        self.arbalet.set_model(model)

    def run(self):
        raise NotImplementedError("Arbapp.run() must be overidden")

    def start(self):
        try:
            self.run()
        except:
            self.close("Program raised exception")
            raise
        else:
            self.close("Program naturally ended")

    def close(self, reason='unknown'):
        self.arbalet.close(reason)