from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.appointment_schema import ChatResponse
from app.utils.transcription import transcribe_audio
from app.utils.openai_client import get_chat_response_with_history
import os

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def voice_chat_endpoint(audio: UploadFile = File(...)):
    try:
        # Transcribe audio file to text
        transcript = transcribe_audio(audio)
        if not transcript:
            raise HTTPException(status_code=400, detail="Transcription failed.")
        
        # Create a message history format that matches what the function expects
        message = [{"role": "user", "content": transcript}]
        response_text = get_chat_response_with_history(message)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
