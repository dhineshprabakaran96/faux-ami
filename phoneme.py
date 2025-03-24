import librosa
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import phonemeRecognizerWrapper  # Replace with actual phoneme recognition library

def extract_phonemes(audio_file):
    try:
        # Load the audio file
        y, sr = librosa.load(audio_file)
        # Use a phoneme recognition library to extract phonemes
        phonemes = phonemeRecognizerWrapper.recognize(y, sr)
        return phonemes
    except FileNotFoundError:
        print(f"Error: Audio file not found: {audio_file}")
        return None
    except Exception as e:
        print(f"Error processing audio file {audio_file}: {e}")
        return None

def compare_pronunciations(dataset_phonemes, my_phonemes, threshold):
    if dataset_phonemes is None or my_phonemes is None:
        return "Error: Phoneme extraction failed", float('inf')

    distance, path = fastdtw(dataset_phonemes, my_phonemes, dist=euclidean)
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
        "Blessé": "/Users/dprabak7/Documents/Code/faux-ami/my-samples/Blessé.mp3",  # Replace with your paths
    }

    # Set threshold (needs to be determined empirically from your test set)
    dtw_threshold = 100  # Example threshold. Adjust based on your experiments!

    for word, dataset_audio in dataset.items():
        my_audio = my_recordings.get(word)
        if my_audio is None:
            print(f"Warning: No recording found for '{word}'")
            continue

        dataset_phonemes = extract_phonemes(dataset_audio)
        my_phonemes = extract_phonemes(my_audio)
        result, distance = compare_pronunciations(dataset_phonemes, my_phonemes, dtw_threshold)
        print(f"Pronunciation of '{word}': Result = {result}, Distance = {distance:.2f}")

if __name__ == "__main__":
    main()
