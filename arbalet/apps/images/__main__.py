import argparse
from .images import ImageReader
from arbalet.application import get_application_parser

parser = argparse.ArgumentParser(description='Render an animated image (gif, apng, mng...) on Arbalet')
parser.add_argument('-i', '--input',
                    type=str,
                    required=True,
                    nargs='+',
                    help='Path to the image(s) to render')

parser.add_argument('-l', '--loop',
                    action='store_true',
                    default=True,
                    help='Keep playing infinitely')

parser.add_argument('-do', '--display-original',
                    action='store_const',
                    const=True,
                    default=False,
                    help='Display the original image (require access to X display)')

parser = get_application_parser(parser)
args = parser.parse_args()

ImageReader(**args.__dict__).start()
