from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

class TextEmbedder:
    def __init__(self):
        # We load this once globally
        self.model = SentenceTransformer(EMBEDDING_MODEL, device='cpu')

    def embed(self, text: str):
        # Returns numpy array
        return self.model.encode(text)

    def embed_batch(self, texts: list):
        return self.model.encode(texts)
