#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table

    Arbalet client
    Client for controlling Arbalet over the network

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

import zmq
from threading import Thread
from time import sleep

__all__ = ['Arbaclient']

class Arbaclient(Thread):
    def __init__(self, server='127.0.0.1', port=33400, rate=30, autorun=True):
        Thread.__init__(self)
        self.setDaemon(True)
        self.server = server
        self.port = str(port)
        self.model = None
        self.running = True
        self.rate = rate

        # Network-related attributes
        self.context = zmq.Context()
        self.sender = None

        if autorun:
            self.start()

    def connect(self):
        if not self.sender:
            self.sender = self.context.socket(zmq.PUSH)
            self.sender.connect("tcp://{}:{}".format(self.server, self.port))

    def send_model(self):
        if self.model:
            self.sender.send_json(self.model.to_json())

    def set_model(self, model):
        self.model = model

    def close(self, reason='unknown'):
        self.running = False

    def run(self):
        self.connect()
        while self.running:
            self.send_model()
            sleep(1./self.rate)
        self.sender.close()

if __name__=='__main__':
    c = Arbaclient()
    raw_input("[Arbaclient test routine] Press enter when server is listening to {}:{}".format(c.server, c.port))
    c.run()