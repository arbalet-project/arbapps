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
# - colors is the vector of HSV colors to swipe in the given duration


animations = {'swipe': { 'rate': 20, 'dur_min': 30, 'dur_max': 35, 'generator_id': 1,
                         'colors': [(0.1, 1, 1)] },

              'african': { 'rate': 20, 'dur_min': 10, 'dur_max': 15, 'generator_id': 2,
                           'colors': [(0.05833333333333333, 0.5128205128205129, 0.15294117647058825),
                                      (0.05769230769230769, 0.5306122448979592, 0.19215686274509805),
                                      (0.05769230769230771, 0.52, 0.39215686274509803),
                                      (0.060041407867494824, 0.9360465116279071, 0.6745098039215687),
                                      (0.08758503401360544, 0.8448275862068965, 0.9098039215686274)]
                         },

              'flashes': { 'rate': 20, 'dur_min': 3, 'dur_max': 30, 'generator_id': 0,
                           'colors': list(map(name_to_hsv, ['darkblue'])) },

              'gender': { 'rate': 20, 'dur_min': 5, 'dur_max': 15, 'generator_id': 2,
                           'colors': list(map(name_to_hsv, ['darkblue', 'deeppink'])) },

              'teddy':  { 'rate': 20, 'dur_min': 5, 'dur_max': 20, 'generator_id': 2,
                           'colors': [(0.5, 1.0, 0.11764705882352941), (0.08333333333333333, 1.0, 0.0784313725490196)]
 },

              'warm':  { 'rate': 20, 'dur_min': 10, 'dur_max': 30, 'generator_id': 2,
                           'colors': [(0.08333333333333333, 0.9, 0.0784313725490196),
                                      (0.9615384615384616, 1.0, 0.050980392156862744),
                                      (0.9444444444444444, 0.9, 0.0392156862745098)]
                       },

              }

parser = argparse.ArgumentParser(description='Color demonstrator and coloured ambient light')
parser.add_argument('-t', '--type',
                    default='swipe',
                    choices=list(animations.keys()),
                    help='Type of effect')

ColorDemo(parser, animations).start()
