import math
import threading
import time

import numpy as np
import pyaudio

#BITRATE = 1024 * 40 #  31440 Hz and 10480 Hz possible on Atari
#BITRATE = 44100
BITRATE = 10480

waveform_0 = np.array([1]).astype(np.float32)
waveform_1 = np.array([0,0,1,0,1,0,0,0,0,1,1,1,0,1,1]).astype(np.float32)
waveform_4 = np.array([0, 1]).astype(np.float32)
waveform_7 = np.array([0,0,1,0,1,1,0,0,1,1,1,1,1,0,0,0,1,1,0,1,1,1,0,1,0,1,0,0,0,0,1]).astype(np.float32)

WAVEFORMS = {
    #0: waveform_0,
    1: waveform_1,
    4: waveform_4,
    7: waveform_7
}


# Create a sample by stretching the waveforms by a frequency number
# frequency = 4
# sample = np.repeat(waveform_x, frequency)
# Then extend the length with tile
# sample = np.tile(sample, x)

# Create two streams like this
# p = PyAudio()
# stream = p.open(format = pyaudio.paFloat32,
#                 channels = 1,
#                 rate = BITRATE,
#                 output = True)


# https://www.randomterrain.com/atari-2600-memories-music-and-sound.html#freq_wav_guide
# https://www.randomterrain.com/atari-2600-memories-batari-basic-music-toy.html
# https://stackoverflow.com/questions/47513950/how-to-loop-play-an-audio-with-pyaudio
# https://stackoverflow.com/questions/67045992/how-can-i-make-my-audio-loop-with-pyaudio

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

class AudioChannel:
    def __init__(self, audio):
        self._audio = audio
        self._frames_per_buffer = self._audio._frames_per_buffer

        self._volume = 0
        self._frequency = 1
        self._waveform = 1
        self._index = 0
        self._sample = np.zeros(self._frames_per_buffer)
        #self._set_sample()

    def _set_sample(self):
        self._index = 0
        if self._volume == 0 or self._frequency == 0:
            self._sample = np.zeros(self._frames_per_buffer)
        else:
            waveform = WAVEFORMS[self._waveform]
            self._sample = np.repeat(waveform*self._volume, self._frequency)
            num_tiles = lcm(len(self._sample), self._frames_per_buffer)
            #num_tiles = abs(len(self._sample) * self._frames_per_buffer) // math.gcd(len(self._sample), self._frames_per_buffer)
            self._sample = np.tile(self._sample, num_tiles)

        self._audio._set_sample()

    def get_sample_slice(self):
        #sample = self._sample.take(range(self._index, self._index+self._frames_per_buffer), mode='wrap')
        sample = self._sample[self._index: self._index + self._frames_per_buffer]
        self._index = (self._index + self._frames_per_buffer) % len(self._sample)
        return sample

    #def get_sample(self):
    #    waveform = WAVEFORMS[self._waveform]
    #    return np.repeat(waveform*self._volume, max(self._frequency, 1))

    # @property
    # def volume(self):
    #     return self._volume
    #
    # @volume.setter
    # def volume(self):

def create_property(attr):
    internal_name = f"_{attr}"
    setattr(AudioChannel, attr, property(lambda self: getattr(self, internal_name)))
    #print(AudioChannel.volume)

    def setter(self, value):
        #print(self, internal_name, value)
        setattr(self, internal_name, value)
        self._set_sample()
        #self._audio.set_sample()

    setattr(AudioChannel, attr, getattr(AudioChannel, attr).setter(setter))

for attr in ["volume", "frequency", "waveform"]:
    create_property(attr)


