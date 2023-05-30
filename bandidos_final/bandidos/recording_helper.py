import pyaudio
import numpy as np

frames_per_buffer = 3200
format = pyaudio.paInt16
channels = 1
rate = 16000
p = pyaudio.PyAudio()

def record_audio():
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=frames_per_buffer)
    frames = []
    seconds = 1
    for i in range(0, int(rate/frames_per_buffer*seconds)):
        data = stream.read(frames_per_buffer)
        frames.append(data)
        stream.stop_stream()
        stream.close()

        return np.frombuffer(b''.join(frames), dtype=np.int16)
def terminate():
    p.terminate()