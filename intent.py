# intent.py
import json
import re
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def get_intent_and_query(chat_history):
    """Analyze intent and extract query for vector DB."""
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are an AI assistant for doctor appointment bookings.
    Determine:
    1. If a database query is needed (Yes/No).
    2. A meaningful search query string if needed.

    ## Chat History:
    {chat_history}

    ## Response Format (JSON):
    {{
        "intent": "Yes" or "No",
        "query": "Generated query string"
    }}
    """

    response = model.generate_content(prompt)
    response_text = re.sub(r"```json\n(.*?)\n```", r"\1", response.text.strip(), flags=re.DOTALL)

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"intent": "No", "query": ""}
