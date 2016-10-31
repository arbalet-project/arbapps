import argparse
from os.path import join, dirname
from .lightshero import LightsHero

parser = argparse.ArgumentParser(description='LightsHero, is a rhythm video game for Arbalet. It is inspired from Guitar Hero and compatible with Frets On Fire songs,'
                                             'but this time, notes are lights and the keyboard your guitar. Be a Lights Hero!'
                                             'Players use the keyboard keys F1 to F5 or touch screen to play along with markers which scroll on screen'
                                             'Press any joystick button to activate or deactivate the simulated player')
parser.add_argument('-l', '--level',
                    default='difficult',
                    choices=['easy', 'medium', 'difficult', 'expert'],
                    help='Difficulty of the game, if the selected level is implemented for this song')

parser.add_argument('-sp', '--simulate-player',
                    action='store_const',
                    const=True,
                    default=False,
                    help='Simulate a player, i.e. do not mute the guitar when the user fails to play')

song = join(dirname(__file__), 'songs', 'Feelings')
LightsHero(parser, num_lanes=5, path=song, speed=15).start()
