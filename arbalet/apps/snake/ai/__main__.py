import argparse
from arbalet.application import get_application_parser
from .ai import SnakeAI

parser = argparse.ArgumentParser(description='Autoplaying snake game with a trivial AI')
parser.add_argument('--speed', type=float, default=0.15)
parser.add_argument('--food', type=int, default=3)

parser = get_application_parser(parser)
args = parser.parse_args(parser)

SnakeAI(**args.__dict__).start()

