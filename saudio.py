import numpy as np
import simpleaudio as sa
import time

BITRATE = 32000

waveform_1 = np.array([0,0,1,0,1,0,0,0,0,1,1,1,0,1,1]).astype(np.float32)
waveform_4 = np.array([0, 1]).astype(np.float32)
frequency = 16

sample = np.repeat(waveform_1, 32)
sample = np.tile(sample, 5000)
background = sa.play_buffer(sample, 1, 4, BITRATE)

for frequency in range(2, 64, 2):
    sample = np.repeat(waveform_4, frequency)
    sample = np.tile(sample, 5000)

    play_obj = sa.play_buffer(sample, 1, 4, BITRATE)

    time.sleep(.3)
    play_obj.stop()


background.stop()
# wait for playback to finish before exiting
#play_obj.wait_done()

# # calculate note frequencies
# A_freq = 440
# Csh_freq = A_freq * 2 ** (4 / 12)
# E_freq = A_freq * 2 ** (7 / 12)
#
# # get timesteps for each sample, T is note duration in seconds
# sample_rate = 44100
# T = 0.25
# t = np.linspace(0, T, int(T * sample_rate), False)
#
# # generate sine wave notes
# A_note = np.sin(A_freq * t * 2 * np.pi)
# Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
# E_note = np.sin(E_freq * t * 2 * np.pi)
#
# # concatenate notes
# audio = np.hstack((A_note, Csh_note, E_note))
# # normalize to 16-bit range
# audio *= 32767 / np.max(np.abs(audio))
# # convert to 16-bit data
# audio = audio.astype(np.int16)
#
# # start playback
# play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
#
# # wait for playback to finish before exiting
# play_obj.wait_done()
