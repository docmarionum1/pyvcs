import numpy as np
import sounddevice as sd
import math
import time

BITRATE = 32000
BLOCKSIZE = 1024

waveform_0 = np.array([0, 1]).astype(np.float32)
waveform_1 = np.array([0,0,1,0,1,0,0,0,0,1,1,1,0,1,1]).astype(np.float32)
waveform_2 = np.array([0,0,1,0,1,1,0,0,1,1,1,1,1,0,0,0,1,1,0,1,1,1,0,1,0,1,0,0,0,0,1]).astype(np.float32)
waveform_3 = np.array([0,1,0,0,1,1,0,0,0,1,1,1,0,0,0,0,1,1,1,1]).astype(np.float32)
waveform_4 = np.array([0,0,0,0,1,0,0,0,0]).astype(np.float32)

WAVEFORMS = {
    0: waveform_0,
    1: waveform_1,
    2: waveform_2,
    3: waveform_3,
    4: waveform_4
}

class AudioChannel:
    def __init__(self):
        self._frames_per_buffer = BLOCKSIZE

        self._volume = 0
        self._frequency = 1
        self._waveform = 1
        self._index = 0
        self._sample = np.zeros(self._frames_per_buffer)

    def _set_sample(self):
        if self._volume == 0 or self._frequency == 0:
            self._index, self._sample = 0, np.zeros(self._frames_per_buffer)
        else:
            waveform = WAVEFORMS[self._waveform]
            sample = np.repeat(waveform*self._volume, self._frequency)
            self._index, self._sample = 0, sample


    def get_sample_slice(self):
        sample = self._sample.take(range(self._index, self._index+self._frames_per_buffer), mode='wrap')
        #sample = self._sample[self._index: self._index + self._frames_per_buffer]
        self._index = (self._index + self._frames_per_buffer) % len(self._sample)
        return sample


def create_property(attr):
    internal_name = f"_{attr}"
    setattr(AudioChannel, attr, property(lambda self: getattr(self, internal_name)))

    def setter(self, value):
        setattr(self, internal_name, value)
        self._set_sample()

    setattr(AudioChannel, attr, getattr(AudioChannel, attr).setter(setter))

for attr in ["volume", "frequency", "waveform"]:
    create_property(attr)

class Audio:
    def __init__(self):
        self.channel_1 = AudioChannel()
        self.channel_2 = AudioChannel()

        self.volume = 0

    def get_sample_slice(self):
        return self.volume * (
            self.channel_1.get_sample_slice() * .5 +
            self.channel_2.get_sample_slice() * .5
        ).reshape(-1,1)

audio = Audio()

def callback(outdata, frames, time, status):
    outdata[:] = audio.get_sample_slice()

audio_context = sd.OutputStream(samplerate=BITRATE, channels=1, callback=callback, blocksize=BLOCKSIZE)

if __name__ == '__main__':
    with audio_context:
        audio.volume = 1
        audio.channel_1.volume = 2
        audio.channel_1.waveform = 7
        audio.channel_1.frequency = 31

        #time.sleep(1)
        for i in range(10):
            audio.channel_1.volume -= .2
            audio.channel_1.frequency += 1
            time.sleep(.1)
