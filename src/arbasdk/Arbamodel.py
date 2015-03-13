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
    def __init__(self, width, height, color=None):
        self.height = height
        self.width = width
        self.state = [[Arbapixel(color if color else 'white') for j in range(width)] for i in range(height)]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_pixel(self, h, w):
        return self.state[h][w]

    def set_pixel(self, h, w, color):
        self.state[h][w].setColor(color)

    def set_all(self, color):
        for w in range(self.width):
            for h in range(self.height):
                self.state[h][w].setColor(color)

if __name__ == '__main__':
    s1 = Arbamodel(100, 50)
    s2 = Arbamodel(100, 50)
    s1.set_pixel(10, 10, 'white')
    s2.set_pixel(10, 10, [255, 255, 255])
    s3 = copy.deepcopy(s1)
    print s1==s3
