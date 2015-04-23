#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Video pixeliser

    Renders a high-def video on Arbalet by reducing dramatically its resolution
    in real time.

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
import time, cv2, argparse
from arbasdk import Arbapp

class Pixeliser(Arbapp):
    def __init__(self, height, width, argparser):
        Arbapp.__init__(self, width, height, argparser)
        self.video_reader = None

    def play_file(self, f):
        self.video_reader = cv2.VideoCapture(f)

        while True:
            r, image = self.video_reader.read()
            if r:
                pix_image = cv2.resize(image, (self.height, self.width))
                pix_image = cv2.transpose(pix_image)
                self.update_model(pix_image)
                cv2.imshow(f, image)
                cv2.waitKey(100)
            else:
                break

    def update_model(self, image):
        for h in range(self.height):
            for w in range(self.width):
                pixel = map(int, image[h][w])
                pixel = [pixel[2], pixel[1], pixel[0]] # OpenCV pixels in BGR order
                self.model.set_pixel(h, w, pixel)

    def run(self):
        for f in self.args.input:
            self.play_file(f)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Pixelise a video file, i.e. decrease dramatically the number of'
                                                 'pixels to play the latter on the table')
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        nargs='+',
                        help='Video file(s) to pixelise')
    
    Pixeliser(15, 10, parser).start()