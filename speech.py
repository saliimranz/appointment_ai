# speech.py
import os
from transformers import pipeline
from IPython.display import Audio, display
from gtts import gTTS
import streamlit as st

# Load Whisper STT
stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-base")

def stt_from_file(audio_file_path):
    """Convert speech to text using Whisper."""
    result = stt_pipeline(audio_file_path)
    return result.get("text", "").strip()

def tts_to_audio(text):
    """Convert text to speech using Google TTS."""
    output_file = "output.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)
    st.audio(output_file, format="audio/mp3", autoplay=True)
