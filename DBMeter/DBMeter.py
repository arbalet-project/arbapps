#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Decibel-Meter for Audio files

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
import sys
sys.path.append('../../src/')
import numpy
from pylab import *
from arbasdk import Arbamodel, Arbapp
import pygame, pyaudio, audioop, math, wave


class DBMeter(Arbapp):
    def __init__(self, height, width, file, with_sound=True):
        Arbapp.__init__(self, width, height)
        self.chunk = 1024
        self.with_sound = with_sound

        self.file = wave.open(file, 'rb')
        if self.with_sound:
            self.pyaudio = pyaudio.PyAudio()
            self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.file.getsampwidth()),
                                            channels=self.file.getnchannels(),
                                            rate=self.file.getframerate(),
                                            output=True)

        self.max_level = float(2**(8*self.file.getsampwidth()-1))
        self.levels = []

    def run(self):
        try:
            data = self.file.readframes(self.chunk)
            while data != '':
                mono_data = audioop.tomono(data, self.file.getsampwidth(), 0.5, 0.5)
                local_max_level = audioop.rms(mono_data, self.file.getsampwidth())
                local_dB = int(20*(math.log10(local_max_level/self.max_level)))

                self.levels.append(local_dB)
                if self.with_sound:
                    self.stream.write(data)
                data = self.file.readframes(self.chunk)
        finally:
            if self.with_sound:
                self.stream.stop_stream()
                self.stream.close()
                self.pyaudio.terminate()

        if not self.with_sound:
            plot(self.levels)
            show()



if __name__=='__main__':
    dbm = DBMeter(15, 10, 'Nytrogen_-_Nytrogen_-_Jupiter.wav', False)
    dbm.start()

