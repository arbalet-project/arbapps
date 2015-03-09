#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Arbasim - Arbalet Simulator

    Simulate an Arbalet table

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

class Arbapixel(object):

    colors = {'black': [0, 0, 0],
              'white' : [255,255,255],
              'blue': [0,0,255],
              'green' : [0,255,0],
              'red' : [255,0,0],
              'grey' : [171,171,171],
              'darkgrey' : [85,85,85]}

    def __init__(self):
        self.setColor('white')

    def __init__(self, r, g=None, b=None):
        if g!=None and b!=None:
            self.setColor([r, g, b])
        else:
            self.setColor(r)

    def setColor(self, color):
        if isinstance(color, str):
            self.setColor(self.colors[color.lower()])
        elif isinstance(color, tuple):
            self.setColor(list(color))
        elif isinstance(color, list) and len(color)==3:
            self.pixel = color
        else:
            raise Exception("[setColor] Unexpected color type")

    def getColor(self):
        return self.pixel

    def isColor(self, color):
        if isinstance(color, list):
            return self.pixel==color
        elif isinstance(color, str):
            return self.pixel==self.colors[color]
        else:
            return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        try:
            return [key for key in self.colors.keys() if self.isColor(key)][0]
        except:
            return self.pixel

if __name__ == '__main__':
    black1 = Arbapixel('red')
    black2 = Arbapixel(255, 0, 0)
    print "{} = {} ? {}".format(black1.getColor(), black2.getColor(), black1.isColor(black2.getColor()))

