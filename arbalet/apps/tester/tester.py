#!/usr/bin/env python
"""
    simpleTester.py - simple Arbalet tester.
    Copyright 2015 Thierry Chantier
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html

    Arbalet - ARduino-BAsed LEd Table
    Copyright 2015 Thierry Chantier, Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
__author__ = 'titimoby@gmail.com'

from arbalet.core import Application, Rate


class SimpleTester(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.colors = ['red', 'green', 'blue']
        self.color_index = 0

    def run(self):
        # Update the screen every second.
        rate = Rate(2.0)
        for w in range(self.width):
            for h in range(self.height):
                with self.model:
                    self.model.set_pixel(h, w, self.colors[self.color_index])
                rate.sleep()
            self.color_index = (self.color_index +1) % len(self.colors)
