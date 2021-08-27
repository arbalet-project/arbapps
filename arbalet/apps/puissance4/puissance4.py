import random
from arbalet.core import Application, Rate
import pygame
import time
from subprocess import call

LEFT=(0,-1)
RIGHT=(0, 1)
LIMRIGHT = 8
LIMLEFT = 0

# Set up the joystick
pygame.joystick.init()

nbjoysticks = pygame.joystick.get_count()
joysticks = []
for i in range(nbjoysticks):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)

class Puissance4(Application):
    BG_COLOR = 'black'
    PLATEAU_COLOR = 'blue'
    P1_COLOR = 'yellow'
    P1_FLASHCOLOR = 'lightyellow'
    P2_FLASHCOLOR = 'crimson'
    P2_COLOR = 'red'
    P_COLOR = P1_COLOR
    RATE_SPEED = 1.5
    COLPLEINES = []
    CASESGAGNANTES = []
    
    def __init__(self):
        Application.__init__(self)
        self.PIECE = (8,4)
        self.TABJEU = [[0] * 7 for _ in range(6)]
        self.DIRECTION = (0,0)
        self.fin = False
        self.rate = Rate(self.RATE_SPEED)
        self.player_actu = True

    def run(self):
        self.init_grille()
        self.deroulementJeu()
        if self.fin == 'draw':
            self.model.flash()
            self.model.write("DRAW!", 'deeppink')
        elif self.fin == 'J1':
            self.animationWin(self.fin)
            self.model.write("YELLOW WINS!", self.P1_COLOR)
        elif self.fin == 'J2':
            self.animationWin(self.fin)
            self.model.write("RED WINS!", self.P2_COLOR)

        call(["python","-m","arbalet.apps.menu"])
        self.arbalet.close()
        exit()

    def process_events(self):
        new_dir=None
        while 1:
            for event in self.arbalet.events.get():
                key = pygame.key.get_pressed()
                if(len(joysticks)>=1):
                    # Joystick control
                    if event.type==pygame.JOYAXISMOTION:
                        if joysticks[0].get_axis(0) > 0:
                                new_dir = RIGHT
                        if joysticks[0].get_axis(0) < 0:
                                new_dir = LEFT
                    if joysticks[0].get_button(0) or joysticks[0].get_button(1):
                        new_dir = (0,0)
                        self.DIRECTION=new_dir
                        break
                if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                    if key[pygame.K_q]:
                        self.fin = 'QUIT'
                        break
                    if event.key==pygame.K_RIGHT:
                        new_dir = RIGHT
                    elif event.key==pygame.K_LEFT:
                        new_dir = LEFT
                    elif event.key==pygame.K_DOWN:
                        new_dir = (0,0)
                        self.DIRECTION=new_dir
                        break
                if event.type==pygame.JOYHATMOTION:
                    if event.value[1]==-1:
                        new_dir = (0,0)
                        self.DIRECTION=new_dir
                        break
                    if event.value[0]==1:
                        new_dir = RIGHT
                    elif event.value[0]==-1:
                        new_dir = LEFT
                
            if new_dir is not None:
                if (self.PIECE[1]+new_dir[1]) == LIMRIGHT or (self.PIECE[1]+new_dir[1]) == LIMLEFT:
                    new_dir = None
                else:
                    self.DIRECTION=new_dir
                    break

    def wait_for_timeout_or_event(self, allow_events=True):
        t0 = time.time()
        while time.time()-t0 < 1./self.RATE_SPEED:
            time.sleep(0.07)
            if allow_events and self.process_events():
                return

    def init_grille(self):
        self.arbalet.user_model.set_all(self.BG_COLOR)
        for lig in range(9,15): 
            for col in range(1,8):
                self.arbalet.user_model.set_pixel(lig, col, self.PLATEAU_COLOR)
        self.arbalet.user_model.set_pixel(self.PIECE[0], self.PIECE[1], self.P_COLOR)

    def deroulementJeu(self):
        while 1:
            while 1:
                self.wait_for_timeout_or_event()
                if (self.DIRECTION[0] == 0 and self.DIRECTION[1] == 0):
                    break
                else:
                   self.model.set_pixel(self.PIECE[0],self.PIECE[1],self.BG_COLOR)

                new_pos=(self.PIECE[0]+self.DIRECTION[0], self.PIECE[1]+self.DIRECTION[1])
                self.PIECE=new_pos
                self.model.set_pixel(self.PIECE[0],self.PIECE[1],self.P_COLOR)

            self.set_piece()

            testFin = self.game_over()
            if testFin is not False:
                self.fin = testFin
                break
            elif self.fin == 'draw':
                break

                    
    def set_piece(self):
        coltabjeu = self.PIECE[1]-1
        if coltabjeu not in self.COLPLEINES:
            lignetabjeu = 5
            while self.TABJEU[lignetabjeu][coltabjeu] != 0:
                if lignetabjeu == 0:
                    self.COLPLEINES.append(coltabjeu) 
                    break
                lignetabjeu -= 1

            if lignetabjeu >= 0:
                col = self.PIECE[1]
                ligne = lignetabjeu+9

                if lignetabjeu == 0:
                    self.COLPLEINES.append(coltabjeu)
                    if len(self.COLPLEINES) == 7:
                        self.fin = 'draw'

                self.model.set_pixel(self.PIECE[0],col,self.BG_COLOR)
                self.model.set_pixel(self.PIECE[0]+1,col,self.P_COLOR)
                time.sleep(0.1)    

                for i in range(9,ligne):
                    self.model.set_pixel(i,col,self.PLATEAU_COLOR)
                    self.model.set_pixel(i+1,col,self.P_COLOR)
                    time.sleep(0.1)    

                self.player_actu = not self.player_actu

                if(self.player_actu):
                    self.P_COLOR = self.P1_COLOR
                    self.TABJEU[lignetabjeu][coltabjeu] = 'J2'
                else:
                    self.P_COLOR = self.P2_COLOR
                    self.TABJEU[lignetabjeu][coltabjeu] = 'J1'

                self.model.set_pixel(self.PIECE[0],col,self.P_COLOR)

    def animationWin(self,joueur):
        if joueur == 'J1':
            coulJ = self.P1_COLOR
            coulAlt = self.P1_FLASHCOLOR
        elif joueur == 'J2':
            coulJ = self.P2_COLOR
            coulAlt = self.P2_FLASHCOLOR
        
        for i in range(6):
                for case in self.CASESGAGNANTES:
                    self.arbalet.user_model.set_pixel(case[0]+9, case[1]+1, coulAlt)
                    self.arbalet.user_model.set_pixel(case[0]+9, case[1]+1, coulAlt)
                time.sleep(0.3)
                for case in self.CASESGAGNANTES:
                    self.arbalet.user_model.set_pixel(case[0]+9, case[1]+1, coulJ)
                    self.arbalet.user_model.set_pixel(case[0]+9, case[1]+1, coulJ)
                time.sleep(0.3)
                    


    def game_over(self):
        for ligne in range(6):
            for col in range(7):
                if self.TABJEU[ligne][col] == 'J1': 
                    if col < 4:
                         #Parcours droite
                        if self.TABJEU[ligne][col+1] == 'J1' and self.TABJEU[ligne][col+2] == 'J1' and self.TABJEU[ligne][col+3] == 'J1':
                            self.CASESGAGNANTES = [(ligne,col),(ligne,col+1),(ligne,col+2),(ligne,col+3)]
                            return 'J1'
                    if ligne < 3 and col < 4:
                        #Parcours diag bas droite
                        if self.TABJEU[ligne+1][col+1] == 'J1' and self.TABJEU[ligne+2][col+2] == 'J1' and self.TABJEU[ligne+3][col+3] == 'J1':
                            self.CASESGAGNANTES = [(ligne,col),(ligne+1,col+1),(ligne+2,col+2),(ligne+3,col+3)]
                            return 'J1'
                    if ligne < 3:
                        #Parcours bas
                        if self.TABJEU[ligne+1][col] == 'J1' and self.TABJEU[ligne+2][col] == 'J1' and self.TABJEU[ligne+3][col] == 'J1':
                            self.CASESGAGNANTES = [(ligne,col),(ligne+1,col),(ligne+2,col),(ligne+3,col)]
                            return 'J1'
                    if col > 2 and ligne < 3 :
                        #parcours diag bas gauche
                        if self.TABJEU[ligne+1][col-1] == 'J1' and self.TABJEU[ligne+2][col-2] == 'J1' and self.TABJEU[ligne+3][col-3] == 'J1':
                            self.CASESGAGNANTES = [(ligne,col),(ligne+1,col-1),(ligne+2,col-2),(ligne+3,col-3)]
                            return 'J1'
                if self.TABJEU[ligne][col] == 'J2':
                    if col < 4:
                         #Parcours droite
                        if self.TABJEU[ligne][col+1] == 'J2' and self.TABJEU[ligne][col+2] == 'J2' and self.TABJEU[ligne][col+3] == 'J2':
                            self.CASESGAGNANTES = [(ligne,col),(ligne,col+1),(ligne,col+2),(ligne,col+3)]
                            return 'J2'
                    if ligne < 3 and col < 4:
                        #Parcours diag bas droite
                        if self.TABJEU[ligne+1][col+1] == 'J2' and self.TABJEU[ligne+2][col+2] == 'J2' and self.TABJEU[ligne+3][col+3] == 'J2': 
                            self.CASESGAGNANTES = [(ligne,col),(ligne+1,col+1),(ligne+2,col+2),(ligne+3,col+3)]
                            return 'J2'
                    if ligne < 3:
                        #Parcours bas
                        if self.TABJEU[ligne+1][col] == 'J2' and self.TABJEU[ligne+2][col] == 'J2' and self.TABJEU[ligne+3][col] == 'J2': 
                            self.CASESGAGNANTES = [(ligne,col),(ligne+1,col),(ligne+2,col),(ligne+3,col)]
                            return 'J2'
                    if col > 2 and ligne < 3 :
                        #parcours diag bas gauche
                        if self.TABJEU[ligne+1][col-1] == 'J2' and self.TABJEU[ligne+2][col-2] == 'J2' and self.TABJEU[ligne+3][col-3] == 'J2': 
                            self.CASESGAGNANTES = [(ligne,col),(ligne+1,col-1),(ligne+2,col-2),(ligne+3,col-3)]
                            return 'J2'
        return False
        


