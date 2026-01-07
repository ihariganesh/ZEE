"""Configuration management for the AI Assistant."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the AI Assistant."""
    
    # Project paths
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / "logs"
    
    # ===== FREE API Keys =====
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Voice settings
    VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE", "en")
    SPEECH_RATE = int(os.getenv("SPEECH_RATE", "150"))
    USE_WHISPER = os.getenv("USE_WHISPER", "true").lower() == "true"
    
    # System control
    ENABLE_PHONE_CONTROL = os.getenv("ENABLE_PHONE_CONTROL", "false").lower() == "true"
    PHONE_IP_ADDRESS = os.getenv("PHONE_IP_ADDRESS", "")
    
    # Research settings
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    USE_OLLAMA_OFFLINE = os.getenv("USE_OLLAMA_OFFLINE", "true").lower() == "true"
    
    # Create necessary directories
    LOGS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        has_groq = bool(cls.GROQ_API_KEY)
        
        if not has_groq:
            print("⚠️  Warning: No Groq API key configured.")
            print("   Get FREE API key from: https://console.groq.com")
            print("   Using Ollama (local) as fallback if available.")
        else:
            print("✅ Groq API configured")
        
        return True
