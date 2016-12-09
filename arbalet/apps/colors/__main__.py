import argparse
from .colors import ColorDemo
from arbalet.colors import name_to_hsv, rgb_to_hsv

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


animations = {'swipe': { 'rate': 20, 'dur_min': 30, 'dur_max': 35, 'generator_id': 1,
                         'colors': [(0.1, 1, 1)] },

              'african': { 'rate': 20, 'dur_min': 10, 'dur_max': 15, 'generator_id': 2,
                           'colors': map(rgb_to_hsv,
                                         [(39, 26, 19), (49, 32, 23), (100, 66, 48), (172, 69, 11), (232, 139, 36)]) },

              'flashes': { 'rate': 20, 'dur_min': 3, 'dur_max': 30, 'generator_id': 0,
                           'colors': map(name_to_hsv, ['darkblue']) },

              'gender': { 'rate': 20, 'dur_min': 5, 'dur_max': 15, 'generator_id': 2,
                           'colors': map(name_to_hsv, ['darkblue', 'deeppink']) },

              'teddy':  { 'rate': 20, 'dur_min': 5, 'dur_max': 20, 'generator_id': 2,
                           'colors': map(rgb_to_hsv, [(0, 30, 30), (20, 10, 0)]) },

              'warm':  { 'rate': 20, 'dur_min': 10, 'dur_max': 30, 'generator_id': 2,
                           'colors': map(rgb_to_hsv, [[20, 11, 2], [13, 0, 3], [10, 1, 4]]) },

              }

parser = argparse.ArgumentParser(description='Color demonstrator and coloured ambient light')
parser.add_argument('-t', '--type',
                    default='swipe',
                    choices=animations.keys(),
                    help='Type of effect')

ColorDemo(parser, animations).start()
