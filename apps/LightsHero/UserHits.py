from pygame import event, time, key, KEYDOWN, KEYUP, K_F1, K_F2, K_F3, K_F4, K_F5, QUIT
from threading import Thread
from time import sleep

class UserHits(Thread):
    hit_window = {'easy': 0.2, 'medium': 0.18, 'difficult': 0.16, 'expert': 0.14 }
    # More precise hit window: https://raw.githubusercontent.com/fofix/fofix/master/doc/old/hitwindows.htm

    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.keys = [False]*5
        self.working = True
        self.clock = time.Clock()

    def stop(self):
        self.working = False

    def run(self):
        while self.working:
            self.keys = [key.get_pressed()[K_F1], key.get_pressed()[K_F2], key.get_pressed()[K_F3], key.get_pressed()[K_F4], key.get_pressed()[K_F5]]
            self.clock.tick(60)

    def get_pressed(self, num_lane):
        return self.keys[num_lane]
