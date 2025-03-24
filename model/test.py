import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense, Lambda, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K

# Function to extract MFCCs
def extract_mfccs(audio_file, n_mfcc=13, max_pad_len=100):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    # Padding
    pad_width = max_pad_len - mfccs.shape[1]
    if pad_width > 0:
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mfccs = mfccs[:, :max_pad_len]
    return mfccs

# Define the Siamese Network
def create_siamese_model(input_shape):
    input = Input(shape=input_shape)
    x = Flatten()(input)
    x = Dense(128, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    x = Dense(32, activation='relu')(x)
    return Model(input, x)

def euclidean_distance(vectors):
    x, y = vectors
    sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sum_square, K.epsilon()))

def build_siamese_network(input_shape):
    base_network = create_siamese_model(input_shape)
    input_a = Input(shape=input_shape)
    input_b = Input(shape=input_shape)

    processed_a = base_network(input_a)
    processed_b = base_network(input_b)

    distance = Lambda(euclidean_distance, output_shape=(1,))([processed_a, processed_b])

    model = Model([input_a, input_b], distance)
    return model

# Load your data
# For demonstration purposes, replace with actual data loading
audio_file_1 = '/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Blessé.mp3'
audio_file_2 = '/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/abcd.mp3'
mfcc_1 = extract_mfccs(audio_file_1)
mfcc_2 = extract_mfccs(audio_file_2)

# Define input shape
input_shape = mfcc_1.shape

# Build and compile the model
siamese_model = build_siamese_network(input_shape)
siamese_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Dummy data for demonstration
# Replace with actual pairs and labels
pairs = [np.array([mfcc_1, mfcc_2])]
labels = [1]  # 1 for similar, 0 for dissimilar

# Convert data to arrays
pairs = np.array(pairs)
labels = np.array(labels)

# Train the model
siamese_model.fit([pairs[:, 0], pairs[:, 1]], labels, epochs=10, batch_size=1)

# Predict similarity
distance = siamese_model.predict([np.expand_dims(mfcc_1, axis=0), np.expand_dims(mfcc_2, axis=0)])
print(f"Distance between words: {distance[0][0]}")
