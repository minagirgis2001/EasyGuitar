# import wave
# import numpy as np
# import matplotlib.pyplot as plt
from cmath import log10
import math
# wav_obj = wave.open('bassAnalysis.wav', 'rb')

# sample_freq = wav_obj.getframerate()
# print(sample_freq)
# n_samples = wav_obj.getnframes()
# print(n_samples)
# time = n_samples/sample_freq
# print(time)
# signal_wave = wav_obj.readframes(n_samples)
# signal_array = np.frombuffer(signal_wave, dtype=np.int16)
# l_channel = signal_array[0::2]
# r_channel = signal_array[1::2]
# print(signal_array)
# times = np.linspace(0, n_samples/sample_freq, num=n_samples)
# print(times)
# plt.figure(figsize=(15, 5))
# plt.plot(times, l_channel)
# plt.title('Left Channel')
# plt.ylabel('Signal Value')
# plt.xlabel('Time (s)')
# plt.xlim(0, 1)
# #plt.show()
# plt.figure(figsize=(15, 5))
# plt.specgram(l_channel, Fs=sample_freq, vmin=-20, vmax=50)
# plt.title('Left Channel')
# plt.ylabel('Frequency (Hz)')
# plt.xlabel('Time (s)')
# plt.xlim(0, 1)
# plt.colorbar()
# #plt.show()

# # for i in range(0,int(time)):
# #     print(sample.*(math.pow(2,1/12)))
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
from scipy.fftpack import fft, fftshift
# read in sound file
samplerate, data = wavfile.read('bassAnalysis.wav')

# define sound metadata
data_size = data.shape[0]
song_length_seconds = data_size/samplerate

# print sound metadata
print("Data size:", data_size)
print("Sample rate:", samplerate)
print("Song length (seconds):", song_length_seconds, "seconds")
# define domain in seconds
time_domain = np.linspace(0, song_length_seconds, data_size)

# plot sound wave
plt.plot(time_domain, data)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
#plt.show()

# define frequency domain
freq_domain = np.linspace(-samplerate/2,samplerate/2,data_size)

# fourier transform
fourier_data = abs(fft(data))
fourier_data_shift = fftshift(fourier_data)

# plotting spectral content of sound wave
plt.xlim([-5000, 5000])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.plot(freq_domain, fourier_data_shift)
#plt.show()

# define gaussian filter
gaussian = 11000*np.exp(-2*np.power(time_domain - 11.8, 2))

# plot signal with gaussian
plt.plot(time_domain, data)
plt.plot(time_domain, gaussian)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
#plt.show()

# plot signal with gaussian
plt.plot(time_domain, gaussian*data)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
#plt.show()

# apply Gabor transform across sliding window
for i in [2.2, 4.25, 6, 8, 10, 11.8]:
    clear_output(wait=True)
    gaussian = 11000*np.exp(-2*np.power(time_domain - i, 2))
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.plot(time_domain, data*gaussian)
    plt.pause(0.2)

results = []

for i in [2.2, 4.25, 6, 8, 10, 11.8]:
    clear_output(wait=True)
    plt.xlim([0, 600])
    gaussian = 11000*np.exp(-2*np.power(time_domain - i, 2))

    gaussian_filtered = data*gaussian

    fourier_data = abs(fft(gaussian_filtered))
    fourier_data_shift = fftshift(fourier_data)

    results.append(fourier_data_shift)

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude")
    plt.plot(freq_domain, fourier_data_shift)
    plt.pause(1)
# from: https://www.johndcook.com/blog/2016/02/10/musical-pitch-notation/
from math import log2, pow


A4 = 440
C0 = 261.626
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
def pitch(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)

for i in range(len(results)):
    frequency = abs(freq_domain[results[i].argmax()])
    print(frequency)
    print(round(frequency,2), ": ", pitch(frequency))