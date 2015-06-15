#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Image reader

    Reads an animated image and render it

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import argparse
from PIL import Image
from os.path import isfile
from arbasdk import Arbapp
from time import sleep

class ImageReader(Arbapp):
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser)
        self.image = None
        self.palette = None

    def play_file(self, f, time):
        if isfile(f):
            self.image = Image.open(f)
            while True:
                try:
                    self.update_model(self.image.convert('RGB'))
                    self.image.seek(self.image.tell()+1)
                except EOFError:
                    print "End"
                    sleep(time)
                else:
                    print "New frame"
                    sleep(0.1)
        else:
            raise IOError('No such file or directory: \'{}\''.format(f))

    def update_model(self, image):
        self.model.lock()
        for h in range(self.height):
            for w in range(self.width):
                pixel = image.getpixel((h, w))
                self.model.set_pixel(h, w, pixel)
        self.model.unlock()

    def run(self):
        for f in self.args.input:
            self.play_file(f, 5)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Render an animated image (gif, apng, mng...) on Arbalet')
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        nargs='+',
                        help='Path to the image(s) to render')

    parser.add_argument('-do', '--display-original',
                        action='store_const',
                        const=True,
                        default=False,
                        help='Display the original image (require access to X display)')

    ImageReader(parser).start()