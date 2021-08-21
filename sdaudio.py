import numpy as np
import sounddevice as sd
import time
duration = 4  # seconds

BITRATE = 32000
BLOCKSIZE = 1024

waveform_1 = np.array([0,0,1,0,1,0,0,0,0,1,1,1,0,1,1]).astype(np.float32)
waveform_4 = np.array([0, 1]).astype(np.float32)
frequency = 32
volume = 1
sample = volume * np.repeat(waveform_4, frequency)
sample = np.tile(sample, int(np.ceil(BLOCKSIZE / len(sample))))
#sample = sample.reshape(-1,1)
i = 0

def callback(outdata, frames, time, status):
    global i
    #print(frames, time.outputBufferDacTime, time.currentTime)
    if status:
        print(status)
    #outdata[:] = sample[:BLOCKSIZE]
    outdata[:] = sample.take(range(i, i+BLOCKSIZE), mode='wrap').reshape(-1,1)
    i = (i + BLOCKSIZE) % len(sample)

with sd.OutputStream(samplerate=BITRATE, channels=1, callback=callback, blocksize=BLOCKSIZE):
    #sd.sleep(int(duration * 1000))
    time.sleep(duration)
