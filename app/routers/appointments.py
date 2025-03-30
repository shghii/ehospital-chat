from fastapi import APIRouter
from app.schemas.schemas import Appointment, AppointmentResponse

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
async def schedule_appointment(appointment: Appointment):
    # Instead of directly scheduling, we now redirect users to the external scheduling system
    redirect_message = (
        f"Hi {appointment.patient_name}, to complete your appointment booking, "
        f"please visit our scheduling website at https://e-hospital.ca/schedule. "
        f"There you can select your preferred date and time. "
        f"Details provided here will help pre-fill the form: "
        f"Email: {appointment.patient_email}, "
        f"Symptoms: {appointment.symptoms if appointment.symptoms else 'None provided'}."
    )
    return AppointmentResponse(message=redirect_message)
