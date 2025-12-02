"""
Fake Transaction Detector API

Main FastAPI application entry point.

Run with: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
"""

import logging
import sys

import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.analyze import router as analyze_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Fake Transaction Detector API",
    description="""
    API for detecting anomalous/fake transactions in financial data.
    
    ## Features
    - Upload CSV transaction files
    - Get summary statistics
    - Detect anomalies with risk scores
    - Time-series data for visualization
    
    ## For ML Team
    The detection logic is in `backend/services/ml_engine.py`.
    Replace the placeholder functions with real ML models.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        {"status": "ok"} if the service is running
    """
    logger.debug("Health check called")
    return {"status": "ok"}


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "Fake Transaction Detector API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "analyze": "/api/analyze (POST with CSV file)"
    }


app.include_router(analyze_router)


logger.info("Fake Transaction Detector API initialized")
