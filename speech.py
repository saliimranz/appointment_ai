# speech.py
import os
from transformers import pipeline
from IPython.display import Audio, display
from TTS.api import TTS

# Load Whisper STT
stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-base")

# Load Coqui TTS
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def stt_from_file(audio_file_path):
    """Convert speech to text using Whisper."""
    result = stt_pipeline(audio_file_path)
    return result.get("text", "").strip()

def tts_to_audio(text):
    """Convert text to speech using Coqui TTS."""
    output_file = "output.wav"
    tts_model.tts_to_file(text=text, file_path=output_file)
    display(Audio(output_file, autoplay=True))
