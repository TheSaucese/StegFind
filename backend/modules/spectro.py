import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import librosa
import librosa.display
from flask import send_file

# Increase FFT window for higher frequency resolution
n_fft = 4096
# Decrease hop length for higher time resolution
hop_length = 32

def create_spectrogram(filename,output_filename):
    y, sr = librosa.load(filename)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)
    S += 1e-6  # Add a small constant
    S_dB = librosa.power_to_db(S, ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()

    return output_filename