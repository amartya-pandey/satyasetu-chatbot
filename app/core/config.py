from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Satyasetu Chatbot"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # Database (SQLite - embedded, no external service needed)
    DATABASE_URL: str = "sqlite:///./data/satyasetu.db"
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"  # Override with environment variable
    MONGODB_DB_NAME: str = "SatyaSetu"
    
    # Groq API (Free)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"  # Updated free tier model
    
    # ChromaDB
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Models
    TRANSLATION_MODEL: str = "ai4bharat/indictrans2-en-indic-dist-200M"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # RAG Settings
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 5
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
