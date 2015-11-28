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
import struct, argparse, numpy, pyaudio, audioop, wave
from collections import deque
from arbasdk import Arbapp, hsv
from copy import copy

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

    def draw_bars(self, averages):
        """
        Draw the bins using FFT averages whatever the orientation is.
        """
        self.old_model = copy(self.model)
        if len(self.window) == self.len_window:
            self.window.popleft()
            self.max = numpy.average(numpy.array(self.window))
        self.window.append(max(averages))

        self.model.lock()
        for bin in range(self.num_bins):
            ampli_b = bin*self.max/(self.num_bins-2)
            for band in range(self.num_bands):
                if ampli_b < averages[band]:
                    color = self.colors[band]
                elif self.old_model: # animation with light decreasing
                    old = self.old_model.get_pixel(bin if self.vertical else band, band if self.vertical else bin).hsva
                    color = hsv(old[0], old[1], old[2]*0.875)
                else:
                    color = 'black'
                self.model.set_pixel(bin if self.vertical else band, band if self.vertical else bin, color)
        self.model.unlock()

class SpectrumAnalyser(Arbapp):
    """
    This is the main entry point of the spectrum analyser, it reads the file, computes the FFT and plays the sound
    """
    def __init__(self, argparser, vertical=True):
        Arbapp.__init__(self, argparser)
        self.chunk = 1024
        self.vertical = vertical
        self.parser = argparser
        self.renderer = None
        self.file = None
        print "Starting pyaudio..."
        self.pyaudio = pyaudio.PyAudio()

        ##### Fourier related attributes, we generate a suitable log-scale
        self.num_bands = self.width if self.vertical else self.height
        self.min = 50
        self.max = 22050
        #self.db_scale = [self.file.getframerate()*2**(b-self.num_bands) for b in range(self.num_bands)]
        #self.db_scale = [self.min+self.max*2**(b-self.num_bands+1) for b in range(self.num_bands)]
        self.db_scale = [self.max*(numpy.exp(-numpy.log(float(self.min)/self.max)/self.num_bands))**(b-self.num_bands) for b in range(1, self.num_bands+1)]
        print "Scale of maximum frequencies:", map(int, self.db_scale)

    def fft(self, sample):
        """
        Compute the FFT on this sample and update the self.averages FFT result
        """
        def chunks(l, n):
            for i in xrange(0, len(l), n):
                yield l[i:i+n]

        def str_to_int(string):
            return struct.unpack('<h', string)[0] # Convert little-endian char into int

        sample_range = map(str_to_int, list(chunks(sample, self.file.getsampwidth())))
        fft_data = abs(numpy.fft.rfft(sample_range)) # real fft gives samplewidth/2 bands
        try:
            fft_freq = numpy.fft.rfftfreq(len(sample_range))
        except AttributeError:   # numpy<1.8
            fft_freq = [0.5/len(fft_data)*f for f in range(len(fft_data))]
        freq_hz = [abs(fft_freq[i])*self.file.getframerate() for i, fft in enumerate(fft_data)]
        fft_freq_scaled = [0.]*len(self.db_scale)
        ref_index = 0
        for i, f in enumerate(fft_data):
            if freq_hz[i]>self.db_scale[ref_index]:
                ref_index += 1
            fft_freq_scaled[ref_index] += f
        self.averages = fft_freq_scaled

    def play_file(self, f):
        self.file = wave.open(f, 'rb')
        self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.file.getsampwidth()),
                                channels=self.file.getnchannels(),
                                rate=self.file.getframerate(),
                                output=True)
        try:
            data = self.file.readframes(self.chunk)
            while data != '':
                mono_data = audioop.tomono(data, self.file.getsampwidth(), 0.5, 0.5)
                self.fft(mono_data)
                self.renderer.draw_bars(self.averages)

                self.stream.write(data)
                data = self.file.readframes(self.chunk)
        finally:
            self.stream.stop_stream()
            self.stream.close()

    def run(self):
        num_bands = self.width if self.vertical else self.height
        num_bins = self.height if self.vertical else self.width
        self.renderer = Renderer(self.model, self.height, self.width, num_bins, num_bands, self.vertical)
        for f in self.args.input:
            self.play_file(f)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Spectrum analyzer of WAVE files')
    parser.add_argument('-i', '--input',
                        type=str,
                        required=True,
                        nargs='+',
                        help='Wave file(s) to play')
    SpectrumAnalyser(parser, vertical=False).start()
