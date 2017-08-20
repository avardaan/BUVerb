#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Vardaan Aashish
email: vardaan@bu.edu

Purpose: Final Project for CS591
Instructor: Wayne Snyder

Topic: Convolution Reverb with IRs from around BU
"""

# Custom functions modified from thinkdsp.py


import wave as wv
import numpy as np
import thinkplot
import copy
import subprocess



def quantize(ys, bound, dtype):
    """
    Maps the wave to quanta where ys=wave array, 
    bound=max_amp, dtype=np data type
    """
    if max(ys) > 1 or min(ys) < -1:
        print('Warning: normalizing before quantizing.')
        ys = normalize(ys)
        
    zs = (ys * bound).astype(dtype)
    return zs


def find_index(x, xs):
    """Find the index corresponding to a given value in an array."""
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n-1) * (x - start) / (end - start))
    return int(i)


def apodize(ys, samplerate, denom=20, duration=0.1):
    """
    Tapers the amplitude at the beginning and end of the signal.
    ys: wave array
    samplerate: int frames per second
    denom: float fraction of the segment to taper
    duration: float duration of the taper in seconds
    """
    # a fixed fraction of the segment
    n = len(ys)
    k1 = n // denom

    # a fixed duration of time
    k2 = int(duration * samplerate)

    k = min(k1, k2)

    w1 = np.linspace(0, 1, k)
    w2 = np.ones(n - 2*k)
    w3 = np.linspace(1, 0, k)

    window = np.concatenate((w1, w2, w3))
    return ys * window


def truncate(ys, n):
    """
    Trims a wave array to the given length.
    ys: wave array
    n: integer length
    """
    return ys[:n]

def zero_pad(arr, n):
    """
    Extends an array with zeros.
    array: numpy array
    n: length of result
    """
    res = np.zeros(n)
    res[:len(arr)] = arr
    return res


def normalize(ys, amp=1.0):
    """
    Normalizes a wave array so the maximum amplitude is max_amp or min_amp.
    ys: wave array
    amp: max amplitude (pos or neg) in result
    """
    high = abs(max(ys))
    low = abs(min(ys))
    return amp * ys / max(high, low)



class Wave:
    """ Represents a discrete-time signal. """
    
    def __init__(self, ys, ts=None, samplerate=44100):
        """
        Initializes the wave.
        ys: wave array
        ts: array of times
        samplerate: samples per second
        """
        self.ys = np.asanyarray(ys)
        self.samplerate = samplerate if samplerate is not None else 44100

        if ts is None:
            self.ts = np.arange(len(ys)) / self.samplerate
        else:
            self.ts = np.asanyarray(ts)

    def copy(self):
        """
        Makes a deep copy of the wave
        """
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.ys)


    def duration(self):
        """Duration (property).

        returns: float duration in seconds
        """
        return float(len(self.ys) / self.samplerate)

    def __add__(self, other):
        """
        Adds two waves elementwise.
        """
        if other == 0:
            return self

        assert self.samplerate == other.samplerate

        # make an array of times that covers both waves
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        n = int(round((end - start) * self.samplerate)) + 1
        ys = np.zeros(n)
        ts = start + np.arange(n) / self.samplerate

        def add_ys(wv):
            i = find_index(wv.start, ts)

            # make sure the arrays line up reasonably well
            diff = ts[i] - wv.start
            dt = 1 / wv.samplerate
            if (diff / dt) > 0.1:
                warnings.warn("Can't add these waveforms; their "
                              "time arrays don't line up.")

            j = i + len(wv)
            ys[i:j] += wv.ys

        add_ys(self)
        add_ys(other)

        return Wave(ys, ts, self.samplerate)

    __radd__ = __add__
        
    def __or__(self, other):
        """
        Concatenates two waves.
        """
        if self.samplerate != other.samplerate:
            raise ValueError('Wave.__or__: samplerates do not agree')

        ys = np.concatenate((self.ys, other.ys))
        # ts = np.arange(len(ys)) / self.samplerate
        return Wave(ys, samplerate=self.samplerate)

    def __mul__(self, other):
        """Multiplies two waves elementwise.

        Note: this operation ignores the timestamps; the result
        has the timestamps of self.

        other: Wave

        returns: new Wave
        """
        # the spectrums have to have the same samplerate and duration
        assert self.samplerate == other.samplerate
        assert len(self) == len(other)

        ys = self.ys * other.ys
        return Wave(ys, self.ts, self.samplerate)
        
    
    
    def convolve(self, other):
        """Convolves two waves.

        Note: this operation ignores the timestamps; the result
        has the timestamps of self.

        other: Wave or NumPy array
        
        returns: Wave
        """
        if isinstance(other, Wave):
            assert self.samplerate == other.samplerate
            window = other.ys
        else:
            window = other

        ys = np.convolve(self.ys, window, mode='full')
        #ts = np.arange(len(ys)) / self.samplerate
        return Wave(ys, samplerate=self.samplerate)



    def apodize(self, denom=20, duration=0.1):
        """Tapers the amplitude at the beginning and end of the signal.

        Tapers either the given duration of time or the given
        fraction of the total duration, whichever is less.

        denom: float fraction of the segment to taper
        duration: float duration of the taper in seconds
        """
        self.ys = apodize(self.ys, self.samplerate, denom, duration)

    def scale(self, factor):
        """Multplies the wave by a factor.

        factor: scale factor
        """
        self.ys *= factor

    def shift(self, shift):
        """Shifts the wave left or right in time.

        shift: float time shift
        """
        self.ts += shift

        
    def truncate(self, n):
        """Trims this wave to the given length.

        n: integer index
        """
        self.ys = truncate(self.ys, n)
        self.ts = truncate(self.ts, n)

    def zero_pad(self, n):
        """Trims this wave to the given length.

        n: integer index
        """
        self.ys = zero_pad(self.ys, n)
        self.ts = self.start + np.arange(n) / self.samplerate

    def normalize(self, amp=1.0):
        """Normalizes the signal to the given amplitude.

        amp: float amplitude
        """
        self.ys = normalize(self.ys, amp=amp)

    
    def segment(self, start=None, duration=None):
        """Extracts a segment.

        start: float start time in seconds
        duration: float duration in seconds

        returns: Wave
        """
        if start is None:
            start = self.ts[0]
            i = 0
        else:
            i = self.find_index(start)

        j = None if duration is None else self.find_index(start + duration)
        return self.slice(i, j)

    def slice(self, i, j):
        """Makes a slice from a Wave.

        i: first slice index
        j: second slice index
        """
        ys = self.ys[i:j].copy()
        ts = self.ts[i:j].copy()
        return Wave(ys, ts, self.samplerate)

    
    def get_xfactor(self, options):
        try:
            xfactor = options['xfactor']
            options.pop('xfactor')
        except KeyError:
            xfactor = 1
        return xfactor

    def plot(self, **options):
        """Plots the wave.

        """
        xfactor = self.get_xfactor(options)
        thinkplot.plot(self.ts * xfactor, self.ys, **options)

    def quantize(self, bound, dtype):
        """Maps the waveform to quanta.

        bound: maximum amplitude
        dtype: numpy data type or string

        returns: quantized signal
        """
        return quantize(self.ys, bound, dtype)
        
    
    def write(self, filename='sound.wav'):
        """Write a wave file.

        filename: string
        """
        print('Writing:', filename)
        # WaveFileWriter imported directly from thinkdsp
        wfile = WavFileWriter(filename, self.samplerate)
        wfile.write(self)
        wfile.close()
        print(filename, 'successfully written!')
    
    


def read(filename = 'sound.wav'):
    """Reads a wave file.

    filename: string

    returns: Wave
    """
    fp = wv.open(filename, 'r')

    nchannels = fp.getnchannels()
    nframes = fp.getnframes()
    sampwidth = fp.getsampwidth()
    samplerate = fp.getframerate()
    
    raw = fp.readframes(nframes)
    
    fp.close()

    dtype_map = {1:np.int8, 2:np.int16, 3:'special', 4:np.int32}
    if sampwidth not in dtype_map:
        raise ValueError('sampwidth %d unknown' % sampwidth)
    
    if sampwidth == 3:
        xs = np.fromstring(raw, dtype=np.int8).astype(np.int32)
        ys = (xs[2::3] * 256 + xs[1::3]) * 256 + xs[0::3]
    else:
        ys = np.fromstring(raw, dtype=dtype_map[sampwidth])

    # if it's in stereo, just pull out the first channel
    if nchannels == 2:
        # ys = ys[::2]
        print("cannot read stereo tracks")
        return

    #ts = np.arange(len(ys)) / samplerate
    wave = Wave(ys, samplerate=samplerate)
    wave.normalize()
    
    # personal modification to read audio files as np arrays
    #X = array.array('h', ys)
    #X = np.array(X,dtype='int16')
        
    return wave


class WavFileWriter:
    """Writes wav files."""

    def __init__(self, filename='sound.wav', samplerate=44100):
        """Opens the file and sets parameters.

        filename: string
        samplerate: samples per second
        """
        self.filename = filename
        self.samplerate = samplerate
        self.nchannels = 1
        self.sampwidth = 2
        self.bits = self.sampwidth * 8
        self.bound = 2**(self.bits-1) - 1

        self.fmt = 'h'
        self.dtype = np.int16

        self.fp = wv.open(self.filename, 'w')
        self.fp.setnchannels(self.nchannels)
        self.fp.setsampwidth(self.sampwidth)
        self.fp.setframerate(self.samplerate)
    
    def write(self, wave):
        """Writes a wave.

        wave: Wave
        """
        zs = wave.quantize(self.bound, self.dtype)
        self.fp.writeframes(zs.tostring())

    def close(self, duration=0):
        """Closes the file.

        duration: how many seconds of silence to append
        """
        if duration:
            self.write(np.zeros(duration*self.samplerate))

        self.fp.close()


