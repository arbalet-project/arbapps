import argparse
from .sequencer import Sequencer

parser = argparse.ArgumentParser(description='Application sequencer. Runs and closes Arbalet apps according to a sequence file. In general the timeout specifies the duration of user inactivity (joystick or keyboard before switching to the next app. A press on any jostick upper joystick key forces app swicthing unless this has been disabled by interruptible = False within the config files, e.g. for apps already using upper keys. Only apps that guarantee termination in case of user inactivity should set a timeout to -1')
parser.add_argument('-q', '--sequence',
                    type=str,
                    default='sequences/default.json',
                    nargs='?',
                    help='Configuration file describing the sequence of apps to launch')
Sequencer(parser).start()
