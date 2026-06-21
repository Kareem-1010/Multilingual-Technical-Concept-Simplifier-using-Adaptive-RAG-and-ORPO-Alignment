from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).parent
INDICES_DIR = BASE_DIR / "knowledge_base" / "indices"
INDICES_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = BASE_DIR / "feedback" / "mtcs_feedback.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Model identifiers (all free, CPU-compatible, HuggingFace public)
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
SIMPLIFIER_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
FAITHFULNESS_MODEL = "typeform/distilbert-base-uncased-mnli"
HYDE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

# RAG config
CHUNK_SIZE = 400
CHUNK_OVERLAP = 60
RETRIEVAL_TOP_K = 10
RERANK_TOP_K = 3

# Faithfulness threshold (0.0 to 1.0)
FAITHFULNESS_THRESHOLD = 0.45

# Supported languages (ISO 639-1 codes)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ar": "Arabic",
    "zh-cn": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean",
    "pt": "Portuguese",
}

# Supported domains
DOMAINS = ["computer_science", "biology", "physics", "mathematics"]

# CORS origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
