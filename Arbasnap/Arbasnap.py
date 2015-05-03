#!/usr/bin/env python
from bottle import Bottle
from arbasdk import Arbapp


class SnapServer(Arbapp):
    def __init__(self, port, width, height, argparser=None):
        Arbapp.__init__(self, width, height, argparser)
        self.bottle = Bottle()
        self.port = int(port)
        self.route()

    def route(self):
        self.bottle.route('/set_pixel/<h>/<w>/<color>', callback=self.set_pixel)

    def set_pixel(self, h, w, color):
        self.model.set_pixel(int(h), int(w), color)
        return ''

    def run(self):
        self.bottle.run(host='localhost', port=self.port)

if __name__=='__main__':
    SnapServer(33450, 10, 15).run()