from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llama_cpp import Llama
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Simple LLM Chat API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

class ChatResponse(BaseModel):
    response: str

# Global variable for the model
llm = None

@app.on_event("startup")
async def load_model():
    """Load the model when the server starts"""
    global llm
    model_path = "models/mistral-model.gguf"
    
    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
        return
    
    try:
        logger.info("Loading Mistral model...")
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=2,  # Reduced threads for stability
            verbose=False,  # Disable verbose to reduce noise
            n_batch=512,
            use_mmap=True,
            use_mlock=False
        )
        logger.info("Model loaded successfully!")
        
        # Test the model
        test_response = llm("Test", max_tokens=5, stop=["</s>"])
        logger.info(f"Model test successful: {test_response}")
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        llm = None

@app.get("/")
async def root():
    return {"message": "Simple LLM API", "model_loaded": llm is not None}

@app.get("/health")
async def health():
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model": "loaded"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        logger.info(f"Processing request: {request.prompt[:50]}...")
        
        # Simple prompt format for Mistral 7B v0.1
        formatted_prompt = f"{request.prompt}"
        
        # Generate response
        result = llm(
            formatted_prompt,
            max_tokens=request.max_tokens,
            temperature=0.7,
            top_p=0.9,
            stop=["</s>"],
            echo=False
        )
        
        response_text = result["choices"][0]["text"].strip()
        logger.info(f"Generated response: {response_text[:100]}...")
        
        return ChatResponse(response=response_text)
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/test-direct")
async def test_direct(request: ChatRequest):
    """Direct test endpoint to see raw model output"""
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Try different prompt styles
        prompts_to_try = [
            request.prompt,
            f"Question: {request.prompt}\nAnswer:",
            f"Human: {request.prompt}\nAssistant:",
            f"### Instruction: {request.prompt}\n### Response:",
        ]
        
        results = []
        for i, prompt in enumerate(prompts_to_try):
            try:
                result = llm(prompt, max_tokens=50, temperature=0.7)
                results.append({
                    "format": i + 1,
                    "prompt": prompt,
                    "response": result["choices"][0]["text"].strip(),
                    "full_result": result
                })
            except Exception as e:
                results.append({
                    "format": i + 1,
                    "prompt": prompt,
                    "error": str(e)
                })
        
        return {"test_results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

