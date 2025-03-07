# app.py
import streamlit as st
import os
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
    main()
