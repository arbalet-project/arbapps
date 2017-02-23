#!/usr/bin/env python
"""
    Arbalet - ARduino-BAsed LEd Table
    Musical spectrum analyzer, read the default system stream and render its spectrum

    It works in vertical and horizontal, splitting the range of frequencies consequently

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""
from collections import deque
from arbalet.core import Application, Rate
from arbalet.colors import mul, hsv_to_rgb
from copy import copy

import numpy
import pyaudio
import numpy as np


class Renderer(object):
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
        self.colors = [hsv_to_rgb((float(c)/self.num_bands, 1., 1.)) for c in range(self.num_bands)]

        # A window stores the last len_window samples to scale the height of the spectrum
        self.max = 150  # Empiric value of an average sum to start with
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
                        old = self.old_model.get_pixel(bin if self.vertical else band, band if self.vertical else bin)
                        color = mul(old, 0.875)
                    else:
                        color = 'black'
                    self.model.set_pixel(bin if self.vertical else band, band if self.vertical else bin, color)


class SpectrumAnalyser(Application):
    """
    This is the main entry point of the spectrum analyser, it reads the file, computes the FFT and plays the sound
    """
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.parser = argparser
        self.renderer = None
        self.framerate = 44100

        ##### Fourier related attributes, we generate a suitable log-scale
        self.num_bands = self.width if self.args.vertical else self.height
        self.min = 50
        self.max = 22050
        #self.db_scale = [self.framerate*2**(b-self.num_bands) for b in range(self.num_bands)]
        #self.db_scale = [self.min+self.max*2**(b-self.num_bands+1) for b in range(self.num_bands)]
        self.db_scale = [self.max*(numpy.exp(-numpy.log(float(self.min)/self.max)/self.num_bands))**(b-self.num_bands) for b in range(1, self.num_bands+1)]
        print("Scale of maximum frequencies:", list(map(int, self.db_scale)))

    def get_fft(self, sample):
        """
        Compute the FFT on this sample and update the self.averages FFT result
        """
        fft_data = abs(numpy.fft.rfft(sample)) # real fft gives samplewidth/2 bands
        try:
            fft_freq = numpy.fft.rfftfreq(len(sample))
        except AttributeError:   # numpy<1.8
            fft_freq = [0.5/len(fft_data)*f for f in range(len(fft_data))]
        freq_hz = [abs(fft_freq[i])*self.framerate for i, fft in enumerate(fft_data)]
        fft_freq_scaled = [0.]*len(self.db_scale)
        ref_index = 0
        for i, f in enumerate(fft_data):
            if freq_hz[i]>self.db_scale[ref_index]:
                ref_index += 1
            fft_freq_scaled[ref_index] += f
        return fft_freq_scaled

    def callback(self, in_data, frame_count, time_info, flag):
        self.sample_width = frame_count
        audio_data = np.fromstring(in_data, dtype=np.float32)
        averages = self.get_fft(audio_data)
        self.renderer.draw_frame(averages)

        return None, pyaudio.paContinue

    def run(self):
        pa = pyaudio.PyAudio()
        num_bands = self.width if self.args.vertical else self.height
        num_bins = self.height if self.args.vertical else self.width
        self.renderer = Renderer(self.model, self.height, self.width, num_bins, num_bands, self.args.vertical)

        input_device_info = pa.get_default_input_device_info()
        self.framerate = int(input_device_info['defaultSampleRate'])

        stream = pa.open(format=pyaudio.paFloat32,
                         channels=1,
                         rate=self.framerate,
                         output=False,
                         input=True,
                         stream_callback=self.callback)

        stream.start_stream()

        rate = Rate(5)
        while stream.is_active():
            rate.sleep()

        stream.close()
        pa.terminate()

