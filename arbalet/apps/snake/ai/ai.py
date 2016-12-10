#!/usr/bin/env python
"""
    Simple snake AI
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html

    Arbalet - ARduino-BAsed LEd Table
    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from arbalet.colors import mul, name_to_rgb, equal
from ..snake import Snake
from numpy import zeros


class SnakeAI(Snake):
    FOOD = name_to_rgb(Snake.FOOD_COLOR)
    BODY = name_to_rgb(Snake.PIXEL_COLOR)
    
    SCORE_FOOD_ATTRACTION = 100
    SCORE_FOOD_TARGET = 500
    SCORE_BODY_ATTRACTION = -5
    SCORE_BODY_TARGET = -500
    
    def __init__(self, argparser):
        Snake.__init__(self, argparser, touch_mode='off')
        self.potential_field = zeros((self.height, self.width))

    def process_extras(self, x=None, y=None):
        if x is not None and y is not None:
            self.update_potential_field_of(x, y)
        for h in range(self.height):
            for w in range(self.width):
                pixel = self.model.get_pixel(h, w)
                if not equal(pixel, SnakeAI.FOOD) and not equal(pixel, SnakeAI.BODY):
                    color = mul('white', self.potential_field[h, w]/(3*self.SCORE_FOOD_ATTRACTION))
                    self.model.set_pixel(h, w, color)

    @staticmethod
    def norm(x, y):
        # Not using the euclidian distance for faster calculations
        return abs(y[0]-x[0]) + abs(y[1]-x[1])

    def update_potential_field(self):
        for h in range(self.height):
            for w in range(self.width):
                self.update_potential_field_of(h, w)

    def update_potential_field_of(self, h, w):
        pixel = (h, w)
        score = 0
        if equal(self.model.get_pixel(h, w), SnakeAI.FOOD):
            score = SnakeAI.SCORE_FOOD_TARGET
        elif equal(self.model.get_pixel(h, w), SnakeAI.BODY):
            score = SnakeAI.SCORE_BODY_TARGET
        else:
            for food in self.FOOD_POSITIONS:
                distance = self.norm(food, pixel)
                score += SnakeAI.SCORE_FOOD_ATTRACTION/distance
            for body in self.queue:
                distance = self.norm(body, pixel)
                if distance < 4:
                    score += SnakeAI.SCORE_BODY_ATTRACTION/distance
        self.potential_field[h, w] = score           
    
    def process_events(self):
        self.update_potential_field()
        directions = {'left': (0, -1), 'up': (-1, 0), 'right': (0, 1), 'down':(1, 0)}
        max_score = -float('inf')
        for name, direction in directions.items():
            next_x = (self.HEAD[0] + direction[0])%self.height
            next_y = (self.HEAD[1] + direction[1])%self.width
            score = self.potential_field[next_x][next_y]
            print("Decision {} has a score of {}".format(name, score))
            if score > max_score:
                max_score = score
                decision = direction
                decision_name = name
        print("Choosen decision {} score {}".format(decision_name, max_score))
        self.DIRECTION = decision

