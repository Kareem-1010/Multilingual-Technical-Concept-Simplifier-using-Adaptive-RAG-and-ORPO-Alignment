import os
import httpx
from loguru import logger

class HyDEGenerator:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, query: str, domain: str) -> str:
        prompt = f"Write a concise technical explanation for: {query} in the domain of {domain}. Keep it under 100 words."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 120
        }
        
        try:
            response = httpx.post(self.url, headers=headers, json=data, timeout=10.0)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"HyDE generation failed: {e}. Falling back to original query.")
            return query
