import argparse
from arbalet.application import get_application_parser
from .bounces import Bounces

parser = argparse.ArgumentParser(description='Bouncing pixels propelled by a leap motion controller'
                                             'You must plug a Leap Motion controller, install its SDK and run its daemon first')

parser = get_application_parser(parser)
args = parser.parse_args()

Bounces(**args.__dict__).start()