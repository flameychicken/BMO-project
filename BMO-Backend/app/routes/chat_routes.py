from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import get_llm_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_bmo(request: ChatRequest):
    """
    Chat with BMO!
    """
    try:
        logger.info(f"New chat request: '{request.prompt[:50]}...'")
        
        service = get_llm_service()
        if not service.is_ready():
            raise HTTPException(
                status_code=503, 
                detail="BMO is still starting up! Please wait a moment and try again. *beep boop*"
            )
        
        result = service.generate_bmo_response(
            user_message=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            reset_conversation=request.reset_conversation
        )
        
        response = ChatResponse(
            response=result["response"],
            tokens_used=result.get("tokens_used"),
            conversation_length=result.get("conversation_length"),
            bmo_mood=result.get("bmo_mood", "happy")
        )
        
        logger.info(f"BMO responded successfully (mood: {response.bmo_mood})")
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        
        # Return a BMO-style error message
        return ChatResponse(
            response="Oh no! BMO encountered a glitch! *sad beep* Please try again or ask Finn and Jake for help!",
            tokens_used=0,
            conversation_length=0,
            bmo_mood="confused"
        )

@router.get("/status")
async def bmo_status():
    """Check BMO's status"""
    try:
        service = get_llm_service()
        status = service.get_status()
        
        if not status["ready"]:
            return {
                "status": "loading",
                "message": "BMO is waking up! *beep boop beep*",
                "mood": "sleepy",
                "ready": False
            }
        
        # Test BMO with a simple message
        try:
            test_result = service.generate_bmo_response(
                "Hi BMO!", 
                max_tokens=20, 
                temperature=0.7
            )
            
            return {
                "status": "ready",
                "message": "BMO is ready for adventure! Mathematical!",
                "mood": status["mood"],
                "conversation_length": status["conversation_length"],
                "test_response": test_result["response"],
                "ready": True
            }
        except Exception as test_error:
            logger.error(f"BMO test failed: {test_error}")
            return {
                "status": "error",
                "message": f"BMO is having trouble: {str(test_error)}",
                "mood": "confused",
                "ready": False
            }
            
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return {
            "status": "error",
            "message": f"Cannot check BMO's status: {str(e)}",
            "mood": "broken",
            "ready": False
        }

@router.post("/reset")
async def reset_bmo_conversation():
    """Reset BMO's conversation memory"""
    try:
        service = get_llm_service()
        if service.is_ready():
            service.bmo.reset_conversation()
            return {
                "status": "success",
                "message": "BMO's memory has been refreshed! Ready for new adventures!",
                "mood": "happy"
            }
        else:
            raise HTTPException(status_code=503, detail="BMO is not ready")
    except Exception as e:
        logger.error(f"Reset failed: {e}")
        raise HTTPException(status_code=500, detail=f"Could not reset BMO: {str(e)}")
