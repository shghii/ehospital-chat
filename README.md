# Medical Assistance Backend API

![Work in Progress](https://img.shields.io/badge/status-WIP-yellow.svg)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.1-009688.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI%20API-0.27.2-412991.svg)](https://platform.openai.com/)

A backend service for a medical assistance application providing AI-powered chat/voice interactions and appointment scheduling capabilities.

**Warning**: This project is currently under active development and not production-ready. Core functionality is implemented but requires additional safety measures and validation for medical use cases.

## Features

✅ **Implemented**
- Text-based medical Q&A with OpenAI GPT-3.5
- Voice message transcription and AI response generation
- Basic appointment scheduling system
- Conversation history management
- API endpoints for:
  - Chat interactions (`/chat`)
  - Voice interactions (`/voice-chat`)
  - Appointment management (`/appointments`)

🚧 **Upcoming Features**
- User authentication system
- Real doctor calendar integration
- Medical symptom validation layer
- Emergency contact integration
- Multi-language support
- HIPAA compliance measures

## Installation

1. Clone the repository:

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```env
OPENAI_API_KEY=
```

4. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

## API Reference

### Base URL
`http://localhost:8000` (development)

### Endpoints

#### Chat Interaction
```http
POST /chat/
Content-Type: application/json

{
  "message": "What are the symptoms of diabetes?"
}
```

#### Voice Interaction
```http
POST /voice-chat/
Content-Type: multipart/form-data

File: audio=@voice_message.wav
```

#### Appointment Management
```http
POST /appointments/
Content-Type: application/json

{
  "patient_name": "John Doe",
  "patient_email": "john@example.com",
  "appointment_date": "2025-03-22",
  "appointment_time": "09:00",
  "symptoms": "Persistent cough"
}
```

## Environment Variables

- `OPENAI_API_KEY`: Required OpenAI API key

## Testing
Run the test suite with:
```bash
pytest tests/
```

## Disclaimer
This application is not intended for actual medical diagnosis or treatment. Always consult a qualified healthcare professional for medical advice. The AI responses should not be considered as medical opinions.

