#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Example - Arbalet Program Example

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

import time
from arbasdk.Arbamodel import Arbamodel
from arbasdk.Arbapp import Arbapp

class Example(Arbapp):
    def run(self):

        time.sleep(1)

        # We construct 2 different models to give an example
        model_red = Arbamodel(self.width, self.height)
        model_green = Arbamodel(self.width, self.height)

        # The "green" model is filled in background but not shown
        for w in range(self.width):
            for h in range(self.height):
                model_green.set_pixel(h, w, 'green')

        # The "red" model is now shown
        self.set_model(model_red)

        # The "red" model is updated by reference, shown in live
        for w in range(self.width):
            for h in range(self.height):
                model_red.set_pixel(h, w, 'red')
                time.sleep(0.05)

        time.sleep(1)

        # We switch immediately to the "green" model...
        self.set_model(model_green)
        time.sleep(1)

        # ...and back to the "red" again
        self.set_model(model_red)
        time.sleep(1)

# Actual call starting the program
Example(width = 10, height = 15)