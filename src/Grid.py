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
import pygame

class Grid(object):
    def __init__(self, cell_height,cell_width,num_cells_wide,num_cells_tall, color):
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.num_cells_wide = num_cells_wide
        self.num_cells_tall = num_cells_tall
        self.color = color
        self.height = cell_height * num_cells_tall
        self.width = cell_width  * num_cells_wide
        self.border_thickness = 1

    def render(self, screen, state):
        screen.lock()
        # Draw vertical lines
        for w in range(self.num_cells_wide):
            pygame.draw.line(screen, self.color, (w*self.cell_width, 0), (w*self.cell_width, self.height))
        # Draw horizontal lines
        for h in range(self.num_cells_tall):
            pygame.draw.line(screen, self.color, (0, h*self.cell_height), (self.width, h*self.cell_height), self.border_thickness)
        # Draw pixels
        if state:
            i = 0
            for w in range(state.get_width()):
                for h in range(state.get_height()):
                    i = i+1
                    pixel = state.get_pixel(h, w)
                    screen.fill(pixel.getColor(), pygame.Rect(w*self.cell_width,
                                                              h*self.cell_height,
                                                              self.cell_width-self.border_thickness,
                                                              self.cell_height-self.border_thickness))
        screen.unlock()



