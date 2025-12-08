"""
Simple test script to verify the chatbot is working
"""

import asyncio
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.translation_service import translation_service


async def test_llm():
    """Test LLM service."""
    print("\n" + "="*60)
    print("Testing LLM Service")
    print("="*60)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is document forgery?"}
    ]
    
    response = await llm_service.generate_response(messages)
    print(f"Response: {response[:200]}...")


def test_rag():
    """Test RAG service."""
    print("\n" + "="*60)
    print("Testing RAG Service")
    print("="*60)
    
    query = "How to detect forged degrees?"
    context = rag_service.get_context_for_query(query)
    print(f"Query: {query}")
    print(f"Context found: {len(context)} characters")
    print(f"Preview: {context[:200]}...")


async def test_translation():
    """Test translation service."""
    print("\n" + "="*60)
    print("Testing Translation Service")
    print("="*60)
    
    text = "How to verify educational documents?"
    result = await translation_service.translate(text, target_lang="hi")
    print(f"Original: {text}")
    print(f"Detected Language: {result['source_lang']}")


async def main():
    """Run all tests."""
    print("🧪 Satyasetu Chatbot - Component Tests")
    
    try:
        test_rag()
        await test_translation()
        await test_llm()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
