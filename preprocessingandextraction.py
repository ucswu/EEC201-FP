# -*- coding: utf-8 -*-
"""preprocessingAndExtraction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17m-9q5WOA-sDbah-B04KolScPFeF7_oD

Preprocessing func
"""

from google.colab import drive
drive.mount('/content/drive')
import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal

# Path link
DRIVE_PATH = "/content/drive/MyDrive/GivenSpeech_Data/Training_Data"
audio_files = ["s1.wav", "s2.wav", "s3.wav","s4.wav","s5.wav","s6.wav","s7.wav","s8.wav","s9.wav","s10.wav","s11.wav"]

def load_audio(file_name, sr=16000):
    file_path = os.path.join(DRIVE_PATH, file_name)
    signal, sample_rate = librosa.load(file_path, sr=sr)
    return signal, sample_rate # np.ndarray, int

def normalize_audio(signal):
    return signal / np.max(np.abs(signal)) # np.ndarray

def lowpass_filter(signal, sr, cutoff=3000, order=5):
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = scipy.signal.butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = scipy.signal.filtfilt(b, a, signal)
    return filtered_signal # np.ndarray

def compute_sample_time(sr, N=256):
    time_ms = (N / sr) * 1000
    print(f"sample time: {time_ms:.2f} ms")

def compute_mfcc(signal, sr, n_mfcc=13, n_fft=2048, hop_length=512):
    mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    return mfccs # np.ndarray

def plot_waveform(signal, sr, title="Waveform"):
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(signal, sr=sr)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()


def plot_stft(signal, sr, n_fft=512, hop_length=256, title="STFT Spectrogram"):
    D = librosa.stft(signal, n_fft=n_fft, hop_length=hop_length)
    D_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(D_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log')
    plt.colorbar(label="Decibels (dB)")
    plt.title(title)
    plt.show()

# Different window sizes mfcc
def compare_mfcc(signal, sr):
    n_fft_values = [128, 256, 512]
    plt.figure(figsize=(12, 6))
    for i, n_fft in enumerate(n_fft_values):
        mfccs = compute_mfcc(signal, sr, n_mfcc=13, n_fft=n_fft, hop_length=n_fft//2)
        plt.subplot(1, 3, i+1)
        librosa.display.specshow(mfccs, sr=sr, x_axis='time')
        plt.colorbar(label="MFCC Coefficients")
        plt.title(f"MFCC (N={n_fft})")
    plt.tight_layout()
    plt.show()

def plot_mel_filterbank(sr=16000, n_fft=256, n_mels=26):
    mel_filters = librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=n_mels)
    plt.figure(figsize=(10, 4))
    for i in range(mel_filters.shape[0]):
        plt.plot(mel_filters[i], label=f"Mel {i+1}")
    plt.title("Mel-Spaced Filterbank")
    plt.xlabel("Frequency Bin")
    plt.ylabel("Amplitude")
    plt.show()

# Preprocess function
# Return value: filtered_signal and mfcc_matrix
def process_audio(file_name):
    signal, sr = load_audio(file_name)
    normalized_signal = normalize_audio(signal)
    filtered_signal = lowpass_filter(normalized_signal, sr)
    mfccs = compute_mfcc(filtered_signal, sr)

    compute_sample_time(sr)
    plot_waveform(filtered_signal, sr, title=f"Filtered Waveform: {file_name}")
    plot_stft(filtered_signal, sr, title=f"STFT Spectrogram: {file_name}")
    compare_mfcc(filtered_signal, sr)
    plot_mel_filterbank(sr, n_fft=2048, n_mels=26)
    return filtered_signal, mfccs

for file in audio_files:
    process_audio(file)