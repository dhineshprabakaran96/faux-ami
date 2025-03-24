import librosa
import numpy as np
from scipy.spatial.distance import cosine

def extract_mfccs(audio_file):
    """Extracts MFCC features from an audio file."""
    y, sr = librosa.load(audio_file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Adjust n_mfcc as needed
    return mfccs.mean(axis=1)  # Average across time frames


def compare_pronunciation(reference_mfccs, user_mfccs):
    """Compares MFCC features using cosine similarity."""
    similarity = 1 - cosine(reference_mfccs, user_mfccs)
    return similarity


# Example usage (replace with your actual audio files)
reference_audio = "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Blessé.mp3"  # Correct pronunciation
user_audio = input("Enter the path to the user's audio file: ") # Your pronunciation


reference_mfccs = extract_mfccs(reference_audio)
user_mfccs = extract_mfccs(user_audio)

similarity_score = compare_pronunciation(reference_mfccs, user_mfccs)
print(f"Similarity score: {similarity_score}")

# You'll need to define a threshold to determine if the pronunciation is "correct enough"
threshold = 0.8  # Adjust this based on experimentation
if similarity_score > threshold:
    print("Pronunciation is likely correct.")
else:
    print("Pronunciation may be incorrect.")

