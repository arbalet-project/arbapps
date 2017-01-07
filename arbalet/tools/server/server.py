#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Server allowing multiple clients to connect to hardware alternatively

    Controllable from a GUI or command-line, the server can also stream
    data like sound and joystick/keyboard inputs from/to a headless computer

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from arbalet.core import Application
import zmq

class Arbaserver(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.port = str(self.args.port)
        self.context = zmq.Context()
        self.connection = None

    def bind(self):
        self.connection = self.context.socket(zmq.PAIR)
        connect_to = "tcp://0.0.0.0:" + self.port
        self.connection.bind(connect_to)

    def work(self):
        json_model = self.connection.recv_json()
        self.model.from_json(json_model)
        frame = self.arbalet.touch.get_touch_frame()
        frame = (frame[0], list(map(bool, frame[1])))  # Hack because json is not able to serialize type 'numpy.bool_'
        self.connection.send_json(frame)

    def run(self):
        print("[Arbalet server] Waiting for app connection...")
        self.bind()
        print("[Arbalet server] App connected successfully")
        while True:
            try:
                self.work()
            except KeyboardInterrupt:
                print("[Arbalet server] Shutdown initiated via SIGINT, closing...")
                if not self.connection.closed:
                    self.connection.close()
                return

