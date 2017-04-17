from .lost_in_space import LostInSpace
from arbalet.application import get_application_parser
from argparse import ArgumentParser

parser = ArgumentParser(description="Inspired by modern art and its relation to code, this game allows players to express themselves with digital tools. "
                                    "The traditional painter's palette is replaced with RVB/CMY colour sources that the player needs to hit to get paint on his brush."
                                    "Press space/action to make the palette appear and simply use the keyboard arrows to move around the painting, hitting sources "
                                    "and getting speed and momentum as you go.")


parser.add_argument('--invader', action='store_true', help='Super Space Invader mod (default: disabled)')
parser.add_argument('-a-', '--auto', action='store_true', help='The computer plays alone (default: disabled)')
parser.add_argument('--pattern', default='', help='Input file, to begin the game with a default pattern as background (expected format : jpg or png)')
parser.add_argument('--save', action='store_true', help='Save the result: Dump the artwork in folder ./output/')
parser = get_application_parser(parser)
args = parser.parse_args()

LostInSpace(**args.__dict__).start()
