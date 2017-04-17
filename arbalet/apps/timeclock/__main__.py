import argparse
from .timeclock import TimeClockApp
from arbalet.application import get_application_parser

parser = argparse.ArgumentParser(description='Display a simple clock. The colour is configurable. The app has been written for a 15x10 screen, and does not scale.')
parser.add_argument('--color',
                    default='darkred',
                    help="Font color")

parser = get_application_parser(parser)
args = parser.parse_args()

TimeClockApp(**args.__dict__).start()
