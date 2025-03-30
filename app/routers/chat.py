# app/routers/chat.py
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.schemas import ChatRequest, IntegratedChatResponse, Appointment
from app.utils.openai_client import get_chat_response_with_history
from datetime import datetime

router = APIRouter()

# For demonstration, we're using an in-memory dictionary keyed by a dummy user id.
user_conversations = {}
appointments_db = []

def get_user_id():
    # In production, replace with proper authentication/session management.
    return "dummy_user_id"

# This function is no longer used as we're redirecting to an external scheduling system
def get_available_slots():
    # This function returns available appointment slots.
    # In a real scenario, this might query a calendar database.
    return [
        "2025-03-22 09:00",
        "2025-03-22 11:00",
        "2025-03-22 15:00"
    ]

@router.post("/", response_model=IntegratedChatResponse)
async def chat_endpoint(request: ChatRequest, user_id: str = Depends(get_user_id)):
    # Initialize conversation history
    conversation_history = []
    
    # If history is provided in the request, use it
    if request.history:
        conversation_history = request.history
    # Otherwise use server-side stored history if available
    else:
        conversation_history = user_conversations.get(user_id, [])
    
    # Append the new user message if not already in history
    if not conversation_history or conversation_history[-1].get("content") != request.message:
        conversation_history.append({"role": "user", "content": request.message})
    
    user_msg = request.message.lower()
    
    # Check if the user message indicates a need for an appointment (e.g., contains keywords)
    appointment_keywords = ["appointment", "book", "schedule", "see a doctor", "doctor"]
    if any(keyword in user_msg for keyword in appointment_keywords):
        scheduling_message = (
            "If you'd like to schedule an appointment with one of our healthcare providers, "
            "you can do so through our online scheduling system. "
            "Please visit <a href='https://e-hospital.ca/schedule' target='_blank'>e-hospital.ca/schedule</a> "
            "to view available appointments and book a time that works for you."
        )
        conversation_history.append({"role": "assistant", "content": scheduling_message})
        user_conversations[user_id] = conversation_history
        return IntegratedChatResponse(response=scheduling_message, appointment_options=[])
    
    # Otherwise, treat it as a normal conversation.
    try:
        ai_response = get_chat_response_with_history(conversation_history)
        conversation_history.append({"role": "assistant", "content": ai_response})
        user_conversations[user_id] = conversation_history
        return IntegratedChatResponse(response=ai_response, appointment_options=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
