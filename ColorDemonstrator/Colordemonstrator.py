#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Color Demonstrator - Arbalet Color Demonstrator

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import random
from arbasdk import Arbapp, Arbapixel, Rate
import argparse

def gen_sweep_async(n_frames, n_frames_fade, n_frames_rand, colors):
    # TODO randomization to change to avoid overlapping of farthest colors
    """
    This generator generates sweeping colors with a unique duration between colors for all pixels
    Randomization is made during initial fading up, pixels start weeping at different times
    This generator can be used when colors are ordered, they do not go well all together, a given
    color must be mixed only with colors right before or right after it.
    :param n_frames: Duration between two consecutive colors
    :param n_frames_fade: Unused
    :param n_frames_rand: Duration of fade + random seed
    :param colors: list of colors with order respected
    """
    # This loop fades up and is also the random seed
    for f in range(n_frames_rand):
        yield Arbapixel(colors[0])*(float(f)/n_frames_rand)

    color_generator = [[float(x)/n_frames for x in range(n_frames, -1, -1)],           # Descending phase
                       [float(x)/n_frames for x in range(n_frames)]]                   # Ascending phase

    # Infinite loop on color sequence
    pairs = zip(colors, colors[1:])
    while True:
        for color1, color2 in pairs:
            for s in range(n_frames):
                col = Arbapixel(color1)*color_generator[0][s] + Arbapixel(color2)*color_generator[1][s]
                yield col

def gen_sweep_rand(n_frames, n_frames_fade, n_frames_rand, colors):
    """
    This generator generates sweeping colors with a unique duration between colors for all pixels
    This generator can be used when all colors go well together, there is no external random seed
    :param n_frames: Duration between two consecutive colors
    :param n_frames_fade: Duration of fade
    :param n_frames_rand: Random seed, extra duration added to n_frames to get the total duration
    :param colors: list of colors
    """
    pairs = list(enumerate(zip(colors, colors[1:])))
    start = random.randint(0, len(pairs)-1)
    n_frames += n_frames_rand

    color_generator = [[float(x)/n_frames for x in range(n_frames, -1, -1)],           # Descending phase
                       [float(x)/n_frames for x in range(n_frames)]]                   # Ascending phase

    # This loop fades up
    fade_color = Arbapixel(pairs[start][1][0])*color_generator[0][0] + Arbapixel(pairs[start][1][1])*color_generator[1][0]
    for f in range(n_frames_fade):
        yield fade_color*(float(f)/n_frames_fade)

    # Infinite loop on color sequence
    while True:
        for c in range(start, len(pairs)):
            for s in range(n_frames):
                col = Arbapixel(pairs[c][1][0])*color_generator[0][s] + Arbapixel(pairs[c][1][1])*color_generator[1][s]
                yield col
        start = 0

def gen_random_flashing(n_frames, n_frames_fade, n_frames_rand, colors):
    """
    This generator generates exponential rises/descents from the first color to the second color
    External randomization is brought though the duration of the rise = n_frames + n_frames_rand
    Internal randomization is made through a random starting frame between start of the rise and end of the descent
    :param n_frames: Common minimum duration of all pixels
    :param n_frames_fade: Duration of fade
    :param n_frames_rand: Random seed, extra duration added to n_frames to get the total duration
    :param colors: List of two colors. The other colors, if any, are ignored
    """
    n_frames += n_frames_rand
    n_frames -= n_frames%2  # We need an even number of frames since we are going to divide them by two
    base_exp = [1.1**(p-n_frames/2+1) for p in range(n_frames/2)]  # The first n_frames/2 are an exponential ascending phase
    reverse_base = [base_exp[i] for i in range(n_frames/2-1, -1, -1)]  # The last n_frames/2 are an exponential descending phase
    white_generator = base_exp+reverse_base
    blue_generator = [1.0-i for i in white_generator]
    color_generator = [blue_generator, white_generator]

    start = random.randint(0, n_frames-1)  # Allows to advance browsing and get immediate flashing after start

    # Fade up
    for f in range(n_frames_fade):
        yield Arbapixel(colors[0]) + Arbapixel(colors[1])*(color_generator[1][start]*(float(f)/n_frames_fade))

    while True:
        for s in range(start, n_frames):
            col = Arbapixel(colors[0]) + Arbapixel(colors[1])*color_generator[1][s]
            yield col
        start = 0

