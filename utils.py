from typing import Any, Dict, Optional
#extract key info from llm
import json
import re
import typing_extensions as typing 
import genai


def get_slot_id(vectordb, doctor_name, date, time):
    # Combine multiple conditions using the "$and" operator
    results = vectordb.get(where={"$and": [
        {"DoctorName": doctor_name},
        {"Date": date},
        {"Time": time}
    ]})

    if results["ids"]:
        print(f"Results: {results}")
        # Iterate over the returned metadata entries to find one with a valid SlotID
        for meta in results["metadatas"]:
            slot_id = meta.get("SlotID")
            if slot_id:
                print(f"SlotID: {slot_id}")
                return slot_id
    return None

class AppointmentInfo(typing.TypedDict):
    doctor: str
    date: str
    time: str

def extract_appointment_info(llm_response):
    model = genai.GenerativeModel(
        'gemini-1.5-flash',  # Or your preferred Gemini model
        generation_config=genai.GenerationConfig(
            temperature=0.1,  # Adjust as needed
            response_mime_type="application/json",
            response_schema=AppointmentInfo
        ))

    prompt = f"""
    Extract the doctor's name, date, and time from the following text and return them as a JSON object, convert time to 24-Hour format, date format to yyyy-mm-dd (if year not provided default as 2025):

    ```
    {llm_response}
    ```
    """

    response = model.generate_content(prompt)
    print(f"Decoding json method's response: {response.text}")  # Keep this for debugging

    try:
        appointment_info = json.loads(response.text)
        # appointment_info = response.text  # Directly access the JSON data
        print(f"Decoded json: {appointment_info}")
        return appointment_info
    except Exception as e:  # Catch any potential errors
        print(f"Error extracting appointment info: {e}")
        return None