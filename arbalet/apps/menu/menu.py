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

class Menu(Application):

    BG_COLOR = 'black'
    BTN_COLOR = 'green'

    def __init__(self):
        Application.__init__(self)
        pygame.init()
        self.fin = False
        self.games = ['pong','puissance4','tetris']
        self.indiceGame = 0
        self.choix = self.games[self.indiceGame]
        self.PLATEAU_COLOR = 'blue'
        self.launch = False

    def run(self):
        self.init_grille()
        
        t2 = thread.start_new_thread(self.preview_game,("preview_game", ))
        t2 = thread.start_new_thread(self.process_events,("process_events", ))    

        while 1:
            pass

        arbalet.close()

    def preview_game(self,threadName):
        while self.fin == False:
            self.clear_preview()
            if self.choix == "pong":
                ligne1 = 3
                ligne2 = 9
                dirX = 1
                dirY = 1
                BALLE = [ligne2-3,5]
                retour = True;
                while self.choix == "pong":
                    if retour or BALLE[0] == ligne2-1 or BALLE[0] == ligne1+1:
                        self.arbalet.user_model.set_pixel(ligne1, 7, self.BG_COLOR)
                        self.arbalet.user_model.set_pixel(ligne1, 8, self.BG_COLOR)
                        self.arbalet.user_model.set_pixel(ligne2, 1, self.BG_COLOR)
                        self.arbalet.user_model.set_pixel(ligne2, 2, self.BG_COLOR)

                        for i in range(3,7):
                            self.arbalet.user_model.set_pixel(ligne1, i, 'red')
                            self.arbalet.user_model.set_pixel(ligne2, i, 'blue')

                        retour = False
                    self.arbalet.user_model.set_pixel(BALLE[0], BALLE[1], self.BG_COLOR)
                    if (BALLE[0] == ligne1+1) or (BALLE[0] == ligne2-1):
                        retour = False    
                        dirY = -dirY
                        dirX = -dirX

                    if (BALLE[0] == ligne1+2):
                        self.arbalet.user_model.set_pixel(ligne1, 4, self.BG_COLOR)
                        self.arbalet.user_model.set_pixel(ligne1, 3, self.BG_COLOR)
                        for i in range(5,9):
                            self.arbalet.user_model.set_pixel(ligne1, i, 'red')

                    if (BALLE[0] == ligne2-2):
                        self.arbalet.user_model.set_pixel(ligne2, 5, self.BG_COLOR)
                        self.arbalet.user_model.set_pixel(ligne2, 6, self.BG_COLOR)
                        for i in range(1,5):
                            self.arbalet.user_model.set_pixel(ligne2, i, 'blue')
                            
                    BALLE[0] += dirY
                    BALLE[1] -= dirX

                    self.arbalet.user_model.set_pixel(BALLE[0], BALLE[1], 'white')
                    time.sleep(0.5)

            self.clear_preview()
                
            while self.choix == "puissance4":
                colorp1 = 'yellow'
                colorp2 = 'red'
                col = 4
                ligne = 10
                for lig in range(4,10): 
                    for colo in range(2,8):
                        self.arbalet.user_model.set_pixel(lig, colo, self.PLATEAU_COLOR)    
                
                while ligne > 3 or self.choix == "puissance4": 
                    self.model.set_pixel(3,col,colorp1)
                    time.sleep(0.16)
                    self.model.set_pixel(3,col,self.BG_COLOR)
                    for lig in range(4,ligne):
                        self.model.set_pixel(lig,col,colorp1)
                        if lig != 4:
                            self.model.set_pixel(lig-1,col,'blue')
                        time.sleep(0.16)
                    if ligne == 7 or self.choix != "puissance4":
                        break
                    self.model.set_pixel(3,col+1,colorp2)
                    time.sleep(0.16)
                    self.model.set_pixel(3,col+1,self.BG_COLOR)
                    for lig in range(4,ligne):
                        self.model.set_pixel(lig,col+1,colorp2)
                        if lig != 4:
                            self.model.set_pixel(lig-1,col+1,'blue')
                        time.sleep(0.16)
                    ligne -= 1
                if self.choix == "puissance4":
                    for i in range(3):
                        for i in range(0,4):
                            self.model.set_pixel(lig+i,col,'lightyellow')
                        time.sleep(0.16)
                        for i in range(0,4):
                            self.model.set_pixel(lig+i,col,colorp1)
                        time.sleep(0.16)
            print self.choix
            print self.indiceGame
            if self.choix == "snake":
                HEAD=(5,5)
                queue=[self.HEAD]
                pass

            while self.choix == "tetris":
                self.clear_preview()

                for i in range (0,10):
                    if self.choix != "tetris":
                        break
                    self.model.set_pixel(i+1,4,'deeppink')
                    self.model.set_pixel(i,5,'deeppink')
                    self.model.set_pixel(i+1,5,'deeppink')
                    self.model.set_pixel(i+1,6,'deeppink')
                    if i> 0:
                        self.model.set_pixel(i-1,5,self.BG_COLOR)
                        self.model.set_pixel(i,4,self.BG_COLOR)
                        self.model.set_pixel(i,6,self.BG_COLOR)
                    time.sleep(0.16)

                for i in range(0,7):
                    if self.choix != "tetris":
                        break
                    self.model.set_pixel(i,2,'green')
                    self.model.set_pixel(i,3,'green')
                    self.model.set_pixel(i+1,3,'green')
                    self.model.set_pixel(i+1,4,'green')
                    if i> 0:
                        self.model.set_pixel(i-1,2,self.BG_COLOR)
                        self.model.set_pixel(i-1,3,self.BG_COLOR)
                    self.model.set_pixel(i,4,self.BG_COLOR)

                    time.sleep(0.16)


                self.model.set_pixel(6,2,self.BG_COLOR)
                self.model.set_pixel(6,3,self.BG_COLOR)

                for i in range(7,9):
                    if self.choix != "tetris":
                        break
                    self.model.set_pixel(i,4,'green')
                    self.model.set_pixel(i+1,3,'green')
                    self.model.set_pixel(i+1,4,'green')
                    self.model.set_pixel(i+2,3,'green')
                    if i> 0:
                        self.model.set_pixel(i-1,4,self.BG_COLOR)
                        self.model.set_pixel(i,3,self.BG_COLOR)

                    time.sleep(0.16)



                for i in range (0,10):
                    if self.choix != "tetris":
                        break
                    self.model.set_pixel(i+1,0,'orangered')
                    self.model.set_pixel(i+1,1,'orangered')
                    self.model.set_pixel(i+1,2,'orangered')
                    self.model.set_pixel(i,2,'orangered')

                    if i> 0:
                        self.model.set_pixel(i-1,2,self.BG_COLOR)

                    self.model.set_pixel(i,0,self.BG_COLOR)
                    self.model.set_pixel(i,1,self.BG_COLOR)

                    time.sleep(0.16)


                for i in range (0,8):
                    if self.choix != "tetris":
                        break
                    self.model.set_pixel(i,9,'yellow')
                    self.model.set_pixel(i+1,9,'yellow')
                    self.model.set_pixel(i+2,9,'yellow')
                    self.model.set_pixel(i+3,9,'yellow')

                    if i> 0:
                        self.model.set_pixel(i-1,9,self.BG_COLOR)

                    time.sleep(0.16)


                for i in range (0,10):
                    if self.choix != "tetris":
                        break
                    self.model.set_pixel(i,7,'cyan')
                    self.model.set_pixel(i,8,'cyan')
                    self.model.set_pixel(i+1,7,'cyan')
                    self.model.set_pixel(i+1,8,'cyan')

                    if i> 0:
                        self.model.set_pixel(i-1,7,self.BG_COLOR)
                        self.model.set_pixel(i-1,8,self.BG_COLOR)

                    time.sleep(0.16)



    def clear_preview(self):
        for lig in range(0,12): 
            for col in range(0,10):
                self.arbalet.user_model.set_pixel(lig, col, self.BG_COLOR)


    def process_events(self, threadName):
        new_dir=None
        while self.fin == False:
            for event in self.arbalet.events.get():
                key = pygame.key.get_pressed();
                if event.type == pygame.QUIT:
                        self.fin = 'QUIT'
                        break
                if event.type==pygame.JOYAXISMOTION:
                    if joysticks[0].get_axis(0) > 0:
                        new_dir = RIGHT
                        print "droite"
                        break
                    if joysticks[0].get_axis(0) < 0:
                        print "gauche"
                        new_dir = LEFT
                        break

                if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    if event.key==pygame.K_RIGHT:
                        new_dir = RIGHT
                        print "droite"
                        break

                    elif event.key==pygame.K_LEFT:
                        new_dir = LEFT
                        print "gauche"
                        break

                elif event.type==pygame.JOYHATMOTION:
                    if event.value[0]==1:
                        new_dir = RIGHT
                        print "droite"
                        break
                    elif event.value[0]==-1:
                        new_dir = LEFT
                        print "gauche"
                        break
                if key[pygame.K_p]:
                    self.launch = True


            if new_dir is not None :     
                if self.indiceGame == len(self.games)-1 and new_dir == RIGHT:
                    self.indiceGame = 0
                elif self.indiceGame == 0 and new_dir == LEFT:
                    self.indiceGame = len(self.games)-1
                else:
                    self.indiceGame += new_dir
                new_dir=None
                self.choix = self.games[self.indiceGame]

            if self.launch:
                self.arbalet.close()
                self.launchGame()

            time.sleep(1.2)

    def launchGame(self):
        call(["python","-m","arbalet.apps."+self.choix])



    def init_grille(self):
        self.arbalet.user_model.set_all(self.BG_COLOR)

        self.arbalet.user_model.set_pixel(14, 4, 'yellow')
        self.arbalet.user_model.set_pixel(14, 5, 'yellow')
        self.arbalet.user_model.set_pixel(13, 4, 'yellow')
        self.arbalet.user_model.set_pixel(13, 5, 'yellow')

        self.arbalet.user_model.set_pixel(14, 0, self.BTN_COLOR)
        self.arbalet.user_model.set_pixel(14, 1, self.BTN_COLOR)
        self.arbalet.user_model.set_pixel(13, 0, self.BTN_COLOR)
        self.arbalet.user_model.set_pixel(13, 1, self.BTN_COLOR)

        self.arbalet.user_model.set_pixel(14, 9, self.BTN_COLOR)
        self.arbalet.user_model.set_pixel(14, 8, self.BTN_COLOR)
        self.arbalet.user_model.set_pixel(13, 8, self.BTN_COLOR)
        self.arbalet.user_model.set_pixel(13, 9, self.BTN_COLOR)
        