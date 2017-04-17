import argparse
from .pixeliser import Pixeliser
from arbalet.application import get_application_parser

parser = argparse.ArgumentParser(description='Pixelate a video file, i.e. decrease dramatically the number of'
                                             'pixels to play the latter on the table')
parser.add_argument('-i', '--input',
                    type=str,
                    required=True,
                    nargs='+',
                    help='Video file(s) to pixelate')

parser.add_argument('-do', '--display-original',
                    action='store_const',
                    const=True,
                    default=False,
                    help='Display the original video in an OpenCV window (requires access to X display)')

parser = get_application_parser(parser)
args = parser.parse_args()

Pixeliser(**args.__dict__).start()