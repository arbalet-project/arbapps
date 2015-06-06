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

    def start(self):
        self.started = True

        # Start background music
        mixer.music.play()

        # Start tracks
        for name, track in self.tracks.iteritems():
            if track:
                track.play()

    def mute(self, track, muted):
        if muted:
            self.tracks[track].mute()
        else:
            self.tracks[track].unmute()


