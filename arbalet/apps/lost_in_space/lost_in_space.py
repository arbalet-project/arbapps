#!/usr/bin/env python
# -*- coding = utf-8 -*-
"""
Digital Art Jam
"""


from time import gmtime, strftime
from arbalet.application import Application
from arbalet.colors import hsv_to_rgb, rgb_to_hsv
from PIL import Image
from numpy import floor
from spawn import Spawn
import random
import time

#size must be greater than the table size
size = 25,25
MAX_SPEED = 3
MIN_SPEED = 1
MAX_SPAWNS = size[0]*size[1]/10
#MAX_SPAWNS = 25 # for testing purposes

class LostInSpace(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.base_color = None
        self.color = (1.0, 1.0, 1.0)
        # relative coordonate to image center
        self.y = self.height/2
        self.x = self.width/2
        # offset from
        self.offset_y = 0
        self.offset_x = 0
        self.model.set_all('white')
        self.state = 'init'
        self.spawns = []
        self.speed = 1
        self.fade = 1
        self.vector = None
        self.color_level = [0]*6
        self.last_spawn_color = 0
        # Treating arguments
        self.invader = self.args.invader
        self.ai = self.args.auto
        self.file = self.args.pattern
        self.last_events = {'up': False, 'down': False, 'right': False, 'left': False, 'action': False}

        if (self.file==''):
            self.image = Image.new('RGB',size, (255,255,255))
        else:
            self.image = Image.open(self.file)
            self.image = self.image.resize(size)

    def find_spawn(self, coord):
        for spawn in self.spawns:
            if coord in spawn.points:
                return spawn

    def spawn_source(self,position, parent = None, color=None):
        new_spawn=Spawn(size, position, parent,color, self.invader)
        self.spawns.append(new_spawn)

    def mix_color(self,(r1,g1,b1),(r2,g2,b2)):
        r = (r1+r2)/2
        g = (g2+g1)/2
        b = (b1+b2)/2
        return r,g,b

    def event(self):
        action = False

        if(self.ai):
            dir_list = ['up', 'down', 'left', 'right']
            direction = dir_list[random.randint(0,len(dir_list)-1)]
            steps = random.randint(0,10)
        else:
            direction =''
            steps = 1
            self.last_events.update({event['key']: event['pressed'] for event in self.events.get()})

        for it in range(steps):
            if self.last_events['up'] or direction == 'up':
                self.offset_y = (self.offset_y - 1) % size[1]
                self.vector = 'up'
                action = True
            elif self.last_events['down'] or direction == 'down':
                self.offset_y = (self.offset_y + 1) % size[1]
                self.vector = 'down'
                action = True
            elif self.last_events['right'] or direction == 'right':
                self.offset_x = (self.offset_x + 1) % size[0]
                self.vector = 'right'
                action = True
            elif self.last_events['left'] or direction == 'left':
                self.offset_x = (self.offset_x - 1) % size[0]
                self.vector = 'left'
                action = True
            elif self.last_events['action']:
                if self.state == 'init':
                    self.first_spawns()
                    action = True
                else:
                    self.state = 'end'
                    return

            if not action:
                self.speed = max(self.speed/1.2, MIN_SPEED)
                self.fade = max(self.fade/1.2, 1)
                if self.speed!=MIN_SPEED:
                    if self.vector=='up':
                        self.offset_y = (self.offset_y - 1) % size[1]
                    elif self.vector=='down':
                        self.offset_y = (self.offset_y + 1) % size[1]
                    elif self.vector=='left':
                        self.offset_x = (self.offset_x - 1) % size[0]
                    elif self.vector=='right':
                        self.offset_x = (self.offset_x + 1) % size[0]
                    action = True
            if self.state == 'init':
                return
            elif self.state == 'running' and action:
                with self.model:
                    # Changing color
                    brightness = max(rgb_to_hsv(self.color)[1] - 1./self.fade, 0)
                    self.color = hsv_to_rgb(rgb_to_hsv(self.color)[0], brightness, rgb_to_hsv(self.color)[2])
                    collide_spawn = None
                    # if we are on a spot
                    x = (self.offset_x + self.x)%size[0]
                    y = (self.offset_y + self.y)%size[1]
                    for spawn in self.spawns:
                        if (x, y) == (spawn.x, spawn.y):
                            collide_spawn = spawn
                    if collide_spawn is not None:
                        spawn = collide_spawn
                        self.last_spawn_color = spawn.color
                        #print self.last_spawn_color
                        self.base_color = spawn.color
                        r = int(round(spawn.color[0] * 255))
                        g = int(round(spawn.color[1] * 255))
                        b = int(round(spawn.color[2] * 255))
                        self.image.putpixel(((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]),
                                            (r, g, b))
                        self.color = self.base_color

                        # play sound
                        sound = spawn.get_sound(self.color_level[spawn.color_id])
                        sound.play()
                        sound.fadeout(3000)

                        # draw spawn
                        points = spawn.get_points(self.color_level[spawn.color_id], size)
                        for point in points:
                            self.image.putpixel((point[0], point[1]),(r, g, b))
                        self.spawns.remove(spawn)

                        # generate two new spawns
                        random.seed()
                        self.spawn_source([random.randint(floor(self.x-self.width/2)+1,floor(self.x+self.width/2)-1),
                            random.randint(floor(self.y-self.height/2)+1,floor(self.y + self.height/2)-1)],parent=spawn)
                        self.spawn_source([random.randint(0, size[0]-1), random.randint(0, size[1]-1)])
                    
                        # delete two old spawns if too many spawns
                        #print len(self.spawns), MAX_SPAWNS
                        if len(self.spawns)>=MAX_SPAWNS:
                            spawns_to_remove = 2
                            indices_to_remove = []
                            iterations = 0
                            while(len(indices_to_remove) <2 and iterations<MAX_SPAWNS):
                                tmp_index = random.randint(0,floor(MAX_SPAWNS/2))
                                iterations += 1
                                tmp_spawn = self.spawns[tmp_index]
                                if (tmp_spawn.x<=(self.x-self.width/2) or tmp_spawn.x>=(self.x +
                                    self.width/2) or tmp_spawn.y <= (self.y - self.height/2) or
                                    tmp_spawn.y >= (self.y + self.height/2)):
                                    #self.spawns.remove(tmp_index)
                                    if not tmp_index in indices_to_remove :
                                        indices_to_remove.append(tmp_index)
                                    spawns_to_remove -=1
                                #print indices_to_remove
                            for index in indices_to_remove:
                                self.spawns.remove(self.spawns[index])
                            indices_to_remove = []
                            #print len(self.spawns)
                        # get information about speed and fading
                        self.speed = spawn.get_speed(self.color_level[spawn.color_id])
                        self.fade = spawn.get_fading(self.color_level[spawn.color_id])

                        self.color_level[spawn.color_id] = min(self.color_level[spawn.color_id]+1, 3)

                    # else we tranform the current color
                    else:
                        # transforming player color to PIL RGB
                        r = int(round(self.color[0] * 255))
                        g = int(round(self.color[1] * 255))
                        b = int(round(self.color[2] * 255))

                        # we only print on the image if we still have color
                        if not (rgb_to_hsv(self.color)[0] == 0.):
                            actual_color = self.image.getpixel(
                                ((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]))
                            if actual_color != (255, 255, 255):
                                r, g, b = self.mix_color((r, g, b), (actual_color[0], actual_color[1], actual_color[2]))
                            self.image.putpixel(((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]),
                                            (r, g, b))
                        # random diffusion on the sides with bluuuueee !   
                            if self.last_spawn_color == [0.047058823529411764,
                                    0.14901960784313725,0.7019607843137254] and self.color_level[2]==3:
                                # blue is hard-coded
                                #print "fuuuuuusioooon"
                                tmp_brightness = max(rgb_to_hsv(self.color)[1] -random.randint(1.,8.)/self.fade, 0)
                                tmp_color = hsv_to_rgb(rgb_to_hsv(self.color)[0], tmp_brightness, rgb_to_hsv(self.color)[2])
    
                                r = int(round(tmp_color[0] * 255))
                                g = int(round(tmp_color[1] * 255))
                                b = int(round(tmp_color[2] * 255))

                                # uncomment to smoothen the sides of the blue track    
                                #r, g, b = self.mix_color((r, g, b), (actual_color[0], actual_color[1], actual_color[2]))

                                if self.vector ==  'up':
                                    self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                    self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                elif self.vector == 'down':
                                    self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                                    self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                                elif self.vector == 'left':
                                    self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                    self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                                elif self.vector == 'right':
                                    self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                        (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                    self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                                if self.last_spawn_color == [0.06666666666666667, 0.6470588235294118,
                             0.2784313725490196] and self.color_level[1]==1:
                                    tmp_brightness = max(rgb_to_hsv(self.color)[1] -1./self.fade, 0)
                                    tmp_color = hsv_to_rgb(rgb_to_hsv(self.color)[0], tmp_brightness, rgb_to_hsv(self.color)[2])

                                    r = int(round(tmp_color[0] * 255))
                                    g = int(round(tmp_color[1] * 255))
                                    b = int(round(tmp_color[2] * 255))

                                if self.vector ==  'up':
                                    if ((self.y + self.offset_y)%2 == 0):
                                        self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                    else:
                                        self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                elif self.vector == 'down':
                                    if ((self.y + self.offset_y)%2 == 0):
                                        self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                                    else :
                                        self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                                elif self.vector == 'left':
                                    if ((self.x + self.offset_x)%2 == 0):
                                        self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                    else :
                                        self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                                elif self.vector == 'right':
                                    if ((self.x + self.offset_x)%2 ==0):
                                        self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                    else :
                                        self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                        (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))

                        else:
                            self.color=(1.0, 1.0, 1.0)
                            for i in range(len(self.color_level)):
                                self.color_level[i] = 0
                            self.speed = max(self.speed / 1.2, MIN_SPEED)

            # finaly, we draw the grid
            self.draw_grid()

    def draw_grid(self):
        #drag from image
        for i in range(0,self.model.width):
            for j in range(0,self.model.height):
                x = (self.offset_x + i + size[0])%size[0]
                y = (self.offset_y + j + size[1])%size[1]
                c = self.image.getpixel((x,y))
                r = c[0]/255.
                g = c[1]/255.
                b = c[2]/255.
                self.model.set_pixel(j, i, [r, g ,b])
        # draw spawn, QLE style
        for spawn in self.spawns:
            try:
                self.model.set_pixel((spawn.y-self.offset_y+size[1])%size[1],(spawn.x-self.offset_x+size[0])%size[0],spawn.draw_color)
            except:
                pass
        if self.color == (1.0, 1.0, 1.0):
            self.model.set_pixel(self.y, self.x, 'black')

    def first_spawns(self):
                with self.model:
                    # set initial color
                    self.model.set_pixel(self.y, self.x, (1.0,1.0,1.0))
                    self.color = self.model.get_pixel(self.y, self.x)
                    self.base_color = self.color

                    # spawn first stop near the player
                    self.spawn_source([self.offset_x + self.x, self.offset_y + self.y + 2], color=0)
                    self.spawn_source([self.offset_x + self.x - 2, self.offset_y + self.y + 1], color=1)
                    self.spawn_source([self.offset_x + self.x - 2, self.offset_y + self.y - 1], color=2)
                    self.spawn_source([self.offset_x + self.x, self.offset_y + self.y - 2], color=3)
                    self.spawn_source([self.offset_x + self.x + 2, self.offset_y + self.y + 1], color=4)
                    self.spawn_source([self.offset_x + self.x + 2, self.offset_y + self.y - 1], color=5)
                    self.state = 'running'
    def run(self):
        if(self.ai):
            self.state = 'init'
            self.first_spawns()
            random.seed()
            for it in range(5):
                self.spawn_source([random.randint(floor(self.x-self.width/2)+1,floor(self.x+self.width/2)-1),
             random.randint(floor(self.y-self.height/2)+1,floor(self.y + self.height/2)-1)],parent=None)
        while self.state is not 'end':
            self.event()
            time.sleep(0.15/self.speed)

        if self.args.save:
            image = self.image.resize((1000,1000))
            image.show()
            if (self.ai):
                image.save('output/ai_' +strftime("%Y-%m-%d %H.%M.%S", gmtime()) + '.bmp')
            else:
                image.save('output/' +strftime("%Y-%m-%d %H.%M.%S", gmtime()) + '.bmp')

