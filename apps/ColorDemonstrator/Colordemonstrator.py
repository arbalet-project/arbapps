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
from threading import Thread

class LivingPixel(Thread):
    def __init__(self, h, w, model, colors, max_rate, duration):
        Thread.__init__(self)
        self.h = h
        self.w = w
        self.model = model
        self.max_rate = max_rate
        self.duration = duration
        self.colors = colors
        self.running = True

    def fade_colors(self, h, w, duration):
        num_steps = int(self.max_rate*duration)
        pairs = zip(self.colors, self.colors[1:])
        for color1, color2 in pairs:
            for v in range(num_steps):
                col = Arbapixel(color1)*((num_steps-v)/float(num_steps)) + Arbapixel(color2)*(v/float(num_steps))
                self.model.set_pixel(h, w, col)
                time.sleep(duration/float(num_steps))
                if not self.running: return

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            self.fade_colors(self.h, self.w, self.duration)

class ColorDemo(Arbapp):
    def __init__(self, width, height, colors, dur_min, dur_max, max_rate = 10):
        Arbapp.__init__(self, width, height)
        self.max_rate = max_rate  # Max refreshing rate in Hz
        self.durations = [dur_min, dur_max]
        self.threads = []
        if colors[:-1]!=colors[0]:
            colors.append(colors[0])
        self.colors = colors

    def run(self):
        for w in range(self.width):
            for h in range(self.height):
                duration = random.randrange(self.durations[0]*10, self.durations[1]*10)/10.
                self.threads.append(LivingPixel(h, w, self.model, self.colors, self.max_rate, duration))
        for t in self.threads:
            t.start()
        raw_input('Press enter to kill Color Demonstrator')
        for t in self.threads:
            t.running = False

e = ColorDemo(width = 10, height = 15, colors=['navy', 'gold', 'deeppink', 'yellowgreen', 'purple'],
              dur_min=10, dur_max=60)
e.run()
e.close("end")