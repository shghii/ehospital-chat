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
- Integrated FAQ section for common medical questions
- PDF export of chat history
- Rate limiting for API protection
- Conversation persistence across sessions
- Character counter for input messages (cost optimization)
- Basic appointment scheduling system
- Conversation history management
- API endpoints for:
  - Chat interactions (`/chat`)
  - Voice interactions (`/voice-chat`)
  - Appointment management (`/appointments`)


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
  "message": "What are the symptoms of diabetes?",
  "history": [{"role": "user", "content": "previous message"}, {"role": "assistant", "content": "previous response"}]
}
```

#### Voice Interaction
```http
POST /voice-chat/
Content-Type: multipart/form-data

File: audio=@voice_message.wav
Field: history=JSON_string_of_conversation_history
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

## User Experience Features

### FAQ Section
- Quick access to common medical questions
- Clicking on a question automatically sends it to the chat

### Conversation Persistence
- Last 20 messages are saved locally in the browser
- Conversation history is restored when returning to the application
- Clear history option to remove all saved messages

### PDF Export
- Export entire chat history as a PDF document
- Includes both user and assistant messages with timestamps

### Rate Limiting
- Protects API from overuse with 15 requests per minute limit
- Helps prevent abuse and controls costs

### Character Counter
- Shows remaining characters for input messages
- Limit of 500 characters to optimize API costs
- Visual warning when approaching the limit

## Testing
Run the test suite with:
```bash
pytest tests/
```

## Deployment

This application can be deployed on [Render.com](https://render.com) using the provided `render.yaml` configuration file.

## Disclaimer
This application is not intended for actual medical diagnosis or treatment. Always consult a qualified healthcare professional for medical advice. The AI responses should not be considered as medical opinions.

