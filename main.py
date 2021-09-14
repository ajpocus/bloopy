import threading
import time
import pyaudio

from scipy import signal

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 15
WAVE_OUTPUT_FILENAME = "output.wav"
BPM = 120
NOTE = 1/8

pa = pyaudio.PyAudio()

stream = pa.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK)

print("* recording")

beat_seconds = 60 / BPM
interval = beat_seconds * NOTE

def record():
	threading.Timer(interval, record).start()

	frames = []
	t_end = time.time() + 60 / BPM * pow(NOTE, 2)
	while time.time() < t_end:
		data = list(stream.read(CHUNK))
		frames.append(data)

	# Compute PSD:
	f, P = signal.periodogram(frames, fs=RATE) # Frequencies and PSD

	max_index = P.argmax()
	power = P[max_index]
	print("POWER", power)
	if power > 50:
		freq = f[max_index]
		print(freq)

record()

print("* done recording")

stream.stop_stream()
stream.close()
pa.terminate()
