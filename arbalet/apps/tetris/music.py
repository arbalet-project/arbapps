from os.path import join, realpath, dirname
from pygame import mixer
from time import sleep

class Music(object):
    # Music files for each level 1, 2, 3+...
    files = ['Cailloux_-_tetris.ogg',
             'ExDeath_-_Another_Tetris_Remix.ogg',
             'Mic_-_Mic_music_tetris__.ogg']

    def __init__(self):
        mixer.init()
        self.level = 0
        self.loops = 0  # -1 to repeat the music
        path = join(dirname(__file__), 'music')
        self.sounds = [mixer.Sound(realpath(join(path, file))) for file in self.files]
        # Start playing the first level
        self.play()

    def play(self):
        channel = self.sounds[self.level].play(loops=self.loops)
        sleep(0.25)
        if not channel.get_busy():
            print("Error: unable to play file {}".format(self.files[self.level]))

    def level_end(self):
        self.sounds[self.level].fadeout(5000)

    def game_over(self):
        self.level_end()

    def level_up(self):
        self.level = min(self.level + 1, len(self.sounds) - 1)
        self.play()
