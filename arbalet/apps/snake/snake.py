#!/usr/bin/env python
"""
    Copyright 2016:
        Tomas Beati
        Maxime Carere
        Nicolas Verdier
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html

    Arbalet - ARduino-BAsed LEd Table
    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import random
from arbalet.core import Application, Rate
import pygame

LEFT=(0,-1)
RIGHT=(0, 1)
DOWN=(1, 0)
UP=(-1, 0)

class Snake(Application):
    BG_COLOR = 'black'
    PIXEL_COLOR='darkred'
    FOOD_COLOR='green'
    
    def __init__(self, argparser, touch_mode='quadridirectional'):
        Application.__init__(self, argparser, touch_mode=touch_mode)
        self.DIRECTION=DOWN
        self.HEAD=(5,5)
        self.queue=[self.HEAD]
        self.FOOD_POSITIONS={}
        self.rate=2
        self.rate_increase=self.args.speed
        self.start_food=self.args.food

    def process_events(self):
        new_dir=None
        for event in self.arbalet.events.get():
            # Joystick control
            if event.type == pygame.JOYBUTTONDOWN:
                #self.command['rotate'] = True
                pass
            elif event.type==pygame.JOYHATMOTION:
                if event.value[1]==1 and self.DIRECTION != DOWN:
                    new_dir = UP
                elif event.value[1]==-1 and self.DIRECTION != UP:
                     new_dir = DOWN
                elif event.value[1]==0:
                    pass
                if event.value[0]==1 and self.DIRECTION != LEFT:
                     new_dir = RIGHT
                elif event.value[0]==-1 and self.DIRECTION != RIGHT:
                     new_dir = LEFT
                elif event.value[0]==0:
                    pass
            # Keyboard control
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.key==pygame.K_UP:
                    new_dir=UP
                elif event.key==pygame.K_DOWN:
                    new_dir=DOWN
                elif event.key==pygame.K_RIGHT:
                    new_dir = RIGHT
                elif event.key==pygame.K_LEFT:
                    new_dir = LEFT

        for event in self.arbalet.touch.get():
            if event['key']=='up':
                new_dir = UP
            elif event['key']=='down':
                new_dir = DOWN
            elif event['key']=='right':
                new_dir = RIGHT
            elif event['key']=='left':
                new_dir = LEFT

        if new_dir is not None:
            self.DIRECTION=new_dir
        
    def process_extras(self, x=None, y=None):
        pass

    def spawn_food(self, quantity=4):
        for _ in range(0,quantity):
            while True:
                f=(random.randint(0,self.height-1),random.randint(0,self.width-1))
                if f not in self.queue and f not in self.FOOD_POSITIONS:
                    break
            self.FOOD_POSITIONS[f]=True

            self.model.set_pixel(f[0], f[1], self.FOOD_COLOR)

    def run(self):
        rate = Rate(self.rate)

        self.model.set_all(self.BG_COLOR)
        self.model.set_pixel(self.HEAD[0],self.HEAD[1],self.PIXEL_COLOR)
        self.spawn_food(self.start_food)
        for x,y in self.FOOD_POSITIONS:
            self.model.set_pixel(x, y, self.FOOD_COLOR)

        while True:
            rate.sleep_dur=1.0/self.rate
            with self.model:
                self.process_events()
                new_pos=((self.HEAD[0]+self.DIRECTION[0])%self.height, (self.HEAD[1]+self.DIRECTION[1])%self.width)
                #check
                if new_pos in self.queue:
                    break


                self.HEAD=new_pos
                self.model.set_pixel(new_pos[0],new_pos[1],self.PIXEL_COLOR)
                self.queue.append(new_pos)

                if new_pos not in self.FOOD_POSITIONS:
                    x, y=self.queue.pop(0)
                    self.model.set_pixel(x, y, self.BG_COLOR)
                    self.process_extras(x, y)
                else:
                    del self.FOOD_POSITIONS[new_pos]
                    self.spawn_food(1)
                    self.rate+=self.rate_increase
                    self.process_extras()
            rate.sleep()
        self.game_over()
        exit()

    def game_over(self):
        print("Game OVER")
        self.model.flash()
        self.model.write("GAME OVER! Score: {}".format(len(self.queue)), 'deeppink')

