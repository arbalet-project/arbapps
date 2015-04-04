#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Lights Hero - Guitar Hero/Frets-on-fire like game

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
from copy import deepcopy
import random
from threading import Thread
import pygame
from arbasdk import Arbamodel, Arbapp, Arbapixel

class Renderer(Thread):
    """
    This thread renders the game on Arbalet
    """
    def __init__(self, rate, model, grid, table_height, num_lines, table_width):
        Thread.__init__(self)
        self.setDaemon(True)
        self.rate = rate
        self.model = model
        self.grid = grid
        self.height = table_height
        self.width = table_width
        self.num_lines = num_lines
        self.colors = ['darkgreen', 'darkred', 'gold', 'navy', 'purple']
        self.intensity = {'background': 0.01, 'marker': 0.05, 'active': 0.5, 'new': 1.0}
        self.running = True


    def stop(self):
        self.running = False

    def update_view(self):
        for line in range(self.num_lines):
            for chunk_line in range(self.width/self.num_lines):
                w = line*self.width/self.num_lines + chunk_line
                for h in range(self.height):
                    self.model.set_pixel(h, w, Arbapixel(self.colors[line])*self.intensity[self.grid[h][line]])

    def run(self):
        while self.running:
            self.update_view()
            time.sleep(1./self.rate)

class LightsHero(Arbapp):
    def __init__(self, width, height, num_lines):
        Arbapp.__init__(self, width, height)
        self.num_lines = num_lines
        self.grid = [['background']*num_lines for h in range(height)]
        model = Arbamodel(width, height, 'black')
        self.set_model(model)
        self.renderer = Renderer(30, model, self.grid, height, num_lines, width)
        self.score = 0
        self.speed = 10. # Speed of game in Hertz
        self.playing = True
        pygame.init()
        pygame.joystick.init()
        self.renderer.start()

    def next_line(self):
        for h in range(self.height):
            for line in range(self.num_lines):
                self.grid[h][line] = random.choice(['background', 'background', 'background', 'active', 'active', 'marker', 'marker', 'new'])

    def run(self):
        while self.playing:
            self.next_line()
            time.sleep(1./self.speed)
        self.renderer.stop()

t = LightsHero(width = 10, height = 15, num_lines=5)
t.start()

