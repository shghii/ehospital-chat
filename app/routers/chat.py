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
    # Retrieve conversation history for the user, or start fresh.
    conversation_history = user_conversations.get(user_id, [])
    
    # Append the new user message.
    conversation_history.append({"role": "user", "content": request.message})
    user_msg = request.message.lower()
    
    # Check if the user's message contains an available time slot (for appointment confirmation).
    available_slots = get_available_slots()
    selected_slot = next((slot for slot in available_slots if slot in user_msg), None)
    
    if selected_slot:
        # Schedule the appointment (here using default user details for demo).
        appointment = Appointment(
            patient_name="User",  # Replace with actual user info from session/auth.
            patient_email="user@example.com",
            appointment_date=selected_slot.split()[0],
            appointment_time=selected_slot.split()[1],
            symptoms=""
        )
        appointments_db.append(appointment)
        confirmation = (
            f"Your appointment has been scheduled for {appointment.appointment_date} at "
            f"{appointment.appointment_time}. A confirmation email will be sent to {appointment.patient_email}."
        )
        conversation_history.append({"role": "assistant", "content": confirmation})
        user_conversations[user_id] = conversation_history
        return IntegratedChatResponse(response=confirmation, appointment_options=[])
    
    # If the user message indicates a need for an appointment (e.g., contains keywords)
    appointment_keywords = ["appointment", "book", "schedule", "see a doctor", "doctor"]
    if any(keyword in user_msg for keyword in appointment_keywords):
        slots_text = "It looks like you might need to see a doctor. " \
                     "Here are some available appointment slots: " + ", ".join(available_slots) + \
                     ". Please reply with the exact slot you prefer (e.g., '2025-02-22 11:00')."
        conversation_history.append({"role": "assistant", "content": slots_text})
        user_conversations[user_id] = conversation_history
        return IntegratedChatResponse(response=slots_text, appointment_options=available_slots)
    
    # Otherwise, treat it as a normal conversation.
    try:
        ai_response = get_chat_response_with_history(conversation_history)
        conversation_history.append({"role": "assistant", "content": ai_response})
        user_conversations[user_id] = conversation_history
        return IntegratedChatResponse(response=ai_response, appointment_options=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
