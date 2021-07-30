import threading
import time

import numpy as np
import pyaudio

BITRATE = 31440 #  31440 Hz and 10480 Hz possible on Atari

waveform_0 = np.array([1]).astype(np.float32)
waveform_1 = np.array([0,0,1,0,1,0,0,0,0,1,1,1,0,1,1]).astype(np.float32)
waveform_4 = np.array([0, 1]).astype(np.float32)

WAVEFORMS = {
    0: waveform_0,
    1: waveform_1,
    4: waveform_4
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

class AudioChannel:
    def __init__(self, audio):
        self._audio = audio

        self._volume = 0
        self._frequency = 1
        self._waveform = 0

    def get_sample(self):
        waveform = WAVEFORMS[self._waveform]
        return np.repeat(waveform*self._volume, self._frequency)

    # @property
    # def volume(self):
    #     return self._volume
    #
    # @volume.setter
    # def volume(self):

def create_property(attr):
    internal_name = f"_{attr}"
    setattr(AudioChannel, attr, property(lambda self: getattr(self, internal_name)))
    print(AudioChannel.volume)

    def setter(self, value):
        print(self, internal_name, value)
        setattr(self, internal_name, value)
        self._audio.set_sample()

    setattr(AudioChannel, attr, getattr(AudioChannel, attr).setter(setter))

for attr in ["volume", "frequency", "waveform"]:
    create_property(attr)


class Audio(threading.Thread):
    def __init__(self):
        super().__init__()
        self.frames_per_buffer = 1024

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

        self.set_sample()

        self.run()

    def set_sample(self):
        #sample_1 = np.repeat(self.waveform_1*self.volume_1, self.frequency_1)
        sample_1 = self.channel_1.get_sample()
        sample_1 = np.tile(sample_1, self.frames_per_buffer//2)[:self.frames_per_buffer]

        sample_2 = self.channel_2.get_sample()
        sample_2 = np.tile(sample_2, self.frames_per_buffer//2)[:self.frames_per_buffer]

        #self.sample = np.concatenate((sample_1, sample_2))
        self.sample = np.array(list(zip(sample_1, sample_2))).flatten()

        #print(self.sample.tolist())

    def stream_callback(self, in_data, frame_count, time_info, status_flags):
        #print(self.waveform)
        #print(in_data)
        #sample = np.repeat(self.waveform_1, self.frequency_1)
        #sample = np.tile(sample, self.frames_per_buffer//2)[:self.frames_per_buffer]
        #print(self.loop, self.sample)
        if self.loop:
            return (self.sample, pyaudio.paContinue)
        else:
            return (in_data, pyaudio.paComplete)

    def run(self):
        #self.sample = np.repeat(self.waveform, self.frequency)

        player = pyaudio.PyAudio()
        stream = player.open(format = pyaudio.paFloat32,
                        channels = 2,
                        rate = BITRATE,
                        output = True,
                        #frames_per_buffer = len(self.sample),
                        frames_per_buffer = self.frames_per_buffer,
                        stream_callback = self.stream_callback,
                        )

        # PLAYBACK LOOP
        #data = wf.readframes(self.CHUNK)

        #sample = np.repeat(self.waveform, self.frequency)
        #sample = np.tile(sample, 4)
        #sample = np.tile(self.waveform, self.frequency)

        #reps = BITRATE // 60 // len(sample)

        #sample = np.tile(sample, reps)

        #print(sample.tolist())

        stream.start_stream()

        #while self.loop:
            #print(sample.tolist())
            #stream.write(sample)
            #data = wf.readframes(self.CHUNK)
            #if data == b'':  # If file is over then rewind.
            #    wf.rewind()
            #    data = wf.readframes(self.CHUNK)

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


# ac = AudioChannel(None)
# ac.volume = 1
# print(ac._volume)
#
#
# 1/0

audio = Audio()

audio.channel_1.waveform = 4
audio.channel_1.frequency = 32
audio.channel_1.volume = 1

audio.channel_2.waveform = 0
audio.channel_2.frequency = 32

#audio.set_sample()

for i in range(5):
    time.sleep(.5)
    audio.channel_2.volume = 1
    #audio.set_sample()
    time.sleep(.5)
    audio.channel_2.volume = 0
    #audio.set_sample()

# channel_1 = AudioChannel(waveform_4)
# channel_2 = AudioChannel(waveform_1)
#
# channel_1.play(frequency=64)
# channel_2.play(frequency=32)

#time.sleep(3)

#channel_1.stop()
#channel_2.stop()

audio.stop()
