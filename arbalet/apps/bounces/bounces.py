#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Arbalet - ARduino-BAsed LEd Table
    Bounces - Bouncing pixels propeled by motions over a Leap controller
    This program requires that you plug a Leap Motion controller with its SDK installed and daemon running

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from random import randint, uniform, choice
from arbalet.core import Application, Rate
from threading import RLock
import os, sys, inspect

# Provide the path of your Leapmotion Python SDK
lib = '/home/yoan/Téléchargements/LeapDeveloperKit_2.2.6+29154_linux/LeapSDK/lib'
sys.path.append(lib)

# These import instructions are provided by Leapmotion at the time of coding, check for updates
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = lib+'/x64' if sys.maxsize > 2**32 else lib+'/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

try:
    from Leap import SwipeGesture, Gesture, Listener, Controller
except ImportError:
    print("Leapmotion SDK for Python not found, the gesture feature will not be available")
    print("If installed, you might want to edit the *lib* variable at the top of {}".format(__file__))
    leapmotion = False
else:
    leapmotion = True
    class SampleListener(Listener):
        def __init__(self, swipe, swipe_lock):
            Listener.__init__(self)
            self.swipe = swipe
            self.swipe_lock = swipe_lock
            print "Leap listener is started!"

        def on_connect(self, controller):
            controller.enable_gesture(Gesture.TYPE_SWIPE)

        def on_frame(self, controller):
            frame = controller.frame()
            for gesture in frame.gestures():
                if gesture.type == Gesture.TYPE_SWIPE and gesture.state in [1, 3]: # States 1 and 3 are START and STOP, we omit updates
                    with self.swipe_lock:
                        self.swipe[0] = SwipeGesture(gesture)
                    #print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                    #    self.swipe[0].id, self.swipe[0].state, self.swipe[0].position, self.swipe[0].direction, self.swipe[0].speed)

class Ball():
    colors = ['deeppink', 'navy', 'gold', 'white', 'grey', 'darkgreen', 'chocolate']

    def __init__(self, id, x, y, height, width, color='white', x_speed=0, y_speed=0, friction_factor=0.99, min_speed=0.1):
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
        self.friction_factor = friction_factor
        self.min_speed = min_speed

    @property
    def x(self):
        return int(self._x)

    @property
    def y(self):
        return int(self._y)

    def step_forward(self):
        x = self._x + self.x_speed
        y = self._y + self.y_speed
        x_in = 0 < x < self.height
        y_in = 0 < y < self.width

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

        # Simulate friction, slow down
        if abs(self.x_speed)>self.min_speed:
            self.x_speed *= self.friction_factor
        if abs(self.y_speed)>self.min_speed:
            self.y_speed *= self.friction_factor

class Bounces(Application):

    def __init__(self, parser, rate):
        Application.__init__(self, parser)
        self.balls = []
        self.rate = Rate(rate)

        def rand():
            return choice([-1, 1])*uniform(1./rate, 10./rate)

        for ball in range(4):
            self.balls.append(Ball(ball, randint(0, self.height-1), randint(0, self.width-1),
                                   self.height, self.width,
                                   Ball.colors[ball%len(Ball.colors)],
                                   rand(), rand()))

        # Motion control via Leap Motion
        self.swipe = [None]
        self.swipe_lock = RLock()

        if leapmotion:
            self.leap_listener = SampleListener(self.swipe, self.swipe_lock)
            self.controller = Controller()
            self.controller.add_listener(self.leap_listener)

    def close(self, reason='unknown'):
        Application.close(self, reason)
        if leapmotion:
            self.controller.remove_listener(self.leap_listener)

    def render(self):
        with self.model:
            self.model.set_all('black')
            with self.swipe_lock:
                for ball in self.balls:
                    self.model.set_pixel(ball.x, ball.y, ball.color)
                    if self.swipe[0] is not None:
                        # mapping axes (height, width) of Arbalet on axes (x, z) of Leap Motion
                        x_speed_boost = self.swipe[0].direction[0] * self.swipe[0].speed / 500.
                        y_speed_boost = self.swipe[0].direction[2] * self.swipe[0].speed / 500.
                        ball.x_speed += x_speed_boost
                        ball.y_speed += y_speed_boost
                self.swipe[0] = None

    def run(self):
        while True:
            for ball in self.balls:
                ball.step_forward()
            self.render()
            self.rate.sleep()
