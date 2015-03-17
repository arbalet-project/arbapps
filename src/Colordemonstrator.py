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
from arbasdk.Arbamodel import Arbamodel
from arbasdk.Arbapp import Arbapp
from arbasdk.Arbapixel import Arbapixel
from itertools import product

class ColorDemo(Arbapp):

    def __init__(self, width, height):
        Arbapp.__init__(self, width, height)
        self.model = Arbamodel(self.width, self.height)
        self.set_model(self.model)
        self.max_rate = 100  # Max refreshing rate in Hz

    def all_fade_up(self, duration, color):
        num_steps = min(int(round(self.max_rate*duration, 0)), 256)
        #print num_steps, "steps for", duration, "sec"
        for v in range(num_steps):
            self.model.set_all(Arbapixel(color)*(v/float(num_steps)))
            time.sleep(duration/float(num_steps))

    def all_fade_down(self, duration, color):
        num_steps = min(int(round(self.max_rate*duration, 0)), 256)
        #print num_steps, "steps for", duration, "sec"
        for v in range(num_steps-1, -1, -1):
            self.model.set_all(Arbapixel(color)*(v/float(num_steps)))
            time.sleep(duration/float(num_steps))

    def all_fade_up_down(self, overall_time, color, time_fade=0.1):
        self.all_fade_up(time_fade, color)
        time.sleep(overall_time-2*time_fade)
        self.all_fade_down(time_fade, color)

    def all_color_wheel(self, overall_time, fading=True):
        # 6 transitions + 2 fades in overall_time seconds
        num_transitions = 8 if fading else 6
        if fading:
            self.all_fade_up(float(overall_time)/num_transitions, "red")
        color = Arbapixel("red")
        self.model.set_all(color)
        wheel = [(0, 1, 0), (-1, 0, 0), (0, 0, 1), (0, -1, 0), (1, 0, 0), (0, 0, -1)]
        for w in wheel:
            for i in range(255):
                color.set_color(color.r + w[0], color.g + w[1], color.b + w[2])
                self.model.set_all(color)
                time.sleep(float(overall_time)/num_transitions/256.)
        if fading:
            self.all_fade_down(float(overall_time)/num_transitions, "red")

    def run(self):
        #self.all_color_wheel(5)
        for combination in list(product([0, 128, 255], repeat=3))[1:]:
            self.all_fade_up_down(0.7, combination)

        time.sleep(0.1)

# Actual call starting the program
e = ColorDemo(width = 10, height = 15)
e.run()
e.close("end")