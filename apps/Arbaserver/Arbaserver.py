#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Server allowing multiple clients to connect to hardware alternatively

    Controllable from a GUI or command-line, the server can also stream
    data like sound and joystick/keyboard inputs from/to a headless computer

    Copyright (C) 2015 Yoan Mollard <yoan@konqifr.fr>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
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