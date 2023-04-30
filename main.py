
import numpy as np
import librosa
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
import aubio
from subprocess import call
import os


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def apply_spectral_mask(y, sr, hop_length=512, mask_threshold=0.2):
    # Compute the Short-Time Fourier Transform (STFT)
    stft = librosa.stft(y, hop_length=hop_length)

    # Compute the magnitude spectrogram
    magnitude = np.abs(stft)

    # Create a spectral mask based on the magnitude threshold
    mask = magnitude > (np.max(magnitude) * mask_threshold)

    # Apply the mask to the STFT
    stft_masked = stft * mask.astype(np.float32)

    # Compute the inverse STFT to obtain the filtered audio
    y_filtered = librosa.istft(stft_masked, hop_length=hop_length)

    return y_filtered

def extract_bass(input_wav, output_wav, cutoff_frequency=250, mask_threshold=0.2):
    # Load the WAV file
    y, sr = librosa.load(input_wav, sr=None)
    if len(y.shape) > 1:
        # If stereo, take the average of both channels
        y = y.mean(axis=1)

    # Apply low-pass filter
    bass_data = butter_lowpass_filter(y, cutoff_frequency, sr)

    # Apply spectral mask to suppress less prominent frequencies
    bass_data_filtered = apply_spectral_mask(bass_data, sr, mask_threshold=mask_threshold)

    # Normalize output and convert to int16
    bass_data_normalized = np.int16(bass_data_filtered / np.max(np.abs(bass_data_filtered)) * 32767)

    # Save bass frequencies to a new WAV file
    wavfile.write(output_wav, sr, bass_data_normalized)
    
# def extract_notes_and_times(wav_file, hop_length=512, sr=None):
#     # Load the bass WAV file
#     y, sr = librosa.load(wav_file, sr=sr)

#     # Detect pitch and onset
#     pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=hop_length)
#     onsets = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)

#     # Extract notes, frequencies, and their start times
#     notes_and_times = []
#     for onset in onsets:
#         idx = magnitudes[:, onset].argmax()
#         pitch = pitches[idx, onset]
#         if pitch > 0:
#             note = librosa.hz_to_note(pitch)
#             start_time = onset * hop_length / sr
#             notes_and_times.append((note, pitch, start_time))

#     return notes_and_times

def extract_notes_per_second(wav_file, hop_length=512, sr=None):
    # Load the bass WAV file
    y, sr = librosa.load(wav_file, sr=sr)

    # Detect pitch and onset
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, hop_length=hop_length)
    onsets = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)

    # Extract notes, frequencies, and their start times
    notes_and_times = []
    notes_per_second = []
    for onset in onsets:
        idx = magnitudes[:, onset].argmax()
        pitch = pitches[idx, onset]
        if pitch > 0:
            note = librosa.hz_to_note(pitch)
            start_time = onset * hop_length / sr
            notes_and_times.append((note, pitch, start_time))
            notes_per_second.append((start_time, note))

    avg_notes_per_second = []
    start_time = 0
    for i in range(len(notes_per_second)):
        time, note = notes_per_second[i]
        if time - start_time >= 1:
            notes_for_second = [n for t, n in notes_per_second if start_time <= t < time]
            avg_note = max(set(notes_for_second), key=notes_for_second.count)
            avg_notes_per_second.append((start_time, avg_note))
            start_time = time

    return avg_notes_per_second

def estimate_key(wav_file, sr=None, hop_length=512):
    # Load the audio file
    y, sr = librosa.load(wav_file, sr=sr)

    # Compute chroma features
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length)

    # Compute the mean chroma features for the entire audio
    mean_chroma = np.mean(chroma, axis=1)

    # Find the index of the maximum mean chroma feature
    key_index = np.argmax(mean_chroma)

    # Convert the key index to a key name
    key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = key_names[key_index]

    return key
def note_to_fret_and_string(note):
    bass_tuning = ['E1', 'A1', 'D2', 'G2']
    frets_per_string = 12

    note_name, octave = note[:-1], int(note[-1])
    semitones_from_tuning = [librosa.note_to_midi(note) - librosa.note_to_midi(tuning) for tuning in bass_tuning]

    for string, semitones in enumerate(semitones_from_tuning):
        if 0 <= semitones <= frets_per_string:
            return string + 1, semitones

    return None, None



if __name__ == "__main__":
    current_directory = os.getcwd()
    input_wav = current_directory +"/../song.wav"
    output_wav = current_directory +"/../output_bass.wav"
    cutoff_frequency = 250  # Adjust this value to include the desired range of bass frequencies
    mask_threshold = 0.05
    extract_bass(input_wav, output_wav, cutoff_frequency, mask_threshold)
    avg_notes_per_second = extract_notes_per_second(output_wav)
    original_key = estimate_key(input_wav)
    bass_key = estimate_key(output_wav)

    print(f"Original Estimated key: {original_key}")
    print(f"Bass Estimated key: {bass_key}")
    for start_time, avg_note in avg_notes_per_second:
        pass
        # print(f"Average note: {avg_note}, Start Time: {start_time:.2f}s")

    with open(current_directory +'/../song.txt', 'w', encoding='utf-8') as txt_file: 
        for i in range(len(avg_notes_per_second)):
            note = avg_notes_per_second[i][1] 
            start_time = avg_notes_per_second[i][0]
            if i + 1 < len(avg_notes_per_second):
                next_start_time = avg_notes_per_second[i+1][0]
                print(next_start_time)
                note_length = float(next_start_time) - float(start_time)
                
            else:
                note_length = 0
            string, fret = note_to_fret_and_string(note)
            if string is not None and fret is not None:
                txt_file.write(f"{string}, {fret}, {note_length:.2f}, {start_time:.2f}\n")
                # print(f"String: {string}, Fret: {fret}, Note Length: {note_length:.2f}, Start Time: {start_time:.2f}")
            else:
                pass
                # print(f"Note: {note} cannot be played on a standard four-string bass guitar")
    call(["python", current_directory +"/../LED.py",])
