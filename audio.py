import numpy as np
import sounddevice as sd
import math
import time
#duration = 2  # seconds

BITRATE = 32000
BLOCKSIZE = 1024

waveform_0 = np.array([1]).astype(np.float32)
waveform_1 = np.array([0,0,1,0,1,0,0,0,0,1,1,1,0,1,1]).astype(np.float32)
waveform_4 = np.array([0, 1]).astype(np.float32)
waveform_7 = np.array([0,0,1,0,1,1,0,0,1,1,1,1,1,0,0,0,1,1,0,1,1,1,0,1,0,1,0,0,0,0,1]).astype(np.float32)

WAVEFORMS = {
    0: waveform_0,
    1: waveform_1,
    4: waveform_4,
    7: waveform_7
}

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

class AudioChannel:
    def __init__(self):
        #self._audio = audio
        self._frames_per_buffer = BLOCKSIZE#self._audio._frames_per_buffer

        self._volume = 0
        self._frequency = 1
        self._waveform = 1
        self._index = 0
        self._sample = np.zeros(self._frames_per_buffer)
        #self._set_sample()

    def _set_sample(self):
        #self._index = 0
        if self._volume == 0 or self._frequency == 0:
            self._index, self._sample = 0, np.zeros(self._frames_per_buffer)
        else:
            waveform = WAVEFORMS[self._waveform]
            sample = np.repeat(waveform*self._volume, self._frequency)
            #num_tiles = lcm(len(sample), self._frames_per_buffer)
            self._index, self._sample = 0, sample#np.tile(sample, num_tiles)

        #print(len(self._sample) / BLOCKSIZE)

        #self._audio._set_sample()

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

# frequency = 32
# volume = 1
# sample = volume * np.repeat(waveform_4, frequency)
# sample = np.tile(sample, int(np.ceil(BLOCKSIZE / len(sample))))
# #sample = sample.reshape(-1,1)
# i = 0

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

#ac = AudioChannel()
#ac.volume = 1
#ac.waveform = 4
#ac.frequency = 16

audio = Audio()
#audio.volume = 1
#audio.channel_1.volume = 2
#audio.channel_1.waveform = 4
#audio.channel_1.frequency = 28

def callback(outdata, frames, time, status):
    #global i
    #print(frames, time.outputBufferDacTime, time.currentTime)
    #if status:
    #    print(status)
    #outdata[:] = sample[:BLOCKSIZE]
    #outdata[:] = sample.take(range(i, i+BLOCKSIZE), mode='wrap').reshape(-1,1)
    #i = (i + BLOCKSIZE) % len(sample)
    #outdata[:] = global_volume*ac.get_sample_slice().reshape(-1,1)
    outdata[:] = audio.get_sample_slice()

audio_context = sd.OutputStream(samplerate=BITRATE, channels=1, callback=callback, blocksize=BLOCKSIZE)

#with sd.OutputStream(samplerate=BITRATE, channels=1, callback=callback, blocksize=BLOCKSIZE):
    #sd.sleep(int(duration * 1000))
    #time.sleep(duration)
#    for i in range(0, duration*10, 1):
#        audio.channel_1.frequency += 1
#        print(audio.channel_1.frequency)
#        time.sleep(.5)

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
