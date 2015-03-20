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
from arbasdk.Arbamodel import Arbamodel
from arbasdk.Arbapp import Arbapp
from arbasdk.Arbapixel import Arbapixel
from itertools import product
from threading import Thread, Semaphore
from copy import deepcopy

class ColorDemo(Arbapp):

    def __init__(self, width, height):
        Arbapp.__init__(self, width, height)
        self.model = Arbamodel(self.width, self.height)
        self.set_model(self.model)
        self.max_rate = 100  # Max refreshing rate in Hz
        self.semaphore = Semaphore(self.width*self.height)  # Thread synchronization

    def group_fade_colors(self, group_name, colors, duration, synchronized=None):
        num_steps = min(int(round(self.max_rate*duration, 0)), 256)
        #print num_steps, "steps for", duration, "sec"
        pairs = zip(colors, colors[1:])
        for color1, color2 in pairs:
            if synchronized:
                synchronized.acquire()
            for v in range(num_steps):
                col = Arbapixel(color1)*((num_steps-v)/float(num_steps)) + Arbapixel(color2)*(v/float(num_steps))
                self.model.set_group(group_name, col)
                time.sleep(duration/float(num_steps))
            #print "# to", color2

    def group_fade_colors_loop(self, group_name, colors, duration_transition, overall_duration, synchronized=None):
        if colors[:-1]!=colors[0]:
            colors = deepcopy(colors)
            colors.append(colors[0])
        t0 = time.time()
        while time.time()-t0 < overall_duration:
            self.group_fade_colors(group_name, colors, duration_transition, synchronized)


# DEPRECATED


    def group_fade_up(self, group_name, duration, color):
        num_steps = min(int(round(self.max_rate*duration, 0)), 256)
        #print num_steps, "steps for", duration, "sec"
        for v in range(num_steps):
            self.model.set_group(group_name, Arbapixel(color)*(v/float(num_steps)))
            time.sleep(duration/float(num_steps))

    def group_fade_down(self, group_name, duration, color):
        num_steps = min(int(round(self.max_rate*duration, 0)), 256)
        #print num_steps, "steps for", duration, "sec"
        for v in range(num_steps-1, -1, -1):
            self.model.set_group(group_name, Arbapixel(color)*(v/float(num_steps)))
            time.sleep(duration/float(num_steps))

    def group_fade_up_down(self, group_name, overall_time, color, time_fade=0.1):
        self.group_fade_up(group_name, time_fade, color)
        time.sleep(overall_time-2*time_fade)
        self.group_fade_down(group_name, time_fade, color)

    def group_fade_loop(self, group_name, overall_time, loop_time, color, fade_time):
        t0 = time.time()
        while time.time()-t0<overall_time:
            self.group_fade_up_down(group_name, loop_time, color, fade_time)













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

    def random_flashing_pixels(self, colors):
        all_pixels = set(self.model.get_all_combinations())
        self.set_model(self.model)
        for color in colors:
            group = random.sample(all_pixels, self.width*self.height/len(colors))
            all_pixels = all_pixels.difference(group)
            self.model.group_pixels(group, "group_"+color, color)

        threads = []
        for color in colors:
            ot = random.randrange(1,3)
            t = Thread(None, self.group_fade_loop, None, ("group_"+color, 10, ot, color, 0.45))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()


    def living_pixels(self, colors, synchronized=None):
        for w in range(self.width):
            for h in range(self.height):
                color = random.choice(colors)
                self.model.group_pixels([[h, w]], str(h)+'-'+str(w), 'black')
        threads = []
        for w in range(self.width):
            for h in range(self.height):
                color = random.choice(colors)
                speed = random.randrange(350, 700)/100.
                t = Thread(None, self.group_fade_colors_loop, None, (str(h)+'-'+str(w), colors, speed, 60, synchronized))
                t.start()
                threads.append(t)
        for t in threads:
            t.join()

    def run(self):
        #self.all_color_wheel(5)
        #for combination in list(product([0, 128, 255], repeat=3))[1:]:
        #    self.all_fade_up_down("all", 0.7, combination)
        self.living_pixels(['slateblue', 'gold', 'deeppink', 'peru', 'yellowgreen'])
        time.sleep(1)

# Actual call starting the program
e = ColorDemo(width = 10, height = 15)
e.run()
e.close("end")