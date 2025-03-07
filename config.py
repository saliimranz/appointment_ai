import os
import streamlit as st

# Check if running on Streamlit Cloud (st.secrets exists)
if "HF_SECRET" in st.secrets:
    HF_TOKEN = st.secrets["HF_SECRET"]
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    from dotenv import load_dotenv
    load_dotenv()
    HF_TOKEN = os.getenv("HF_SECRET")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN

# Constants
COLLECTION_NAME = "doctor_schedule_v2"
CSV_FILE_PATH = "doctor_schedule_fixed.csv"
USER_ID = 66
