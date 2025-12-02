"""
ML Engine for Transaction Anomaly Detection.

=============================================================================
                    ML TEAM: THIS IS YOUR MAIN FILE
=============================================================================

Replace the placeholder logic in `analyze_transactions()` with your real ML pipeline.

Suggested improvements:
    1. Amount anomaly detection (z-score, IQR, Isolation Forest)
    2. Frequency analysis (transaction velocity per user)
    3. Location-based anomaly detection (impossible travel, unusual cities)
    4. Time-based patterns (unusual hours, weekends)
    5. User behavior profiling (deviation from normal patterns)
    6. ML models: IsolationForest, LocalOutlierFactor, Autoencoders

The API contract (AnalysisResult) will stay the same - just update the logic here.
=============================================================================
"""

import logging
import random
from datetime import datetime, timedelta
from io import BytesIO
from typing import Optional

import pandas as pd

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from models import AnalysisResult, Summary, TimePoint, Anomaly
from utils.parser import parse_csv, validate_dataframe

logger = logging.getLogger(__name__)


class CSVParseError(Exception):
    """Raised when CSV parsing fails."""
    pass


class ValidationError(Exception):
    """Raised when data validation fails."""
    pass


def analyze_transactions(file_bytes: bytes) -> AnalysisResult:
    """
    Main entry point for transaction analysis.
    
    This function receives raw CSV bytes and returns a complete analysis.
    
    Args:
        file_bytes: Raw bytes from the uploaded CSV file
        
    Returns:
        AnalysisResult containing summary stats, time series, and anomalies
        
    Raises:
        CSVParseError: If the file cannot be parsed as CSV
        ValidationError: If required columns are missing
        
    ML Team TODO:
        1. Replace dummy anomaly detection with real algorithms
        2. Implement proper risk scoring (currently random 70-99)
        3. Add meaningful reasons based on actual detection logic
        4. Generate real time series from transaction timestamps
    """
    logger.info("Starting transaction analysis...")
    
    if not file_bytes or len(file_bytes) == 0:
        logger.error("Empty file received")
        raise CSVParseError("Empty file received. Please upload a valid CSV file.")
    
    df = parse_csv(file_bytes)
    
    if df is None:
        logger.error("Failed to parse CSV file")
        raise CSVParseError("Failed to parse file as CSV. Please ensure the file is a valid CSV format.")
    
    if df.empty:
        logger.error("CSV file is empty (no data rows)")
        raise CSVParseError("CSV file contains no data rows. Please upload a CSV with transaction data.")
    
    is_valid, missing_cols = validate_dataframe(df)
    if not is_valid:
        logger.error(f"Validation failed, missing columns: {missing_cols}")
        raise ValidationError(f"Missing required columns: {', '.join(missing_cols)}. Expected columns: transaction_id, user_id, amount, timestamp, city")
    
    summary = _compute_summary(df)
    logger.debug(f"Computed summary: {summary}")
    
    anomalies = _detect_anomalies(df)
    logger.info(f"Detected {len(anomalies)} anomalies")
    
    time_series = _generate_time_series(df, anomalies)
    
    summary.anomaly_count = len(anomalies)
    summary.anomaly_percentage = (len(anomalies) / summary.total_transactions) * 100 if summary.total_transactions > 0 else 0.0
    
    logger.info("Analysis complete")
    
    return AnalysisResult(
        summary=summary,
        time_series=time_series,
        anomalies=anomalies
    )




