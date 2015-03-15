#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Arbapixel - Arbalet Pixel

    Represent a rgb-colored pixel in an Arbalet table

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
from pygame.color import Color

# This class has a hack to inherit from pygame.Color with getattr since its C
# implementation does not allow to inherit properly
class Arbapixel(object):

    def __init__(self, *args):
        self.__pygame_color = Color(*args)

    def __limit(self, v):
        """
        Limitator avoiding overflows and underflows
        """
        return int(max(0, min(255, v)))

    def __set__(self, instance, value):
        self.__pygame_color = value

    def __getattr__(self, name):
        return getattr(self.__pygame_color, name)

    def __add__(self, other):
        return Arbapixel(self.__limit(self.r+other.r),
                         self.__limit(self.g+other.g),
                         self.__limit(self.b+other.b),
                         self.__limit(self.a+other.a))

    def __eq__(self, other):
        return self.__pygame_color == other.__pygame_color

    def __sub__(self, other):
        return Arbapixel(self.__limit(self.r-other.r),
                         self.__limit(self.g-other.g),
                         self.__limit(self.b-other.b),
                         self.__limit(self.a-other.a))

    def __repr__(self):
        return self.__pygame_color.__repr__()

    def __str__(self):
        return self.__pygame_color.__str__()

    def __mul__(self, m):
        return Arbapixel(self.__limit(self.r*m),
                         self.__limit(self.g*m),
                         self.__limit(self.b*m),
                         self.__limit(self.a*m))

    def get_color(self):
        return self.__pygame_color

if __name__ == '__main__':
    black1 = Arbapixel('red')
    black2 = Arbapixel(255, 0, 0)
    print "{} = {} ? {}".format(black1, black2, black1 == black2)

    white1 = Arbapixel('white')
    white2 = Arbapixel('red') + Arbapixel('green') + Arbapixel('blue')
    white3 = Arbapixel(1, 1, 1)*255
    print "{} = {} = {} ? {}".format(white1, white2, white3, white1 == white2 and white2==white3)
