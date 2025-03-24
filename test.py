from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import torch
import librosa

# Load pre-trained model and tokenizer
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")

# Load French audio file
audio_path = "/Users/dprabak7/Documents/Code/faux-ami/audio-samples/French/Chanter.mp3"
audio_input, sample_rate = librosa.load(audio_path, sr=16000)

# Tokenize audio input
input_values = tokenizer(audio_input, return_tensors="pt").input_values

# Perform inference
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)

# Decode predicted ids to transcriptions
transcription = tokenizer.decode(predicted_ids[0])

print("Transcription:", transcription)
