import wave
import sys
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
		indices = largest_powers[:FREQ_LIMIT]

		for idx in indices:
			power = powers[idx]
			print("POWER", power)
			freq = f[idx]
			print(freq)

	f, P = get_signal(data)

	print("RMS", np.sqrt(P.max()))
	plt.semilogy(f, P)
	plt.show()
	print("* done")

if __name__ == '__main__':
	main()