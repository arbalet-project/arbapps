#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    DBus Proxy - Proxy for the Arbalet Data Bus
    Gathers all data from publishers and transmits them to all subscribers

    Copyright 2017 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import zmq
from arbalet.core.config import ConfigReader

class Proxy(object):
    def __init__(self, argparser):
        config_reader = ConfigReader()
        self.config = config_reader.dbus
        self.context = zmq.Context()

    def run(self):
        ingoing_connection = "tcp://{}:{}".format(self.config['ip_binding'], self.config['xpub_port'])
        outgoing_connection = "tcp://{}:{}".format(self.config['ip_binding'], self.config['xsub_port'])
        print("Binding to {} for publishers".format(ingoing_connection))
        print("Binding to {} for subscribers".format(outgoing_connection))
        ingoing_socket = self.context.socket(zmq.SUB)
        ingoing_socket.setsockopt(zmq.SUBSCRIBE, "")
        ingoing_socket.bind(ingoing_connection)
        outgoing_socket = self.context.socket(zmq.PUB)
        outgoing_socket.bind(outgoing_connection)
        print("Arbalet D-Bus running")
        try:
            zmq.proxy(ingoing_socket, outgoing_socket)
        except KeyboardInterrupt as e:
            print("[Arbalet D-Bus Proxy] Shutdown initiated via SIGINT, closing...")
            return
