import genai

user_chat_history = {}

def get_user_chat_history(user_id):
    return user_chat_history.get(user_id, "")

def update_user_chat_history(user_id, user_input, ai_response):
    user_chat_history[user_id] = f"{user_chat_history.get(user_id, '')}\nUser: {user_input}\nAI: {ai_response}"

def generate_answer(user_id, user_query, retrieved_context):
    model = genai.GenerativeModel('gemini-1.5-flash')

    chat_history = get_user_chat_history(user_id)

    # Detect if it's a new conversation
    is_first_interaction = not bool(chat_history.strip())
    greeting = "Hello! How can I assist you with booking a doctor appointment today?\n\n" if is_first_interaction else ""

    # Construct a better prompt
    prompt = f"""
    You are an AI call agent assisting patients in booking doctor appointments. Your job is to provide structured, clear, and complete responses.
    Prioritize the information in the `Retrieved Schedule` when answering the query. The `Retrieved Schedule` contains the ONLY valid information for booking appointments.

    ## Conversation Context
    {chat_history}

    ## Retrieved Schedule
    {retrieved_context}

    ## Instructions:
    1. Only greet the user in the first message. If chat history exists, do NOT greet again.
    2. If the user has already provided a doctor name, date, or time in previous messages, do not ask again.
    3. If the user is trying to book an appointment but hasn't provided a time yet, ask for the time.
    4. If all required details are available, confirm the appointment in a structured way.

    ## User Query:
    {user_query}
    """

    # Generate response using Gemini
    response = model.generate_content(prompt)
    response_text = response.text.strip()
    print(f"History: {chat_history}")
    # Only prepend greeting if it's the first interaction AND the response doesn't already contain a greeting
    if is_first_interaction and not response_text.lower().startswith(("hello", "hi", "greetings")):
      response_text = greeting + response_text
    # Store conversation history
    update_user_chat_history(user_id, user_query, response_text)

    return response_text