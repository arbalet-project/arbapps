#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Bridge for the Snap! visual programming language

    Provides a visual programming language to Arbalet for children or beginners

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from flask import Flask
from flask import request
from flask_cors import CORS
from flask import render_template
from flask import request, Response
from functools import wraps

from arbalet.core import Application
from threading import RLock
import sys
import signal

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import petname
from json import dumps 
from time import time
import logging
import socket



class SnapServer(Application):
    OFF = "turnoff"
    def __init__(self, port, argparser=None):
        Application.__init__(self, argparser)
        self.port = int(port)
        self.flask = Flask(__name__)
        logging.basicConfig(level=logging.DEBUG)
        self.current_auth_nick = self.OFF 
        self.nicknames = {}
        self.lock = RLock()
        CORS(self.flask)
        self.loop = None
        self.route()
    
    def signal_handler(self, signal, frame):
        print("Received SIGINT, closing...")
        if self.loop is not None:
            self.loop.stop()

    def route(self):
        self.flask.route('/admin', methods=['GET', 'POST'])(self.render_admin_page)
        self.flask.route('/admin/nicknames', methods=['GET'])(self.get_admin_nicknames)
        self.flask.route('/admin/active_nickname', methods=['GET'])(self.get_admin_active_nickname)
        self.flask.route('/set_rgb_matrix', methods=['POST'])(self.set_rgb_matrix)
        self.flask.route('/is_authorized/<nickname>', methods=['GET'])(self.is_authorized)
        self.flask.route('/authorize', methods=['POST'])(self.authorize)
        self.flask.route('/get_nickname', methods=['GET'])(self.get_nickname)

    def get_admin_active_nickname(self):
        return dumps(self.current_auth_nick)
    
    def get_admin_nicknames(self):
        # update user table
        self.check_nicknames_validity()
        return dumps(sorted(self.nicknames.keys(), key=lambda x: self.nicknames[x]["appeared"]))


    def check_nicknames_validity(self):
        with self.lock:
            temp_dict = {}
            for nick, timestamps in self.nicknames.items():
                if time() - timestamps["last_seen"] < 20:
                    temp_dict[nick] = timestamps
                else:
                    if nick == self.current_auth_nick:
                        self.current_auth_nick = self.OFF
                        self.erase_all()
            self.nicknames = temp_dict

    def render_admin_page(self):
        res = render_template('admin.html')
        return res

    def authorize(self):
        nick = request.get_data()
        with self.lock:
            if nick in list(self.nicknames.keys()) + [self.OFF]:
                self.current_auth_nick = nick
                self.erase_all()
                return ''
        return 'No such client', 404

    @staticmethod
    def scale(v):
        return min(1, max(0., float(v)/255.))

    def set_rgb_matrix(self):
        try:
            data = request.get_data().split(':')
            with self.lock:
                if data.pop(0) == self.current_auth_nick:
                    r = 0
                    c = 0
                    while data:
                        red = data.pop(0)
                        green = data.pop(0)
                        blue = data.pop(0)
                        self.model.set_pixel(r, c, map(self.scale, [red, green, blue]))
                        if c < self.model.width - 1:
                            c += 1
                        else:
                            c = 0
                            r += 1
        except Exception as e:
            print(repr(e))
            sys.exc_clear()
        return ''  

    def erase_all(self):
        self.model.set_all('black')
        return ''

    def is_authorized(self, nickname):
        with self.lock:
            if nickname in self.nicknames:
                self.nicknames[nickname]["last_seen"] = time()
        return str(nickname == self.current_auth_nick)

    def get_nickname(self):
        rand_id = petname.generate()
        with self.lock:
            while rand_id in self.nicknames.keys():
                rand_id = petname.generate()
            self.nicknames[rand_id] = {"appeared": time(), "last_seen": time()}
        return rand_id

    def run(self):
        # open('http://snap.berkeley.edu/run')
        signal.signal(signal.SIGINT, self.signal_handler)
        self.loop = IOLoop()
        http_server = HTTPServer(WSGIContainer(self.flask))
        http_server.listen(self.port)
        self.loop.start()



