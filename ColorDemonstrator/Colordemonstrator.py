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

def gen_swipe_async(n_frames, colors):
    color_generator = [[float(x)/n_frames for x in range(n_frames, -1, -1)],           # Descending phase
                       [float(x)/n_frames for x in range(n_frames)]]                   # Ascending phase

    pairs = zip(colors, colors[1:])
    while True:
        for color1, color2 in pairs:
            for s in range(n_frames):
                col = Arbapixel(color1)*color_generator[0][s] + Arbapixel(color2)*color_generator[1][s]
                yield col

def gen_random_flashing(n_frames, colors):
    n_frames -= n_frames%2  # We need an even number of frames since we are going to divide them by two
    base_exp = [1.1**(p-n_frames/2+1) for p in range(n_frames/2)]  # The first n_frames/2 are an exponential ascending phase
    reverse_base = [base_exp[i] for i in range(n_frames/2-1, -1, -1)]  # The last n_frames/2 are an exponential descending phase
    white_generator = base_exp+reverse_base
    blue_generator = [1.0-i for i in white_generator]
    color_generator = [blue_generator, white_generator]

    while True:
        for s in range(n_frames):
            col = Arbapixel(colors[0])*color_generator[0][s] + Arbapixel(colors[1])*color_generator[1][s]
            yield col

class ColorDemo(Arbapp):
    generators = [gen_random_flashing, gen_swipe_async, ]

    def __init__(self, width, height, colors, rate, dur_min, dur_max, generator_id):
        Arbapp.__init__(self, width, height)
        self.durations = [int(dur_min*rate), int(dur_max*rate)]
        self.rate = rate
        if colors[:-1]!=colors[0]:
            colors.append(colors[0])
        self.colors = colors
        self.generator = self.generators[generator_id]

    def run(self):
        # Construct all pixel generators
        generators = [[None for w in range(self.width)] for h in range(self.height)]
        for h in range(self.height):
            for w in range(self.width):
                duration = random.randrange(self.durations[0], self.durations[1])
                generators[h][w] = self.generator(duration, self.colors)

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


#e = ColorDemo(width = 10, height = 15, colors=['gold', 'orange', 'darkorange', 'red'], rate=20, dur_min=1, dur_max=10, generator_id=1)
e = ColorDemo(width = 10, height = 15, colors=['darkblue', 'white'], rate=20, dur_min=10, dur_max=60, generator_id=0)

e.run()
e.close("end")