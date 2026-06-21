import torch
from transformers import pipeline
from loguru import logger
from config import FAITHFULNESS_MODEL, FAITHFULNESS_THRESHOLD

class FaithfulnessVerifier:
    def __init__(self):
        try:
            self.nli_model = pipeline(
                "text-classification",
                model=FAITHFULNESS_MODEL,
                device="cpu"
            )
        except Exception as e:
            logger.error(f"Failed to load NLI model: {e}")
            self.nli_model = None

    def verify(self, explanation: str, context_passages: list) -> dict:
        if not self.nli_model or not context_passages:
            return {
                "score": 0.5,
                "is_faithful": None,
                "label": "verification_failed"
            }
            
        scores = []
        try:
            for passage in context_passages:
                result = self.nli_model({"text": passage["text"], "text_pair": explanation})
                
                entailment_score = 0.0
                if result.get("label") == "ENTAILMENT":
                    entailment_score = result.get("score", 0.0)
                elif result.get("label") == "LABEL_2":
                    entailment_score = result.get("score", 0.0)
                    
                scores.append(entailment_score)
                
            avg_score = sum(scores) / len(scores) if scores else 0.0
            
            return {
                "score": float(avg_score),
                "is_faithful": avg_score >= FAITHFULNESS_THRESHOLD,
                "label": "faithful" if avg_score >= FAITHFULNESS_THRESHOLD else "unfaithful"
            }
        except Exception as e:
            logger.warning(f"Faithfulness verification failed: {e}")
            return {
                "score": 0.5,
                "is_faithful": None,
                "label": "verification_failed"
            }
