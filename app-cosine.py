import streamlit as st
import librosa
import numpy as np
from scipy.spatial.distance import cosine

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

    # Pad the shorter MFCC sequence to match the length of the longer one.  This is crucial for cosine similarity.
    max_len = max(len(dataset_mfccs), len(my_mfccs))
    dataset_mfccs = np.pad(dataset_mfccs, ((0, max_len - len(dataset_mfccs)), (0,0)), mode='constant')
    my_mfccs = np.pad(my_mfccs, ((0, max_len - len(my_mfccs)), (0,0)), mode='constant')


    #Calculate average MFCC vectors for each audio
    avg_dataset_mfccs = np.mean(dataset_mfccs, axis=0)
    avg_my_mfccs = np.mean(my_mfccs, axis=0)

    distance = cosine(avg_dataset_mfccs, avg_my_mfccs) #Cosine Similarity

    #Interpreting Cosine Similarity:  Closer to 0 means more similar.
    if distance < threshold:
        return "Correct", distance
    elif distance < threshold * 1.5: # Adjust multiplier as needed
        return "Partially Correct", distance
    else:
        return "Incorrect", distance

def main():
    st.title("PronouncePal")
    st.write("Upload a dataset audio sample and your recording to compare pronunciations.")

    dataset_audio = st.file_uploader("Upload Dataset Audio", type=['mp3', 'wav'])
    my_audio = st.file_uploader("Upload Your Recording", type=['mp3', 'wav'])

    #Cosine similarity threshold is between 0 and 1.
    cosine_threshold = st.slider("Set Cosine Similarity Threshold", 0.0, 1.0, 0.3)

    if dataset_audio and my_audio:
        dataset_mfccs = extract_mfccs(dataset_audio)
        my_mfccs = extract_mfccs(my_audio)
        result, distance = compare_pronunciations(dataset_mfccs, my_mfccs, cosine_threshold)
        st.write(f"Result: {result}")
        st.write(f"Distance: {distance:.2f}")

if __name__ == "__main__":
    main()
