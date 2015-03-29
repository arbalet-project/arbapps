#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Decibel-Meter for Audio files
    Spectrum analysis based on https://github.com/n00bsys0p/python-visualiser

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
import sys, struct
sys.path.append('../../src/')
import numpy
from pylab import *
from arbasdk import Arbamodel, Arbapp
import pygame, pyaudio, audioop, math, wave, time


class DBMeter(Arbapp):
    def __init__(self, height, width, file, with_sound=True, invert=False):
        Arbapp.__init__(self, width, height)
        self.chunk = 4*1024
        self.with_sound = with_sound
        self.model = Arbamodel(width, height, 'black')
        self.set_model(self.model)

        self.file = wave.open(file, 'rb')
        if self.with_sound:
            self.pyaudio = pyaudio.PyAudio()
            self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.file.getsampwidth()),
                                            channels=self.file.getnchannels(),
                                            rate=self.file.getframerate(),
                                            output=True)

        self.max_level = float(2**(8*self.file.getsampwidth()-1))
        self.levels = []

        ##### Fourier related attributes
        self.num_bands = 12 #self.height
        self.range_db = self.width
        self.fouriers_per_second = 24 # Frames per second
        self.fourier_spread = 1.0/self.fouriers_per_second
        self.fourier_width = self.fourier_spread
        self.fourier_width_index = self.fourier_width * float(self.file.getframerate())
        self.sample_size = self.fourier_width_index
        #self.sample_size = 600 # TODO HACK, sample size too high!!

        ##### Color rendering
        self.colors = ['yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
                       'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',] # We should have as colors as bands # TODo: auto-colors
        self.fft_display_rate = 24  # Rate of Fourier transforms rendering in Hz

    ############################################# Fourier-related methods #############################################
    def fft(self, sample):
        def chunks(l, n):
            for i in xrange(0, len(l), n):
                yield l[i:i+n]

        def str_to_int(string):
            return struct.unpack('<h', string)[0] # Convert little-endian char into int

        sample_range = map(str_to_int, list(chunks(sample, self.file.getsampwidth())))
        fft_data = abs(numpy.fft.fft(sample_range))
        # Normalise the data a second time, to make numbers sensible
        fft_data *= ((2**.5)/self.chunk)
        self.averages = self.average_fft_bands(fft_data)

    # Gives the average FFT band (y-axis of vu-meter)
    def average_fft_bands(self, fft_array):
        fft_averages = []
        for band in range(0, self.num_bands):
            avg = 0.0
            if band == 0:
                lowFreq = int(0)
            else:
                lowFreq = int(int(self.file.getframerate()/2) / float(2 ** (self.num_bands - band)))
            hiFreq = int((self.file.getframerate()/2) / float(2 ** ((self.num_bands-1) - band)))
            lowBound = int(self.freqToIndex(lowFreq))
            hiBound = int(self.freqToIndex(hiFreq))
            for j in range(lowBound, hiBound):
                avg += fft_array[j]
            avg /= (hiBound - lowBound + 1)
            fft_averages.append(avg)
        return fft_averages

    def getBandWidth(self):
        return (2.0/self.sample_size) * (self.file.getframerate()/2.0)

    def freqToIndex(self, f):
        # If f (frequency is lower than the bandwidth of spectrum[0]
        if f < self.getBandWidth()/2:
            return 0
        if f > (self.file.getframerate()/2) - (self.getBandWidth()/2):
            return self.sample_size -1
        fraction = float(f)/float(self.file.getframerate())
        index = round(self.sample_size * fraction)
        return index
    ###################################################################################################################

    def draw_bars(self):
        for w in range(self.width):
            for h in range(self.num_bands):
                self.model.set_pixel(h, w, self.colors[w] if w < int(self.averages[h]*self.width/1000) else 'black')

    def run(self):
        try:
            data = self.file.readframes(self.chunk)
            last_update = time.time()
            while data != '':
                if True: #time.time()-last_update > 1./self.fft_display_rate:
                    mono_data = audioop.tomono(data, self.file.getsampwidth(), 0.5, 0.5)
                    local_max_level = audioop.max(mono_data, self.file.getsampwidth())
                    local_dB = int(20*(math.log10(local_max_level/self.max_level)))
                    self.levels.append(local_dB)
                    self.fft(mono_data)
                    self.draw_bars()

                    if not self.with_sound:
                        plot(self.averages)
                        show()
                    last_update = time.time()

                if self.with_sound:
                    self.stream.write(data)
                data = self.file.readframes(self.chunk)
        finally:
            if self.with_sound:
                self.stream.stop_stream()
                self.stream.close()
                self.pyaudio.terminate()



if __name__=='__main__':
    dbm = DBMeter(15, 10, 'Spectrum.wav', True)
    #dbm = DBMeter(15, 10, 'Love_you.wav', True)
    #dbm = DBMeter(15, 10, 'Nytrogen_-_Nytrogen_-_Jupiter.wav', True)
    #dbm = DBMeter(15, 10, 'Lion.wav', True)
    #dbm = DBMeter(15, 10, 'Silence.wav', False)

    dbm.start()

