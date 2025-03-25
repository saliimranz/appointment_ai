import os
from speech import stt_from_file, tts_to_audio
from vector_db import query_vector_database
from intent import get_intent_and_query
from config import USER_ID, CSV_FILE_PATH
import streamlit as st
from appointment import update_appointment_csv, update_slot_metadata_by_details
from utils import extract_appointment_info
from llm import generate_answer, get_user_chat_history
from app import vectordb_unique

def chat_session():
    global chat_history_str  
    chat_history_str = ""  

    while True:
        st.write("Upload an audio file containing your query:")
        
        # ✅ Use Streamlit's File Uploader Instead of Colab's `files.upload()`
        uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "ogg"])

        if uploaded_file is None:
            st.warning("No file uploaded. Please upload an audio file.")
            continue  # Keep asking for input

        # ✅ Save uploaded file temporarily
        temp_audio_path = f"temp_{USER_ID}.mp3"
        with open(temp_audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # ✅ Convert uploaded audio to text using STT
        user_query = stt_from_file(temp_audio_path)
        st.write(f"**User (transcribed):** {user_query}")

        if user_query.lower() in ["exit", "quit"]:
            break

        # ✅ Fetch chat history
        chat_history = get_user_chat_history(user_id=USER_ID)

        # ✅ Append latest user query to chat history
        updated_chat_history = f"{chat_history}\nUser: {user_query}"

        # ✅ Get intent and details
        intent_details = get_intent_and_query(updated_chat_history)
        intent = intent_details.get("intent", "No")
        details = intent_details.get("details", {})

        # ✅ Retrieve context only when needed
        retrieved_context = query_vector_database(vectordb_unique, user_query) if intent == "Yes" else {"documents": []}

        # ✅ Generate AI response
        final_answer = generate_answer(USER_ID, user_query, retrieved_context["documents"])
        st.write(f"\n**AI Response:** {final_answer}")

        # ✅ Convert AI response to speech
        tts_to_audio(final_answer)

        # ✅ Accumulate chat history
        chat_history_str += f"User: {user_query}\nAI: {final_answer}\n"

        # ✅ Process appointment booking
        if any(x in final_answer.lower() for x in ["confirmed", "yes", "correct", "okay"]):
            appointment_info = extract_appointment_info(chat_history_str)
            if appointment_info:
                update_appointment_csv(CSV_FILE_PATH, appointment_info, USER_ID)
                update_slot_metadata_by_details(vectordb_unique, appointment_info, USER_ID)
                break  
            else:
                st.error("Could not extract appointment information. Please provide details again.")
                chat_history_str = ""  

        elif "cancel" in final_answer.lower():
            st.warning("Booking cancelled")
            chat_history_str = ""  
            break  

    else:
        st.warning("Booking process incomplete")