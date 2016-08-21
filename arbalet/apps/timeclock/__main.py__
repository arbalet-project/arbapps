import argparse
from .timeclock import TimeClockApp

parser = argparse.ArgumentParser(description='Display a simple clock. The colour is configurable. The app has been written for a 15x10 screen, and does not scale.')
parser.add_argument('-t', '--type',
                    default='darkred',
                    help="Font's color")

TimeClockApp(parser).start()
