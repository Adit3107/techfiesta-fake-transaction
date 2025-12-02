"""
Analysis router for transaction anomaly detection.

Exposes the /api/analyze endpoint that accepts CSV uploads.
"""

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from services.ml_engine import analyze_transactions, CSVParseError, ValidationError
from models import AnalysisResult

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_endpoint(file: UploadFile = File(...)):
    """
    Analyze uploaded transaction CSV file for anomalies.
    
    Accepts a CSV file with transaction data and returns:
        - Summary statistics (total transactions, volume, avg amount)
        - Time series data for visualization
        - List of detected anomalies with risk scores
    
    Expected CSV format:
        transaction_id,user_id,amount,timestamp,city
        T001,U001,500.00,2024-01-15T10:30:00,Mumbai
        T002,U002,75000.00,2024-01-15T10:35:00,Delhi
        ...
    
    Returns:
        AnalysisResult with summary, time_series, and anomalies
        
    Raises:
        HTTPException 400: If file is not a CSV or processing fails
        
    ML team: The API contract will remain stable. Update the backend logic 
    in services/ml_engine.py - this endpoint just passes data through.
    """
    logger.info(f"Received file: {file.filename}, content_type: {file.content_type}")
    
    if file.filename and not file.filename.lower().endswith('.csv'):
        logger.warning(f"Non-CSV file extension: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Please upload a CSV file. Received: {file.filename}"
        )
    
    try:
        contents = await file.read()
        logger.info(f"Read {len(contents)} bytes from uploaded file")
        
        if len(contents) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty file received. Please upload a CSV file with transaction data."
            )
        
        result = analyze_transactions(contents)
        
        logger.info(f"Analysis complete. Found {result.summary.anomaly_count} anomalies in {result.summary.total_transactions} transactions")
        
        return result
    
    except CSVParseError as e:
        logger.error(f"CSV parsing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error processing file: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred while processing the file."
        )
