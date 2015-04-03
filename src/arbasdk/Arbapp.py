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
import sys
from threading import Thread

__all__ = ['Arbapp']

class Arbapp(object):

    # Authorized arguments
    authorized_opts = ["simulation", "hardware", "s", "a"]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        opts = self.readopts(sys.argv)
        self.arbalet = Arbalet("simulation" in opts or "s" in opts or len(opts)==0,
                               "hardware" in opts or "a" in opts,
                               width, height, 1)
        #self.run()
        #self.close("Program naturally ended")

    def readopts(self, argv):
        return [x.lstrip('-') for x in argv if x.lstrip('-') in self.authorized_opts]

    def set_model(self, model):
        self.arbalet.set_model(model)

    def run(self):
        raise NotImplementedError("Arbapp.run() must be overidden")

    def start(self):
        try:
            self.run()
        finally:
            self.close("Program naturally ended")

    def close(self, reason='unknown'):
        self.arbalet.close(reason)