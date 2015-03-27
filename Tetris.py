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
from arbasdk import Arbamodel, Arbapp

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

    def update_position(self, x, y):
        self.position[0] += x
        self.position[1] += y

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
        self.playing = True
        self.tetromino = None
        pygame.joystick.init()

    def process_events(self):
        """
        Sleep until the next step and process user events: game commands + exit
        :return: True if user asked to abort sleeping (accelerate or quit), False otherwise
        """
        self.new_event = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                return True
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            if event.type == pygame.JOYBUTTONDOWN:
                self.tetromino.rotate()
                self.new_event = True

        if pygame.joystick.get_count()>0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            hat = joystick.get_hat(0)

        if hat[0]!=0 or hat[1]!=0:
            self.new_event = True

        if self.new_event:
            self.tetromino.update_position(0, hat[0])
            self.old_grid_empty = deepcopy(self.grid)
            self.draw_tetromino()
            self.old_grid_filled = deepcopy(self.grid)
            self.update_view()
            self.grid = self.old_grid_empty

        return hat[1]!=0   # Return True in case of speed increasing request, False otherwise

    def game_over(self):
        return not self.playing

    def draw_tetromino(self):
        #print "Pasting" if not clear else "Clearing", tetromino.type, "at place", tetromino.position
        for x, z in enumerate(self.tetromino.get_value()):
            for y, v in enumerate(z):
                px = x + self.tetromino.position[0] # x-position of the pixel we are about to draw
                py = y + self.tetromino.position[1] # y-position of the pixel we are about to draw

                before_world = px<0
                in_world = not before_world and px<self.height
                touchdown = not before_world and not in_world or in_world and self.grid[px][py]>0 and v

                if touchdown:
                    self.touchdown = True
                    self.tetromino.falldown(True)
                    return
                elif in_world and self.grid[px][py]==0: # Don't overwrite a previous tetro and
                    self.grid[px][py] = v

    def wait_for_timeout_or_event(self):
        t0 = time.time()
        while time.time()-t0 < 1./self.speed:
            time.sleep(0.075)
            if self.process_events():
                return


    def new_tetromino(self):
        self.touchdown = False
        self.tetromino = Tetromino(0, self.width/2)
        while not self.touchdown:
            self.old_grid_empty = deepcopy(self.grid)
            self.draw_tetromino()
            if self.touchdown:
                self.grid = self.old_grid_filled
            else:
                self.old_grid_filled = deepcopy(self.grid)
                self.update_view()
                self.grid = self.old_grid_empty
                self.tetromino.falldown()
            self.wait_for_timeout_or_event()


    def update_view(self):
        for w in range(self.width):
            for h in range(self.height):
                self.model.set_pixel(h, w, Tetromino.colors[self.grid[h][w]])

    def run(self):

        while not self.game_over():
            if not False:#self.pressed_keys[pygame.K_ESCAPE]:
                self.new_tetromino()
                print "TOUCHDOWN"
                #time.sleep(1)
            else:
                break

t = Tetris(width = 10, height = 15)
t.start()

