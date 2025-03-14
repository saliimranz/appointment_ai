# vector_db.py
import pandas as pd
import hashlib
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings
from config import CSV_FILE_PATH, COLLECTION_NAME

def generate_slot_id(doctor, date, time):
    # Create a deterministic hash based on key fields
    unique_str = f"{doctor}_{date}_{time}"
    return hashlib.sha256(unique_str.encode()).hexdigest()

def query_vector_database(vectordb, user_query, k=10):
    # Search for the k most similar documents to the user query
    results = vectordb.similarity_search(user_query, k=k)
    # Concatenate the retrieved document texts to form a context string
    context = "\n".join([doc.page_content for doc in results])
    return {"documents": context, "results": results}

def load_and_embed_data_unique(csv_file, collection_name="doctor_schedule_v2"):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Normalize time format (ensure consistency)
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M").dt.strftime("%H:%M")

    documents = []
    metadatas = []
    ids = []

    for _, row in df.iterrows():
        # Generate a unique SlotID using a hash of DoctorName, Date, and Time
        slot_id = generate_slot_id(row["DoctorName"], row["Date"], row["Time"])
        ids.append(slot_id)

        # Create structured text representation including the unique SlotID
        doc = (
            f"SlotID: {slot_id}, Doctor: {row['DoctorName']}, Date: {row['Date']}, "
            f"Time: {row['Time']}, Patient: {row['PatientName'] if pd.notna(row['PatientName']) else 'Available'}"
        )
        documents.append(doc)

        # Create metadata including the unique SlotID
        metadatas.append({
            "SlotID": slot_id,
            "DoctorName": row["DoctorName"],
            "Date": row["Date"],
            "Time": row["Time"],
            "PatientName": row["PatientName"] if pd.notna(row["PatientName"]) else "Available"
        })

    # Initialize the embedding model with improved instructions
    embedder = HuggingFaceInstructEmbeddings(
        model_name="BAAI/bge-large-en",
        embed_instruction="Represent the doctor's schedule entry uniquely, emphasizing DoctorName, Date, Time, and PatientName.",
        query_instruction="Retrieve the most relevant schedule by closely matching DoctorName, Date, and Time."
    )

    # Create the ChromaDB collection with documents, metadata, and unique IDs.
    # Using deterministic IDs ensures that reingesting duplicates won't add extra entries.
    vectordb = Chroma.from_texts(
        texts=documents,
        embedding=embedder,
        metadatas=metadatas,
        ids=ids,  # deterministic IDs prevent duplicates
        collection_name=collection_name
    )

    return vectordb
