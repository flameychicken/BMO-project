from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The user's message to BMO")
    max_tokens: Optional[int] = Field(default=150, ge=1, le=500, description="Maximum tokens for BMO's response")
    temperature: Optional[float] = Field(default=0.8, ge=0.0, le=1.5, description="BMO's creativity level")
    reset_conversation: Optional[bool] = Field(default=False, description="Reset BMO's memory")

class ChatResponse(BaseModel):
    response: str = Field(..., description="BMO's response")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    conversation_length: Optional[int] = Field(None, description="Number of exchanges in current conversation")
    bmo_mood: Optional[str] = Field(default="happy", description="BMO's current mood")

class ConversationHistory(BaseModel):
    user_message: str
    bmo_response: str
    timestamp: str
