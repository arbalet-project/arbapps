from os.path import join, realpath, dirname
from pygame import mixer
from threading import Thread

class Music(object):
    # Music files for each level 1, 2, 3+...
    files = ['Cailloux_-_tetris.ogg',
             'ExDeath_-_Another_Tetris_Remix.ogg',
             'Mic_-_Mic_music_tetris__.ogg']

    def __init__(self):
        mixer.init()
        self.level = 0
        self.loops = 0  # -1 to repeat the music
        self.path = join(dirname(__file__), 'music')
        self.sounds = [None for file in self.files]
        # Start loading (slow on RPi, thus threaded)
        self.loader = Thread(target=self.load_and_play)
        self.loader.daemon = True
        self.loader.start()

    def load_and_play(self):
        # Load the first level
        self.sounds[0] = mixer.Sound(realpath(join(self.path, self.files[0])))
        # Start playing the first level
        self.play()
        # Load the rest
        for id, file in enumerate(self.files[1:]):
            self.sounds[id + 1] = mixer.Sound(realpath(join(self.path, file)))

    def play(self):
        if self.sounds[self.level] is not None:
            self.sounds[self.level].play(loops=self.loops)

    def level_end(self):
        if self.sounds[self.level] is not None:
            self.sounds[self.level].fadeout(5000)

    def game_over(self):
        self.level_end()

    def level_up(self):
        self.level = min(self.level + 1, len(self.sounds) - 1)
        self.play()

