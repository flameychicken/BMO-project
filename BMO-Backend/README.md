# BMO Backend - Local AI Chatbot Server

This is the backend service for BMO, a local AI chatbot inspired by Adventure Time's lovable video game console. BMO uses a native LLM (Mistral 7B) to provide friendly, character-accurate responses with conversation memory.

## Features

- **Local LLM Processing**: Uses `llama-cpp-python` to run quantized Mistral 7B locally
- **BMO Personality**: Authentic Adventure Time BMO character with mood tracking
- **Conversation Memory**: Remembers context across multiple exchanges
- **Apple M1 Optimized**: Special optimizations for Apple Silicon with Metal acceleration
- **FastAPI REST API**: Clean, documented API endpoints
- **Memory Management**: Intelligent conversation history and low-memory optimizations
- **Real-time Status**: Health checks and model status monitoring

## Project Structure

```
BMO-Backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   └── chat.py          # Pydantic schemas
│   ├── routes/
│   │   └── chat_route.py    # API endpoints
│   └── services/
│       └── chat_service.py  # LLM service & BMO personality
├── models/                  # Store .gguf model files here
│   └── mistral-7b-v0.1.Q4_K_M.gguf
├── requirements.txt
├── startup.py               # Enhanced startup script
├── test_bmo_client.py       # Test client
└── test_bmo_memory.py       # Memory testing suite
```

## Setup & Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download BMO's Brain (Model)
Choose based on your system memory:

**For systems with <4GB available RAM (Recommended):**
```bash
mkdir -p models
wget -O models/mistral-7b-v0.1.Q3_K_M.gguf https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.q3_k_m.gguf
```

**For systems with 4-6GB available RAM:**
```bash
wget -O models/mistral-7b-v0.1.Q4_K_M.gguf https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.q4_k_m.gguf
```

### 3. Start BMO Server
```bash
python startup.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📬 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and API info |
| GET | `/health` | Health check |
| POST | `/chat/` | Chat with BMO |
| GET | `/chat/status` | Check BMO's status |
| POST | `/chat/reset` | Reset conversation memory |

---

### POST `/chat/` - Chat with BMO

Send a message to BMO and get a response with conversation memory.

**Request Body:**
```json
{
  "prompt": "Hi BMO! How are you today?",
  "max_tokens": 150,
  "temperature": 0.8,
  "reset_conversation": false
}
```

**Parameters:**
- `prompt` (string, required): Your message to BMO
- `max_tokens` (integer, optional): Maximum response length (1-500, default: 150)
- `temperature` (float, optional): BMO's creativity level (0.0-1.5, default: 0.8)
- `reset_conversation` (boolean, optional): Clear BMO's memory (default: false)

**Response:**
```json
{
  "response": "Mathematical! I'm doing great! Ready for adventure! What would you like to do today?",
  "tokens_used": 23,
  "conversation_length": 1,
  "bmo_mood": "excited"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Tell me a joke, BMO!",
    "max_tokens": 100,
    "temperature": 0.9
  }'
```

---

### GET `/chat/status` - Check BMO's Status

Get BMO's current operational status and conversation state.

**Response:**
```json
{
  "status": "ready",
  "message": "BMO is ready for adventure! Mathematical!",
  "mood": "happy",
  "conversation_length": 3,
  "test_response": "Beep boop! BMO is working perfectly!",
  "ready": true
}
```

**Status Values:**
- `"ready"`: BMO is loaded and ready to chat
- `"loading"`: BMO is still initializing
- `"error"`: BMO encountered a problem

---

### POST `/chat/reset` - Reset Conversation

Clear BMO's conversation memory and start fresh.

**Response:**
```json
{
  "status": "success",
  "message": "BMO's memory has been refreshed! Ready for new adventures!",
  "mood": "happy"
}
```

---

### GET `/health` - Health Check

Simple health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "bmo_says": "All systems go! Time for adventure!"
}
```

---

