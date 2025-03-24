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
    """Calculates the average MFCCs from multiple audio files, handling varying lengths robustly."""
    mfccs_list = []
    for file_path in glob.glob(os.path.join(directory, "*.mp3")):
        mfccs = extract_features(file_path)
        if mfccs is not None:
            mfccs_list.append(mfccs)

    if not mfccs_list:
        print("No valid audio files found in the directory.")
        return None

    # Find the maximum number of frames across all MFCCs.
    max_frames = max(mfccs.shape[0] for mfccs in mfccs_list)
    num_mfccs = mfccs_list[0].shape[1] # Number of MFCC coefficients

    # Pad MFCCs to ensure uniform shape before averaging
    padded_mfccs = np.zeros((len(mfccs_list), max_frames, num_mfccs))
    for i, mfccs in enumerate(mfccs_list):
        padded_mfccs[i, :mfccs.shape[0], :] = mfccs

    #Compute the average.  Check for potential errors during averaging.
    try:
        average_mfccs = np.mean(padded_mfccs, axis=0)
    except ValueError as e:
        print(f"Error during averaging: {e}.  Check the shapes of your MFCCs.")
        print(f"Shapes of padded MFCCs: {[mfccs.shape for mfccs in padded_mfccs]}")
        return None

    return average_mfccs

    # Pad or truncate MFCCs to make them uniform before averaging:
    max_frames = max(mfccs.shape[0] for mfccs in mfccs_list)
    padded_mfccs = [np.pad(mfccs, ((0, max_frames - mfccs.shape[0]), (0, 0)), mode='constant') for mfccs in mfccs_list]

    average_mfccs = np.mean(np.array(padded_mfccs), axis=0)
    return average_mfccs

# --- Example Usage ---
reference_audio_directory = "/Users/dprabak7/Documents/Code/faux-ami/multiple-samples"
log_file = "pronunciation_log.txt"
threshold = 500  # Needs experimental determination

average_reference_mfccs = get_average_mfccs(reference_audio_directory)

if average_reference_mfccs is None:
    exit()


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
