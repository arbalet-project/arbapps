import argparse
from .spectrum import SpectrumAnalyser
from arbalet.application import get_application_parser

parser = argparse.ArgumentParser(description='Musical spectrum display for the default system audio input.')

parser.add_argument('-d', '--scan-devices',
                    action='store_true',
                    help='Scan storage devices, play a random song and exit.')

parser.add_argument('-v', '--vertical',
                    action='store_true',
                    help='The spectrum must be vertical (less bands, more bins)')

parser = get_application_parser(parser)
args = parser.parse_args()

SpectrumAnalyser(**args.__dict__).start()

