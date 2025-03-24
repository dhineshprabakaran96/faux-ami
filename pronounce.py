import librosa
import numpy as np
from dtaidistance import dtw
import os

def calculate_pronunciation_distance(ref_file, user_file, sr=16000, n_mfcc=13):
    """Calculates the pronunciation distance between two audio files using MFCCs and DTW.
       Returns the distance and the warping path.
    """
    try:
        # Load audio files
        ref_audio, sr = librosa.load(ref_file, sr=sr)
        user_audio, sr = librosa.load(user_file, sr=sr)

        # Extract MFCCs
        ref_mfccs = librosa.feature.mfcc(y=ref_audio, sr=sr, n_mfcc=n_mfcc)
        user_mfccs = librosa.feature.mfcc(y=user_audio, sr=sr, n_mfcc=n_mfcc)

        # Normalize MFCCs (example: mean subtraction)
        ref_mfccs -= np.mean(ref_mfccs, axis=1, keepdims=True)
        user_mfccs -= np.mean(user_mfccs, axis=1, keepdims=True)

        # Compute the DTW distance and path
        distance_matrix = dtw.distance_matrix_fast(ref_mfccs.T, user_mfccs.T)
        distance, path = dtw.warping_paths(ref_mfccs.T, user_mfccs.T, window=25, max_dist=distance_matrix)

        return distance, path

    except FileNotFoundError:
        print(f"Error: One or both audio files not found.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Example usage (replace with your actual file paths):
ref_audio_path = "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Chanter.mp3" #Reference audio file
user_audio_path = "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Chanter.mp3" #User audio file

if os.path.exists(ref_audio_path) and os.path.exists(user_audio_path):
    distance, path = calculate_pronunciation_distance(ref_audio_path, user_audio_path)
    if distance is not None:
        print("Pronunciation Distance:", distance)
        # Further processing of the path variable can be done here to visualize the warping path
        # import matplotlib.pyplot as plt
        # dtw.plot_warping(path, ref_mfccs.T, user_mfccs.T)
        # plt.show()
else:
    print("One or both audio files do not exist.")
