import argparse
from os.path import join, dirname
from .lightshero import LightsHero

parser = argparse.ArgumentParser(description='LightsHero, is a rhythm video game for Arbalet. It is inspired from Guitar Hero and compatible with Frets On Fire songs,'
                                             'but this time, notes are lights and the keyboard your guitar. Be a Lights Hero!'
                                             'Players use the keyboard keys F1 to F5 to play along with markers which scroll on screen')
parser.add_argument('-l', '--level',
                    default='difficult',
                    choices=['easy', 'medium', 'difficult', 'expert'],
                    help='Difficulty of the game, if the selected level is implemented for this song')

song = join(dirname(__file__), 'songs', 'Feelings')
LightsHero(parser, num_lanes=5, path=song, speed=15).start()
