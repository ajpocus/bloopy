import wave
import sys

from math import log2, pow

import matplotlib.pyplot as plt
import numpy as np

from scipy import signal

CHANNELS = 1
RATE = 44100
BPM = 120
BEAT_SECONDS = 60 / BPM
CHUNK = 1024
NOTE = 1/8
FREQ_LIMIT = 3
A4 = 440
C0 = A4 * pow(2, -4.75)
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def pitch(freq):
    h = round(12 * log2(freq / C0))
    octave = h // 12
    n = h % 12

    return NAMES[n] + str(octave)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_signal(chunk):
	f, P = signal.periodogram(chunk, fs=RATE) # Frequencies and PSD
	f = [i * 2 for i in f[:len(f)//2]]
	P = P[:len(P)//2]

	return f, P

def main():
	filename = sys.argv[1]
	if not filename:
		raise Exception("Please provide a wav file path as the first argument.")

	print("* reading")

	wav = wave.open(filename, mode="rb")
	data = list(wav.readframes(wav.getnframes()))
	wav.close()

	data_chunks = chunks(data, CHUNK)
	for chunk in data_chunks:
		# Compute PSD:
		f, P = get_signal(chunk)
		powers = P	# get the non-mirrored data from the frequency analysis

		largest_powers = list(reversed(np.argsort(powers)))
		idx = largest_powers[0]
		power = powers[idx]
		print("POWER", power)
		freq = f[idx]
		print("FREQ", freq)
		print("PITCH", pitch(freq))

	f, P = get_signal(data)

	plt.semilogy(f, P)
	plt.show()
	print("* done")

if __name__ == '__main__':
	main()