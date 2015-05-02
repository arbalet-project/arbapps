#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Arbasim - Arbalet Simulator Kivy version

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
from kivy.interactive import InteractiveLauncher
from kivy.app import App
from kivy.uix.layout import Layout
from kivy.graphics import Rectangle, Color
from threading import Lock

__all__ = ['Arbasim']

class Arbagrid(Layout):
    def __init__(self, arbalet_width, arbalet_height, sim_width, sim_height):
        """
        Arbasim constructor: launches the simulation
        Simulate a "arbalet_width x arbalet_height px" table rendered in a "sim_width x sim_height" window
        :param arbalet_width: Number of pixels of Arbalet in width
        :param arbalet_height: Number of pixels of Arbalet in height
        :param sim_width:
        :param sim_height:
        :param rate: Refresh rate in Hertz
        :return:
        """
        super(Arbagrid, self).__init__()
        self.arbalet_width = arbalet_width
        self.arbalet_height = arbalet_height
        self.sim_width = sim_width
        self.sim_height = sim_height
        self.border = 1

    def paint(self, model):
        with self.canvas:
            for h in range(self.arbalet_height):
                for w in range(self.arbalet_width):
                    print h, w
                    color = model.get_pixel(h, w)
                    Color(color.r, color.g, color.b)
                    Rectangle(pos=(w*self.sim_width, h*self.sim_height),
                              size=(self.sim_width-self.border, self.sim_height-self.border))


class ArbasimApp(App):
    def __init__(self, *args):
        super(ArbasimApp, self).__init__()
        self.grid = Arbagrid(*args)

    def set_model(self, model):
        self.grid.paint(model)

    def build(self):
        return self.grid


class Arbasim():
    def __init__(self, arbalet_width, arbalet_height, sim_width, sim_height):
        self._app = ArbasimApp(arbalet_width, arbalet_height, sim_width, sim_height)
        self._launcher = InteractiveLauncher(self._app)
        self.start()

    def start(self):
        self._launcher.run()

    def set_model(self, model):
        self._app.set_model(model)

    def close(self, reason='unknown'):
        self._launcher.stop()

