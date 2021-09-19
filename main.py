import wave
import sys

from math import log2, pow

import matplotlib.pyplot as plt
import numpy as np

from scipy import signal
from midiutil import MIDIFile

track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 120  # In BPM
volume   = 100  # 0-127, as per the MIDI standard

CHANNELS = 1
RATE = 44100
BPM = 120
BEAT = 1/4
BEATS_PER_MEASURE = 4
SECONDS_PER_BEAT = 60 / BPM
CHUNK = 1024
NOTE = 1/8
FREQ_LIMIT = 3
A4 = 440
C4 = 48
C0 = A4 * pow(2, -4.75)
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MIDI_BASE = 69
FRAME_COUNT = int(round(SECONDS_PER_BEAT * RATE * NOTE * 4))
DEFAULT_DURATION = NOTE / BEAT

class Note:
	def __init__(self, value=C4, duration=DEFAULT_DURATION):
		self.value = value
		self.duration = duration

def freq_to_midi(freq):
	return round(12 * log2(freq / A4) + MIDI_BASE)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_signal(chunk):
	f, P = signal.periodogram(chunk, fs=RATE) # Frequencies and PSD
	f = [i * 2 for i in f[:len(f)//2]] # double the frequency for the non-mirrored half
	P = P[:len(P)//2] # take the non-mirrored part of the power distribution

	return f, P

def main():
	filename = sys.argv[1]
	if len(filename) <= 0 or not filename.endswith(".wav"):
		raise Exception("Please provide a wav file path as the first argument.")

	print("* reading")

	wav = wave.open(filename, mode="rb")
	data = list(wav.readframes(wav.getnframes()))
	wav.close()

	data_chunks = chunks(data, FRAME_COUNT)
	note_list = []

	current_note = None
	for chunk in data_chunks:
		# Compute PSD:
		f, P = get_signal(chunk)

		powers = P
		largest_powers = list(reversed(np.argsort(powers)))
		idx = largest_powers[0]
		power = powers[idx]
		freq = f[idx]

		print("POWER", power)
		print("FREQ", freq)
		note = freq_to_midi(freq)
		print("PITCH", freq_to_midi(freq))
		if current_note == freq:
			note = note_list[-1]
			note.duration += DEFAULT_DURATION
		else:
			note_list.append(Note(note))

		current_note = freq

	print("* writing midi")
	midi = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
	midi.addTempo(track, time, tempo)

	for i, note in enumerate(note_list):
		midi.addNote(track, channel, note.value, time + i, note.duration, volume)

	mid_filename = filename.split(".")[0] + ".mid"
	with open(mid_filename, "wb") as output_file:
		midi.writeFile(output_file)

	print("* done")

if __name__ == '__main__':
	main()