# app.py

import os
import threading

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from vector_db import load_and_embed_data_unique
from config import CSV_FILE_PATH

def initialize_vector_db():
    global vectordb_unique
    st.write("Initializing vector database... Please wait.")
    vectordb_unique = load_and_embed_data_unique(csv_file = CSV_FILE_PATH)
    st.success("Vector database initialized!")

vectordb_thread = threading.Thread(target=initialize_vector_db)
vectordb_thread.start()

from chat import chat_session

def main():
    st.title("Appointment AI")

    uploaded_file = st.file_uploader("Upload Doctor's Schedule CSV", type=["csv"])

    if uploaded_file:
        CSV_FILE_PATH = "doctor_schedule_fixed.csv"
        with open(CSV_FILE_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())  # Save the file
        st.success("File uploaded successfully!")
    else:
        st.warning("Please upload a CSV file to proceed.")

    if st.button("Call to Schedule Appointment"):
        st.session_state.running = True
        chat_session()

    if st.button("End Call"):
        st.session_state.running = False

    st.subheader("Call Logs")
    if os.path.exists("logs/chat_log.txt"):
        with open("logs/chat_log.txt", "r") as log_file:
            st.text_area("Call Logs:", log_file.read(), height=200)

if __name__ == "__main__":
    if "running" not in st.session_state:
        st.session_state.running = False
    # 🔥 Print logs to debug startup issues
    print("Starting Streamlit app...")

    # ✅ Ensure correct port
    os.system("streamlit run app.py --server.port 8501 --server.address 0.0.0.0")
    main()
