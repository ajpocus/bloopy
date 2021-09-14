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
BEAT_SECONDS = 60 / BPM
CHUNK = int(RATE // (BEAT_SECONDS / 2))
NOTE = 1/8

print("CHUNK", CHUNK)

pa = pyaudio.PyAudio()

stream = pa.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK)

print("* recording")

interval = BEAT_SECONDS * NOTE

def record():
	current_thread = threading.Timer(interval, record)
	current_thread.start()

	data = list(stream.read(CHUNK))

	# Compute PSD:
	f, P = signal.periodogram(data, fs=RATE) # Frequencies and PSD

	max_index = P.argmax()
	power = P[max_index]
	print("POWER", power)
	if power > 50:
		freq = f[max_index]
		print(freq)

current_thread = threading.Timer(interval, record)

try:
	record()
except KeyboardInterrupt:
	current_thread.cancel()

print("* done recording")

# stream.stop_stream()
# stream.close()
# pa.terminate()
