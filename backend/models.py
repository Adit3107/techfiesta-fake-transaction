"""
Pydantic models for the Fake Transaction Detector API.

These models define the response schema for the /api/analyze endpoint.
ML team: You don't need to modify these unless you want to add new fields.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Anomaly(BaseModel):
    """
    Represents a single anomalous transaction.
    
    ML team: Add more fields here if your model detects additional attributes.
    For example: 'device_fingerprint', 'ip_address', 'transaction_type', etc.
    """
    transaction_id: str = Field(..., description="Unique transaction identifier")
    user_id: str = Field(..., description="User who made the transaction")
    amount: float = Field(..., description="Transaction amount in currency")
    timestamp: str = Field(..., description="ISO format timestamp of transaction")
    city: str = Field(..., description="City where transaction occurred")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score 0-100, higher = more suspicious")
    reasons: List[str] = Field(..., description="List of reasons why this was flagged")


class TimePoint(BaseModel):
    """
    Represents aggregated data at a specific time point for time-series visualization.
    
    ML team: Useful for plotting transaction patterns over time.
    """
    timestamp: str = Field(..., description="ISO format timestamp")
    total_amount: float = Field(..., description="Sum of transaction amounts at this time")
    transaction_count: int = Field(..., description="Number of transactions at this time")
    anomaly_count: int = Field(..., description="Number of anomalies detected at this time")


class Summary(BaseModel):
    """
    High-level summary statistics of the analyzed dataset.
    
    ML team: Add more aggregate metrics here as needed.
    For example: 'median_amount', 'std_amount', 'unique_cities', etc.
    """
    total_transactions: int = Field(..., description="Total number of transactions analyzed")
    total_volume: float = Field(..., description="Sum of all transaction amounts")
    avg_amount: float = Field(..., description="Average transaction amount")
    anomaly_count: int = Field(..., description="Number of anomalies detected")
    anomaly_percentage: float = Field(..., description="Percentage of transactions flagged as anomalies")
    most_active_user: Optional[str] = Field(None, description="User with most transactions")


class AnalysisResult(BaseModel):
    """
    Complete response from the /api/analyze endpoint.
    
    Contains:
        - summary: Aggregate statistics
        - time_series: Time-bucketed data for charts
        - anomalies: List of flagged transactions
    """
    summary: Summary
    time_series: List[TimePoint]
    anomalies: List[Anomaly]
