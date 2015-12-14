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
        self.nbstrips=self.args.nbstrips
        self.nbleds=self.args.nbleds

    def run(self):
         # Update the screen every second.
        rate = Rate(2.0)

        for y in range(self.nbstrips):
            for x in range(self.nbleds):
                self.model.lock()

                self.model.set_pixel(x, y, self.PIXEL_COLOR)

                self.model.unlock()
                rate.sleep()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='light every pixel one by one')
    parser.add_argument('-ns', '--nbstrips',
                        type=int,
                        default='10',
                        help="number of strips")
    parser.add_argument('-nl', '--nbleds',
                        type=int,
                        default='15',
                        help="number of led per strip")
    app = SimpleTester(parser)
    app.start()
    app.close("end of app")