from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.appointment_schema import ChatResponse
from app.utils.transcription import transcribe_audio
from app.utils.openai_client import get_chat_response_with_history
import os
import json
from typing import Optional

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def voice_chat_endpoint(audio: UploadFile = File(...), history: Optional[str] = Form(None)):
    try:
        # Transcribe audio file to text
        transcript = transcribe_audio(audio)
        if not transcript:
            raise HTTPException(status_code=400, detail="Transcription failed.")
        
        # Parse history if provided
        conversation_history = []
        if history:
            try:
                conversation_history = json.loads(history)
            except json.JSONDecodeError:
                # If history can't be parsed, just proceed with empty history
                pass
        
        # Check if the user is asking about scheduling an appointment
        appointment_keywords = ["appointment", "book", "schedule", "see a doctor", "doctor"]
        transcript_lower = transcript.lower()
        
        if any(keyword in transcript_lower for keyword in appointment_keywords):
            scheduling_message = (
                "If you'd like to schedule an appointment with one of our healthcare providers, "
                "you can do so through our online scheduling system. "
                "Please visit <a href='https://e-hospital.ca/schedule' target='_blank'>e-hospital.ca/schedule</a> "
                "to view available appointments and book a time that works for you."
            )
            return ChatResponse(response=scheduling_message)
        
        # Add the current transcript to the conversation history
        conversation_history.append({"role": "user", "content": transcript})
        
        # Get response with the full conversation history
        response_text = get_chat_response_with_history(conversation_history)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
