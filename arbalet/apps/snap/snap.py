#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Bridge for the Snap! visual programming language

    Provides a visual programming language to Arbalet for children or beginners

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from bottle import Bottle
from arbasdk import Arbapp


class SnapServer(Arbapp):
    def __init__(self, port, argparser=None):
        Arbapp.__init__(self, argparser)
        self.bottle = Bottle()
        self.port = int(port)
        self.route()

    def route(self):
        self.bottle.route('/set_pixel/<h>/<w>/<color>', callback=self.set_pixel)
        self.bottle.route('/set_pixel_rgb/<h>/<w>/<r>/<g>/<b>', callback=self.set_pixel_rgb)

    def set_pixel(self, h, w, color):
        self.model.set_pixel(int(h)-1, int(w)-1, color)
        return ''

    def set_pixel_rgb(self, h, w, r, g, b):
        self.model.set_pixel(int(h)-1, int(w)-1, [int(float(r)), int(float(g)), int(float(b))])
        return ''

    def run(self):
        self.bottle.run(host='localhost', port=self.port)

if __name__=='__main__':
    SnapServer(33450).run()
