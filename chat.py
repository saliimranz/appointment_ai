# chat.py
import os
from speech import stt_from_file, tts_to_audio
from vector_db import query_vector_database
from intent import get_intent_and_query
from config import USER_ID, CSV_FILE_PATH
import streamlit as st

def chat_session():
    chat_history_str = ""

    while st.session_state.running:
        user_query = stt_from_file("audio_file.wav")  # Replace with actual file input
        intent_details = get_intent_and_query(chat_history_str + f"\nUser: {user_query}")

        retrieved_context = query_vector_database(user_query) if intent_details["intent"] == "Yes" else {"documents": []}
        final_answer = "AI-generated response based on context."

        tts_to_audio(final_answer)
        chat_history_str += f"User: {user_query}\nAI: {final_answer}\n"

        with open("logs/chat_log.txt", "a") as log_file:
            log_file.write(chat_history_str + "\n")

        if "confirmed" in final_answer.lower():
            break