class Audio(threading.Thread):
    def __init__(self):
        super().__init__()
        self._frames_per_buffer = 1024

        self.channel_1 = AudioChannel(self)
        self.channel_2 = AudioChannel(self)

        # self.volume_1 = 0
        # self.frequency_1 = 1
        # self.waveform_1 = waveform_1
        #
        # self.volume_2 = 0
        # self.frequency_2 = 1
        # self.waveform_2 = waveform_4

        self.loop = True

        #self.set_sample()
        self._set_sample()

        #self.run()

    def _set_sample(self):
        #sample_1 = self.channel_1.get_sample_slice()
        #sample_2 = self.channel_2.get_sample_slice()
        sample_1 = self.channel_1._sample
        sample_2 = self.channel_2._sample
        print(len(sample_1), len(sample_2))
        l = lcm(len(sample_1), len(sample_2))
        sample_1 = np.tile(sample_1, l // len(sample_1))
        sample_2 = np.tile(sample_2, l // len(sample_2))
        print(l, len(sample_1), len(sample_2))

        self._sample = np.dstack((sample_1, sample_2)).flatten()
        self._index = 0

    # def set_sample(self):
    #     #sample_1 = np.repeat(self.waveform_1*self.volume_1, self.frequency_1)
    #     sample_1 = self.channel_1.get_sample()
    #     print("sample_1", len(sample_1), sample_1.sum())
    #     sample_1 = np.tile(sample_1, int(np.ceil(self.frames_per_buffer/(len(sample_1)))))
    #     print("sample_1", len(sample_1), sample_1.sum())
    #     #sample_1 = sample_1[:self.frames_per_buffer]
    #     print("sample_1", len(sample_1), sample_1.sum())
    #
    #     sample_2 = self.channel_2.get_sample()
    #     sample_2 = np.tile(sample_2, self.frames_per_buffer//(len(sample_2) + 1))
    #     sample_2 = np.pad(sample_2, (0, self.frames_per_buffer))[:self.frames_per_buffer]
    #     print("sample_2", len(sample_2), sample_2.sum())
    #
    #     #self.sample = np.concatenate((sample_1, sample_2))
    #     self.sample = np.array(list(zip(sample_1, sample_2))).flatten()
    #
    #     #print(self.sample.tolist())

    # def stream_callback(self, in_data, frame_count, time_info, status_flags):
    #     #print(self.waveform)
    #     #print(in_data)
    #     #sample = np.repeat(self.waveform_1, self.frequency_1)
    #     #sample = np.tile(sample, self.frames_per_buffer//2)[:self.frames_per_buffer]
    #     #print(self.loop, self.sample)
    #     #print("callback", self.sample)
    #
    #     #sample_1 = self.channel_1.get_sample_slice()
    #     #sample_2 = self.channel_2.get_sample_slice()
    #     #sample = np.dstack((sample_1, sample_2)).flatten()
    #     sample = self._sample[self._index:self._index + self._frames_per_buffer * 4]
    #     #sample = self._sample[:self._frames_per_buffer * 2]
    #     print(len(sample), sample.sum())
    #     self._index += self._frames_per_buffer * 2
    #     if self.loop:
    #         #print(len(self.sample))
    #         return (sample, pyaudio.paContinue)
    #     else:
    #         #print("WHY DID YOU STOP?")
    #         return (in_data, pyaudio.paComplete)


    def run(self):
        #self.sample = np.repeat(self.waveform, self.frequency)

        player = pyaudio.PyAudio()
        stream = player.open(format = pyaudio.paFloat32,
                        channels = 2,
                        rate = BITRATE,
                        output = True,
                        #frames_per_buffer = len(self.sample),
                        frames_per_buffer = self._frames_per_buffer,
                        #stream_callback = self.stream_callback,
                        )

        # PLAYBACK LOOP
        #data = wf.readframes(self.CHUNK)

        #sample = np.repeat(self.waveform, self.frequency)
        #sample = np.tile(sample, 4)
        #sample = np.tile(self.waveform, self.frequency)

        #reps = BITRATE // 60 // len(sample)

        #sample = np.tile(sample, reps)

        #print(sample.tolist())

        #stream.start_stream()

        #self.stream = stream

        #while self.loop:
            #print(sample.tolist())
            #stream.write(sample)
            #data = wf.readframes(self.CHUNK)
            #if data == b'':  # If file is over then rewind.
            #    wf.rewind()
            #    data = wf.readframes(self.CHUNK)

        while self.loop:
            #stream.write(self._sample)
            #continue
            sample = self._sample[self._index:self._index + self._frames_per_buffer * 2]
            stream.write(sample)
            #print(len(sample), sample.sum())
            self._index = (self._index + self._frames_per_buffer * 2) % len(self._sample)

    # def play(self, frequency=None, waveform=None, volume=None):
    #     self.loop = True
    #
    #     if frequency is not None:
    #         self.frequency = frequency
    #
    #     if waveform is not None:
    #         self.waveform = waveform
    #
    #     if volume is not None:
    #         self.volume = volume
    #
    #     self.start()

    def stop(self):
        self.loop = False

audio = Audio()
audio.start()
audio.channel_1.volume = 1


# for k in WAVEFORMS:
#     for frequency in range(32):
#         audio.channel_1.waveform = k
#         audio.channel_1.frequency = frequency
#         print(k, frequency)
#         #print(audio.sample)
#         #print(len(audio.sample), audio.sample.sum())
#         #print(audio.stream.is_active())
#         time.sleep(.5)

audio.channel_1.waveform = 4
audio.channel_1.frequency = 25
time.sleep(3)

#audio.frequency = 32
#audio.

# ac = AudioChannel(None)
# ac.volume = 1
# print(ac._volume)
#
#
# 1/0

# audio = Audio()
#
# audio.channel_1.waveform = 4
# audio.channel_1.frequency = 8
# audio.channel_1.volume = 1
#
# audio.channel_2.waveform = 7
# audio.channel_2.frequency = 32
#
# #audio.set_sample()
#
# for i in range(5):
#     time.sleep(.5)
#     audio.channel_2.volume = 1
#     #audio.set_sample()
#     time.sleep(.5)
#     audio.channel_2.volume = 0
#     #audio.set_sample()

# channel_1 = AudioChannel(waveform_4)
# channel_2 = AudioChannel(waveform_1)
#
# channel_1.play(frequency=64)
# channel_2.play(frequency=32)

#time.sleep(3)

#channel_1.stop()
#channel_2.stop()

audio.stop()
