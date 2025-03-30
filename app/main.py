from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.routers import chat, voice_chat, appointments

app = FastAPI(
    title="Medical Assistance App",
    description="Chat with an AI medical assistant and schedule appointments.",
)

# Mount templates
templates = Jinja2Templates(directory="app/templates")

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(voice_chat.router, prefix="/voice-chat", tags=["Voice Chat"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
