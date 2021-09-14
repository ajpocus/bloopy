import pyaudio
import wave
from scipy import signal
from scipy.io import wavfile
import matplotlib
import matplotlib.pyplot as plt

# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 2
# RATE = 44100
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "output.wav"

# p = pyaudio.PyAudio()

# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNK)

# print("* recording")

# frames = []

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)

# print("* done recording")

# stream.stop_stream()
# stream.close()
# p.terminate()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()

# Read the file (rate and data):
rate, data = wavfile.read('data/1k.wav') # See source

# Compute PSD:
f, P = signal.periodogram(data, rate) # Frequencies and PSD

# Display PSD:
fig, axe = plt.subplots()
axe.semilogy(f, P)
axe.set_xlim([0,2e3])
axe.set_ylim([1e-8, 1e10])
axe.set_xlabel(r'Frequency, $\nu$ $[\mathrm{Hz}]$')
axe.set_ylabel(r'PSD, $P$ $[\mathrm{AU^2Hz}^{-1}]$')
axe.set_title('Periodogram')
axe.grid(which='both')
axe.plot()
plt.savefig("test.jpg")