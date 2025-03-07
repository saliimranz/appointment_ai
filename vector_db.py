# vector_db.py
import pandas as pd
import hashlib
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings
from config import CSV_FILE_PATH, COLLECTION_NAME

def generate_slot_id(doctor, date, time):
    """Generate a unique SlotID based on doctor, date, and time."""
    unique_str = f"{doctor}_{date}_{time}"
    return hashlib.sha256(unique_str.encode()).hexdigest()

def load_and_embed_data_unique():
    """Load CSV, generate embeddings, and store in ChromaDB."""
    df = pd.read_csv(CSV_FILE_PATH)
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M").dt.strftime("%H:%M")

    documents, metadatas, ids = [], [], []
    for _, row in df.iterrows():
        slot_id = generate_slot_id(row["DoctorName"], row["Date"], row["Time"])
        ids.append(slot_id)
        doc = f"SlotID: {slot_id}, Doctor: {row['DoctorName']}, Date: {row['Date']}, Time: {row['Time']}, Patient: {row.get('PatientName', 'Available')}"
        documents.append(doc)
        metadatas.append({"SlotID": slot_id, "DoctorName": row["DoctorName"], "Date": row["Date"], "Time": row["Time"], "PatientName": row.get("PatientName", "Available")})

    embedder = HuggingFaceInstructEmbeddings(model_name="BAAI/bge-large-en")
    vectordb = Chroma.from_texts(texts=documents, embedding=embedder, metadatas=metadatas, ids=ids, collection_name=COLLECTION_NAME)
    return vectordb

vectordb_unique = load_and_embed_data_unique()
