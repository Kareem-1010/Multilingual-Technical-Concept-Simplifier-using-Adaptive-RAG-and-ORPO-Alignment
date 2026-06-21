import numpy as np
from loguru import logger
from config import DOMAINS, RETRIEVAL_TOP_K
from knowledge_base.builder import load_index, load_bm25
from pipeline.embedder import TextEmbedder

class AdaptiveRetriever:
    def __init__(self):
        self.embedder = TextEmbedder()
        self.indices = {}
        self.bm25_indices = {}
        
        # Load all 4 FAISS and BM25 indices into memory
        for domain in DOMAINS:
            index = load_index(domain)
            bm25_data = load_bm25(domain)
            if index is not None:
                self.indices[domain] = index
            else:
                logger.warning(f"Index for {domain} not found during retriever initialization.")
            if bm25_data is not None:
                self.bm25_indices[domain] = bm25_data
            else:
                logger.warning(f"BM25 Index for {domain} not found.")

    def retrieve(self, query: str, hyde_doc: str, domain: str, top_k: int = RETRIEVAL_TOP_K) -> list:
        query_embedding = self.embedder.embed(query)
        hyde_embedding = self.embedder.embed(hyde_doc)
        
        # Average the query and HyDE embeddings
        avg_embedding = np.mean([query_embedding, hyde_embedding], axis=0)
        
        # Determine which index to search by normalizing the domain
        normalized_domain = domain.lower().replace(" ", "_")
        search_index = self.indices.get(normalized_domain)
        bm25_data = self.bm25_indices.get(normalized_domain)
        
        # Handle domain fallback
        if search_index is None:
            logger.warning(f"Index for {domain} ({normalized_domain}) not available. Searching all indices.")
            all_docs = []
            for d, idx in self.indices.items():
                docs = idx.similarity_search_with_score_by_vector(avg_embedding.tolist(), k=top_k)
                all_docs.extend(docs)
                
            all_docs.sort(key=lambda x: x[1])
            
            # Deduplicate by text content
            seen_texts = set()
            unique_docs = []
            for doc, score in all_docs:
                if doc.page_content not in seen_texts:
                    seen_texts.add(doc.page_content)
                    unique_docs.append({"text": doc.page_content, "score": float(score)})
                    
            return unique_docs[:top_k]

        # 1. Dense Retrieval (FAISS)
        dense_docs = search_index.similarity_search_with_score_by_vector(avg_embedding.tolist(), k=top_k*2)
        
        # 2. Sparse Retrieval (BM25)
        sparse_docs = []
        if bm25_data is not None:
            bm25 = bm25_data['bm25']
            chunks = bm25_data['chunks']
            tokenized_query = query.lower().split()
            bm25_scores = bm25.get_scores(tokenized_query)
            top_bm25_indices = np.argsort(bm25_scores)[::-1][:top_k*2]
            sparse_docs = [(chunks[i], bm25_scores[i]) for i in top_bm25_indices if bm25_scores[i] > 0]
            
        # 3. Reciprocal Rank Fusion (RRF)
        rrf_k = 60
        fused_scores = {}
        
        for rank, (doc, score) in enumerate(dense_docs):
            text = doc.page_content
            fused_scores[text] = fused_scores.get(text, 0.0) + 1.0 / (rrf_k + rank + 1)
            
        for rank, (text, score) in enumerate(sparse_docs):
            fused_scores[text] = fused_scores.get(text, 0.0) + 1.0 / (rrf_k + rank + 1)
            
        sorted_fused = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        top_fused = sorted_fused[:top_k]
        
        return [{"text": text, "score": float(score)} for text, score in top_fused]
