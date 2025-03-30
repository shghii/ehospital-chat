from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.routers import chat, voice_chat, appointments
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Medical Assistance App",
    description="Chat with an AI medical assistant and schedule appointments.",
)

# Rate limiting configuration
class RateLimitMiddleware:
    def __init__(self, app, limit=15, window=60):
        self.app = app
        self.limit = limit  # Number of requests allowed
        self.window = window  # Time window in seconds
        self.requests = {}  # Store IP addresses and their request timestamps

    async def __call__(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host
        
        # Initialize or get client's request timestamps
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Clean up old timestamps
        current_time = time.time()
        self.requests[client_ip] = [ts for ts in self.requests[client_ip] 
                                   if current_time - ts < self.window]
        
        # Check if rate limit is exceeded
        if len(self.requests[client_ip]) >= self.limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Please try again later."}
            )
        
        # Add current request timestamp
        self.requests[client_ip].append(current_time)
        
        # Process the request
        return await call_next(request)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.middleware("http")(RateLimitMiddleware(app))

# Mount templates
templates = Jinja2Templates(directory="app/templates")

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(voice_chat.router, prefix="/voice-chat", tags=["Voice Chat"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
