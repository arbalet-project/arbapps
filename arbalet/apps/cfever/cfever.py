import random
from arbalet.core import Application, Rate
import pygame

LEFT=(0,-1)
RIGHT=(0, 1)
DOWN=(1, 0)
UP=(-1, 0)

K_LEFT2 = 113
K_RIGHT2 = 100
K_DOWN2 = 115
K_UP2 = 122

# Set up the joystick
pygame.joystick.init()

nbjoysticks = pygame.joystick.get_count()
joysticks = []
for i in range(nbjoysticks):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)


class Cfever(Application):
    BG_COLOR = 'black'
    P1COLOR = 'red'
    P2COLOR = 'blue'
    FOOD_COLOR='green'

    def __init__(self, touch_mode='quadridirectional'):
        Application.__init__(self, touch_mode=touch_mode)
        self.rate=2
       
        self.DIRECTION1=DOWN
        self.HEAD1=(1,1)
        self.queue1=[self.HEAD1]

        self.DIRECTION2=UP
        self.HEAD2=(13,8)
        self.queue2=[self.HEAD2]
        
        self.FOOD_POSITIONS={}
        self.rate_increase=0.15
        self.start_food=3



    def process_events(self):
        new_dir=None
        new_dir2=None
        for event in self.arbalet.events.get():
            if event.type==pygame.JOYAXISMOTION:
                if joysticks[0].get_axis(1) < 0 and (self.DIRECTION1!=DOWN or len(self.queue1)<=1):
                    print("up")
                    new_dir=UP
                if joysticks[0].get_axis(1) > 0 and (self.DIRECTION1!=UP or len(self.queue1)<=1):
                    print("down")
                    new_dir=DOWN
                if joysticks[0].get_axis(0) > 0 and not(joysticks[0].get_axis(1) < 0 or joysticks[0].get_axis(1)) and (self.DIRECTION1!=LEFT or len(self.queue1)<=1):
                    print("right")
                    new_dir = RIGHT
                if joysticks[0].get_axis(0) < 0 and not(joysticks[0].get_axis(1) < 0 or joysticks[0].get_axis(1)) and (self.DIRECTION1!=RIGHT or len(self.queue1)<=1):
                    new_dir = LEFT


                if joysticks[1].get_axis(1) < 0 and (self.DIRECTION2!=DOWN or len(self.queue2)<=1):
                    print("up")
                    new_dir2=UP
                if joysticks[1].get_axis(1) > 0 and (self.DIRECTION2!=UP or len(self.queue2)<=1):
                    print("down")
                    new_dir2=DOWN
                if joysticks[1].get_axis(0) > 0 and not(joysticks[1].get_axis(1) < 0 or joysticks[0].get_axis(1)) and (self.DIRECTION2!=LEFT or len(self.queue2)<=1):
                    print("right")
                    new_dir2 = RIGHT
                if joysticks[1].get_axis(0) < 0 and not(joysticks[1].get_axis(1) < 0 or joysticks[0].get_axis(1)) and (self.DIRECTION2!=RIGHT or len(self.queue2)<=1):
                    new_dir2 = LEFT
            # Keyboard control
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.key==pygame.K_UP and (self.DIRECTION1!=DOWN or len(self.queue1)<=1):
                    new_dir=UP
                elif event.key==pygame.K_DOWN and (self.DIRECTION1!=UP or len(self.queue1)<=1):
                    new_dir=DOWN
                elif event.key==pygame.K_RIGHT and (self.DIRECTION1!=LEFT or len(self.queue1)<=1):
                    new_dir = RIGHT
                elif event.key==pygame.K_LEFT and (self.DIRECTION1!=RIGHT or len(self.queue1)<=1):
                    new_dir = LEFT

                elif event.key==K_UP2 and (self.DIRECTION2!=DOWN or len(self.queue2)<=1):
                    new_dir2=UP
                elif event.key==K_DOWN2 and (self.DIRECTION2!=UP  or len(self.queue2)<=1):
                    new_dir2=DOWN
                elif event.key==K_RIGHT2 and (self.DIRECTION2!=LEFT or len(self.queue2)<=1):
                    new_dir2 = RIGHT
                elif event.key==K_LEFT2 and (self.DIRECTION2!=RIGHT or len(self.queue2)<=1):
                    new_dir2 = LEFT

        if new_dir is not None:
            self.DIRECTION1=new_dir

        if new_dir2 is not None:
            self.DIRECTION2=new_dir2


    def process_extras(self, x=None, y=None):
        pass

    def spawn_food(self, quantity=4):
        for _ in range(0,quantity):
            while True:
                f=(random.randint(0,self.height-1),random.randint(0,self.width-1))
                if f not in self.queue1 and f not in self.queue2 and f not in self.FOOD_POSITIONS:
                    break
            self.FOOD_POSITIONS[f]=True

            self.model.set_pixel(f[0], f[1], self.FOOD_COLOR)

    def run(self):
        rate = Rate(self.rate)
        self.model.set_all(self.BG_COLOR)
        self.model.set_pixel(self.HEAD1[0],self.HEAD1[1],self.P1COLOR)
        self.model.set_pixel(self.HEAD2[0],self.HEAD2[1],self.P2COLOR)

        self.spawn_food(self.start_food)
        for x,y in self.FOOD_POSITIONS:
            self.model.set_pixel(x, y, self.FOOD_COLOR)

        while True:
            rate.sleep_dur=1.0/self.rate
            with self.model:
                self.process_events()
                new_pos=((self.HEAD1[0]+self.DIRECTION1[0])%self.height, (self.HEAD1[1]+self.DIRECTION1[1])%self.width)
                new_pos2=((self.HEAD2[0]+self.DIRECTION2[0])%self.height, (self.HEAD2[1]+self.DIRECTION2[1])%self.width)

                #check
                if new_pos in self.queue1 or new_pos in self.queue2:
                    gagnant="J2"
                    break

                if new_pos2 in self.queue2 or new_pos2 in self.queue1:
                    gagnant="J1"
                    break

                self.HEAD1=new_pos
                self.HEAD2=new_pos2

                self.model.set_pixel(new_pos[0],new_pos[1],self.P1COLOR)
                self.model.set_pixel(new_pos2[0],new_pos2[1],self.P2COLOR)

                self.queue1.append(new_pos)
                self.queue2.append(new_pos2)

                if new_pos not in self.FOOD_POSITIONS:
                    x, y=self.queue1.pop(0)
                    self.model.set_pixel(x, y, self.BG_COLOR)
                    self.process_extras(x, y)
                else:
                    del self.FOOD_POSITIONS[new_pos]
                    self.spawn_food(1)
                    self.rate+=self.rate_increase
                    self.process_extras()

                if new_pos2 not in self.FOOD_POSITIONS:
                    x, y=self.queue2.pop(0)
                    self.model.set_pixel(x, y, self.BG_COLOR)
                    self.process_extras(x, y)
                else:
                    del self.FOOD_POSITIONS[new_pos2]
                    self.spawn_food(1)
                    self.rate+=self.rate_increase
                    self.process_extras()
            rate.sleep()
        self.game_over(gagnant)
        exit()


    def game_over(self, gagnant):
        print("Game OVER")
        self.model.flash()
        if(gagnant=="J1"):
            self.model.write("PLAYER 1 WINS", self.P1COLOR)
        else:
            self.model.write("PLAYER 2 WINS", self.P2COLOR)