### GET `/` - API Information

Get welcome message and available endpoints.

**Response:**
```json
{
  "message": "BMO is ready to chat!",
  "status": "Mathematical!",
  "endpoints": {
    "chat": "/chat/",
    "status": "/chat/status",
    "health": "/health"
  }
}
```

## BMO's Memory System

BMO remembers your conversations! Here's how it works:

### Memory Features:
- **Persistent Context**: BMO remembers the last 4-6 conversation exchanges
- **Mood Tracking**: BMO's responses affect his mood (happy, excited, caring, curious)
- **Smart Forgetting**: Old conversations are automatically pruned to save memory
- **Reset Option**: You can clear BMO's memory anytime

### Testing Memory:
```bash
# 1. Tell BMO your name
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "My name is Alice!"}'

# 2. Ask BMO your name
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is my name?"}'
```

## Testing & Development

### Run Memory Tests:
```bash
python test_bmo_memory.py
```

### Run Full Test Suite:
```bash
python test_bmo_client.py
```

### Interactive Testing:
Visit `http://localhost:8000/docs` for Swagger UI documentation and interactive testing.

## ⚡ Performance Optimization

### Apple M1/M2 Users:
- BMO automatically detects Apple Silicon and enables Metal acceleration
- Uses optimized settings for GPU layers and batch processing
- Recommended: 8GB+ RAM for best performance

### Low Memory Systems:
- Use Q3_K_M model (3GB) instead of Q4_K_M (4GB)
- Close other applications to free RAM
- BMO includes automatic memory management

### Performance Tips:
- **Faster responses**: Use smaller `max_tokens` (50-100)
- **Better quality**: Use higher `temperature` (0.8-1.0)
- **Memory efficient**: Keep conversations shorter

## Troubleshooting

### BMO Won't Start:
```bash
# Check if model file exists
ls -la models/

# Check system memory
python -c "import psutil; print(f'Available RAM: {psutil.virtual_memory().available/1024**3:.1f}GB')"

# Check logs for detailed error info
python startup.py
```

### Slow Responses:
- Try Q3_K_M model for better speed
- Reduce `max_tokens` to 50-100
- Close other applications
- Restart your system to clear memory

### Memory Issues:
- BMO's memory resets when server restarts
- Use `/chat/reset` to clear memory manually
- Check `conversation_length` in responses to verify memory is working

## Configuration

### Environment Variables:
Create a `.env` file:
```env
BMO_MODEL_PATH=models/mistral-7b-v0.1.Q4_K_M.gguf
BMO_MAX_TOKENS=200
BMO_TEMPERATURE=0.8
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

## Example Usage Scenarios

### Basic Chat:
```python
import requests

response = requests.post("http://localhost:8000/chat/", json={
    "prompt": "Hi BMO!"
})
print(response.json()["response"])
```

### Teaching BMO:
```python
# Tell BMO about yourself
requests.post("http://localhost:8000/chat/", json={
    "prompt": "I love playing guitar and my favorite color is blue."
})

# Ask BMO to remember
response = requests.post("http://localhost:8000/chat/", json={
    "prompt": "What do you know about me?"
})
```

### Creative Conversation:
```python
# High creativity for storytelling
response = requests.post("http://localhost:8000/chat/", json={
    "prompt": "Tell me an adventure story!",
    "temperature": 1.2,
    "max_tokens": 200
})
```

## BMO Character Guide

BMO responds authentically to Adventure Time themes:
- **Games & Music**: BMO loves talking about games and making music
- **Finn & Jake**: References the main characters naturally
- **Mathematical!**: Uses signature Adventure Time expressions
- **Innocent & Helpful**: Maintains BMO's childlike wonder and helpfulness

## API Rate Limits

Currently no rate limits are enforced, but for production use consider:
- Max 60 requests per minute per IP
- Max conversation length of 50 exchanges
- Automatic memory cleanup after 1 hour of inactivity

---
