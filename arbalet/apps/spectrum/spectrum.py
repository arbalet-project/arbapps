#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Spectrum Analyzer for Audio files

    This Spectrum analyzer has 2 classes:
    * SpectrumAnalyser: reading a wave file, computing the Discrete Fourier Transform
      (DFT, FFT) for each chunk of file, and playing the chunk of sound
    * Renderer: coloring the table with respect to the FFT
    It works in vertical and horizontal, splitting the range of frequencies consequently

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
import struct, numpy, alsaaudio, audioop, wave
from collections import deque
from arbalet.core import Arbapp, hsv
from copy import copy
from random import shuffle

class Renderer():
    """
    This class renders the FFT bands on Arbalet
    It is in charge of all colors and animations once a FFT averages list arrives in draw_bars()
    """
    def __init__(self, model, height, width, num_bins, num_bands, vertical=True):
        self.model = model
        self.height = height
        self.width = width
        self.num_bands = num_bands
        self.num_bins = num_bins
        self.vertical = vertical
        self.colors = [hsv(c, 100, 100) for c in range(0, 360, int(360./self.num_bands))]

        # A window stores the last len_window samples to scale the height of the spectrum
        self.max = 1000000
        self.window = deque()
        self.len_window = 50

    def draw_frame(self, bands):
        """
        Draw the bins using FFT averages whatever the orientation is.
        """
        self.old_model = copy(self.model)
        if len(self.window) == self.len_window:
            self.window.popleft()
            self.max = numpy.average(numpy.array(self.window))
        self.window.append(max(bands))

        with self.model:
            for bin in range(self.num_bins):
                ampli_b = bin*self.max/(self.num_bins-2)
                for band in range(self.num_bands):
                    if ampli_b < bands[band]:
                        color = self.colors[band]
                    elif self.old_model: # animation with light decreasing
                        old = self.old_model.get_pixel(bin if self.vertical else band, band if self.vertical else bin).hsva
                        color = hsv(old[0], old[1], old[2]*0.875)
                    else:
                        color = 'black'
                    self.model.set_pixel(bin if self.vertical else band, band if self.vertical else bin, color)

class SpectrumAnalyser(Arbapp):
    """
    This is the main entry point of the spectrum analyser, it reads the file, computes the FFT and plays the sound
    """
    def __init__(self, argparser):
        Arbapp.__init__(self, argparser)
        self.chunk = 1024
        self.parser = argparser
        self.renderer = None
        self.file = None
        self.output = alsaaudio.PCM()

        ##### Fourier related attributes, we generate a suitable log-scale
        self.num_bands = self.width if self.args.vertical else self.height
        self.min = 50
        self.max = 22050
        #self.db_scale = [self.framerate*2**(b-self.num_bands) for b in range(self.num_bands)]
        #self.db_scale = [self.min+self.max*2**(b-self.num_bands+1) for b in range(self.num_bands)]
        self.db_scale = [self.max*(numpy.exp(-numpy.log(float(self.min)/self.max)/self.num_bands))**(b-self.num_bands) for b in range(1, self.num_bands+1)]
        print("Scale of maximum frequencies:", list(map(int, self.db_scale)))

    def fft(self, sample):
        """
        Compute the FFT on this sample and update the self.averages FFT result
        """
        sample_range = struct.unpack('<{}h'.format(len(sample)//self.sample_width), sample)
        fft_data = abs(numpy.fft.rfft(sample_range)) # real fft gives samplewidth/2 bands
        try:
            fft_freq = numpy.fft.rfftfreq(len(sample_range))
        except AttributeError:   # numpy<1.8
            fft_freq = [0.5/len(fft_data)*f for f in range(len(fft_data))]
        freq_hz = [abs(fft_freq[i])*self.framerate for i, fft in enumerate(fft_data)]
        fft_freq_scaled = [0.]*len(self.db_scale)
        ref_index = 0
        for i, f in enumerate(fft_data):
            if freq_hz[i]>self.db_scale[ref_index]:
                ref_index += 1
            fft_freq_scaled[ref_index] += f
        self.averages = fft_freq_scaled

    def play_file(self, f):
        try:
            self.file = wave.open(f, 'rb')
        except IOError as e:
            print("Can't open file {}, skipping: {}".format(f, repr(e)))
        else:
            try:
                self.output.setchannels(self.file.getnchannels())
                self.framerate = self.file.getframerate()
                self.output.setrate(self.framerate)
                self.output.setformat(alsaaudio.PCM_FORMAT_S16_LE)
                self.output.setperiodsize(self.chunk)
                self.sample_width = self.file.getsampwidth()

                while True:
                    data = self.file.readframes(self.chunk)
                    if not data: break
                    mono_data = audioop.tomono(data, self.sample_width, 0.5, 0.5)
                    self.fft(mono_data)
                    self.renderer.draw_frame(self.averages)

                    self.output.write(data)
            finally:
                self.file.close()


    def run(self):
        num_bands = self.width if self.args.vertical else self.height
        num_bins = self.height if self.args.vertical else self.width
        self.renderer = Renderer(self.model, self.height, self.width, num_bins, num_bands, self.args.vertical)

        if self.args.random != 'none':
            shuffle(self.args.input)
        if self.args.random == 'once':
            self.args.input = self.args.input[:1]

        for f in self.args.input:
            self.play_file(f)

