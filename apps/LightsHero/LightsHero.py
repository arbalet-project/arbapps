#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Lights Hero - Guitar Hero/Frets-on-fire like game

    In this app, a lane is one of the 5 colored lanes (vertical), a line
    corresponds to a specific timestamp, an intersection between a line and
    a lane is a cell that can have different states: background, marker,
    active, bump.

    Class SongReader reads a song in the fretsonfire format line-by-line.
    Class LightsHero is the main controller
    Class Renderer renders the grid on the table

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
from SongReader import SongReader
import pygame
from arbasdk import Arbamodel, Arbapp, Arbapixel


class Renderer(Thread):
    """
    This thread renders the game on Arbalet
    """
    def __init__(self, rate, model, grid, table_height, num_lanes, table_width):
        Thread.__init__(self)
        self.setDaemon(True)
        self.rate = rate
        self.model = model
        self.grid = grid
        self.height = table_height
        self.width = table_width
        self.num_lanes = num_lanes
        self.colors = ['darkgreen', 'darkred', 'gold', 'navy', 'purple']
        self.intensity = {'background': 0.01, 'marker': 0.05, 'active': 0.2, 'bump': 1.0}
        self.running = True


    def stop(self):
        self.running = False

    def update_view(self):
        for lane in range(self.num_lanes):
            for chunk_lane in range(self.width/self.num_lanes):
                w = lane*self.width/self.num_lanes + chunk_lane
                for h in range(self.height):
                    self.model.set_pixel(h, w, Arbapixel(self.colors[lane])*self.intensity[self.grid[h][lane]])

    def run(self):
        while self.running:
            self.update_view()
            time.sleep(1./self.rate)

class LightsHero(Arbapp):
    def __init__(self, width, height, num_lanes, path, level):
        Arbapp.__init__(self, width, height)
        self.num_lanes = num_lanes
        self.grid = [['background']*num_lanes for h in range(height)]
        model = Arbamodel(width, height, 'black')
        self.set_model(model)
        self.renderer = Renderer(30, model, self.grid, height, num_lanes, width)
        self.reader = SongReader(path, num_lanes, level)
        self.score = 0
        self.speed = 10. # Speed of game in Hertz
        self.playing = True
        pygame.init()
        pygame.joystick.init()
        self.renderer.start()

    def next_line(self):
        # Delete the last but one line (very last line is reserved for buttons)
        for l in range(self.height-1, 0, -1):
            for w in range(self.num_lanes):
                self.grid[l][w] = self.grid[l-1][w]

        new_line = self.reader.read()
        for lane in range(self.num_lanes):
            self.grid[0][lane] = new_line[lane]

    def run(self):
        while self.playing:
            self.next_line()
            time.sleep(0.1)
        self.renderer.stop()

t = LightsHero(width = 10, height = 15, num_lanes=5, path='./songs/Feelings', level=('difficult'))
t.start()