class ColorDemo(Arbapp):
    generators = [gen_random_flashing, gen_sweep_async, gen_sweep_rand, ]

    def __init__(self, parser, animations):
        Arbapp.__init__(self, parser)
        config = animations[self.args.type]
        self.durations = [int(config['dur_min']*config['rate']), int(config['dur_max']*config['rate'])]
        self.rate = Rate(config['rate'])
        if config['colors'][-1]!=config['colors'][0]:
            config['colors'].append(config['colors'][0])
        self.colors = config['colors']
        self.generator = self.generators[config['generator_id']]

    def run(self):
        # Construct all pixel generators
        generators = [[None for w in range(self.width)] for h in range(self.height)]
        for h in range(self.height):
            for w in range(self.width):
                duration = random.randrange(0, self.durations[1]-self.durations[0])
                generators[h][w] = self.generator(self.durations[0], int(2./self.rate.sleep_dur), duration, self.colors)

        # Browse all pixel generators at each time
        while True:
            self.model.lock()
            for h in range(self.height):
                for w in range(self.width):
                    try:
                        color = generators[h][w].next()
                    except StopIteration:
                        pass
                    else:
                        self.model.set_pixel(h, w, color)
            self.model.unlock()
            self.rate.sleep()

if __name__=='__main__':
    # Below is declared the dictionary of available effects
    # Effects are generated thanks to Python generators: https://wiki.python.org/moin/Generators
    # At a certain framerate the chosen generator will provide a new color, whether it has changed or not
    # A generator is finite, it has a life, that can be different for each pixel
    #
    # - rate is the frame rate in Hz
    # - dur_min is the minimum duration life in seconds (duration of the faster pixel)
    # - dur_max is tha maximum duration life in seconds (duration of the slower pixel)
    # the duration of a pixel life is picked randomly between dur_min and dur_max
    # the small dur_max - dur_min is, the more synchronized all the pixels are
    # - colors is the vector of colors to swipe in the given duration
    
    animations = {'swipe': { 'rate': 20, 'dur_min': 10, 'dur_max': 15, 'generator_id': 1,
                             'colors': ['gold', 'darkorange', 'darkred', 'deeppink',
                                        'purple', 'darkblue', 'turquoise', 'darkgreen', 'yellowgreen'] },

                  'african': { 'rate': 20, 'dur_min': 10, 'dur_max':15, 'generator_id': 2,
                               'colors':[(39, 26, 19), (49, 32, 23), (100, 66, 48), (172, 69, 11), (232, 139, 36)] },

                  'flashes': { 'rate': 20, 'dur_min': 10, 'dur_max': 60, 'generator_id': 0,
                               'colors':['darkblue', 'white'] },

                  'gender': { 'rate': 20, 'dur_min': 5, 'dur_max': 15, 'generator_id': 2,
                               'colors':['darkblue', 'deeppink'] },

                  'teddy':  { 'rate': 20, 'dur_min': 5, 'dur_max': 20, 'generator_id': 2,
                               'colors':['turquoise', (49, 32, 23)] },

                  'summer':  { 'rate': 20, 'dur_min': 10, 'dur_max': 30, 'generator_id': 2,
                               'colors':['gold', 'red'] },
                  }

    parser = argparse.ArgumentParser(description='Color demonstrator with nice effects and animations for demos (and pleasure!)'
                                                 'To be enriched with newer animations!')
    parser.add_argument('-t', '--type',
                        default='swipe',
                        choices=animations.keys(),
                        help='Type of effect')

    e = ColorDemo(parser, animations)
    e.start()
    e.close("end")
