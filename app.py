import streamlit as st
import librosa
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

def extract_mfccs(audio_file, n_mfcc=13):
    try:
        y, sr = librosa.load(audio_file)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
        return mfccs.T
    except FileNotFoundError:
        st.error(f"Error: Audio file not found: {audio_file}")
        return None
    except Exception as e:
        st.error(f"Error processing audio file {audio_file}: {e}")
        return None

def compare_pronunciations(dataset_mfccs, my_mfccs, threshold):
    if dataset_mfccs is None or my_mfccs is None:
        return "Error: Feature extraction failed", float('inf')

    distance, path = fastdtw(dataset_mfccs, my_mfccs, dist=euclidean)
    if 15000 < distance < 20000:
        return "Correct", distance
    elif 10000 < distance < 15000:  # Adjust multiplier as needed
        return "Partially Correct", distance
    else:
        return "Incorrect", distance

def main():
    st.title("PronouncePal")

    st.write("Upload a dataset audio sample and your recording to compare pronunciations.")

    dataset_audio = st.file_uploader("Upload Dataset Audio", type=['mp3', 'wav'])
    my_audio = st.file_uploader("Upload Your Recording", type=['mp3', 'wav'])

    dtw_threshold = st.slider("Set DTW Threshold", 0, 20000, 100)

    if dataset_audio and my_audio:
        dataset_mfccs = extract_mfccs(dataset_audio)
        my_mfccs = extract_mfccs(my_audio)
        result, distance = compare_pronunciations(dataset_mfccs, my_mfccs, dtw_threshold)
        st.write(f"Result: {result}")
        st.write(f"Distance: {distance:.2f}")

if __name__ == "__main__":
    main()
