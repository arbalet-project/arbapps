from .tetris import Tetris
from argparse import ArgumentParser

parser = ArgumentParser(description='A simple Tetris game. Make combos to win points faster. There is an infinite number of levels. '
                                    'A different music plays at each level.')

Tetris(parser).start()
