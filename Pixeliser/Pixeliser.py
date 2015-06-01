#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Video pixeliser

    Renders a high-def video on Arbalet by reducing dramatically its resolution
    in real time.

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import time, cv2, argparse
from arbasdk import Arbapp

class Pixeliser(Arbapp):
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser)
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
    
    Pixeliser(parser).start()