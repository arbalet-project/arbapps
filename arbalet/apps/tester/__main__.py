import argparse
from .tester import SimpleTester
from arbalet.application import get_application_parser

parser = argparse.ArgumentParser(description='Light every pixel one by one for hardware address debuging purposes. Columns are filled in first progressively, then rows. All pixels in a column share the same color.')
parser = get_application_parser(parser)
args = parser.parse_args(parser)

SimpleTester(**args.__dict__).start()