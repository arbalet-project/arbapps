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
from arbalet.dbus import DBusClient


class Arbaserver(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.port = str(self.args.port)
        self.bus = DBusClient(display_subscriber=True)
        self.running = False

    def work(self):
        model = self.bus.display.recv(blocking=True)
        self.model.from_dict(model)

    def run(self):
        self.running = True
        while self.running:
            try:
                self.work()
            except KeyboardInterrupt:
                print("[Arbalet Display server] Shutdown initiated via SIGINT, closing...")
                self.running = False
                return

