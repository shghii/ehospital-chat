# app/utils/openai_client.py
import openai
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def get_chat_response_with_history(conversation_history):
    system_message = {
        "role": "system",
        "content": (
            "You are a helpful medical assistant. "
            "Remind the user that your responses are for general guidance only."
        ),
    }
    messages = [system_message] + conversation_history
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
    )
    return completion.choices[0].message.content.strip()
