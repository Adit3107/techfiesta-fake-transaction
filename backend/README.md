# Fake Transaction Detector

A hackathon project for detecting anomalous/fake transactions in financial data.

## Features

- **CSV Upload**: Drag-and-drop or browse to upload transaction files
- **Real-time Analysis**: Instant anomaly detection and statistics
- **Dashboard**: Visual summary of transaction patterns
- **Anomaly Table**: Sortable list of flagged transactions with risk scores
- **Time Series View**: Transaction activity over time

## Project Structure

```
fake-transaction-detector/
│
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # Pydantic response schemas
│   ├── routers/
│   │   └── analyze.py       # /api/analyze endpoint
│   ├── services/
│   │   └── ml_engine.py     # ML pipeline (replace dummy logic here!)
│   └── utils/
│       └── parser.py        # CSV parsing utilities
│
├── frontend/
│   ├── src/
│   │   ├── pages/           # Next.js pages
│   │   ├── components/      # React components (FileUpload, SummaryCard, etc.)
│   │   └── styles/          # Tailwind CSS styles
│   ├── next.config.js       # API proxy configuration
│   └── package.json         # Frontend dependencies
│
├── sample_transactions.csv  # Test data
├── start.sh                 # Startup script
└── README.md
```

## Quick Start

### Run the Application

```bash
bash start.sh
```

This starts:
- **Frontend** (Next.js) on port 5000 - User-facing dashboard
- **Backend** (FastAPI) on port 8000 - API server

### Test with Sample Data

1. Open the app in your browser
2. Upload `sample_transactions.csv`
3. View the analysis results

### API Documentation

Visit `http://localhost:8000/docs` for Swagger UI.

## API Endpoints

### `GET /health`
Health check endpoint.

**Response:**
```json
{"status": "ok"}
```

### `POST /api/analyze`
Upload a CSV file for analysis.

**Request:** Multipart form data with a CSV file.

**Response:**
```json
{
  "summary": {
    "total_transactions": 100,
    "total_volume": 500000.00,
    "avg_amount": 5000.00,
    "anomaly_count": 5,
    "anomaly_percentage": 5.0,
    "most_active_user": "U001"
  },
  "time_series": [...],
  "anomalies": [...]
}
```

## Expected CSV Format

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | string | Unique transaction ID |
| user_id | string | User identifier |
| amount | float | Transaction amount |
| timestamp | string | ISO format datetime |
| city | string | Transaction location |

**Example:**
```csv
transaction_id,user_id,amount,timestamp,city
T001,U001,500.00,2024-01-15T10:30:00,Mumbai
T002,U002,75000.00,2024-01-15T10:35:00,Delhi
```

---

## For ML Team

### Where to Add Your Logic

**File:** `backend/services/ml_engine.py`

### Functions to Replace

1. **`_detect_anomalies(df)`** - Currently returns random anomalies
   - Implement: Isolation Forest, LOF, Z-score, etc.
   - Add proper risk scoring based on model confidence

2. **`_generate_time_series(df)`** - Currently returns fake data
   - Implement: Real time bucketing from transaction timestamps

3. **`_compute_summary(df)`** - Basic stats are real
   - Add: More metrics like median, std, unique users/cities

### Example Implementation

```python
from sklearn.ensemble import IsolationForest

def _detect_anomalies(df):
    features = df[['amount']].values
    model = IsolationForest(contamination=0.1, random_state=42)
    predictions = model.fit_predict(features)
    
    anomaly_indices = df.index[predictions == -1]
    # ... convert to Anomaly objects
```

---

## Tech Stack

**Backend:**
- FastAPI (Python web framework)
- Pydantic (data validation)
- Pandas (data processing)
- Uvicorn (ASGI server)

**Frontend:**
- Next.js 14 (React framework)
- Tailwind CSS (styling)
- React 18 (UI library)

## Future Improvements

- [ ] Real ML model integration (Isolation Forest, LOF)
- [ ] User behavior profiling
- [ ] Location-based anomaly detection (impossible travel)
- [ ] Transaction velocity analysis
- [ ] Database for storing results
- [ ] Authentication and rate limiting
- [ ] Export analysis results

---

*Built for Hackathon 2024*
