#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Bounces - Bouncing pixels propeled by motions over a Leap controller
    This program requires that you plug a Leap Motion controller with its SDK installed and daemon running

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from random import randint, uniform, choice
from arbasdk import Arbapp, Arbapixel, Rate
import argparse

class Ball():
    colors = ['deeppink', 'navy', 'gold', 'white', 'grey', 'darkgreen', 'chocolate']
    def __init__(self, id, x, y, height, width, color='white', x_speed=0, y_speed=0):
        """

        :param x:
        :param y:
        :param speed:
        :param color:
        :param x_speed:
        :param y_speed: in pixel/
        :return:
        """
        self.id = id
        self._x, self._y = (x, y)
        self.width, self.height = width, height
        self.color = color
        self.x_speed, self.y_speed = (x_speed, y_speed)

    @property
    def x(self):
        return int(self._x)

    @property
    def y(self):
        return int(self._y)

    def step_forward(self):
        x = self._x + self.x_speed
        y = self._y + self.y_speed
        x_in = 0 < x < self.height-1
        y_in = 0 < y < self.width-1

        if x_in:
            self._x = x
        else:
            self.x_speed = -self.x_speed
            self.step_forward()

        if y_in:
            self._y = y
        else:
            self.y_speed = -self.y_speed
            self.step_forward()


class Bounces(Arbapp):

    def __init__(self, parser, rate):
        Arbapp.__init__(self, parser)
        self.balls = []
        self.rate = Rate(rate)

        def rand():
            return choice([-1, 1])*uniform(0.1, 1)

        for ball in range(11):
            self.balls.append(Ball(ball, randint(0, self.height-1), randint(0, self.width-1),
                                   self.height, self.width,
                                   Ball.colors[ball%len(Ball.colors)],
                                   rand(), rand()))



    def render(self):
        self.model.lock()
        self.model.set_all('black')
        for ball in self.balls:
            self.model.set_pixel(ball.x, ball.y, ball.color)
        self.model.unlock()

    def run(self):
        while True:
            for ball in self.balls:
                ball.step_forward()
            self.render()
            self.rate.sleep()

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Bouncing pixels propelled by a leap motion controller'
                                                 'You must plug a Leap Motion controller, install its SDK and run its daemon first')

    e = Bounces(parser, 10)
    e.start()
    e.close("end")
