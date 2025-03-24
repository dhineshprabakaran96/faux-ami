import librosa
import numpy as np
from scipy.spatial.distance import cosine  # Import cosine distance

def extract_mfccs(audio_file, n_mfcc=13):
    try:
        y, sr = librosa.load(audio_file)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        return mfccs.T
    except FileNotFoundError:
        print(f"Error: Audio file not found: {audio_file}")
        return None
    except Exception as e:
        print(f"Error processing audio file {audio_file}: {e}")
        return None

def compare_pronunciations(dataset_mfccs, my_mfccs, threshold):
    if dataset_mfccs is None or my_mfccs is None:
        return "Error: Feature extraction failed", float('inf')

    # Compute the mean MFCC vector for each audio
    dataset_mean_mfcc = np.mean(dataset_mfccs, axis=0)
    my_mean_mfcc = np.mean(my_mfccs, axis=0)

    # Calculate cosine similarity
    similarity = 1 - cosine(dataset_mean_mfcc, my_mean_mfcc)  # Cosine similarity

    # Convert similarity to a distance-like measure
    distance = 1 - similarity

    if distance < threshold:
        return "Correct", distance
    elif distance < threshold * 1.5:  # Adjust multiplier as needed
        return "Partially Correct", distance
    else:
        return "Incorrect", distance

def main():
    dataset = {
        "Blessé": "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Blessé.mp3",  # Replace with your paths
    }

    my_recordings = {
        "Blessé": "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Comment.mp3",  # Replace with your paths
    }

    # Set threshold (needs to be determined empirically from your test set)
    cosine_threshold = 0.1  # Example threshold. Adjust based on your experiments!

    for word, dataset_audio in dataset.items():
        my_audio = my_recordings.get(word)
        if my_audio is None:
            print(f"Warning: No recording found for '{word}'")
            continue

        dataset_mfccs = extract_mfccs(dataset_audio)
        my_mfccs = extract_mfccs(my_audio)
        result, distance = compare_pronunciations(dataset_mfccs, my_mfccs, cosine_threshold)
        print(f"Pronunciation of '{word}': Result = {result}, Distance = {distance:.2f}")

if __name__ == "__main__":
    main()
