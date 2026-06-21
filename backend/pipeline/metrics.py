import textstat
import evaluate
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class MetricsEvaluator:
    def __init__(self):
        self.bleu = evaluate.load("sacrebleu")
        self.sari = evaluate.load("sari")
        self.rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        self.encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device='cpu')

    def evaluate(self, generated_text: str, reference_text: str = None) -> dict:
        # Always compute
        readability = textstat.flesch_reading_ease(generated_text)
        token_count = len(generated_text.split())
        sentence_count = textstat.sentence_count(generated_text)
        
        metrics = {
            "readability_score": readability,
            "token_count": token_count,
            "sentence_count": sentence_count
        }
        
        if reference_text:
            try:
                # Advanced RAG Metrics (Answer Relevance)
                query_emb = self.encoder.encode([reference_text])
                gen_emb = self.encoder.encode([generated_text])
                answer_relevance = float(cosine_similarity(query_emb, gen_emb)[0][0])
                metrics["answer_relevance"] = answer_relevance

                bleu_score = self.bleu.compute(predictions=[generated_text], references=[[reference_text]])
                metrics["bleu"] = bleu_score["score"]
                
                # SARI expects (sources, predictions, references)
                # Since we are just evaluating generated vs ref, we might just pass empty source or duplicate
                sari_score = self.sari.compute(sources=[reference_text], predictions=[generated_text], references=[[reference_text]])
                metrics["sari"] = sari_score["sari"]
                
                rouge_scores = self.rouge.score(reference_text, generated_text)
                metrics["rouge_l"] = rouge_scores['rougeL'].fmeasure
            except Exception as e:
                # Log or handle error if evaluation fails
                pass
                
        return metrics
