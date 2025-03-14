# intent.py
import json
import re
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def get_intent_and_query(chat_history):
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Define prompt template
    prompt = f"""
    You are an AI assistant helping with doctor appointment bookings.
    Analyze the conversation history below and determine:

    1. Whether a database query is needed to fetch appointment details (respond "Yes" or "No").
    2. If "Yes", generate a **meaningful search query string** containing relevant details for searching the vector database.

    ## Chat History:
    {chat_history}

    ## Instructions:
    - If the user is **asking about appointment availability, booking, rescheduling, or confirming** an appointment, return intent "Yes".
    - If the user is just **greeting, making small talk, or asking general non-booking questions**, return intent "No".
    - If intent is "Yes":
        - **Extract the core intent** (e.g., checking availability, booking, modifying, or canceling).
        - **Include key details** (Doctor Name, Date, Time) if mentioned.
        - If no specific date is provided but the user asks about availability, assume the query is about "next available appointment."
        - If the user asks for **earliest availability**, include "earliest available appointment."
        - If the user is checking a **specific date and time**, ensure it's included in the query.
        - If rescheduling or modifying, include "reschedule" in the query.
        - If canceling an appointment, include "cancel appointment."
        - The final query should be **a well-formed, natural search string** that captures the exact request.

    ## Response Format (JSON):
    {{
        "intent": "Yes" or "No",
        "query": "A single search string summarizing the user request."
    }}
    """

    response = model.generate_content(prompt)

    response_text = response.candidates[0].content.parts[0].text

    print(f"Response Full: {response_text}")  # Debugging print

    # **Remove Markdown formatting (` ```json ... ``` `)**
    cleaned_response = re.sub(r"```json\n(.*?)\n```", r"\1", response_text, flags=re.DOTALL)

    try:
        # Convert to dictionary
        response_json = json.loads(cleaned_response)
        return response_json
    except json.JSONDecodeError as e:
        print(f"Error parsing LLM response: {e}")
        return {"intent": "No", "query": ""}
