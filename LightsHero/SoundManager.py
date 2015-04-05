from pygame import mixer, init
from threading import Thread
from time import sleep

class SoundManager(Thread):
    background = '/song.ogg'
    guitar = '/guitar.ogg'

    def __init__(self, path, delay):
        Thread.__init__(self)
        self.setDaemon(True)
        self.delay = delay
        init()
        mixer.init()
        mixer.music.load(path+self.background)
        self.guitar = mixer.Sound(path+self.guitar)

    def run(self):
        sleep(self.delay)
        mixer.music.play()
        self.guitar.play()
        #self.play_drums()
        #self.play_bass()
        while True:
            sleep(1)

