import argparse
from .ai import SnakeAI

parser = argparse.ArgumentParser(description='Autoplaying snake game with a trivial AI')
parser.add_argument('--speed', type=float, default=0.15)
parser.add_argument('--food', type=int, default=3)

SnakeAI(parser).start()

