from pygame import mixer
from os.path import join

class SoundManager():
    background = 'song.ogg'
    guitar = 'guitar.ogg'

    def __init__(self, path):
        mixer.init()
        mixer.music.load(join(path, self.background))
        self.guitar = mixer.Sound(join(path, self.guitar))
        self.started = False

    def start(self):
        self.started = True
        mixer.music.play()
        self.guitar.play()
        #self.play_drums()
        #self.play_bass()


