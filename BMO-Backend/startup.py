import uvicorn
import logging
import sys
import os
import time

# Set up BMO-themed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BMO-Server")

def check_model_exists():
    """Check if BMO's brain (model file) exists"""
    model_paths = [
        "models/mistral-7b-v0.1.Q4_K_M.gguf",
        "models/mistral-7b-v0.1.Q3_K_M.gguf", 
        "models/mistral-7b-v0.1.Q5_K_M.gguf",
        "mistral-7b-v0.1.Q4_K_M.gguf",
        "models/mistral-model.gguf",
        "mistral-model.gguf"
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            logger.info(f"Found BMO's brain at: {path}")
            return True
    
    logger.error("BMO's brain (model file) not found!")
    logger.error("BMO looked in these places:")
    for path in model_paths:
        logger.error(f"   - {path}")
    
    logger.error("\nTo give BMO a brain, download a Mistral model:")
    logger.error("mkdir -p models")
    logger.error("# For faster performance (3-4 GB):")
    logger.error("wget -O models/mistral-7b-v0.1.Q3_K_M.gguf https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.q3_k_m.gguf")
    logger.error("# For better quality (4-5 GB):")  
    logger.error("wget -O models/mistral-7b-v0.1.Q4_K_M.gguf https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.q4_k_m.gguf")
    
    return False

def print_bmo_banner():
    """Print BMO startup banner"""
    banner = """
    BMO CHAT SERVER
    =====================
    
         ┌─────────┐
         │ ● ▄ ● │
         │   ═   │  
         └─┬─────┘
           │
         Mathematical!
    
    Adventure Time Local Chat API
    Powered by Mistral 7B + Apple M1 Magic
    
    """
    print(banner)

if __name__ == "__main__":
    print_bmo_banner()
    
    logger.info("Starting BMO server...")
    
    # Check if BMO has a brain
    if not check_model_exists():
        logger.error("BMO can't start without a brain!")
        sys.exit(1)
    
    try:
        logger.info("BMO is waking up...")
        logger.info("Server will be available at: http://localhost:8000")
        logger.info("API docs at: http://localhost:8000/docs")
        logger.info("Chat endpoint: http://localhost:8000/chat/")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for better performance with large models
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("BMO is going to sleep... Goodbye!")
    except Exception as e:
        logger.error(f"BMO crashed: {e}")
        sys.exit(1)
