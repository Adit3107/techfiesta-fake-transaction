"""
CSV parsing utilities for transaction data.

ML team: Extend this module for additional parsing/preprocessing logic.
"""

import logging
from io import BytesIO
from typing import Optional
import pandas as pd

logger = logging.getLogger(__name__)


def parse_csv(file_bytes: bytes) -> Optional[pd.DataFrame]:
    """
    Parse CSV file bytes into a pandas DataFrame.
    
    Expected CSV columns:
        - transaction_id: str
        - user_id: str
        - amount: float
        - timestamp: str (ISO format preferred)
        - city: str
    
    Args:
        file_bytes: Raw bytes from uploaded CSV file
        
    Returns:
        DataFrame if parsing succeeds, None if parsing fails
        
    ML team: Add data validation, type coercion, or preprocessing here.
    For example:
        - Convert timestamps to datetime
        - Normalize city names
        - Handle missing values
        - Feature engineering
    """
    try:
        buf = BytesIO(file_bytes)
        df = pd.read_csv(buf)
        
        logger.info(f"Successfully parsed CSV with {len(df)} rows and {len(df.columns)} columns")
        logger.debug(f"Columns found: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        logger.error(f"Failed to parse CSV: {str(e)}")
        return None


def validate_dataframe(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate that the DataFrame has required columns.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Tuple of (is_valid, list_of_missing_columns)
        
    ML team: Add additional validation rules here.
    """
    required_columns = ["transaction_id", "user_id", "amount", "timestamp", "city"]
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        logger.warning(f"Missing required columns: {missing}")
        return False, missing
    
    logger.info("DataFrame validation passed")
    return True, []
