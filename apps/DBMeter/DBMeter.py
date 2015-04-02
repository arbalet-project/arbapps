#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Spectrum Analyzer for Audio files

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
from arbasdk import Arbamodel, Arbapp, hsv
from threading import Thread
import pyaudio, audioop, wave, time

class Renderer(Thread):
    """
    This thread renders the FFT bands on Arbalet
    It is in charge of all colors and animations
    """
    def __init__(self, rate, model, height, width, vertical=True):
        Thread.__init__(self)
        self.setDaemon(True)
        self.rate = rate
        self.model = model
        self.height = height
        self.width = width
        self.averages = None
        self.num_bands = width if vertical else height
        self.vertical = vertical
        self.colors = [hsv(c, 100, 100) for c in range(0, 360, int(360./self.num_bands))]

    def update_bands(self, averages):
        """
        This function is called when a new FFT is available and sent to the render thanks to the latter
        TODO: thread-safe
        """
        self.averages = averages

    def draw_bars(self):
        if self.averages:
            if self.vertical:
                for h in range(self.height):
                    for w in range(self.num_bands):
                        self.model.set_pixel(h, w, self.colors[w] if h < int(self.averages[w]/10000000) else 'black')
            else:
                for w in range(self.width):
                    for h in range(self.num_bands):
                        self.model.set_pixel(h, w, self.colors[h] if w < int(self.averages[h]/10000000) else 'black')

    def run(self):
        while True:
            self.draw_bars()
            time.sleep(1./self.rate)


class DBMeter(Arbapp):
    """
    This is the main entry point of the spectrum analyser, it reads the file, computes the FFT and plays the sound
    """
    def __init__(self, height, width, file, with_sound=True, vertical=True):
        Arbapp.__init__(self, width, height)
        self.chunk = 4*1024
        self.with_sound = with_sound
        self.file = wave.open(file, 'rb')
        self.vertical = vertical
        if self.with_sound:
            self.pyaudio = pyaudio.PyAudio()
            self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.file.getsampwidth()),
                                            channels=self.file.getnchannels(),
                                            rate=self.file.getframerate(),
                                            output=True)
        ##### Init and start the renderer
        model = Arbamodel(width, height, 'black')
        self.set_model(model)
        self.renderer = Renderer(100, model, height, width, vertical)
        self.renderer.start()

        ##### Fourier related attributes
        if self.vertical:
            self.num_bands = self.width
        else:
            self.num_bands = self.height # TODO 12 bands and more generate <10Hz bands
    ############################################# Fourier-related methods #############################################
    def fft(self, sample):
        def chunks(l, n):
            for i in xrange(0, len(l), n):
                yield l[i:i+n]

        def str_to_int(string):
            return struct.unpack('<h', string)[0] # Convert little-endian char into int

        sample_range = map(str_to_int, list(chunks(sample, self.file.getsampwidth())))
        fft_data = abs(numpy.fft.rfft(sample_range)) # real fft gives samplewidth/2 bands
        fft_freq = numpy.fft.rfftfreq(len(sample_range))
        freq_hz = [abs(fft_freq[i])*self.file.getframerate() for i, fft in enumerate(fft_data)]

        db_scale = [self.file.getframerate()*2**(b-self.num_bands) for b in range(self.num_bands)]
        fft_freq_scaled = [0.]*len(db_scale)

        ref_index = 0
        for i, f in enumerate(fft_data):
            if freq_hz[i]>db_scale[ref_index]:
                ref_index += 1
            fft_freq_scaled[ref_index] += f

        #numpy.set_printoptions(threshold=numpy.nan)
        #print fft_freq_scaled
        self.averages = fft_freq_scaled
    ###################################################################################################################

    def run(self):
        try:
            data = self.file.readframes(self.chunk)
            while data != '':
                mono_data = audioop.tomono(data, self.file.getsampwidth(), 0.5, 0.5)
                self.fft(mono_data)
                self.renderer.update_bands(self.averages)

                if self.with_sound:
                    self.stream.write(data)
                data = self.file.readframes(self.chunk)
        finally:
            if self.with_sound:
                self.stream.stop_stream()
                self.stream.close()
                self.pyaudio.terminate()



if __name__=='__main__':


    #dbm = DBMeter(15, 10, 'Spectrum.wav', True)
    #dbm = DBMeter(15, 10, 'Love_you.wav', True)
    #dbm = DBMeter(15, 10, 'Nytrogen_-_Nytrogen_-_Jupiter.wav', True)
    dbm = DBMeter(15, 10, 'survive.wav', True)
    #dbm = DBMeter(15, 10, 'Lion.wav', True)
    #dbm = DBMeter(15, 10, 'Silence.wav', False)

    dbm.start()

