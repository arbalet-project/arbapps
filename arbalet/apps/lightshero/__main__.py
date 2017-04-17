import argparse
from .lightshero import LightsHero
from arbalet.application import get_application_parser

parser = argparse.ArgumentParser(description='LightsHero, is a rhythm video game for Arbalet. It is inspired from Guitar Hero and compatible with Frets On Fire songs,'
                                             'but this time, notes are lights and the keyboard your guitar. Be a Lights Hero!'
                                             'Players use the keyboard keys F1 to F5 or touch screen to play along with markers which scroll on screen'
                                             'Press any joystick button to activate or deactivate the simulated player')
parser.add_argument('-l', '--level',
                    default='difficult',
                    choices=['easy', 'medium', 'difficult', 'expert'],
                    help='Difficulty of the game, if the selected level is implemented for this song')

parser.add_argument('-p', '--path',
                    default='default',
                    nargs='?',
                    const=True,
                    help='Path to the song: must be a directory containing the MID and OGG files. '
                         'If not provided the default song will play.')

parser.add_argument('-sp', '--simulate-player',
                    action='store_const',
                    const=True,
                    default=False,
                    help='Simulate a player, i.e. do not mute the guitar when the user fails to play')

parser = get_application_parser(parser)
args = parser.parse_args()

LightsHero(**args.__dict__).start()
