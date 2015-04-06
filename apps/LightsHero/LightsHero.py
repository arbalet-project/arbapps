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
from SoundManager import SoundManager
import pygame
from arbasdk import Arbamodel, Arbapp, Arbapixel


class Renderer(Thread):
    """
    This thread renders the game on Arbalet
    """
    def __init__(self, rate, model, grid, bottom_bar, table_height, num_lanes, table_width):
        Thread.__init__(self)
        self.setDaemon(True)
        self.rate = rate
        self.model = model
        self.grid = grid
        self.bar = bottom_bar
        self.height = table_height
        self.width = table_width
        self.num_lanes = num_lanes
        self.colors = ['darkgreen', 'darkred', 'gold', 'navy', 'purple']
        self.intensity = {'background': 0.01, 'marker': 0.05, 'active': 0.9, 'bump': 1.0} # TODO bump sometimes raises KeyError
        self.running = True

    def stop(self):
        self.running = False

    def update_view(self, flash_color):
        # Big area of coming notes
        for lane in range(self.num_lanes):
            for chunk_lane in range(self.width/self.num_lanes):
                w = lane*self.width/self.num_lanes + chunk_lane
                for h in range(self.height-1): # -1 in order not to update the bottom bar
                    if self.grid[h][lane]=='bump':
                        color = Arbapixel(100, 100, 100) + Arbapixel(self.colors[lane])
                    else:
                        color = Arbapixel(self.colors[lane])*self.intensity[self.grid[h][lane]]
                    self.model.set_pixel(h, w, color)

        # Bottom bar of present notes
        for lane in range(self.num_lanes):
            color = self.colors[lane] if flash_color or not self.bar[lane] else 'white' # To make the note "burning" we alternate white/color
            for chunk_lane in range(self.width/self.num_lanes):
                w = lane*self.width/self.num_lanes + chunk_lane
                self.model.set_pixel(self.height-1, w, color)


    def run(self):
        flash_color = False # Boolean giving a "burning" impression
        while self.running:
            self.update_view(flash_color)
            time.sleep(1./self.rate)
            flash_color = not flash_color

class LightsHero(Arbapp):
    def __init__(self, width, height, num_lanes, path, level, speed):
        Arbapp.__init__(self, width, height)
        self.num_lanes = num_lanes
        self.score = 0
        self.speed = float(speed)
        self.grid = [['background']*num_lanes for h in range(height)] # The coming notes (last line included even if it will overwritten by the bottom bar)
        self.bar = [False]*num_lanes # The bottom bar, False means "idle", True means "being hit"
        model = Arbamodel(width, height, 'black')
        self.set_model(model)
        self.renderer = Renderer(40, model, self.grid, self.bar, height, num_lanes, width)
        self.reader = SongReader(path, num_lanes, level)
        self.sound = SoundManager(path, self.height/self.speed)
        self.playing = True
        pygame.init()
        pygame.joystick.init()
        self.renderer.start()

    def next_line(self):
        # Delete the last line leaving the grid
        # Note : The bottom bar will overwrite the last line but the latter needs to be kept to draw the bottom bar
        for l in range(self.height-1, 0, -1):
            for w in range(self.num_lanes):
                self.grid[l][w] = self.grid[l-1][w]

        # Ask for a new line to the song reader and fill the top of the grid with it
        new_line = self.reader.read()
        for lane in range(self.num_lanes):
            self.grid[0][lane] = new_line[lane]

    def correct_hit(self):
        """
        Return True if user has hit the good key within the permitted time
        """
        raise NotImplementedError("")

    def run(self):
        self.sound.start()
        while self.playing:
            self.next_line()

            time.sleep(1./self.speed)
        self.renderer.stop()

t = LightsHero(width = 10, height = 15, num_lanes=5, path='./songs/Feelings', level='expert', speed=15)
t.start()
