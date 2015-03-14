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

class Arbapixel(object):

    def __init__(self, r, g=None, b=None):

        if g!=None and b!=None:
            self.setColor([self.__limit(r), self.__limit(g), self.__limit(b)])
        else:
            self.setColor(r)

    def __limit(self, v):
        """
        Limitator avoiding overflows and underflows
        """
        return int(max(0, min(255, v)))

    def setColor(self, color):
        if isinstance(color, str):
            self.setColor(Color(color)[:3])
        elif isinstance(color, tuple):
            self.setColor(list(color))
        elif isinstance(color, list) and len(color)==3:
            self.pixel = color
        elif isinstance(color, Arbapixel):
            self.pixel = color.getColor()
        else:
            raise Exception("[setColor] Unexpected color type {}".format(type(color)))

    def getColor(self):
        return self.pixel

    def __add__(self, c):
        return Arbapixel(self.__limit(self.pixel[0]+c.pixel[0]),
                         self.__limit(self.pixel[1]+c.pixel[1]),
                         self.__limit(self.pixel[2]+c.pixel[2]))
    def __sub__(self, c):
        return Arbapixel(self.__limit(self.pixel[0]-c.pixel[0]),
                         self.__limit(self.pixel[1]-c.pixel[1]),
                         self.__limit(self.pixel[2]-c.pixel[2]))
    def __mul__(self, m):
        return Arbapixel(self.__limit(self.pixel[0]*m),
                         self.__limit(self.pixel[1]*m),
                         self.__limit(self.pixel[2]*m))

    def __div__(self, m):
        return Arbapixel(self.__limit(self.pixel[0]/float(m)),
                         self.__limit(self.pixel[1]/float(m)),
                         self.__limit(self.pixel[2]/float(m)))

    def __eq__(self, c):
        return self.pixel[0]==c.getColor()[0] and self.pixel[1]==c.getColor()[1] and self.pixel[2]==c.getColor()[2]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Arbapixel(" + str(self.pixel[0]) + ', ' + str(self.pixel[1]) + ', ' + str(self.pixel[2]) + ')'

if __name__ == '__main__':
    black1 = Arbapixel('red')
    black2 = Arbapixel(255, 0, 0)
    print "{} = {} ? {}".format(black1.getColor(), black2.getColor(), black1 == black2)

    white1 = Arbapixel('white')
    white2 = Arbapixel('red') + Arbapixel('green') + Arbapixel('blue')
    white3 = Arbapixel(1, 1, 1)*255
    print "{} = {} = {} ? {}".format(white1.getColor(), white2.getColor(), white3.getColor(),
                                     white1 == white2 and white2==white3)
