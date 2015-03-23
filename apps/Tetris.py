#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Tetris game

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
import sys
sys.path.append('../src/')
import time
import random
import numpy
from copy import deepcopy

import pygame
from arbasdk.Arbamodel import Arbamodel
from arbasdk.Arbapp import Arbapp

class Tetromino(object):
    types = {'i' : [[1],
                    [1],
                    [1],
                    [1]],
             's': [[0, 2],
                   [2, 2],
                   [2, 0]],
             't': [[3, 0],
                   [3, 3],
                   [3, 0]],
             'o': [[4, 4],
                   [4, 4]],
             'l': [[4, 0],
                   [4, 0],
                   [4, 4]]}
    colors = ['black', 'cyan', 'green', 'pink', 'yellow', 'orange']


    def rotate(self):
        self.rotated = not self.rotated

    def falldown(self, cancel=False):
        self.position = [self.position[0]-1 if cancel else self.position[0]+1, self.position[1]]

    def get_value(self):
        if self.rotated:
            return numpy.array(self.types[self.type], dtype=int).transpose()
        else:
            return numpy.array(self.types[self.type], dtype=int)

    def __init__(self, px, py):
        self.type = random.choice(self.types.keys())
        self.rotated = False
        self.position = [px-len(self.get_value())+1, py]

class Tetris(Arbapp):

    def __init__(self, width, height):
        Arbapp.__init__(self, width, height)
        self.grid = numpy.zeros([height, width], dtype=int)
        self.old_grid = deepcopy(self.grid)
        self.model = Arbamodel(width, height)
        self.set_model(self.model)
        self.speed = 2 # Speed of tetromino fall in Hertz

    def game_over(self):
        return False

    def draw_tetromino(self, tetromino):
        #print "Pasting" if not clear else "Clearing", tetromino.type, "at place", tetromino.position
        for x, z in enumerate(tetromino.get_value()):
            for y, v in enumerate(z):
                px = x + tetromino.position[0] # x-position of the pixel we are about to draw
                py = y + tetromino.position[1] # y-position of the pixel we are about to draw

                before_world = px<0
                in_world = not before_world and px<self.height
                touchdown = not before_world and not in_world or in_world and self.grid[px][py]>0 and v

                if touchdown:
                    self.touchdown = True
                    # Restore the old grid before collision
                    self.grid = self.old_grid
                elif in_world and self.grid[px][py]==0: # Don't overwrite a previous tetro and
                    self.grid[px][py] = v




    def new_tetromino(self):
        self.touchdown = False
        tetro = Tetromino(0, self.width/2)
        while not self.touchdown:
            self.old_grid = deepcopy(self.grid)
            self.draw_tetromino(tetro)
            time.sleep(1./self.speed)
            self.update_view()
            if not self.touchdown:
                self.grid = self.old_grid
                tetro.falldown()


    def update_view(self):
        for w in range(self.width):
            for h in range(self.height):
                self.model.set_pixel(h, w, Tetromino.colors[self.grid[h][w]])

    def run(self):

        while not self.game_over():
            if not False:#self.pressed_keys[pygame.K_ESCAPE]:
                self.new_tetromino()
                print "TOUCHDOWN"
                time.sleep(1)
            else:
                break


# Actual call starting the program
t = Tetris(width = 10, height = 15)
t.start()