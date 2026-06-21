from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from config import RERANKER_MODEL, RERANK_TOP_K

class CrossEncoderReranker:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(RERANKER_MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(RERANKER_MODEL)
        self.model.eval()

    def rerank(self, query: str, passages: list, top_k: int = RERANK_TOP_K) -> list:
        if not passages:
            return []
            
        texts = [p["text"] for p in passages]
        pairs = [[query, text] for text in texts]
        
        with torch.no_grad():
            inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
            scores = self.model(**inputs).logits.squeeze(-1)
            
        if scores.dim() == 0:
            scores = [scores.item()]
        else:
            scores = scores.tolist()
            
        # Combine texts with scores
        scored_passages = [{"text": text, "rerank_score": score} for text, score in zip(texts, scores)]
        
        # Sort descending
        scored_passages.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        return scored_passages[:top_k]
