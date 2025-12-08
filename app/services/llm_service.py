from groq import Groq
from typing import List, Dict, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with Groq LLM (Free tier)."""
    
    def __init__(self):
        if not settings.GROQ_API_KEY:
            logger.warning("GROQ_API_KEY not set. LLM functionality will be limited.")
            self.client = None
        else:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False
    ) -> str:
        """Generate response from LLM."""
        if not self.client:
            return "LLM service is not configured. Please set GROQ_API_KEY."
        
        try:
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            
            if stream:
                return response
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return f"Error: Unable to generate response. {str(e)}"
    
    def create_system_prompt(self, context: str, language: str = "en") -> str:
        """Create system prompt with RAG context."""
        if language == "hi":
            return f"""आप सत्यसेतु (Satyasetu) के लिए एक सहायक AI हैं, जो शैक्षिक दस्तावेज़ जालसाजी पहचान प्रणाली है।
आपका काम है उपयोगकर्ताओं को शैक्षिक दस्तावेज़ों (डिग्री, मार्कशीट, प्रमाणपत्र) में जालसाजी का पता लगाने में मदद करना।

संदर्भ जानकारी:
{context}

कृपया:
1. सटीक और मददगार जवाब दें
2. दस्तावेज़ सत्यापन के बारे में तकनीकी विवरण प्रदान करें
3. यदि आप सुनिश्चित नहीं हैं, तो स्पष्ट रूप से बताएं
4. विभिन्न विश्वविद्यालयों की सत्यापन प्रक्रियाओं के बारे में जानकारी दें"""
        
        return f"""You are a helpful AI assistant for Satyasetu, an educational document forgery detection system.
Your role is to help users identify forgery in educational documents (degrees, marksheets, certificates).

Context Information:
{context}

Please:
1. Provide accurate and helpful responses
2. Give technical details about document verification
3. If you're unsure, clearly state it
4. Share information about different university verification processes"""


# Singleton instance
llm_service = LLMService()
