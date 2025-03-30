from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict

# Chat endpoint schemas
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseModel):
    response: str

# Appointment schemas (used by both appointments endpoint and integrated chat)
class Appointment(BaseModel):
    patient_name: str
    patient_email: EmailStr
    appointment_date: str  # Format: YYYY-MM-DD
    appointment_time: str  # Format: HH:MM (24-hour)
    symptoms: Optional[str] = None

class AppointmentResponse(BaseModel):
    message: str

# Integrated chat schemas for handling both conversation and appointment scheduling flow
class IntegratedChatRequest(BaseModel):
    message: str
    # Flags for integrated flow; these can be passed from the frontend
    confirm_appointment: Optional[bool] = False
    selected_time: Optional[str] = None  # E.g., "2025-02-22 09:00"
    # Optionally include user details for appointment booking:
    patient_name: Optional[str] = None
    patient_email: Optional[EmailStr] = None
    history: Optional[List[Dict[str, str]]] = None

class IntegratedChatResponse(BaseModel):
    response: str
    appointment_options: List[str] = []