def _compute_summary(df: pd.DataFrame) -> Summary:
    """
    Compute aggregate statistics from the transaction data.
    
    ML team: Add more metrics here as needed.
    For example: median, std, unique users, unique cities, etc.
    """
    total_tx = len(df)
    
    if "amount" in df.columns:
        total_vol = float(df["amount"].sum())
        avg_amount = float(df["amount"].mean())
    else:
        total_vol = 0.0
        avg_amount = 0.0
    
    most_active_user = None
    if "user_id" in df.columns:
        user_counts = df["user_id"].value_counts()
        if not user_counts.empty:
            most_active_user = str(user_counts.index[0])
    
    return Summary(
        total_transactions=total_tx,
        total_volume=total_vol,
        avg_amount=avg_amount,
        anomaly_count=0,
        anomaly_percentage=0.0,
        most_active_user=most_active_user
    )


def _detect_anomalies(df: pd.DataFrame) -> list[Anomaly]:
    """
    Detect anomalous transactions.
    """
    anomalies = []
    
    # Simple rule-based detection for demonstration
    # 1. High amount (> 50000)
    # 2. Random check for others
    
    for index, row in df.iterrows():
        is_anomaly = False
        reasons = []
        risk_score = 0.0
        
        amount = float(row.get("amount", 0))
        
        if amount > 50000:
            is_anomaly = True
            reasons.append("High transaction amount")
            risk_score = random.uniform(80, 99)
        elif random.random() < 0.05:  # 5% random chance for demo
            is_anomaly = True
            reasons.append("Unusual transaction pattern")
            risk_score = random.uniform(60, 80)
            
        if is_anomaly:
            anomalies.append(
                Anomaly(
                    transaction_id=str(row.get("transaction_id", f"T{index}")),
                    user_id=str(row.get("user_id", "unknown")),
                    amount=amount,
                    timestamp=str(row.get("timestamp", datetime.utcnow().isoformat())),
                    city=str(row.get("city", "Unknown")),
                    risk_score=round(risk_score, 2),
                    reasons=reasons
                )
            )
            
    # Sort by risk score descending
    anomalies.sort(key=lambda x: x.risk_score, reverse=True)
    
    return anomalies


def _generate_time_series(df: pd.DataFrame, anomalies: list[Anomaly]) -> list[TimePoint]:
    """
    Generate time-series data from actual dataframe.
    """
    try:
        # Ensure timestamp is datetime
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
        # Group by 5 minutes for better granularity
        df['bucket'] = df['timestamp'].dt.floor('5min')
        
        grouped = df.groupby('bucket').agg({
            'amount': ['sum', 'count'],
            'transaction_id': 'count' # Just to get count
        }).reset_index()
        
        # Flatten columns
        grouped.columns = ['bucket', 'total_amount', 'transaction_count', 'count_2']
        
        # Process anomalies for time series
        anomaly_counts = {}
        if anomalies:
            # Create a temporary dataframe for anomalies to group them
            # Use model_dump() for Pydantic v2, or dict() for v1
            try:
                anomaly_data = [a.model_dump() for a in anomalies]
            except AttributeError:
                anomaly_data = [a.dict() for a in anomalies]
                
            if anomaly_data:
                a_df = pd.DataFrame(anomaly_data)
                if 'timestamp' in a_df.columns:
                    a_df['timestamp'] = pd.to_datetime(a_df['timestamp'])
                    a_df['bucket'] = a_df['timestamp'].dt.floor('5min')
                    anomaly_counts = a_df.groupby('bucket').size().to_dict()
        
        time_series = []
        for _, row in grouped.iterrows():
            bucket = row['bucket']
            time_series.append(
                TimePoint(
                    timestamp=bucket.isoformat(),
                    total_amount=float(row['total_amount']),
                    transaction_count=int(row['transaction_count']),
                    anomaly_count=anomaly_counts.get(bucket, 0)
                )
            )
            
        return time_series
        
    except Exception as e:
        logger.error(f"Error generating time series: {e}")
        # Fallback to dummy data if parsing fails
        now = datetime.utcnow()
        return [
            TimePoint(
                timestamp=(now - timedelta(minutes=i * 10)).isoformat(),
                total_amount=1000.0,
                transaction_count=10,
                anomaly_count=0
            ) for i in range(5)
        ]
