import os
import pickle
from loguru import logger
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from config import INDICES_DIR, EMBEDDING_MODEL
from knowledge_base import cs_corpus, bio_corpus, physics_corpus, math_corpus

DOMAINS_MAP = {
    "computer_science": cs_corpus,
    "biology": bio_corpus,
    "physics": physics_corpus,
    "mathematics": math_corpus
}

def build_all():
    logger.info("Building knowledge base indices. This may take 2-3 minutes...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'}
    )
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=60
    )
    
    for domain, corpus_module in DOMAINS_MAP.items():
        index_path = INDICES_DIR / f"{domain}.index"
        bm25_path = INDICES_DIR / f"{domain}_bm25.pkl"
        
        if (INDICES_DIR / f"{domain}.faiss").exists() and bm25_path.exists():
            logger.info(f"Indices for {domain} already exist. Skipping.")
            continue
            
        logger.info(f"Building index for {domain}...")
        raw_docs = corpus_module.get_documents()
        chunks = text_splitter.split_text("\n\n".join(raw_docs))
        
        # FAISS index creation
        vectorstore = FAISS.from_texts(chunks, embeddings)
        
        # Save FAISS index
        vectorstore.save_local(str(INDICES_DIR), index_name=domain)
        
        # BM25 index creation
        tokenized_chunks = [chunk.lower().split() for chunk in chunks]
        bm25 = BM25Okapi(tokenized_chunks)
        
        # Save BM25 and chunks
        with open(bm25_path, 'wb') as f:
            pickle.dump({'bm25': bm25, 'chunks': chunks}, f)
            
        logger.info(f"Successfully saved FAISS and BM25 indices for {domain}.")

def load_index(domain):
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'}
    )
    try:
        return FAISS.load_local(
            str(INDICES_DIR), 
            embeddings, 
            index_name=domain,
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        logger.error(f"Failed to load index for {domain}: {e}")
        return None

def load_bm25(domain):
    bm25_path = INDICES_DIR / f"{domain}_bm25.pkl"
    if not bm25_path.exists():
        return None
    try:
        with open(bm25_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logger.error(f"Failed to load BM25 for {domain}: {e}")
        return None

if __name__ == "__main__":
    build_all()
