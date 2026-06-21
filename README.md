# Multilingual Technical Concept Simplifier (MTCS) v2.0

![MTCS v2.0 Architecture](https://via.placeholder.com/800x400.png?text=MTCS+v2.0+Architecture)

## 📖 Overview
MTCS v2.0 is a production-grade NLP Web Application designed to take complex technical concepts and explain them simply to students with no prior background. It dynamically routes queries to specific knowledge domains (Computer Science, Biology, Physics, Mathematics) and leverages CPU-optimized, free-tier HuggingFace models for language detection, retrieval-augmented generation (RAG), text simplification, and faithfulness verification.

The application is 100% open-source, runs fully locally, and requires no paid APIs or GPU infrastructure.

## 🏗️ Architecture

```text
┌──────────────────┐      HTTP/WS       ┌─────────────────────────────────┐
│   React Frontend │ ◄─────────────────► │     FastAPI Backend (Port 8000) │
│   (Port 3000)    │                     │                                 │
│  ┌────────────┐  │                     │  ┌──────────────────────────┐   │
│  │ Input UI   │  │                     │  │   NLP Preprocessing      │   │
│  │ Lang Sel.  │  │                     │  │   (spaCy + NLTK)         │   │
│  │ Domain Sel │  │                     │  └──────────┬───────────────┘   │
│  │ Output View│  │                     │             │                   │
│  │ Feedback   │  │                     │  ┌──────────▼───────────────┐   │
│  │ History    │  │                     │  │  Language Detection      │   │
│  └────────────┘  │                     │  │  Domain Router (4 areas) │   │
└──────────────────┘                     │  └──────────┬───────────────┘   │
                                         │             │                   │
                                         │  ┌──────────▼───────────────┐   │
                                         │  │   HyDE Layer (flan-t5)   │   │
                                         │  └──────────┬───────────────┘   │
                                         │             │                   │
                                         │  ┌──────────▼───────────────┐   │
                                         │  │   FAISS Vector Store     │   │
                                         │  │   Adaptive RAG Retrieval │   │
                                         │  └──────────┬───────────────┘   │
                                         │             │                   │
                                         │  ┌──────────▼───────────────┐   │
                                         │  │   Cross-Encoder Reranker │   │
                                         │  └──────────┬───────────────┘   │
                                         │             │                   │
                                         │  ┌──────────▼───────────────┐   │
                                         │  │   Simplification Engine  │   │
                                         │  │   flan-t5-base (CPU)     │   │
                                         │  └──────────┬───────────────┘   │
                                         │             │                   │
                                         │  ┌──────────▼───────────────┐   │
                                         │  │   Faithfulness Verifier  │   │
                                         │  │   Metrics Evaluator      │   │
                                         │  └──────────┬───────────────┘   │
                                         │             │                   │
                                         │  ┌──────────▼───────────────┐   │
                                         │  │   SQLite Feedback Store  │   │
                                         │  └──────────────────────────┘   │
                                         └─────────────────────────────────┘
```

## 🚀 Quick Start

Ensure you have Docker and Docker Compose installed.

```bash
git clone <your-repo-url>
cd mtcs-v2
make install
make run
```

Then visit:
- **Frontend**: `http://localhost:3000`
- **Backend API Docs**: `http://localhost:8000/docs`

> Note: On the first startup, the application will take 2-3 minutes to download models and build the FAISS indices.

## 📚 Supported Languages

| Code | Language |
|---|---|
| `en` | English |
| `hi` | Hindi |
| `fr` | French |
| `de` | German |
| `es` | Spanish |
| `ar` | Arabic |
| `zh-cn` | Chinese (Simplified) |
| `ja` | Japanese |
| `ko` | Korean |
| `pt` | Portuguese |

## 📊 Evaluation Metrics

MTCS uses advanced metrics to ensure quality and reliability:
- **Faithfulness Score**: Uses `distilbert-base-uncased-mnli` to check if the generated text is entailed by the retrieved source documents.
- **Readability**: Uses the Flesch Reading Ease score via the `textstat` library.
- **BLEU / ROUGE-L / SARI / BERTScore**: Available for comprehensive pipeline testing against reference texts.

## 🛠️ Developer Guide

### Adding New Domain Knowledge
1. Create a new corpus file in `backend/knowledge_base/` (e.g., `chemistry_corpus.py`).
2. Add a `get_documents()` function returning a list of technical strings.
3. Register the new domain in `backend/config.py` (`DOMAINS` list) and `backend/knowledge_base/builder.py` (`DOMAINS_MAP`).
4. Re-run the application; it will automatically build the new index.

### Exporting Preference Data (ORPO)
To export user preference pairs (high vs. low ratings) for model fine-tuning:
```python
from feedback.orpo_exporter import export_preference_pairs
dataset = export_preference_pairs()
# Check backend/feedback/orpo_dataset.json
```

## 🧪 API Reference

### `POST /api/simplify`
Simplifies a technical concept.
```json
{
  "query": "gradient descent",
  "target_language": "en",
  "domain_hint": "computer_science"
}
```

### `POST /api/feedback`
Submits user feedback for a generated response.
```json
{
  "session_id": "uuid",
  "query": "gradient descent",
  "domain": "computer_science",
  "language": "en",
  "explanation": "...",
  "rating": 5
}
```

### `GET /api/history`
Fetches recent user queries.

### `GET /api/health`
Checks system health, model load status, and index availability.
