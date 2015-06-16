#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Image reader

    Reads an animated image and render it

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import argparse
import Image
from os.path import isfile
from arbasdk import Arbapp
from time import sleep

class ImageReader(Arbapp):
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser)
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
        self.model.lock()
        for h in range(self.height):
            for w in range(self.width):
                pixel = image.getpixel((w, h) if self.vertical else (h, w))
                self.model.set_pixel(h, w, pixel)
        self.model.unlock()

    def run(self):
        for f in self.args.input:
            self.play_file(f)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Render an animated image (gif, apng, mng...) on Arbalet')
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        nargs='+',
                        help='Path to the image(s) to render')

    parser.add_argument('-l', '--loop',
                        action='store_const',
                        const=True,
                        default=False,
                        help='Keep playing infinitely')

    parser.add_argument('-do', '--display-original',
                        action='store_const',
                        const=True,
                        default=False,
                        help='Display the original image (require access to X display)')

    ImageReader(parser).start()