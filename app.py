# app.py
import streamlit as st
import os
from chat import chat_session

def main():
    st.title("Appointment AI")

    uploaded_file = st.file_uploader("Upload Doctor's Schedule CSV", type=["csv"])

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
