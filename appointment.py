from utils import get_slot_id
import pandas as pd
from langchain.schema import Document


def update_appointment_csv(csv_file, appointment_info, patient_name):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return

    if appointment_info:
        mask = (df['DoctorName'] == appointment_info['doctor']) & (df['Date'] == appointment_info['date']) & (df['Time'] == appointment_info['time'])
        if mask.any():
            df.loc[mask, 'PatientName'] = patient_name # Update the CSV
            try:
                df.to_csv(csv_file, index=False)
                print(f"Appointment updated in '{csv_file}'")
            except Exception as e:
                print(f"Error writing to CSV: {e}")
        else:
            print("No matching appointment found in the CSV.")
    else:
        print("No appointment information to update.")


#Update the slot metadata in the vector database
def update_slot_metadata_by_details(vectordb, appointment_info, new_patient_name):
    # Retrieve the SlotID using the helper function
    doctor_name = appointment_info['doctor']
    date = appointment_info['date']
    time = appointment_info['time']
    slot_id = get_slot_id(vectordb, doctor_name, date, time)
    if not slot_id:
        return "No matching slot found for the given details."

    # Now query using the SlotID
    results = vectordb.get(where={"SlotID": slot_id})
    if results["ids"]:
        doc_id = results["ids"][0]
        current_metadata = results["metadatas"][0]

        # Update metadata
        current_metadata["PatientName"] = new_patient_name

        # Create an updated document text
        doc_text = (
            f"SlotID: {slot_id}, Doctor: {doctor_name}, Date: {date}, "
            f"Time: {time}, Patient: {new_patient_name}"
        )

        # Create an updated Document object
        updated_doc = Document(page_content=doc_text, metadata=current_metadata)

        # Update the vector database
        vectordb.update_document(doc_id, updated_doc)

        return f"Slot {slot_id} updated: now booked for {new_patient_name}."

    return f"Slot {slot_id} not found in the vector DB."