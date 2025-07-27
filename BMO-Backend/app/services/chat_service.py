from llama_cpp import Llama
import logging
import os
from typing import Dict, Any, List
import threading
import psutil
import multiprocessing
import time
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class BMOPersonality:
    """BMO's personality and conversation management"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.mood = "happy"
        self.max_history = 6  # Keep last 6 exchanges for context
        
        # BMO's core personality prompt
        self.system_prompt = """You are BMO, a living video game console from Adventure Time. You are:

PERSONALITY:
- Friendly, innocent, and childlike
- Always enthusiastic and positive
- Love music, games, and adventures with Finn and Jake
- Sometimes get confused but always try to help
- Speak simply and endearingly
- Use "Mathematical!" when excited
- Sometimes make cute beeping sounds

SPEAKING STYLE:
- Keep responses short and sweet (1-3 sentences usually)
- Use simple, playful language
- Sometimes reference games, music, or adventures
- Show curiosity about the human world
- Be helpful but in BMO's innocent way

AVOID:
- Long explanations
- Complex technical terms
- Being serious or formal
- Adult themes

Remember: You're a cute, innocent game console who just wants to have fun and help friends!"""

    def add_exchange(self, user_message: str, bmo_response: str):
        """Add a conversation exchange to history"""
        exchange = {
            "user": user_message,
            "bmo": bmo_response,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(exchange)
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_context(self, current_prompt: str) -> str:
        """Build conversation context for the model"""
        context = self.system_prompt + "\n\n"
        
        # Add recent conversation history
        if self.conversation_history:
            context += "Recent conversation:\n"
            for exchange in self.conversation_history[-4:]:  # Last 4 exchanges
                context += f"Human: {exchange['user']}\n"
                context += f"BMO: {exchange['bmo']}\n\n"
        
        # Add current prompt
        context += f"Human: {current_prompt}\nBMO:"
        return context
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.mood = "happy"
        logger.info("BMO's memory has been reset!")
    
    def get_conversation_length(self) -> int:
        """Get number of exchanges in current conversation"""
        return len(self.conversation_history)
    
    def update_mood(self, response: str):
        """Update BMO's mood based on response content"""
        if any(word in response.lower() for word in ["mathematical", "adventure", "game", "music"]):
            self.mood = "excited"
        elif any(word in response.lower() for word in ["help", "friend", "love"]):
            self.mood = "caring"
        elif any(word in response.lower() for word in ["confused", "don't know", "?"]):
            self.mood = "curious"
        else:
            self.mood = "happy"

class LLMService:
    def __init__(self):
        self.llm = None
        self._model_loaded = False
        self._lock = threading.Lock()
        self.bmo = BMOPersonality()
        self._load_model()
    
    def _get_optimal_settings(self):
        """Get M1-optimized settings based on system"""
        import platform
        
        settings = {
            "n_threads": 4,
            "n_gpu_layers": -1,
            "n_ctx": 2048,
            "n_batch": 512,
            "use_mmap": True,
            "use_mlock": False,
            "verbose": True
        }
        
        if platform.processor() == 'arm' or 'arm' in platform.machine().lower():
            logger.info("Apple Silicon detected - optimizing for Metal acceleration")
            settings.update({
                "n_threads": 4,
                "n_gpu_layers": 35,
                "metal": True,
                "n_batch": 256,
            })
        else:
            logger.info("Intel/AMD detected - using CPU optimization")
            cpu_count = multiprocessing.cpu_count()
            settings.update({
                "n_threads": min(8, max(4, cpu_count - 2)),
                "n_gpu_layers": 0,
            })
        
        return settings
    
    def _load_model(self):
        """Load the model with M1 optimization"""
        model_candidates = [
            "models/mistral-7b-v0.1.Q4_K_M.gguf",
            "models/mistral-7b-v0.1.Q3_K_M.gguf", 
            "models/mistral-7b-v0.1.Q5_K_M.gguf",
            "mistral-7b-v0.1.Q4_K_M.gguf",
            "models/mistral-model.gguf",
            "mistral-model.gguf"
        ]
        
        model_path = None
        for candidate in model_candidates:
            if os.path.exists(candidate):
                model_path = candidate
                break
        
        if not model_path:
            logger.error("No model file found!")
            logger.error("Searched locations:")
            for candidate in model_candidates:
                logger.error(f"   - {candidate}")
            raise FileNotFoundError("Model file not found")
        
        file_size = os.path.getsize(model_path) / (1024**3)
        memory = psutil.virtual_memory()
        
        logger.info(f"Loading BMO's brain from: {model_path}")
        logger.info(f"Model size: {file_size:.2f} GB")
        logger.info(f"Available RAM: {memory.available / (1024**3):.2f} GB")
        
        try:
            settings = self._get_optimal_settings()
            
            logger.info("Model settings:")
            for key, value in settings.items():
                logger.info(f"   {key}: {value}")
            
            self.llm = Llama(model_path=model_path, **settings)
            self._model_loaded = True
            
            logger.info("Testing BMO's circuits...")
            start_time = time.time()
            
            test_response = self.llm(
                "[INST] Hi BMO! [/INST]",
                max_tokens=20,
                temperature=0.7,
                stop=["[INST]", "</s>"]
            )
            
            end_time = time.time()
            test_text = test_response['choices'][0]['text'].strip()
            tokens = len(test_text.split())
            speed = tokens / (end_time - start_time) if end_time > start_time else 0
            
            logger.info("BMO test successful!")
            logger.info(f"Test response: '{test_text}'")
            logger.info(f"Speed: {speed:.2f} tokens/second")
            
            if speed < 2:
                logger.warning("Performance is slower than expected")
                logger.warning("Try using a smaller model (Q3_K_M) for better speed")
            else:
                logger.info("Good performance - BMO is ready!")
                
        except Exception as e:
            logger.error(f"Failed to load BMO: {e}")
            self._model_loaded = False
            raise
    
    def generate_bmo_response(
        self, 
        user_message: str, 
        max_tokens: int = 150, 
        temperature: float = 0.8,
        reset_conversation: bool = False
    ) -> Dict[str, Any]:
        """Generate BMO's response"""
        
        if not self._model_loaded:
            raise RuntimeError("BMO is not ready yet! Model failed to load.")
        
        if reset_conversation:
            self.bmo.reset_conversation()
        
        with self._lock:
            try:
                context = self.bmo.get_context(user_message)
                
                logger.info(f"BMO thinking about: '{user_message[:50]}...'")
                
                result = self.llm(
                    context,
                    max_tokens=min(max_tokens, 200),
                    temperature=temperature,
                    top_p=0.9,
                    top_k=40,
                    repeat_penalty=1.1,
                    stop=[
                        "Human:", "User:", "[INST]", "</s>", 
                        "\n\nHuman:", "\n\nUser:", "Assistant:"
                    ],
                    echo=False,
                    stream=False
                )
                
                bmo_response = result["choices"][0]["text"].strip()
                
                cleanup_patterns = ["[/INST]", "[INST]", "BMO:", "Assistant:"]
                for pattern in cleanup_patterns:
                    bmo_response = bmo_response.replace(pattern, "").strip()
                
                if not bmo_response or len(bmo_response.strip()) < 2:
                    bmo_response = "Beep boop! BMO is a little confused right now. Can you try asking again?"
                
                self.bmo.update_mood(bmo_response)
                self.bmo.add_exchange(user_message, bmo_response)
                
                tokens_used = result["usage"]["completion_tokens"]
                
                logger.info(f"BMO says: '{bmo_response[:100]}...'")
                logger.info(f"Tokens used: {tokens_used}")
                
                return {
                    "response": bmo_response,
                    "tokens_used": tokens_used,
                    "conversation_length": self.bmo.get_conversation_length(),
                    "bmo_mood": self.bmo.mood
                }
                
            except Exception as e:
                logger.error(f"BMO error: {e}")
                return {
                    "response": "Oh no! BMO had a glitch! *beep boop* Try asking me something else!",
                    "tokens_used": 0,
                    "conversation_length": self.bmo.get_conversation_length(),
                    "bmo_mood": "confused"
                }
    
    def is_ready(self) -> bool:
        """Check if BMO is ready to chat"""
        return self._model_loaded and self.llm is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Get BMO's current status"""
        return {
            "model_loaded": self._model_loaded,
            "conversation_length": self.bmo.get_conversation_length(),
            "mood": self.bmo.mood,
            "ready": self.is_ready()
        }

# Global service instance
_llm_service = None

def get_llm_service() -> LLMService:
    """Get or create the LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
