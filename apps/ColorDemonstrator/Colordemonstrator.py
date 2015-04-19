#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Color Demonstrator - Arbalet Color Demonstrator

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
import time
import random
from arbasdk import Arbapp, Arbapixel

def rescale(val, in_min, in_max, out_min, out_max):
    return out_min + (val - in_min) * ((out_max - out_min) / float(in_max - in_min))

def LifeGenerator0(colors, duration):
    """
    Generator of pixel values browsing the given colors
    :param colors: The list of colors to browse
    :param duration: Duration of a single color change in number of frames (int from 1 to n)
    :return: the yielded next value of this pixel
    """
    pairs = zip(colors, colors[1:])
    while True:
        for color1, color2 in pairs:
            for v in range(duration):
                col = Arbapixel(color1)*((duration-v)/float(duration)) + Arbapixel(color2)*(v/float(duration))
                yield col

def swipe_async(n_frames, n_colors):
    pairs = zip(range(n_colors), range(1, n_colors))
    n_swipe = n_frames/n_colors # TODO %n_colors=0
    color_generator = [[]]
    raise NotImplementedError()

def gen_random_flashing(n_frames, n_colors):
    if n_frames%2==1:  # We need an odd number of frames since we are going to divide them by two
        n_frames+=1
    base_exp = [1.1**(p-n_frames/2+1) for p in range(n_frames/2)]  # The first n_frames/2 are an exponential rise
    reverse_base = [base_exp[i] for i in range(n_frames/2-1, -1, -1)]
    white_generator = base_exp+reverse_base
    blue_generator = [1.0-i for i in white_generator]
    color_generator = [blue_generator, white_generator]

    return color_generator

class ColorDemo(Arbapp):
    generators = [gen_random_flashing, ]

    def __init__(self, width, height, colors, rate, dur_min, dur_max, generator_id):
        Arbapp.__init__(self, width, height)
        self.durations = [int(dur_min*rate), int(dur_max*rate)]
        self.rate = rate
        if colors[:-1]!=colors[0]:
            colors.append(colors[0])
        self.colors = colors
        self.generator = self.generators[generator_id]

    def apply_color_to_generator(self, colors, color_generator):
        while True:
            for s in range(len(color_generator[0])):
                col = Arbapixel(colors[0])*color_generator[0][s] + Arbapixel(colors[1])*color_generator[1][s]
                yield col

    def run(self):
        # Construct all pixel generators
        generators = [[None for w in range(self.width)] for h in range(self.height)]
        for h in range(self.height):
            for w in range(self.width):
                duration = random.randrange(self.durations[0], self.durations[1])
                generators[h][w] = self.apply_color_to_generator(self.colors, self.generator(duration, len(self.colors)))

        # Browse all pixel generators at each time
        while True:
            for h in range(self.height):
                for w in range(self.width):
                    try:
                        color = generators[h][w].next()
                    except StopIteration:
                        pass
                    else:
                        self.model.set_pixel(h, w, color)
            time.sleep(1./self.rate)


#e = ColorDemo(width = 10, height = 15, colors=['navy', 'gold', 'deeppink', 'yellowgreen', 'purple'], rate=20, dur_min=10, dur_max=30)
e = ColorDemo(width = 10, height = 15, colors=['darkblue', 'white'], rate=20, dur_min=10, dur_max=60, generator_id=0)

e.run()
e.close("end")