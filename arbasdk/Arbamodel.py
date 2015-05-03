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

from Arbapixel import Arbapixel
from copy import deepcopy
from itertools import product
from threading import Lock

__all__ = ['Arbamodel']

class Arbamodel(object):
    # line, column
    def __init__(self, width, height, *color):
        self.height = height
        self.width = width

        self.model_lock = Lock()
        self.model = [[Arbapixel(*color) if len(color)>0 else Arbapixel('black') for j in range(width)] for i in range(height)]

        self.groups_lock = Lock()
        self.groups = {}
        self.reverse_groups = [[None for j in range(width)] for i in range(height)]

    def copy(self):
        return deepcopy(self)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_pixel(self, h, w):
        with self.model_lock:
            p = self.model[h][w]
        return p

    def set_pixel(self, h, w, *color):
        with self.model_lock:
            self.model[h][w] = Arbapixel(*color)
        self.delete_from_group([(h, w)])

    def group_pixels(self, pixels, group_name, *color):
        if not (isinstance(pixels, list) or isinstance(pixels, tuple)) and len(pixels)>0 and \
            (isinstance(pixels[0], list) or isinstance(pixels[0], tuple) and len(pixels[0])==2):
            raise Exception("[Arbamodel.create_groupe] Unexpected parameter type {}, must be a list of coordinates".format(type(pixels)))
        try:
            with self.groups_lock:
                h, w = list(self.groups[group_name])[0]
        except KeyError:
            pixel = Arbapixel(*color)
        else:
            with self.model_lock:
                pixel = self.model[h][w]
        with self.model_lock:
            for h,w in pixels:
                self.model[h][w] = pixel

        # Remove pixels from a former group
        self.delete_from_group(pixels)
        with self.groups_lock:
            if not self.groups.has_key(group_name):
                self.groups[group_name] = set()
            self.groups[group_name] = self.groups[group_name].union(map(tuple, pixels))
            for h, w in pixels:
                self.reverse_groups[h][w] = group_name

    def set_group(self, group_name, *color):
        if (not self.groups.has_key(group_name)) and group_name=="all":
            self.group_pixels(self.get_all_combinations(), "all", *color)
        h, w = next(iter(self.groups[group_name])) # raises a StopIteration if group is empty
        with self.model_lock:
            self.model[h][w].set_color(*color)

    def delete_from_group(self, pixels):
        if not (isinstance(pixels, list) or isinstance(pixels, tuple)) and len(pixels)>0 and \
        (isinstance(pixels[0], list) or isinstance(pixels[0], tuple) and len(pixels[0])==2):
            raise Exception("[Arbamodel.delete_from_group] Unexpected parameter type {}, must be a list of coordinates".format(type(pixels)))

        with self.groups_lock:
            for h, w in pixels:
                if self.reverse_groups[h][w]:
                    group_name = self.reverse_groups[h][w]
                    self.groups[group_name].remove((h, w))
                    self.reverse_groups[h][w] = None
                    # If group has no more pixel, delete it
                    if len(self.groups[group_name])==0:
                        self.groups.pop(group_name)
                    # Copy a new instance of this pixel, apart from the group
                    with self.model_lock:
                        self.model[h][w] = deepcopy(self.model[h][w])


    def get_groups(self):
        return self.groups

    def get_all_combinations(self):
        return map(tuple, product(range(self.height), range(self.width)))

    def set_all(self, *color):
        if not self.groups.has_key('all'):
            self.group_pixels(list(product(range(self.height), range(self.width))), "all", *color)
        else:
            with self.model_lock:
                self.model[0][0].set_color(*color)


    def __add__(self, other):
        model = Arbamodel(self.width, self.height)
        for w in range(self.width):
            for h in range(self.height):
                model.model[h][w] = self.model[h][w] + other.state[h][w]
        return model

    def __eq__(self, other):
        for w in range(self.width):
            for h in range(self.height):
                if self.model[h][w] != other.state[h][w]:
                    return False
        return True

    def __sub__(self, other):
        model = Arbamodel(self.width, self.height)
        for w in range(self.width):
            for h in range(self.height):
                model.model[h][w] = self.model[h][w] - other.state[h][w]
        return model

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.model)

    def __mul__(self, m):
        model = Arbamodel()
        for w in range(self.width):
            for h in range(self.height):
                model.model[h][w] = self.model[h][w]*m
        return model

    def to_json(self):
        return [[p.to_json() for p in self.model[num_row]] for num_row, row in enumerate(self.model)]

    def from_json(self, json_model):
        height = len(json_model)
        width = len(json_model[0]) if height>0 else 0
        if height!=self.get_height() or width!=self.get_width():
            raise ValueError("Data received have size [{}, {}] while model expects [{}, {}]".format(height, width, self.get_height(), self.get_width()))
        for w in range(width):             # TODO Find sth more efficient that constructing objects and browsing lists so much
            for h in range(height):
                self.set_pixel(h, w, *json_model[h][w])


if __name__ == '__main__':
    m = Arbamodel(10, 10, 'black')
    m.group_pixels(zip(range(10), range(10)), "my_red_pixels", 'red')
    print m
    m.delete_from_group([[0,0]])
    m.set_group("my_red_pixels", "white")
    print m
