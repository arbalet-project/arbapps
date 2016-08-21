#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Image reader

    Reads an animated image and render it

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from PIL import Image
from os.path import isfile
from arbalet.core import Application
from time import sleep

class ImageReader(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.image = None
        self.palette = None
        self.vertical = False

    def play_file(self, f):
        if isfile(f):
            self.image = Image.open(f)
            if self.image.size[0]<self.image.size[1]:
                self.vertical = True
            while True:
                try:
                    self.update_model(self.image.convert('RGB').resize((self.width, self.height) if self.vertical
                                                                       else (self.height, self.width)))
                    self.image.seek(self.image.tell()+1)
                except EOFError:
                    if self.args.loop:
                        self.image.seek(0)
                    else:
                        return
                sleep(self.image.info['duration']/1000.)  # Gif duration are in msec
        else:
            raise IOError('No such file or directory: \'{}\''.format(f))

    def update_model(self, image):
        with self.model:
            for h in range(self.height):
                for w in range(self.width):
                    pixel = image.getpixel((w, h) if self.vertical else (h, w))
                    self.model.set_pixel(h, w, pixel)

    def run(self):
        for f in self.args.input:
            self.play_file(f)

