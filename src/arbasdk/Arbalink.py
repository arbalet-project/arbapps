#!/usr/bin/env python3
"""
    Arbalet - ARduino-BAsed LEd Table
    Arbalink - Arbalet Link to the hardware table

    Handle the connection to Arduino

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

from Arbamodel import *
from threading import Thread
from serial import Serial, SerialException
from sys import stderr
from time import sleep, time
from json import load

__all__ = ['Arbalink']

class Arbalink(Thread):
    def __init__(self, config_filename, rate=30, diminution=1, autorun=True):
        Thread.__init__(self)
        self.setDaemon(True)
        self.current_device = 0
        self.serial = None
        self.model = None
        self.refresh_rate = rate
        self.diminution = diminution

        with open(config_filename, 'r') as f:
            self.config = load(f)

        if autorun:
            self.start()

    def connect(self):
        device = self.config['devices'][self.current_device]
        try:
            self.serial = Serial(device, self.config['speed'])
        except Exception, e:
            print >> stderr, "[Arbalink] Connection to {} at speed {} failed: {}".format(device, self.config['speed'], e.message)
            self.serial = None
            self.current_device = (self.current_device+1) % len(self.config['devices'])
            return False
        sleep(2)
        return True

    def connect_until(self, timeout, num_attempts=20):
        success = False
        start_time = time()
        while not success:
            success = self.connect()
            elapsed_time = time()-start_time
            if not success and elapsed_time<timeout:
                sleep(float(timeout)/num_attempts)
            else:
                break
        return success

    def set_model(self, arbamodel):
        self.model = arbamodel

    def close(self, reason='unknown'):
        self.running = False
        if self.serial:
            self.serial.close()
            self.serial = None

    def __limit(self, v):
        """
        Limitator avoiding overflows and underflows
        """
        return int(max(0, min(255, v)))

    def run(self):
        self.running = True
        while(self.running):
            if self.serial and self.serial.isOpen():
                if self.model:
                    array = bytearray(' '*(self.model.get_height()*self.model.get_width()*3))
                    for h in range(self.model.get_height()):
                        for w in range(self.model.get_width()):
                            idx = self.config['mapping'][h][w]*3 # = mapping shift by 3 colors
                            # an IndexError here on bytearray could mean that config file is wrong
                            array[idx] = self.__limit(self.model.model[h][w].r*self.diminution)
                            array[idx+1] = self.__limit(self.model.model[h][w].g*self.diminution)
                            array[idx+2] = self.__limit(self.model.model[h][w].b*self.diminution)
                    try:
                        #print "[Arbalink] Submitting new matrix"
                        self.serial.write(array) # Write the whole rgb-matrix
                        feedback = self.serial.readline() # Wait Arduino's feedback
                        #print "[Arbalink] Feedback: ", feedback
                    except SerialException, e:
                        print e
                        self.connect_until(60)
            else:
                self.connect()
            sleep(1./self.refresh_rate)

if __name__ == '__main__':
    link = Arbalink('/dev/ttyACM1', 1000000, rate=30)
    link.start()
    for i in range(64):
        link.set_model(Arbamodel(10, 15, i, 0, 0))
        sleep(0.2)
    link.close()
