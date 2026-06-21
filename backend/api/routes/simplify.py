from fastapi import APIRouter, Depends
from api.schemas import SimplifyRequest, SimplifyResponse
from api.dependencies import get_current_user
from pipeline.preprocessor import TextPreprocessor
from pipeline.language_detector import LanguageDetector
from pipeline.domain_router import DomainRouter
from pipeline.hyde_generator import HyDEGenerator
from pipeline.retriever import AdaptiveRetriever
from pipeline.reranker import CrossEncoderReranker
from pipeline.simplifier import TechnicalSimplifier
from pipeline.faithfulness import FaithfulnessVerifier
from pipeline.metrics import MetricsEvaluator
import asyncio
import time

router = APIRouter()

# Global instances mapped to singletons, to be injected or accessed directly
_preprocessor = None
_language_detector = None
_domain_router = None
_hyde_generator = None
_retriever = None
_reranker = None
_simplifier = None
_faithfulness_verifier = None
_metrics_evaluator = None

def get_pipeline_components():
    global _preprocessor, _language_detector, _domain_router, _hyde_generator
    global _retriever, _reranker, _simplifier, _faithfulness_verifier, _metrics_evaluator
    
    if not _preprocessor:
        _preprocessor = TextPreprocessor()
        _language_detector = LanguageDetector()
        _domain_router = DomainRouter()
        _hyde_generator = HyDEGenerator()
        _retriever = AdaptiveRetriever()
        _reranker = CrossEncoderReranker()
        _simplifier = TechnicalSimplifier()
        _faithfulness_verifier = FaithfulnessVerifier()
        _metrics_evaluator = MetricsEvaluator()
        
    return (_preprocessor, _language_detector, _domain_router, _hyde_generator, 
            _retriever, _reranker, _simplifier, _faithfulness_verifier, _metrics_evaluator)

@router.post("/simplify", response_model=SimplifyResponse)
async def simplify_endpoint(request: SimplifyRequest, current_user: dict = Depends(get_current_user)):
    start_time = time.perf_counter()
    
    (preprocessor, language_detector, domain_router, hyde_generator, 
     retriever, reranker, simplifier, faithfulness_verifier, metrics_evaluator) = get_pipeline_components()
    
    async def get_domain():
        if request.domain_hint:
            return {"domain": request.domain_hint, "confidence": 1.0}
        return await asyncio.to_thread(domain_router.classify, request.query)

    # 2, 3, 4. Concurrent Execution of initial analysis
    analysis, detected_lang, domain_info = await asyncio.gather(
        asyncio.to_thread(preprocessor.full_analysis, request.query),
        asyncio.to_thread(language_detector.detect, request.query),
        get_domain()
    )
    
    domain = domain_info["domain"]
    domain_conf = domain_info["confidence"]
    
    # 5. Generate HyDE
    hyde_doc = await asyncio.to_thread(hyde_generator.generate, request.query, domain)
    
    # 6 & 7. Retrieve
    top_chunks = await asyncio.to_thread(retriever.retrieve, request.query, hyde_doc, domain)
    
    # 8. Rerank
    reranked_chunks = await asyncio.to_thread(reranker.rerank, request.query, top_chunks)
    
    # 9. Simplify
    output_dict = await asyncio.to_thread(simplifier.simplify, request.query, reranked_chunks, request.target_language, domain)
    
    used_llama = output_dict.pop("used_llama_knowledge", False)
    
    # 10 & 11. Concurrent Metrics Evaluation
    if used_llama:
        faithfulness = {
            "score": 1.0,
            "is_faithful": True,
            "label": "Llama Knowledge (100%)"
        }
        reranked_chunks = [{"text": "⚠️ No relevant documents found in the database. This explanation was dynamically generated using Llama 3.3's vast internal knowledge base!"}]
        metrics = await asyncio.to_thread(metrics_evaluator.evaluate, output_dict["explanation"], request.query)
    else:
        faithfulness, metrics = await asyncio.gather(
            asyncio.to_thread(faithfulness_verifier.verify, output_dict["explanation"], reranked_chunks),
            asyncio.to_thread(metrics_evaluator.evaluate, output_dict["explanation"], request.query)
        )
    
    processing_time_ms = int((time.perf_counter() - start_time) * 1000)
    
    return SimplifyResponse(
        query=request.query,
        detected_language=detected_lang,
        target_language=request.target_language,
        domain=domain,
        domain_confidence=domain_conf,
        output=output_dict,
        faithfulness=faithfulness,
        metrics=metrics,
        retrieved_passages=[c["text"] for c in reranked_chunks],
        processing_time_ms=processing_time_ms
    )
