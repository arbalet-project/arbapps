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

from Arbalet import *
import argparse

__all__ = ['Arbapp']

class Arbapp(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        default_config = 'config150.cfg'

        parser = argparse.ArgumentParser(description='This script runs on Arbalet and allows the following arguments:')
        parser.add_argument('-w', '--hardware',
                            type=bool,
                            default=False,
                            help='True if the program must connect directly to Arbalet hardware')
        parser.add_argument('-s', '--simulation',
                            type=bool,
                            default=True,
                            help='True if the program must be simulated on the workstation in a 2D window')
        parser.add_argument('-c', '--config',
                            type=str,
                            default=default_config,
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

        self.arbalet = Arbalet(self.args.simulation,
                               self.args.hardware, width, height,
                               self.args.brightness, self.args.factor_sim, self.args.config)

    def set_model(self, model):
        self.arbalet.set_model(model)

    def run(self):
        raise NotImplementedError("Arbapp.run() must be overidden")

    def start(self):
        try:
            self.run()
        except:
            self.close("Program raised exception")
        else:
            self.close("Program naturally ended")

    def close(self, reason='unknown'):
        self.arbalet.close(reason)