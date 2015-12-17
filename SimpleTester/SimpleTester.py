#!/usr/bin/env python
"""
    simpleTester.py - simple Arbalet tester.
    Copyright 2015 Thierry Chantier
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html

    Arbalet - ARduino-BAsed LEd Table
    Copyright 2015 Joseph Silvestre, Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
__author__ = 'titimoby@gmail.com'

import argparse
import datetime
from arbasdk import Arbapp, Rate


class SimpleTester(Arbapp):
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser)
        self.BG_COLOR = 'black'
        self.PIXEL_COLOR='darkred'

    def run(self):
        # Update the screen every second.
        rate = Rate(2.0)
        for y in range(self.width):
            for x in range(self.height):
                with self.model:
                    self.model.set_pixel(x, y, self.PIXEL_COLOR)
                rate.sleep()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='light every pixel one by one')

    app = SimpleTester(parser)
    app.start()
    app.close("end of app")