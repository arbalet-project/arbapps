import argparse
from .spectrum import SpectrumAnalyser

parser = argparse.ArgumentParser(description='Spectrum analyzer of WAVE files')
parser.add_argument('-i', '--input',
                    type=str,
                    required=True,
                    nargs='+',
                    help='Wave file(s) to play')
parser.add_argument('-v', '--vertical',
                    action='store_const',
                    const=True,
                    default=False,
                    help='The spectrum must be vertical (less bands, more bins)')
parser.add_argument('-o', '--random',
                    default='none',
                    choices=['none', 'all', 'once'],
                    help='Random playing of the file queue: Play the entire queue as is (none), Shuffle and play the entire queue (all), Randomly pick a single file, play it and exit (once)')
SpectrumAnalyser(parser).start()

