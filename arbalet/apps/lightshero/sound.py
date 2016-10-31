from pygame import mixer
from os.path import join

class SoundManager():
    background = 'song.ogg'
    guitar = 'guitar.ogg'

    def __init__(self, path):
        mixer.init()
        mixer.music.load(join(path, self.background))

        # Mutable sound tracks (muted if the player is wrong)
        self.tracks = {'guitar': mixer.Sound(join(path, self.guitar)),
                       'drums' : None,
                       'bass': None}
        self.started = False
        self.guitar_muted = False

    def start(self):
        self.started = True

        # Start background music
        mixer.music.play()

        # Start tracks
        for name, track in self.tracks.items():
            if track:
                track.play()

    def set_playing_well(self, playing_well):
        if self.guitar_muted and playing_well:
            self.tracks['guitar'].set_volume(1)
            self.guitar_muted = False
        elif not self.guitar_muted and not playing_well:
            self.tracks['guitar'].set_volume(0.1)
            self.guitar_muted = True


