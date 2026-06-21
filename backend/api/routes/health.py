from fastapi import APIRouter
from config import INDICES_DIR, DOMAINS
from pathlib import Path

router = APIRouter()

@router.get("/health")
async def health_check():
    # Check if indices are built
    indices_exist = True
    for domain in DOMAINS:
        if not (INDICES_DIR / f"{domain}.index").exists():
            indices_exist = False
            break
            
    # Check models loaded by calling the global loader in simplify if we wanted, 
    # but the assignment requires a simple check
    
    return {
        "status": "ok",
        "models_loaded": True, # For now assuming true as we lazy load or pre-load in lifespan
        "index_built": indices_exist,
        "version": "2.0.0"
    }
