#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table

    This class is the Arbalet master
    Controller calling all other features

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

from . Arbasim import Arbasim
from . Arbalink import Arbalink
from . Arbaclient import Arbaclient
from os import path
from json import load
from ConfigParser import RawConfigParser
import arbasdk

__all__ = ['Arbalet']

class Arbalet(object):
    def __init__(self, simulation, hardware, server='', diminution=1, factor_sim=30, config=''):
        self.simulation = simulation
        self.hardware = hardware
        self.diminution = diminution
        self.server = server

        if config=='':
            cfg_path = path.join(path.dirname(arbasdk.__file__), '..', 'config', 'default.cfg')
            cfg_parser = RawConfigParser()
            cfg_parser.read(cfg_path)
            config = cfg_parser.get('DEFAULT', 'config')
            print "[Warning] No config file given and no default.cfg found in your arbasdk/config folder"

        if not path.isfile(config):
            config = path.join(path.dirname(arbasdk.__file__), '..', 'config', config)
        if not path.isfile(config):
            raise Exception("Config file '{}' not found".format(config))

        with open(config, 'r') as f:
            self.config = load(f)

        self.height = len(self.config['mapping'])
        self.width = len(self.config['mapping'][0]) if self.height>0 else 0

        if self.simulation:
            self.arbasim = Arbasim(self.width, self.height, self.width*factor_sim, self.height*factor_sim)

        if self.hardware:
            self.arbalink = Arbalink(self.config, diminution=self.diminution)

        if len(self.server)>0:
            server = self.server.split(':')
            if len(server)==2:
                self.arbaclient = Arbaclient(server[0], int(server[1]))
            elif len(server)==1:
                self.arbaclient = Arbaclient(server[0])
            else:
                raise Exception('Incorrect server address, use ip:port or ip')


    def set_model(self, model):
        if self.simulation:
            self.arbasim.set_model(model)
        if self.hardware:
            self.arbalink.set_model(model)
        if len(self.server)>0:
            self.arbaclient.set_model(model)

    def close(self, reason='unknown'):
        if self.simulation:
            self.arbasim.close(reason)
        if self.hardware:
            self.arbalink.close()
        if len(self.server)>0:
            self.arbaclient.close(reason)