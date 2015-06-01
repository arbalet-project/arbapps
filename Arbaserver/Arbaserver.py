#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Server allowing multiple clients to connect to hardware alternatively

    Controllable from a GUI or command-line, the server can also stream
    data like sound and joystick/keyboard inputs from/to a headless computer

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from arbasdk import Arbapp
import zmq, argparse

class Arbaserver(Arbapp):
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser)
        self.port = str(self.args.port)
        self.context = zmq.Context()
        self.connection = None

    def bind(self):
        self.connection = self.context.socket(zmq.SUB)
        connect_to = "tcp://127.0.0.1:"+self.port
        self.connection.bind(connect_to)
        self.connection.setsockopt_string(zmq.SUBSCRIBE, ''.decode('ascii')) # Accepts all incoming messages

    def work(self):
        json_model = self.connection.recv_json()
        self.model.from_json(json_model)

    def run(self):
        print "Waiting for connection..."
        self.bind()

        print "Connection successful"
        while True:
            self.work()


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Server allowing multiple clients to connect to hardware alternatively'
                                                 'Controllable from a GUI or command-line, the server can also stream'
                                                 'data like sound and joystick/keyboard inputs from/to a headless computer')
    parser.add_argument('-p', '--port',
                        default=33400,
                        help='Listening port [default is 33400]')
    s = Arbaserver(parser)
    s.start()