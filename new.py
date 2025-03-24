import librosa
import numpy as np
from scipy.spatial.distance import cosine
from sklearn.preprocessing import normalize

def extract_mfccs(audio_file, n_mfcc=13):
    """Extracts MFCC features from an audio file."""
    try:
        y, sr = librosa.load(audio_file)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        return mfccs.T  # Transpose to (frames, features)
    except FileNotFoundError:
        print(f"Error: Audio file not found: {audio_file}")
        return None
    except Exception as e:
        print(f"Error processing audio file {audio_file}: {e}")
        return None

def compare_pronunciations(dataset_mfccs, my_mfccs):
    """Compares MFCC features using cosine similarity."""
    if dataset_mfccs is None or my_mfccs is None:
        return 1.0 # Return a high distance if features extraction fails

    # Normalize MFCCs (Important for better comparison)
    dataset_mfccs = normalize(dataset_mfccs)
    my_mfccs = normalize(my_mfccs)

    #Simple averaging to get a single vector for comparison (this is a simplification!)
    avg_dataset_mfccs = np.mean(dataset_mfccs, axis=0)
    avg_my_mfccs = np.mean(my_mfccs, axis=0)

    similarity = 1 - cosine(avg_dataset_mfccs, avg_my_mfccs) #Cosine similarity (1-distance)
    return 1 - similarity #Return the distance


# Example Usage (replace with your actual file paths):
dataset = {
    "Blessé": "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Blessé.mp3",  #Replace with your paths
}

my_recordings = {
    "Blessé": "/Users/dprabak7/Documents/Code/faux-ami/my-samples/hello.mp3",  #Replace with your paths
}


for word, dataset_audio in dataset.items():
    my_audio = my_recordings.get(word)  #Use get to handle missing recordings gracefully
    dataset_mfccs = extract_mfccs(dataset_audio)
    my_mfccs = extract_mfccs(my_audio)
    distance = compare_pronunciations(dataset_mfccs, my_mfccs)
    print(f"Pronunciation of '{word}': Distance = {distance:.4f}")
    # Set a threshold for determining if it's a match (e.g., distance < 0.3)

