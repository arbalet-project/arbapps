import argparse
from .bounces import Bounces

parser = argparse.ArgumentParser(description='Bouncing pixels propelled by a leap motion controller'
                                             'You must plug a Leap Motion controller, install its SDK and run its daemon first')

Bounces(parser, 50).start()