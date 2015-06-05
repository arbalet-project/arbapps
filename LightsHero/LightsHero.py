#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Lights Hero - Guitar Hero/Frets-on-fire like game

    In this app, a lane is one of the 5 colored lanes (vertical), a line
    corresponds to a specific timestamp, an intersection between a line and
    a lane is a cell that can have different states: background, marker,
    active, bump.

    Class SongReader reads a song in the fretsonfire format line-by-line.
    Class LightsHero is the main controller
    Class Renderer renders the grid on the table

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import random
from threading import Thread, Lock
from SongReader import SongReader
from SoundManager import SoundManager
from UserHits import UserHits
import pygame
from arbasdk import Arbapp, Arbapixel, Rate


class Renderer(Thread):
    """
    This thread renders the game on Arbalet
    """
    def __init__(self, rate, model, grid, grid_lock, bottom_bar, table_height, num_lanes, table_width):
        Thread.__init__(self)
        self.setDaemon(True)
        self.rate = Rate(rate)
        self.model = model
        self.grid = grid
        self.grid_lock = grid_lock
        self.bar = bottom_bar
        self.height = table_height
        self.width = table_width
        self.num_lanes = num_lanes
        self.colors = ['darkgreen', 'darkred', 'orange', 'navy', 'deeppink']
        self.intensity = {'background': 0.05, 'marker': 0.03, 'active': 0.9}
        self.running = True

    def stop(self):
        self.running = False

    def update_view(self, flash_color):
        with self.grid_lock:
            # Big area of coming notes
            for lane in range(self.num_lanes):
                for chunk_lane in range(self.width/self.num_lanes):
                    w = lane*self.width/self.num_lanes + chunk_lane
                    for h in range(self.height-1): # -1 in order not to update the bottom bar
                        if self.grid[h][lane]=='bump':
                            color = Arbapixel((100, 100, 100)) + Arbapixel(self.colors[lane])
                        else:
                            color = Arbapixel(self.colors[lane])*self.intensity[self.grid[h][lane]]
                        self.model.set_pixel(h, w, color)

            # Bottom bar of present notes
            for lane in range(self.num_lanes):
                if self.bar[lane]=='hit' and flash_color or self.bar[lane]=='idle':
                    # To make the note "burning" we alternate white/color when self.colors[lane]=='hit'
                    color = self.colors[lane]
                else:
                    color = 'white'
                for chunk_lane in range(self.width/self.num_lanes):
                    w = lane*self.width/self.num_lanes + chunk_lane
                    self.model.set_pixel(self.height-1, w, color)



    def run(self):
        flash_color = False # Boolean giving a "burning" impression
        while self.running:
            self.update_view(flash_color)
            self.rate.sleep()
            flash_color = not flash_color

class LightsHero(Arbapp):
    def __init__(self, num_lanes, path, level, speed):
        Arbapp.__init__(self)
        self.num_lanes = num_lanes
        self.score = 0
        self.speed = float(speed)
        self.rate = Rate(self.speed)
        self.grid = [['background']*num_lanes for h in range(self.height)] # The coming notes (last line included even if it will overwritten by the bottom bar)
        self.grid_lock = Lock()
        self.bar = ['idle']*num_lanes # The bottom bar, idle = not pressed, hit = pressed during a note, pressed = pressed outside a note
        pygame.init()

        # Threads creation and starting
        self.renderer = Renderer(50, self.model, self.grid, self.grid_lock, self.bar, self.height, num_lanes, self.width)
        self.reader = SongReader(path, num_lanes, level, speed)
        self.sound = SoundManager(path, (self.height-2)/self.speed)
        self.hits = UserHits()
        self.renderer.start()
        self.hits.start()

    def next_line(self):
        with self.grid_lock:
            # Delete the last line leaving the grid
            # Note : The bottom bar will overwrite the last line but the latter needs to be kept to draw the bottom bar
            for l in range(self.height-1, 0, -1):
                for w in range(self.num_lanes):
                    self.grid[l][w] = self.grid[l-1][w]

            # Ask for a new line to the song reader and fill the top of the grid with it
            new_line = self.reader.read()
            for lane in range(self.num_lanes):
                self.grid[0][lane] = new_line[lane]


    def user_hits(self):
        """
        Read user inputs and update the bottom bar consequently
        """
        with self.grid_lock:
            for lane in range(self.num_lanes):
                must_press = self.grid[self.height-1][lane] == 'active' or self.grid[self.height-1][lane] == 'bump'
                pressed = self.hits.get_pressed(lane)
                if must_press and pressed:
                    status = 'hit'
                elif pressed:
                    status = 'pressed'
                else:
                    status = 'idle'
                self.bar[lane] = status

    def run(self):
        self.sound.start()
        countdown = self.height # Countdown triggered after Midi's EOF
        while countdown>0:
            self.next_line()
            self.user_hits()
            self.rate.sleep()
            if self.reader.eof:
                countdown -= 1
        self.renderer.stop()
        self.hits.stop()

t = LightsHero(num_lanes=5, path='./songs/Feelings', level='expert', speed=15)
t.start()
