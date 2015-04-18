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
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__))+'/../../src/')
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
             'l': [[5, 0],
                   [5, 0],
                   [5, 5]]}
    colors = ['black', 'cyan', 'green', 'deeppink', 'yellow', 'orangered']

    def __init__(self, px, py, height, width):
        self.type = random.choice(self.types.keys())
        self.rotated = 0
        self.position = [px-len(self.get_value())+1, py]
        self.height = height
        self.width = width

    def update_position(self, x, y):
        self.position[0] = max(min(self.position[0]+x, self.height-1), 0)
        self.position[1] = max(min(self.position[1]+y, self.width-len(self.get_value()[0])), 0)

    def rotate(self):
        # TODO: In case of LR touchdown, rotation is authorized (but shouldn't) but blocks the tetro
        # TODO: replace by a drawing simulation to see if rotation is authorized...
        if self.position[1]+len(self.get_value())<self.width:
            self.rotated += 1

    def falldown(self):
        self.position = [self.position[0]+1, self.position[1]]

    def get_value(self):
        return numpy.rot90(numpy.array(self.types[self.type], dtype=int), self.rotated)


class Tetris(Arbapp):

    def __init__(self, width, height):
        Arbapp.__init__(self, width, height)
        self.grid = numpy.zeros([height, width], dtype=int)
        self.old_grid = deepcopy(self.grid)
        self.model = Arbamodel(width, height)
        self.set_model(self.model)
        self.speed = 2 # Speed of tetromino fall in Hertz
        self.last_event = 0
        self.score = 0
        self.playing = True
        self.tetromino = None
        pygame.init()
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

        if (hat[0]!=0 or hat[1]!=0 or self.new_event) and time.time()-self.last_event>0.08:
            self.new_event = True
            self.last_event = time.time()
        else:
            self.new_event = False

        if self.new_event:

            old_position = deepcopy(self.tetromino.position)
            self.tetromino.update_position(0, hat[0])
            self.old_grid_empty = deepcopy(self.grid)
            self.draw_tetromino()
            if self.touchdown and hat[0]!=0:            # Touch left/right
                self.tetromino.position = old_position  # We cancel the last move left/right
                self.grid = self.old_grid_empty         # We remove the collisionning tetro
                #self.draw_tetromino()                   # And redraw
                self.touchdown = False                  # This is not a real touchdown, cancel it
            elif self.touchdown:                        # Touch down
                self.grid = self.old_grid_filled        # We restore the last pose of the tetro before touching down
            else:
                self.old_grid_filled = deepcopy(self.grid)
                self.update_view()
                self.grid = self.old_grid_empty
        return self.new_event and hat[1]!=0   # Return True in case of speed increasing request, False otherwise

    def game_over(self):
        return not self.playing

    def draw_tetromino(self):
        self.touchdown = False
        for x, z in enumerate(self.tetromino.get_value()):
            for y, v in enumerate(z):
                px = x + self.tetromino.position[0] # x-position of the pixel we are about to draw
                py = y + self.tetromino.position[1] # y-position of the pixel we are about to draw

                before_world = px<0
                in_world = not before_world and px<self.height
                touchdown = not before_world and not in_world or in_world and self.grid[px][py]>0 and v

                if touchdown:
                    self.touchdown = True
                    return
                elif in_world and self.grid[px][py]==0: # Don't overwrite a previous tetro and
                    self.grid[px][py] = v

    def wait_for_timeout_or_event(self, allow_events=True):
        t0 = time.time()
        while time.time()-t0 < 1./self.speed:
            time.sleep(0.001)
            if allow_events and self.process_events():
                return

    def check_and_delete_full_lines(self):
        """
        Browse the grid and check for full lines. If lines are found they are deleted.
        :return: The number of deleted lines
        """
        def __delete_line(line):
            for l in range(line, 1, -1):
                for w in range(self.width):
                    self.grid[l][w] = self.grid[l-1][w]

        lines = []
        for h in range(self.height):
            full = True
            for w in range(self.width):
                if self.grid[h][w]==0:
                    full = False
                    break
            if full:
                __delete_line(h)
                lines.append(h)
        return len(lines)


    def new_tetromino(self):
        """
        Brings a new tetromino in the scene and make it falling until touchdown
        :return: The number of steps before touchdown (1 step only = gameover)
        """
        self.touchdown = False
        self.tetromino = Tetromino(0, self.width/2, self.height, self.width)
        steps = 0
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
            self.wait_for_timeout_or_event(not self.touchdown)  # In case of touchdown do not modify this tetro again
                                                                # so we disable events
            steps += 1
        return steps


    def update_view(self):
        for w in range(self.width):
            for h in range(self.height):
                self.model.set_pixel(h, w, Tetromino.colors[self.grid[h][w]])

    def run(self):
        while self.playing:
            if self.new_tetromino()==1:
                print "GAME OVER"
                print "You scored", self.score
                break
            else:
                time.sleep(0.5)
                lines = self.check_and_delete_full_lines()
                self.score += lines*lines


t = Tetris(width = 10, height = 15)
t.start()

