import librosa
import librosa.display
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import os
import glob

def extract_features(file_path):
    """Extracts MFCC features from an audio file."""
    try:
        y, sr = librosa.load(file_path, sr=None)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return mfccs.T
    except FileNotFoundError:
        print(f"Error: Audio file not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred during feature extraction: {e}")
        return None

def compare_pronunciation(reference_mfccs, user_mfccs):
    """Compares MFCC features using Dynamic Time Warping (DTW)."""
    if reference_mfccs is None or user_mfccs is None:
        return float('inf')
    distance, path = fastdtw(reference_mfccs, user_mfccs, dist=euclidean)
    return distance

def log_results(log_file, user_audio, distance):
    """Logs the results to a text file."""
    try:
        with open(log_file, 'a') as f:
            f.write(f"User Audio: {user_audio}, DTW Distance: {distance}\n")
    except Exception as e:
        print(f"An error occurred while writing to the log file: {e}")

def get_average_mfccs(directory):
    """Calculates the average MFCCs from multiple audio files in a directory."""
    mfccs_list = []
    for file_path in glob.glob(os.path.join(directory, "*.mp3")): #Assumes .mp3 files. Change if needed.
        mfccs = extract_features(file_path)
        if mfccs is not None:
            mfccs_list.append(mfccs)

    if not mfccs_list:
        print("No valid audio files found in the directory.")
        return None

    #Average the MFCCs (element-wise mean).  Ensure all MFCCs have the same shape.
    average_mfccs = np.mean(np.array(mfccs_list), axis=0)
    return average_mfccs


# --- Example Usage ---
reference_audio_directory = "/Users/dprabak7/Documents/Code/faux-ami/multiple-samples" #Directory containing multiple samples of "Blessé"
log_file = "pronunciation_log.txt"
threshold = 500  # Adjust this threshold based on your experiments.

average_reference_mfccs = get_average_mfccs(reference_audio_directory)

if average_reference_mfccs is None:
    exit() #Exit if no reference MFCCs could be generated.


while True:
    user_audio = input("Enter the path to the user's audio file (or type 'exit' to quit): ")
    if user_audio.lower() == 'exit':
        break

    user_mfccs = extract_features(user_audio)
    if user_mfccs is None:
        continue

    distance = compare_pronunciation(average_reference_mfccs, user_mfccs)

    print(f"DTW Distance: {distance}")
    log_results(log_file, user_audio, distance)

    if distance < threshold:
        print("Pronunciation is acceptable.")
    else:
        print("Pronunciation needs improvement.")

print("Log file created successfully!")
