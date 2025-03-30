from fastapi import APIRouter
from app.schemas.schemas import Appointment, AppointmentResponse

router = APIRouter()

# Simple in-memory storage (for demonstration)
appointments_db = []

@router.post("/", response_model=AppointmentResponse)
async def schedule_appointment(appointment: Appointment):
    appointments_db.append(appointment)
    confirmation = (
        f"Appointment reserved for {appointment.patient_name} on "
        f"{appointment.appointment_date} at {appointment.appointment_time}. "
        f"A confirmation email will be sent to {appointment.patient_email}."
    )
    return AppointmentResponse(message=confirmation)
