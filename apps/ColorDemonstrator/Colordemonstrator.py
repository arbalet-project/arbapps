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
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__))+'/../../src/')
import time
import random
from arbasdk import Arbamodel, Arbapp, Arbapixel
from itertools import product
from threading import Thread, Semaphore
from copy import deepcopy

class ColorDemo(Arbapp):

    def __init__(self, width, height, max_rate):
        Arbapp.__init__(self, width, height)
        self.model = Arbamodel(self.width, self.height)
        self.set_model(self.model)
        self.max_rate = max_rate  # Max refreshing rate in Hz
        self.semaphore = Semaphore(self.width*self.height)  # Thread synchronization

    def group_fade_colors(self, h, w, colors, duration, synchronized=None):
        num_steps = int(self.max_rate*duration)
        pairs = zip(colors, colors[1:])
        for color1, color2 in pairs:
            for v in range(num_steps):
                col = Arbapixel(color1)*((num_steps-v)/float(num_steps)) + Arbapixel(color2)*(v/float(num_steps))
                self.model.set_pixel(h, w, col)
                time.sleep(duration/float(num_steps))

    def group_fade_colors_loop(self, h, w, colors, duration_transition, overall_duration, synchronized=None):
        if colors[:-1]!=colors[0]:
            colors = deepcopy(colors)
            colors.append(colors[0])
        t0 = time.time()
        while time.time()-t0 < overall_duration:
            self.group_fade_colors(h, w, colors, duration_transition, synchronized)



    def all_color_wheel(self, overall_time, fading=True):
        # 6 transitions + 2 fades in overall_time seconds
        num_transitions = 8 if fading else 6
        if fading:
            self.group_fade_up(float(overall_time)/num_transitions, "red")
        color = Arbapixel("red")
        self.model.set_all(color)
        wheel = [(0, 1, 0), (-1, 0, 0), (0, 0, 1), (0, -1, 0), (1, 0, 0), (0, 0, -1)]
        for w in wheel:
            for i in range(255):
                color.set_color(color.r + w[0], color.g + w[1], color.b + w[2])
                self.model.set_all(color)
                time.sleep(float(overall_time)/num_transitions/256.)
        if fading:
            self.group_fade_down(float(overall_time)/num_transitions, "red")

    def living_pixels(self, colors, synchronized=None):
        threads = []
        for w in range(self.width):
            for h in range(self.height):
                speed = random.randrange(350, 700)/100.
                t = Thread(None, self.group_fade_colors_loop, None, (h, w, colors, speed, 60, synchronized))
                threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        t.s

    def run(self):
        time.sleep(2)
        #self.all_color_wheel(5)
        #for combination in list(product([0, 128, 255], repeat=3))[1:]:
        #    self.all_fade_up_down("all", 0.7, combination)
        self.living_pixels(['slateblue', 'gold', 'deeppink', 'peru', 'yellowgreen'])
        time.sleep(1)

# Actual call starting the program
def main():
    e = ColorDemo(width = 10, height = 15, max_rate=15)
    e.run()
    e.close("end")

import cProfile
cProfile.run('main()')