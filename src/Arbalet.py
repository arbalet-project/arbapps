#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table

    This class is the Arbalet master
    Controller calling all other features

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

from Arbamodel import *
from Arbasim import *
import getopt
import sys

class Arbalet(object):
    def __init__(self, simulation, hardware, width, height, factor_sim=30):
        self.simulation = simulation
        self.hardware = hardware
        self.width = width
        self.height = height

        if self.simulation:
            self.arbasim = Arbasim(self.width, self.height, self.width*factor_sim, self.height*factor_sim)

        if self.hardware:
            raise Exception("Arduino link not implemented")

    def set_model(self, model):
        if self.simulation:
            self.arbasim.set_model(model)
        if self.hardware:
            self.arbalink.set_model(model)

    def close(self, reason='unknown'):
        if self.simulation:
            self.arbasim.close(reason)
        if self.hardware:
            self.arbalink.close()

if __name__ == '__main__':
    width = 10
    height = 15
    simulation = True
    hardware = False

    arbalet = Arbalet(simulation, hardware, width, height)
    time.sleep(1)

    # We construct 2 different models to give an example
    model_red = Arbamodel(width, height)
    model_green = Arbamodel(width, height)

    # The "green" model is filled in background but not shown
    for w in range(width):
        for h in range(height):
            model_green.set_pixel(h, w, 'green')

    # The "red" model is now shown
    arbalet.set_model(model_red)

    # The "red" model is updated by reference, shown in live
    for w in range(width):
        for h in range(height):
            model_red.set_pixel(h, w, 'red')
            time.sleep(0.05)

    time.sleep(1)

    # We switch immediately to the "green" model...
    arbalet.set_model(model_green)
    time.sleep(1)

    # ...and back to the "red" again
    arbalet.set_model(model_red)
    time.sleep(1)
    arbalet.close("__main__ example ended")