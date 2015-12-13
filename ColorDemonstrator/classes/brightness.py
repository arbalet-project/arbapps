#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Brightness management: allows to attenuate the brightness of the color demonstrator depending on user interactions
    Quick-and-dirty class connecting to a second arduino while the touch feature is not yet properly integrated

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from threading import Thread, RLock
from serial import Serial
from arbasdk import Rate
from time import sleep, time

class Brightness(Thread):
    def __init__(self, duration=2, nc=False):
        Thread.__init__(self)
        self.setDaemon(True)
        self.nc = nc # Normally closed (Normally open otherwise)
        self.duration = duration
        self.serial = None
        self.config = {"device": "/dev/ttyACM0", "speed":9600}
        self.rate = Rate(50)
        self.running = True
        self.lock = RLock()
        self.timestamp = {"touched": 0, "untouched": 0}  # Last time the surface as been touched
        self.connect()

    def connect(self):
        success = False
        device = self.config['device']
        try:
            self.serial = Serial(device, self.config['speed'], timeout=0)
        except Exception, e:
            print "[Touch] Connection to {} at speed {} failed: {}".format(device, self.config['speed'], e.message)
            self.serial = None
        else:
            success = True
        return success

    def close(self):
        self.running = False
        if self.serial:
            self.serial.close()
            self.serial = None

    @property
    def brightness(self):
        if self.serial:
            now = time()
            with self.lock:
                if self.nc:
                    if self.timestamp["touched"] > self.timestamp["untouched"]:
                        return min(1, (now - self.timestamp["untouched"])/self.duration)
                    else:
                        return max(0, 1 - (now - self.timestamp["touched"])/self.duration)
                else:
                    if self.timestamp["touched"] > self.timestamp["untouched"]:
                        return max(0, 1 - (now - self.timestamp["untouched"])/self.duration)
                    else:
                        return min(1, (now - self.timestamp["touched"])/self.duration)
        else:
            return 1.  # Touch interface not available

    def run(self):
        while(self.running):
            if self.serial and self.serial.isOpen():
                try:
                    read = self.serial.read()
                except:
                    return False
                else:
                    if len(read)>0:
                        with self.lock:
                            if read == '1':
                                self.timestamp["touched"] = time()
                            else:
                                self.timestamp["untouched"] = time()
            self.rate.sleep()
        return True

if __name__=='__main__':
    Brightness().run()