import os
import httpx
import re
from config import SUPPORTED_LANGUAGES

class TechnicalSimplifier:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def simplify(self, query: str, context_passages: list, target_language: str, domain: str) -> dict:
        joined_passages = "\n".join([p["text"] for p in context_passages])
        
        full_language_name = SUPPORTED_LANGUAGES.get(target_language, target_language)
        
        prompt = f"""You are an expert technical educator. Your goal is to explain the requested concept in the simplest terms possible.
CRITICAL INSTRUCTION: First, try to answer the TASK using the retrieved CONTEXT. If the CONTEXT does not contain enough information to fully explain the concept, COMPLETELY IGNORE the CONTEXT and use your own general knowledge to provide a high-quality explanation. Do not mention that the context was missing, just provide the best explanation you can.

Explain the concept as if you are talking to a 5-year-old (ELI5). Use extremely simple, everyday language. Avoid ALL jargon, complex terminology, and academic phrasing.

CONTEXT:
{joined_passages}

TASK: Explain "{query}" for a student with no prior background. You MUST respond entirely in {full_language_name}.

You MUST output a valid JSON object with the exact following keys. DO NOT translate the keys themselves, only their values:
{{
  "explanation": "2-3 sentence plain explanation",
  "key_terms": [
    {{"term": "important term", "definition": "1-line definition"}}
  ],
  "analogy": "a real-world analogy or example that makes this intuitive",
  "summary": "one-line TL;DR",
  "used_llama_knowledge": true_if_you_ignored_the_context_and_used_your_own_knowledge_otherwise_false
}}
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 800,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = httpx.post(self.url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            output = response.json()["choices"][0]["message"]["content"]
            return self._parse_output(output)
        except Exception as e:
            return {
                "explanation": f"Generation failed: {str(e)}",
                "key_terms": [],
                "analogy": "Generation failed to produce analogy.",
                "summary": "Generation failed to produce summary."
            }

    def _parse_output(self, text: str) -> dict:
        import json
        try:
            result = json.loads(text)
            
            # Ensure all required keys exist
            return {
                "explanation": result.get("explanation", "Generation failed to produce explanation."),
                "key_terms": result.get("key_terms", []),
                "analogy": result.get("analogy", "Generation failed to produce analogy."),
                "summary": result.get("summary", "Generation failed to produce summary."),
                "used_llama_knowledge": result.get("used_llama_knowledge", False)
            }
        except json.JSONDecodeError:
            return {
                "explanation": text,
                "key_terms": [],
                "analogy": "Generation failed to produce analogy.",
                "summary": "Generation failed to produce summary."
            }
