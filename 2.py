import librosa
import librosa.display
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

def extract_features(file_path):
    """Extracts MFCC features from an audio file."""
    y, sr = librosa.load(file_path, sr=None)  # sr=None to preserve original sample rate
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Adjust n_mfcc as needed
    return mfccs.T  # Transpose to have frames as rows


def compare_pronunciation(reference_mfccs, user_mfccs):
    """Compares MFCC features using Dynamic Time Warping (DTW)."""
    distance, path = fastdtw(reference_mfccs, user_mfccs, dist=euclidean)
    # Lower distance indicates higher similarity
    return distance


# --- Example Usage ---
reference_audio_file = "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Blessé.mp3"  # Replace with your reference audio file
user_audio = input("Enter the path to the user's audio file: ") # Your pronunciation

reference_mfccs = extract_features(reference_audio_file)
user_mfccs = extract_features(user_audio)

distance = compare_pronunciation(reference_mfccs, user_mfccs)
print(f"DTW Distance: {distance}")

#  You'll need to define a threshold to determine if the pronunciation is acceptable.
threshold = 100  #  Adjust this threshold based on your experiments.

if distance < threshold:
    print("Pronunciation is acceptable.")
else:
    print("Pronunciation needs improvement.")

