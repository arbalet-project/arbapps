import argparse
from .snake import Snake
from arbalet.application import get_application_parser

parser = argparse.ArgumentParser(description='Snake game')
parser.add_argument('--speed', type=float, default=0.15)
parser.add_argument('--food', type=int, default=3)

parser = get_application_parser(parser)
args = parser.parse_args()

Snake(**args.__dict__).start()

