import random
from arbalet.core import Application, Rate
import pygame
import time
import thread
from arbalet.colors import mul, hsv_to_rgb

LEFT=(0,-1)
RIGHT=(0, 1)
DOWN=(1, 0)
UP=(-1, 0)
STOP=(0,0)

# Set up the joystick
pygame.joystick.init()

nbjoysticks = pygame.joystick.get_count()
joysticks = []
for i in range(nbjoysticks):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)

class Bomb():
    def __init__(self, cord, player):
        self.active = False
        self.timer = 0
        self.player = player
        self.cord = cord

class Player():
    def __init__(self, pos, number, color):
        self.alive = True
        self.direction = STOP
        self.pos = pos
        self.number = number
        self.color = color


class Bomberman(Application):
    BG_COLOR = 'black'
    WALL = 'grey'
    COLORBOMB = 'orange'
    DETONATEBOMB = 'orangered'


    def __init__(self, touch_mode='quadridirectional'):
        Application.__init__(self, touch_mode=touch_mode)
        self.pierres = []

        self.bomb1= Bomb((0,0),1)
        self.bomb2= Bomb((0,0),2)
        self.bomb3= Bomb((0,0),3)
        self.bomb4= Bomb((0,0),4)
        self.bomb5= Bomb((0,0),1)
        self.bomb6= Bomb((0,0),2)
        self.bomb7= Bomb((0,0),3)
        self.bomb8= Bomb((0,0),4)
        self.bomb9= Bomb((0,0),1)
        self.bomb10= Bomb((0,0),2)
        self.bomb11= Bomb((0,0),3)
        self.bomb12= Bomb((0,0),4)

        self.slotbombs = [self.bomb1,self.bomb2,self.bomb3,self.bomb4,self.bomb5,self.bomb6,self.bomb7,self.bomb8,self.bomb9,self.bomb10,self.bomb11,self.bomb12]
        self.bombs = []
        for i in range (1,self.height,2):
                    for j in range(self.width):
                        if(j==1 or j==3 or j==6 or j==8):
                            self.pierres.append((i,j))


        self.p1 = Player((14,5),1,'cyan')
        self.p2 = Player((0,4),2,'darkblue')
        self.p3 = Player((6,0),3,'green')
        self.p4 = Player((8,9),4,'purple')

    def process_events(self):
        new_dir1=None
        new_dir2=None
        new_dir3=None
        new_dir4=None
        for event in self.arbalet.events.get():
            key = pygame.key.get_pressed()

            if(len(joysticks)>=1):
                if(self.p1.alive):
                    # Joystick control
                    if event.type==pygame.JOYAXISMOTION:
                            if joysticks[0].get_axis(1) < 0 and  not(joysticks[0].get_axis(0) < 0 or joysticks[0].get_axis(0) > 0) and self.p1.pos[0]!=0:
                                new_dir1 = UP
                            if joysticks[0].get_axis(1) > 0 and not(joysticks[0].get_axis(0) < 0 or joysticks[0].get_axis(0) > 0) and self.p1.pos[0]!=14:
                                new_dir1 = DOWN
                            if joysticks[0].get_axis(0) > 0 and self.p1.pos[1]!=9:
                                new_dir1 = RIGHT
                            if joysticks[0].get_axis(0) < 0 and self.p1.pos[1]!=0:
                                new_dir1 = LEFT
                    if joysticks[0].get_button(0) or joysticks[0].get_button(1):
                        self.poserBombe(self.p1)

            if(len(joysticks)>=2):
                if(self.p2.alive):
                    if event.type==pygame.JOYAXISMOTION:
                            if joysticks[1].get_axis(1) > 0 and self.p2.pos[0]!=0:
                                new_dir2 = UP
                            if joysticks[1].get_axis(1) < 0 and self.p2.pos[0]!=14:
                                new_dir2 = DOWN
                            if joysticks[1].get_axis(0) < 0 and not(joysticks[1].get_axis(1) < 0 or joysticks[1].get_axis(1) > 0) and self.p2.pos[1]!=9:
                                new_dir2 = RIGHT
                            if joysticks[1].get_axis(0) > 0 and not(joysticks[1].get_axis(1) < 0 or joysticks[1].get_axis(1) > 0) and self.p2.pos[1]!=0:
                                new_dir2 = LEFT
                    if joysticks[1].get_button(0) or joysticks[1].get_button(1):
                        self.poserBombe(self.p2)

            if(len(joysticks)>=3):
                if(self.p3.alive):
                    # Joystick control
                    if event.type==pygame.JOYAXISMOTION:
                            if joysticks[2].get_axis(0) < 0  and self.p3.pos[0]!=0:
                                new_dir3 = UP
                            if joysticks[2].get_axis(0) > 0  and self.p3.pos[0]!=14:
                                new_dir3 = DOWN 
                            if joysticks[2].get_axis(1) < 0 and not(joysticks[2].get_axis(0) < 0 or joysticks[2].get_axis(0) > 0) and self.p3.pos[1]!=9:
                                new_dir3 = RIGHT
                            if joysticks[2].get_axis(1) > 0 and not(joysticks[2].get_axis(0) < 0 or joysticks[2].get_axis(0) > 0) and self.p3.pos[1]!=0:
                                new_dir3 = LEFT
                    if joysticks[2].get_button(0) or joysticks[2].get_button(1):
                        self.poserBombe(self.p3)

            if(len(joysticks)>=4):
                if(self.p4.alive):
                    # Joystick control
                    if event.type==pygame.JOYAXISMOTION:
                            if joysticks[3].get_axis(0) > 0 and not(joysticks[3].get_axis(1) < 0 or joysticks[3].get_axis(1) > 0) and self.p4.pos[0]!=0:
                                new_dir4 = UP
                            if joysticks[3].get_axis(0) < 0 and not(joysticks[3].get_axis(1) < 0 or joysticks[3].get_axis(1) > 0) and self.p4.pos[0]!=14:
                                new_dir4 = DOWN 
                            if joysticks[3].get_axis(1) > 0 and self.p4.pos[1]!=9:
                                new_dir4 = RIGHT
                            if joysticks[3].get_axis(1) < 0 and self.p4.pos[1]!=0:
                                new_dir4 = LEFT
                    if joysticks[3].get_button(0) or joysticks[3].get_button(1):
                        self.poserBombe(self.p4)


            # # Keyboard control
            if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if(self.p1.alive):
                    if key[pygame.K_UP] and self.p1.pos[0]!=0:
                        new_dir1=UP
                    elif key[pygame.K_DOWN] and self.p1.pos[0]!=14:
                        new_dir1=DOWN
                    elif key[pygame.K_RIGHT] and self.p1.pos[1]!=9:
                        new_dir1 = RIGHT
                    elif key[pygame.K_LEFT] and self.p1.pos[1]!=0:
                        new_dir1 = LEFT
                    if key[pygame.K_p]:
                        self.poserBombe(self.p1)

                if(self.p2.alive):
                    if key[pygame.K_z] and self.p2.pos[0]!=0:
                        new_dir2=UP
                    elif key[pygame.K_s] and self.p2.pos[0]!=14:
                        new_dir2=DOWN
                    elif key[pygame.K_d] and self.p2.pos[1]!=9:
                        new_dir2 = RIGHT
                    elif key[pygame.K_q] and self.p2.pos[1]!=0:
                        new_dir2 = LEFT
                    if key[pygame.K_a]:
                        self.poserBombe(self.p2)

            #If you are using the cross instead of the joystick with your pad
            # if event.type==pygame.JOYHATMOTION:
            #     if event.value[1]==1 and self.p3.pos[0]!=0:
            #         new_dir3 = UP
            #     elif event.value[1]==-1 and self.p3.pos[0]!=14:
            #         new_dir3 = DOWN
            #     elif event.value[0]==1 and self.p3.pos[1]!=9:
            #         new_dir3 = RIGHT
            #     elif event.value[0]==-1 and self.p3.pos[1]!=0:
            #         new_dir3 = LEFT
                    # if event.type == pygame.JOYBUTTONDOWN:
                    #     self.poserBombe(self.p3)

        if new_dir1 is not None:
            new_p1=((self.p1.pos[0]+new_dir1[0])%self.height, (self.p1.pos[1]+new_dir1[1])%self.width)
            if new_p1 not in self.pierres and new_p1 not in self.bombs and new_p1 != self.p2.pos and new_p1 != self.p3.pos and new_p1 != self.p4.pos:
                self.p1.direction=new_dir1
            else:
                self.p1.direction=STOP
        else:
            self.p1.direction=STOP

        if new_dir2 is not None:
            new_p2=((self.p2.pos[0]+new_dir2[0])%self.height, (self.p2.pos[1]+new_dir2[1])%self.width)
            if new_p2 not in self.pierres and new_p2 not in self.bombs and new_p2 != self.p1.pos and new_p2 != self.p3.pos and new_p2 != self.p4.pos:
                self.p2.direction=new_dir2
            else:
                self.p2.direction=STOP
        else:
            self.p2.direction=STOP


        if new_dir3 is not None:
            new_p3=((self.p3.pos[0]+new_dir3[0])%self.height, (self.p3.pos[1]+new_dir3[1])%self.width)
            if new_p3 not in self.pierres and new_p3 not in self.bombs and new_p3 != self.p1.pos and new_p3 != self.p2.pos  and new_p3 != self.p4.pos:
                self.p3.direction=new_dir3
            else:
                self.p3.direction=STOP
        else:
            self.p3.direction=STOP

        if new_dir4 is not None:
            new_p4=((self.p4.pos[0]+new_dir4[0])%self.height, (self.p4.pos[1]+new_dir4[1])%self.width)
            if new_p4 not in self.pierres and new_p4 not in self.bombs and new_p4 != self.p1.pos and new_p4 != self.p2.pos and new_p4 != self.p3.pos:
                self.p4.direction=new_dir4
            else:
                self.p4.direction=STOP
        else:
            self.p4.direction=STOP

    def poserBombe(self, player):
        newbombs = []
        for bomb in self.slotbombs:
            if bomb.player == player.number:
                newbombs.append(bomb)
        for bomb in newbombs:
            if not bomb.active:
                if(self.bombAlreadySet(player)):
                    bomb.active = True
                    self.bombs.append((player.pos[0],player.pos[1]))
                    bomb.cord = (player.pos[0],player.pos[1])
                    break

    def bombAlreadySet(self, player):
        if player.pos in self.bombs:
            return False
        else:
            return True
            
    def animateBombe(self,threadName):
        ColorsBomb =['darkred','red','orange','yellow','white']
        while True:
            for b in self.slotbombs:
                if b.active:
                    if b.timer < 1.5:
                        self.model.set_pixel(b.cord[0],b.cord[1],self.DETONATEBOMB)
                        time.sleep(0.2)
                        self.model.set_pixel(b.cord[0],b.cord[1],self.COLORBOMB)
                        b.timer+=0.2*len(self.bombs)
                    else:
                        okH = True
                        okB = True
                        okG = True
                        okD = True
                        suprBomb = [b.cord]
                        for i in range(1,6):
                            #Haut
                            if okH and b.cord[0]-i >= 0 and (b.cord[0]-i,b.cord[1]) not in self.pierres:
                                self.model.set_pixel(b.cord[0]-i,b.cord[1],ColorsBomb[i-1])
                                suprBomb.append((b.cord[0]-i,b.cord[1]))
                            else:
                                okH = False
                            #Bas
                            if okB and b.cord[0]+i <= 14 and (b.cord[0]+i,b.cord[1]) not in self.pierres:
                                self.model.set_pixel(b.cord[0]+i,b.cord[1],ColorsBomb[i-1])
                                suprBomb.append((b.cord[0]+i,b.cord[1]))
                            else:
                                okB = False
                            #Gauche
                            if okG and b.cord[1]-i >= 0 and (b.cord[0],b.cord[1]-i) not in self.pierres:
                                self.model.set_pixel(b.cord[0],b.cord[1]-i,ColorsBomb[i-1])
                                suprBomb.append((b.cord[0],b.cord[1]-i))
                            else:
                                okG = False
                            #Droite
                            if okD and b.cord[1]+i <= 9 and (b.cord[0],b.cord[1]+i) not in self.pierres:
                                self.model.set_pixel(b.cord[0],b.cord[1]+i,ColorsBomb[i-1])
                                suprBomb.append((b.cord[0],b.cord[1]+i))
                            else:
                                okD = False
                            time.sleep(0.1)
                        if self.p1.pos in suprBomb:
                            self.p1.alive = False
                            self.p1.pos=None
                        if self.p2.pos in suprBomb:
                            self.p2.alive = False
                            self.p2.pos=None
                        if self.p3.pos in suprBomb:
                            self.p3.alive = False
                            self.p3.pos=None
                        if self.p4.pos in suprBomb:
                            self.p4.alive = False
                            self.p4.pos=None
                        time.sleep(0.2)
                        for supr in suprBomb:
                            self.model.set_pixel(supr[0],supr[1],self.BG_COLOR)
                        self.bombs.pop(0)
                        b.timer = 0
                        b.active = False

    def updatePlayer(self, player):
        new_p=((player.pos[0]+player.direction[0])%self.height, (player.pos[1]+player.direction[1])%self.width)
        if(player.direction!=STOP and player.pos not in self.bombs):
            self.model.set_pixel(player.pos[0], player.pos[1], self.BG_COLOR)
        player.pos=new_p
        self.model.set_pixel(new_p[0],new_p[1],player.color)
        if player.pos in self.bombs:
            self.model.set_pixel(new_p[0],new_p[1],self.COLORBOMB)

    def isOver(self, players):
        alive = 0
        for player in players:
            if player.alive:
                alive +=1
                possibleWinner = player
        if alive == 0:
            return True
        elif alive == 1:
            return possibleWinner
        elif alive >= 2:
            return False

    def run(self):
        self.model.set_pixel(self.p1.pos[0],self.p1.pos[1],self.p1.color)
        self.model.set_pixel(self.p2.pos[0],self.p2.pos[1],self.p2.color)
        self.model.set_pixel(self.p3.pos[0],self.p3.pos[1],self.p3.color)
        self.model.set_pixel(self.p4.pos[0],self.p4.pos[1],self.p4.color)

        t1 = thread.start_new_thread(self.animateBombe,("animateBombe",))

        rate = Rate(2)

        for i in range (1,self.height,2):
            for j in range(self.width):
                if(j==1 or j==3 or j==6 or j==8):
                    self.model.set_pixel(i,j,self.WALL)

        while True:
            self.process_events()
                
            if(self.p1.alive):
                self.updatePlayer(self.p1)

            if(self.p2.alive):
                self.updatePlayer(self.p2)

            if(self.p3.alive):
                self.updatePlayer(self.p3)

            if(self.p4.alive):
                self.updatePlayer(self.p4)

            isOver = self.isOver([self.p1,self.p2,self.p3,self.p4])
            if(isOver is not False):
                self.game_over(isOver)
                break
    
        exit()


    def game_over(self, winner):
        print("Game OVER")
        self.model.flash()
        if(winner is True):
            self.model.write("DRAW", 'white')
        else:
            self.model.write("P" + str(winner.number) + " WINS", winner.color)

