from .tetris import Tetris
from arbalet.application import get_application_parser
from argparse import ArgumentParser

parser = ArgumentParser(description='A simple Tetris game. Make combos to win points faster. There is an infinite number of levels. '
                                    'A different music plays at each level.')
parser = get_application_parser(parser)
args = parser.parse_args()

Tetris(**args.__dict__).start()
