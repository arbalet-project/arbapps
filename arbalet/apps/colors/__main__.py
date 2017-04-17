import argparse
from .colors import ColorDemo
from arbalet.application import get_application_parser
from .generators import animations

parser = argparse.ArgumentParser(description='Color demonstrator and coloured ambient light')
parser.add_argument('-t', '--type',
                    default='swipe',
                    choices=animations.keys(),
                    help='Type of effect')

parser = get_application_parser(parser)
args = parser.parse_args()

ColorDemo(**args.__dict__).start()
