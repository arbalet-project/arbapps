#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Pong game

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import argparse
import pygame
from arbasdk import Arbapp, Rate
import os, sys

class Pong(Arbapp):
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser)
        self.racket_size = int(self.width/3.)  # Size of the racket in pixels
        self.ball_color = 'deeppink'
        self.racket_color = 'navy'
        self.command = {"left": False, "right": False}  # User asks to move the racket to the left or right
        self.reset_game()

    def reset_game(self):
        print "RESET"
        os.system("beep")
        self.ball_x, self.ball_y = (self.height-1, self.width/2)  # Start pose of the ball
        self.x_speed, self.y_speed = (1, -1)  # Vector giving the speed and direction of the ball
        self.racket_x, self.racket_y = (0, (self.width-self.racket_size/2)/2)   # Left corner of the racket

    def apply_command(self):
        if self.command['left']^self.command['right']:
            if self.command['left'] and self.racket_y>0:
                self.racket_y -= 1
            elif self.command['right'] and self.racket_y<self.width-self.racket_size:
                self.racket_y += 1

    def process_events(self):
        for event in pygame.event.get():
            # Joystick control
            if event.type == pygame.JOYBUTTONDOWN:
                self.command['rotate'] = True
            elif event.type==pygame.JOYHATMOTION:
                if event.value[0]==1:
                    self.command['right'] = True
                elif event.value[0]==-1:
                    self.command['left'] = True
                elif event.value[0]==0:
                    self.command['left'] = False
                    self.command['right'] = False

            # Keyboard control
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.key==pygame.K_RIGHT:
                    self.command['right'] = event.type==pygame.KEYDOWN
                elif event.key==pygame.K_LEFT:
                    self.command['left'] = event.type==pygame.KEYDOWN

    def step_forward(self):
        x = self.ball_x + self.x_speed
        y = self.ball_y + self.y_speed
        x_in = 0 <= x < self.height
        y_in = 0 <= y < self.width

        if x_in:
            self.ball_x = x
        else:
            self.x_speed = -self.x_speed
            self.step_forward()

        if y_in:
            self.ball_y = y
        else:
            self.y_speed = -self.y_speed
            self.step_forward()

    def render(self):
        def render_racket():
            for w in range(self.racket_size):
                self.model.set_pixel(self.racket_x, w+self.racket_y, self.racket_color)

        with self.model:
            self.model.set_all('black')
            print self.ball_x, self.ball_y
            self.model.set_pixel(int(self.ball_x), int(self.ball_y), self.ball_color)
            render_racket()


    def run(self):
        rate = Rate(5)
        while True:
            self.process_events()
            self.apply_command()
            self.render()
            self.step_forward()
            rate.sleep()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Pong game')

    Pong(parser).start()


