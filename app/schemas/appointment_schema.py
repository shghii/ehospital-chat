from pydantic import BaseModel, EmailStr
from typing import Optional

# Chat endpoints schemas
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Appointment schemas
class Appointment(BaseModel):
    patient_name: str
    patient_email: EmailStr
    appointment_date: str  # Expected in YYYY-MM-DD format
    appointment_time: str  # Expected in HH:MM format
    symptoms: Optional[str] = None

class AppointmentResponse(BaseModel):
    message: str
