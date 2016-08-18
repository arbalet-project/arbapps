import argparse
from .server import Arbaserver

parser = argparse.ArgumentParser(description='Server allowing multiple clients to connect to hardware alternatively'
                                             'Controllable from a GUI or command-line, the server can also stream'
                                             'data like sound and joystick/keyboard inputs from/to a headless computer')
parser.add_argument('-p', '--port',
                    default=33400,
                    help='Listening port [default is 33400]')
Arbaserver(parser).start()
