import random
from arbalet.core import Application, Rate
import pygame
from pygame.locals import *
import time
import thread
import threading
from threading import Thread
from subprocess import call

LEFT = -1
RIGHT = 1
LIMRIGHT = 10
LIMLEFT = -1

K_LEFT1 = 113
K_RIGHT1 = 100

# Set up the joystick
pygame.joystick.init()

nbjoysticks = pygame.joystick.get_count()
joysticks = []
for i in range(nbjoysticks):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)

print joysticks

class Pong(Application):

    BG_COLOR = 'black'
    BALLE_COLOR = 'white'
    P1_COLOR = 'blue'
    P2_COLOR = 'red'

    def __init__(self):
        Application.__init__(self)
        pygame.init()
        self.BALLE = [7,random.randrange(0,9)]
        self.P1_RACKET = range(3,6)
        self.P2_RACKET = range(3,6)
        self.P1_DIRECTION = []
        self.P2_DIRECTION = []
        self.P1_SCORE = 0
        self.P2_SCORE = 0
        self.SCORE_WIN = 5
        self.TABJEU = [[0] * 10 for _ in range(14)]
        self.fin = False
        self.ballspeed_increase = 0.01
        self.ballspeed = 0.5
        self.limspeed = 0.11
        self.RATE_SPEED = 2
        self.lenP1_RACKET = len(self.P1_RACKET)
        self.lenP2_RACKET = len(self.P2_RACKET)

    def run(self):
        rate = Rate(self.RATE_SPEED)
        if self.P1_SCORE < self.SCORE_WIN or self.P2_SCORE < self.SCORE_WIN:
            self.init_grille()
            t1 = thread.start_new_thread(self.wait_for_timeout_or_event1,("wait_for_timeout_or_event1", ))
            #t2 = thread.start_new_thread(self.wait_for_timeout_or_event2,("wait_for_timeout_or_event2", ))
            t3 = thread.start_new_thread(self.animationBalle,("animationBalle", ))
        while 1:
            pass
        time.sleep(2)

    def process_events1(self):
        new_dir=None
        while self.fin == False:
            for event in self.arbalet.events.get():
                if event.type == pygame.QUIT:
                        self.fin = 'QUIT' 

                # if joysticks[0].get_hat(0) == (1,0) or joysticks[0].get_hat(0) == (1,1) or joysticks[0].get_hat(0) == (1,-1):
                #     new_dir = RIGHT
                #     if (self.P1_RACKET[self.lenP1_RACKET-1]+new_dir) < LIMRIGHT:
                #         self.model.set_pixel(0,self.P1_RACKET[0], self.BG_COLOR)

                #         for i in range(self.lenP1_RACKET):
                #             self.P1_RACKET[i] += new_dir

                #         self.model.set_pixel(0,self.P1_RACKET[self.lenP1_RACKET-1], self.P1_COLOR)
                #         print self.P1_RACKET
                #         break
                # if joysticks[0].get_hat(0) == (-1,0)  or joysticks[0].get_hat(0) == (-1,1) or joysticks[0].get_hat(0) == (-1,-1):
                #     new_dir = LEFT
                #     if (self.P1_RACKET[0]+new_dir) > LIMLEFT:
                #         self.model.set_pixel(0,self.P1_RACKET[self.lenP1_RACKET-1], self.BG_COLOR)

                #         for i in range(self.lenP1_RACKET):
                #             self.P1_RACKET[i] += new_dir

                #         self.model.set_pixel(0,self.P1_RACKET[0], self.P1_COLOR)
                #         print self.P1_RACKET
                #         break

                if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    if event.key==pygame.K_RIGHT:
                        new_dir = RIGHT
                        if (self.P1_RACKET[self.lenP1_RACKET-1]+new_dir) < LIMRIGHT:
                            self.model.set_pixel(0,self.P1_RACKET[0], self.BG_COLOR)

                            for i in range(self.lenP1_RACKET):
                                self.P1_RACKET[i] += new_dir

                            self.model.set_pixel(0,self.P1_RACKET[self.lenP1_RACKET-1], self.P1_COLOR)

                    elif event.key==pygame.K_LEFT:
                        new_dir = LEFT
                        if (self.P1_RACKET[0]+new_dir) > LIMLEFT:
                            self.model.set_pixel(0,self.P1_RACKET[self.lenP1_RACKET-1], self.BG_COLOR)

                            for i in range(self.lenP1_RACKET):
                                self.P1_RACKET[i] += new_dir

                            self.model.set_pixel(0,self.P1_RACKET[0], self.P1_COLOR)

                if event.type==pygame.JOYAXISMOTION:
                    if joysticks[0].get_axis(0) < 0:
                        new_dir = RIGHT
                        if (self.P1_RACKET[self.lenP1_RACKET-1]+new_dir) < LIMRIGHT:
                            self.model.set_pixel(0,self.P1_RACKET[0], self.BG_COLOR)

                            for i in range(self.lenP1_RACKET):
                                self.P1_RACKET[i] += new_dir

                            self.model.set_pixel(0,self.P1_RACKET[self.lenP1_RACKET-1], self.P1_COLOR)

                    if joysticks[0].get_axis(0) > 0:
                        new_dir = LEFT
                        if (self.P1_RACKET[0]+new_dir) > LIMLEFT:
                            self.model.set_pixel(0,self.P1_RACKET[self.lenP1_RACKET-1], self.BG_COLOR)

                            for i in range(self.lenP1_RACKET):
                                self.P1_RACKET[i] += new_dir

                            self.model.set_pixel(0,self.P1_RACKET[0], self.P1_COLOR)
                        
                    if joysticks[1].get_axis(0) > 0:
                        new_dir = RIGHT
                        if (self.P2_RACKET[self.lenP2_RACKET-1]+new_dir) < LIMRIGHT: 
                            self.model.set_pixel(14,self.P2_RACKET[0], self.BG_COLOR)

                            for i in range(self.lenP2_RACKET):
                                self.P2_RACKET[i] += new_dir

                            self.model.set_pixel(14,self.P2_RACKET[self.lenP2_RACKET-1], self.P2_COLOR)

                        
                    if joysticks[1].get_axis(0) < 0:
                        new_dir = LEFT
                        if (self.P2_RACKET[0]+new_dir) > LIMLEFT:
                            self.model.set_pixel(14,self.P2_RACKET[self.lenP2_RACKET-1], self.BG_COLOR)

                            for i in range(self.lenP2_RACKET):
                                self.P2_RACKET[i] += new_dir

                            self.model.set_pixel(14,self.P2_RACKET[0],self.P2_COLOR)
                        

    def wait_for_timeout_or_event1(self, threadName):
        t0 = time.time()
        while time.time()-t0 < 1./self.RATE_SPEED:
            time.sleep(0.07)
            if self.process_events1():
                return

    # def wait_for_timeout_or_event2(self, threadName):
    #     t0 = time.time()
    #     while time.time()-t0 < 1./self.RATE_SPEED:
    #         time.sleep(0.07)
    #         if self.process_events2():
    #             return
                
    # def process_events2(self):
    #     new_dir=None
    #     while self.fin == False:
    #         for event in self.arbalet.events.get():
    #             # if joysticks[1].get_hat(0) == (1,0):
    #             #         new_dir = RIGHT
    #             #         if (self.P2_RACKET[self.lenP2_RACKET-1]+new_dir) < LIMRIGHT: 
    #             #             self.model.set_pixel(14,self.P2_RACKET[0], self.BG_COLOR)

    #             #             for i in range(self.lenP2_RACKET):
    #             #                 self.P2_RACKET[i] += new_dir

    #             #             self.model.set_pixel(14,self.P2_RACKET[self.lenP2_RACKET-1], self.P2_COLOR)
    #             #             print self.P2_RACKET
    #             #             break
    #             if joysticks[1].get_hat(0) == (-1,0):
    #                     new_dir = LEFT
    #                     if (self.P2_RACKET[0]+new_dir) > LIMLEFT:
    #                         self.model.set_pixel(14,self.P2_RACKET[self.lenP2_RACKET-1], self.BG_COLOR)

    #                         for i in range(self.lenP2_RACKET):
    #                             self.P2_RACKET[i] += new_dir

    #                         self.model.set_pixel(14,self.P2_RACKET[0],self.P2_COLOR)
    #                         print self.P2_RACKET
    #                         break

               

    #             # elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
    #             #     if event.key == K_RIGHT1:
    #             #             new_dir = RIGHT
    #             #             if (self.P2_RACKET[self.lenP2_RACKET-1]+new_dir) < LIMRIGHT: 
    #             #                 self.model.set_pixel(14,self.P2_RACKET[0], self.BG_COLOR)

    #             #                 for i in range(self.lenP2_RACKET):
    #             #                     self.P2_RACKET[i] += new_dir

    #             #                 self.model.set_pixel(14,self.P2_RACKET[self.lenP2_RACKET-1], self.P2_COLOR)
    #             #                 print self.P2_RACKET
    #             #                 break
    #             #     elif event.key==K_LEFT1:
    #             #         new_dir = LEFT
    #             #         if (self.P2_RACKET[0]+new_dir) > LIMLEFT:
    #             #             self.model.set_pixel(14,self.P2_RACKET[self.lenP2_RACKET-1], self.BG_COLOR)

    #             #             for i in range(self.lenP2_RACKET):
    #             #                 self.P2_RACKET[i] += new_dir

    #             #             self.model.set_pixel(14,self.P2_RACKET[0],self.P2_COLOR)    
    #             #             print self.P2_RACKET
    #             #             break

    def init_grille(self):
        self.arbalet.user_model.set_all(self.BG_COLOR)
        for col in self.P1_RACKET: 
            self.arbalet.user_model.set_pixel(0, col, self.P1_COLOR)
            self.arbalet.user_model.set_pixel(14, col, self.P2_COLOR)
        self.arbalet.user_model.set_pixel(self.BALLE[0], self.BALLE[1], self.BALLE_COLOR)

    def nextRound(self):
        self.arbalet.user_model.set_pixel(self.BALLE[0], self.BALLE[1], self.BG_COLOR)
        self.ballspeed = 0.5
        self.BALLE = [7,random.randrange(0,9)]
        print " SCORE P1 : " + str(self.P1_SCORE) + " SCORE P2 : " + str(self.P2_SCORE)
        self.arbalet.user_model.set_pixel(self.BALLE[0], self.BALLE[1], self.BALLE_COLOR)
        time.sleep(1.5)
        self.arbalet.user_model.set_pixel(self.BALLE[0], self.BALLE[1], self.BG_COLOR)
        


    def animationBalle(self, threadName):
        while self.fin == False:
            directionY = random.randrange(-1, 1, 2)
            directionX = random.randrange(-1, 1, 2)

            while 1:
                # CONDITIONS DE VICTOIRES
                if self.BALLE[0] == 0:
                    self.P2_SCORE += 1
                    self.nextRound()
                    if self.P2_SCORE == self.SCORE_WIN:
                        self.fin = "P2"
                        break
                    continue
                if self.BALLE[0] == 14:
                    self.P1_SCORE += 1
                    self.nextRound()
                    if self.P1_SCORE == self.SCORE_WIN:
                        self.fin = "P1"
                        break
                    continue

                olddireX = directionX

                # CONTACT ENTRE RAQUETTE ET BALLE
                if self.BALLE[0] == 13:
                    if (self.BALLE[1] in self.P2_RACKET or self.BALLE[1] == self.P2_RACKET[self.lenP2_RACKET-1]+1 or self.BALLE[1] == self.P2_RACKET[0]-1):    
                        if self.BALLE[1] == LIMLEFT+1 or self.BALLE[1] == LIMRIGHT-1:
                            balleApres = -directionX 
                        else:
                            balleApres = directionX

                        directionY = -directionY

                        if (self.BALLE[1]+balleApres not in self.P2_RACKET):
                            self.P1_SCORE += 1
                            self.nextRound()
                            if self.P1_SCORE == self.SCORE_WIN:
                                self.fin = "P1"
                                break
                            continue
                            
                elif self.BALLE[0] == 1:
                    if (self.BALLE[1] in self.P1_RACKET or self.BALLE[1] == self.P1_RACKET[self.lenP1_RACKET-1]+1 or self.BALLE[1] == self.P1_RACKET[0]-1):
                        if self.BALLE[1] == LIMLEFT+1 or self.BALLE[1] == LIMRIGHT-1:
                            balleApres = -directionX
                        else:
                            balleApres = directionX

                        directionY = -directionY

                        if (self.BALLE[1]+balleApres not in self.P1_RACKET):
                            self.P2_SCORE += 1
                            self.nextRound()
                            if self.P2_SCORE == self.SCORE_WIN:
                                self.fin = "P2"
                                break
                            continue

                # CONTACT ENTRE BALLE ET COIN
                if self.BALLE[1] == LIMLEFT+1 or self.BALLE[1] == LIMRIGHT-1 or (self.BALLE[0] == 1 and self.BALLE[1] == self.P2_RACKET[0]-1 and self.BALLE[1]+olddireX in self.P2_RACKET) or (self.BALLE[0] == 1 and self.BALLE[1] == self.P1_RACKET[0]-1 and self.BALLE[1]+olddireX in self.P1_RACKET) or (self.BALLE[0] == 13 and self.BALLE[1] == self.P1_RACKET[self.lenP1_RACKET-1]+1 and self.BALLE[1]+olddireX in self.P1_RACKET) or (self.BALLE[0] == 13 and self.BALLE[1] == self.P2_RACKET[self.lenP2_RACKET-1]+1 and self.BALLE[1] in self.P2_RACKET):
                        directionX = -directionX 
                
                self.arbalet.user_model.set_pixel(self.BALLE[0], self.BALLE[1], self.BG_COLOR)
                # MAJ POS
                self.BALLE[0] += directionY
                self.BALLE[1] += directionX

                # AFFICHAGE NEW POS
                self.arbalet.user_model.set_pixel(self.BALLE[0], self.BALLE[1], self.BALLE_COLOR)

                time.sleep(self.ballspeed)

                if self.ballspeed >= self.limspeed:
                    self.ballspeed -= self.ballspeed_increase

        if self.fin == 'P1':
            self.model.write("PLAYER 1 WINS!", self.P1_COLOR)
        if self.fin == 'P2':
            self.model.write("PLAYER 2 WINS!", self.P2_COLOR);
        #call(["python","-m","arbalet.apps.menu"])
        self.arbalet.close()
        exit()