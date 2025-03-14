# chat.py
import os
from speech import stt_from_file, tts_to_audio
from vector_db import query_vector_database
from intent import get_intent_and_query
from config import USER_ID, CSV_FILE_PATH
import streamlit as st
import files
from appointment import update_appointment_csv, update_slot_metadata_by_details
from utils import extract_appointment_info
from llm import generate_answer, get_user_chat_history
from app import vectordb_unique

def chat_session():
    global chat_history_str # Declare chat_history_str as global
    chat_history_str = "" # Initialize it as an empty string

    while True:
        # Prompt user to upload an audio file (simulating voice input in Colab)
        print("Please upload an audio file containing your query (or type 'exit' in text input to end):")
        uploaded = files.upload()  # This will prompt a file upload dialog in Colab

        if not uploaded:
            user_input = input("No file uploaded. Type 'exit' to end or press Enter to try again: ")
            if user_input.lower() == "exit":
                break
            else:
                continue

        # Get filename of uploaded audio
        audio_filename = list(uploaded.keys())[0]

        # Convert the uploaded audio to text using STT
        user_query = stt_from_file(audio_filename)
        print(f"User (transcribed): {user_query}")

        if user_query.lower() in ["exit", "quit"]:
            break


        # user_query = input("Enter your query (or type 'exit' to end): ")
        # if user_query.lower() == "exit":
        #     break

        # Fetch chat history
        chat_history = get_user_chat_history(user_id)

        # **Append the latest user query** before sending it to LLM
        updated_chat_history = f"{chat_history}\nUser: {user_query}"

        # Get intent and details
        intent_details = get_intent_and_query(updated_chat_history)
        intent = intent_details.get("intent", "No")
        details = intent_details.get("details", {})

        # Retrieve context only when needed
        retrieved_context = query_vector_database(vectordb_unique, user_query) if intent == "Yes" else {"documents": []}

        final_answer = generate_answer(user_id, user_query, retrieved_context["documents"])
        print(f"\nA: {final_answer}")

        # Convert the final answer to speech using ElevenLabs TTS
        tts_to_audio(final_answer)

        # Accumulate chat history as a string.
        chat_history_str += f"User: {user_query}\nAI: {final_answer}\n"

        # Check for confirmation (example logic - adapt as needed)
        if "confirmed" in final_answer.lower() or "yes" in final_answer.lower() or "correct" in final_answer.lower() or "okay" in final_answer.lower(): # Basic confirmation check
            appointment_info = extract_appointment_info(chat_history_str)
            if appointment_info:
                update_appointment_csv(csv_file, appointment_info, user_id) #Pass user_id as patient name
                update_slot_metadata_by_details(vectordb_unique, appointment_info, user_id)

                break # Exit the loop after processing the confirmed booking
            else:
                print("Could not extract appointment information. Please provide the details again.")
                # You may want to reset chat_history_str here if extraction fails to re-prompt the user.
                chat_history_str = "" # Reset the chat history on extraction failure to restart the booking flow.
        elif "cancel" in final_answer.lower():
            print("Booking cancelled")
            chat_history_str = "" # Reset the chat history on cancel to restart the booking flow.
            break # Exit the loop after processing the confirmed booking

    # If the loop finished without confirmation it means the user exited without booking or cancelled
    else:
        print("Booking process incomplete")
