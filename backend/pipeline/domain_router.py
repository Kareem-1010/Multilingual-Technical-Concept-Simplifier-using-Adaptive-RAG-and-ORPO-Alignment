import os
import httpx
from config import DOMAINS

class DomainRouter:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.valid_domains = ["computer_science", "biology", "physics", "mathematics"]

    def classify(self, text: str) -> dict:
        prompt = f"""You are an expert domain classifier. Categorize the following concept into a highly specific scientific, technical, or academic domain (e.g., Quantum Computing, Biochemistry, Machine Learning, Cognitive Psychology).

Concept: "{text}"

You MUST output a valid JSON object exactly like this:
{{
  "domain": "chosen_domain_name",
  "confidence": 0.95
}}
"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 100,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = httpx.post(self.url, headers=headers, json=data, timeout=10.0)
            response.raise_for_status()
            output = response.json()["choices"][0]["message"]["content"]
            
            import json
            result = json.loads(output)
            domain = result.get("domain", "General Knowledge").title()
                
            return {
                "domain": domain,
                "confidence": float(result.get("confidence", 1.0))
            }
        except Exception as e:
            return {
                "domain": "General Knowledge",
                "confidence": 0.5
            }
