import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger

from config import CORS_ORIGINS
from knowledge_base.builder import build_all
from feedback.store import init_db
from api.routes import simplify, feedback, history, health, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up MTCS v2.0...")
    
    # a) Build FAISS indices if not exist
    build_all()
    
    # b) Pre-load all models into module-level singletons
    logger.info("Pre-loading models...")
    # This will instantiate the singletons
    simplify.get_pipeline_components()
    logger.info("Models loaded.")
    
    # c) Initialize SQLite DB
    await init_db()
    
    yield
    logger.info("Shutting down MTCS v2.0...")

app = FastAPI(title="MTCS v2.0 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(simplify.router, prefix="/api", tags=["Simplify"])
app.include_router(feedback.router, prefix="/api", tags=["Feedback"])
app.include_router(history.router, prefix="/api", tags=["History"])
app.include_router(health.router, prefix="/api", tags=["Health"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
