import argparse
from .snake import Snake

parser = argparse.ArgumentParser(description='Snake game')
parser.add_argument('--speed', type=float, default=0.5)
parser.add_argument('--food', type=int, default=3)

Snake(parser).start()

