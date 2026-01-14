"""
Configuration module for EduBridge AI Tutor
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Ollama Settings
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    
    # Vector Store Settings
    BASE_DIR = Path(__file__).parent.parent
    VECTOR_STORE_PATH = os.getenv(
        "VECTOR_STORE_PATH", 
        str(BASE_DIR / "data" / "vectorstore")
    )
    
    # Chunking Settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Response Settings
    MAX_CONTEXT_DOCS = 3
    TEMPERATURE = 0.1  # Low temperature for factual responses
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        Path(cls.VECTOR_STORE_PATH).mkdir(parents=True, exist_ok=True)
