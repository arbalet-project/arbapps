#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Arbamodel - Arbalet State

    Store a snapshot of the table state

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

from Arbapixel import *
import copy

class Arbamodel(object):
    # line, column
    def __init__(self, width, height, *color):
        self.height = height
        self.width = width
        self.state = [[Arbapixel(*color) if len(color)>0 else Arbapixel(0, 0, 0, 0) for j in range(width)] for i in range(height)]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_pixel(self, h, w):
        return self.state[h][w]

    def set_pixel(self, h, w, *color):
        self.state[h][w] = Arbapixel(*color)

    def set_all(self, *color):
        for w in range(self.width):
            for h in range(self.height):
                self.state[h][w] = Arbapixel(*color)

    def __add__(self, other):
        model = Arbamodel(self.width, self.height)
        for w in range(self.width):
            for h in range(self.height):
                model.state[h][w] = self.state[h][w] + other.state[h][w]
        return model

    def __eq__(self, other):
        for w in range(self.width):
            for h in range(self.height):
                if self.state[h][w] != other.state[h][w]:
                    return False
        return True

    def __sub__(self, other):
        model = Arbamodel(self.width, self.height)
        for w in range(self.width):
            for h in range(self.height):
                model.state[h][w] = self.state[h][w] - other.state[h][w]
        return model

    def __repr__(self):
        return self.state

    def __str__(self):
        return str(self.state)

    def __mul__(self, m):
        model = Arbamodel()
        for w in range(self.width):
            for h in range(self.height):
                model.state[h][w] = self.state[h][w]*m
        return model

if __name__ == '__main__':
    s1 = Arbamodel(100, 50, 255, 0, 0, 0)
    s2 = Arbamodel(100, 50, 0, 0, 255, 128)
    print s1+s2
