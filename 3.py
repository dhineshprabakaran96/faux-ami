import librosa
import librosa.display
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import os

def extract_features(file_path):
    """Extracts MFCC features from an audio file.  Handles file errors."""
    try:
        y, sr = librosa.load(file_path, sr=None)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return mfccs.T
    except FileNotFoundError:
        print(f"Error: Audio file not found at {file_path}")
        return None  # Return None to signal failure
    except Exception as e:
        print(f"An error occurred during feature extraction: {e}")
        return None


def compare_pronunciation(reference_mfccs, user_mfccs):
    """Compares MFCC features using Dynamic Time Warping (DTW)."""
    if reference_mfccs is None or user_mfccs is None:
        return float('inf')  # Return infinity if feature extraction failed.
    distance, path = fastdtw(reference_mfccs, user_mfccs, dist=euclidean)
    return distance


def log_results(log_file, user_audio, distance):
    """Logs the results to a text file."""
    try:
        with open(log_file, 'a') as f:
            f.write(f"User Audio: {user_audio}, DTW Distance: {distance}\n")
    except Exception as e:
        print(f"An error occurred while writing to the log file: {e}")


# --- Example Usage ---
reference_audio_file = "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Court.mp3"  # Replace with your reference audio file
log_file = "pronunciation_log.txt"
threshold = 500 # This threshold needs to be determined experimentally.

reference_mfccs = extract_features(reference_audio_file)

while True:
    user_audio = input("Enter the path to the user's audio file (or type 'exit' to quit): ")
    if user_audio.lower() == 'exit':
        break

    user_mfccs = extract_features(user_audio)
    if user_mfccs is None:
        continue  # Skip to the next iteration if feature extraction failed.

    distance = compare_pronunciation(reference_mfccs, user_mfccs)

    print(f"DTW Distance: {distance}")
    log_results(log_file, user_audio, distance)

    # Add pronunciation assessment based on the threshold
    if distance < threshold:
        print("Pronunciation is acceptable.")
    else:
        print("Pronunciation needs improvement.")

print("Log file created successfully!")

