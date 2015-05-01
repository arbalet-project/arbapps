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

def gen_sweep_async(n_frames, n_frames_fade, n_frames_rand, colors):
    # TODO randomization to change to avoid overlapping of farthest colors
    """
    This generator generates sweeping colors with a unique duration between colors for all pixels
    Randomization is made during initial fading up, pixels start weeping at different times
    This generator can be used when colors are ordered, they do not go well all together, a given
    color must be mixed only with colors right before or right after it.
    :param n_frames: Duration between two consecutive colors
    :param n_frames_fade: Unused
    :param n_frames_rand: Duration of fade + random seed
    :param colors: list of colors with order respected
    """
    # This loop fades up and is also the random seed
    for f in range(n_frames_rand):
        yield Arbapixel(colors[0])*(float(f)/n_frames_rand)

    color_generator = [[float(x)/n_frames for x in range(n_frames, -1, -1)],           # Descending phase
                       [float(x)/n_frames for x in range(n_frames)]]                   # Ascending phase

    # Infinite loop on color sequence
    pairs = zip(colors, colors[1:])
    while True:
        for color1, color2 in pairs:
            for s in range(n_frames):
                col = Arbapixel(color1)*color_generator[0][s] + Arbapixel(color2)*color_generator[1][s]
                yield col

def gen_sweep_rand(n_frames, n_frames_fade, n_frames_rand, colors):
    """
    This generator generates sweeping colors with a unique duration between colors for all pixels
    Randomization is implemented through the order of color browsing
    This generator can be used when all colors go well together, there is no external random seed
    :param n_frames: Duration between two consecutive colors
    :param n_frames_fade: Duration of fade
    :param n_frames_rand: Random seed, extra duration added to n_frames to get the total duration
    :param colors: list of colors whose order will be randomized (no side effect)
    """
    start = 0 #random.randint(0, n_frames-1)  # TODO debug, we should start a a certain PAIR instead

    color_generator = [[float(x)/n_frames for x in range(n_frames, -1, -1)],           # Descending phase
                       [float(x)/n_frames for x in range(n_frames)]]                   # Ascending phase

    # This loop fades up
    for f in range(n_frames_fade):
        yield Arbapixel(colors[0])*(color_generator[1][start]*(float(f)/n_frames_fade))

    # Infinite loop on color sequence
    pairs = zip(colors, colors[1:])
    while True:
        for color1, color2 in pairs:
            for s in range(n_frames):
                col = Arbapixel(color1)*color_generator[0][s] + Arbapixel(color2)*color_generator[1][s]
                yield col

def gen_random_flashing(n_frames, n_frames_fade, n_frames_rand, colors):
    """
    This generator generates exponential rises/descents from the first color to the second color
    External randomization is brought though the duration of the rise = n_frames + n_frames_rand
    Internal randomization is made through a random starting frame between start of the rise and end of the descent
    :param n_frames: Common minimum duration of all pixels
    :param n_frames_fade: Duration of fade
    :param n_frames_rand: Random seed, extra duration added to n_frames to get the total duration
    :param colors: List of two colors. The other colors, if any, are ignored
    """
    n_frames += n_frames_rand
    n_frames -= n_frames%2  # We need an even number of frames since we are going to divide them by two
    base_exp = [1.1**(p-n_frames/2+1) for p in range(n_frames/2)]  # The first n_frames/2 are an exponential ascending phase
    reverse_base = [base_exp[i] for i in range(n_frames/2-1, -1, -1)]  # The last n_frames/2 are an exponential descending phase
    white_generator = base_exp+reverse_base
    blue_generator = [1.0-i for i in white_generator]
    color_generator = [blue_generator, white_generator]

    start = random.randint(0, n_frames-1)  # Allows to advance browsing and get immediate flashing after start

    # Fade up
    for f in range(n_frames_fade):
        yield Arbapixel(colors[0]) + Arbapixel(colors[1])*(color_generator[1][start]*(float(f)/n_frames_fade))

    while True:
        for s in range(start, n_frames):
            col = Arbapixel(colors[0]) + Arbapixel(colors[1])*color_generator[1][s]
            yield col
        start = 0

class ColorDemo(Arbapp):
    generators = [gen_random_flashing, gen_sweep_async, gen_sweep_rand, ]

    def __init__(self, width, height, colors, rate, dur_min, dur_max, generator_id):
        Arbapp.__init__(self, width, height)
        self.durations = [int(dur_min*rate), int(dur_max*rate)]
        self.rate = rate
        if colors[-1]!=colors[0]:
            colors.append(colors[0])
        self.colors = colors
        self.generator = self.generators[generator_id]

    def run(self):
        # Construct all pixel generators
        generators = [[None for w in range(self.width)] for h in range(self.height)]
        for h in range(self.height):
            for w in range(self.width):
                duration = random.randrange(0, self.durations[1]-self.durations[0])
                generators[h][w] = self.generator(self.durations[0], self.rate, duration, self.colors)

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


e = ColorDemo(width = 10, height = 15, colors=['gold', 'darkorange', 'darkred', 'deeppink', 'purple', 'darkblue', 'turquoise', 'darkgreen', 'yellowgreen'], rate=20, dur_min=10, dur_max=15, generator_id=1)

# African style
#e = ColorDemo(width = 10, height = 15, colors=[(39,26, 19), (172, 69, 11), (232, 139, 36)], rate=20, dur_min=5, dur_max=15, generator_id=2)

#e = ColorDemo(width = 10, height = 15, colors=['darkblue', 'white'], rate=20, dur_min=10, dur_max=60, generator_id=0)

e.start()
e.close("end")