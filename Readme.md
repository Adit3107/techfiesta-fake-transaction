```markdown
# Fake Transaction Detector – Spot the Anomaly

A lightweight end‑to‑end fraud detection pipeline for card transactions. The project loads transaction logs, engineers behaviour and time‑based features, trains a CatBoost model, and exposes scripts to score new CSV/Excel files and generate fraud predictions, as commonly done in modern fraud‑detection systems.

---

## 1. Problem Overview

With the growing volume of online transactions, detecting suspicious or fake entries is critical even for smaller financial systems. This project:

- Ingests raw or pre‑engineered transaction data.  
- Engineers features capturing **amount patterns**, **time of transaction**, **distance/geo**, and **recent behaviour (velocity)**.  
- Trains a supervised CatBoost model to classify each transaction as **fraud** (1) or **not fraud** (0).  
- Provides reusable scripts for **training**, **testing**, and **batch prediction**.

---

## 2. Project Structure

All core files live in the root folder:

```
fake_transaction_detection/
├─ basic_eda.ipynb          # EDA + feature engineering + initial training
├─ synthetic_fraud_data.csv # Original synthetic dataset used for experimentation
├─ train_split.csv          # 80% training data (engineered features + is_fraud)
├─ valid_split.csv          # 10% validation data (engineered features + is_fraud)
├─ test_split.csv           # 10% test data (engineered features + is_fraud)
├─ catboost_fraud_model.pkl # Trained CatBoost model (pickle)
├─ testing.py               # Scoring script for RAW-schema CSV/Excel
├─ testing1.py              # Scoring/eval script for ENGINEERED-schema CSV
├─ test_with_predictions.csv# Example output with fraud_proba + fraud_pred
├─ requirements.txt         # Python dependencies for the project
└─ README.md                # Project documentation (this file)
```

**File descriptions:**

- `basic_eda.ipynb`  
  Interactive notebook where you explore the data, engineer features, run EDA plots, and train the CatBoost model with an 80/10/10 split.

- `synthetic_fraud_data.csv`  
  Base synthetic transaction log containing the raw columns (transaction IDs, timestamps, merchant details, velocity field, etc.) used to build all downstream datasets.

- `train_split.csv`, `valid_split.csv`, `test_split.csv`  
  Model‑ready datasets with engineered features and `is_fraud`. These are created from `df_model` after splitting, and are used for training, validation, and final evaluation.

- `catboost_fraud_model.pkl`  
  Pickled CatBoost classifier trained on the 23 engineered features. Loaded by both testing scripts for inference.

- `testing.py`  
  Script for scoring **raw** transaction files (full original schema, including `timestamp` and `velocity_last_hour`). It performs all preprocessing/feature engineering internally and outputs predictions.

- `testing1.py`  
  Script for scoring or evaluating **engineered** CSVs (already in model‑ready schema with `is_fraud`). It directly builds a CatBoost pool from the 23 features, computes metrics, and saves predictions.

- `test_with_predictions.csv`  
  Example output produced by `testing1.py`, containing original engineered features plus model outputs `fraud_proba` and `fraud_pred`.

- `requirements.txt`  
  List of Python dependencies (pandas, numpy, scikit‑learn, catboost, matplotlib, seaborn) required to run the pipeline end‑to‑end.

---

## 3. Installation

```
git clone <this-repo-url>
cd fake_transaction_detection

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

Key libraries:

- `pandas`, `numpy` for data handling.  
- `scikit-learn` for splitting and metrics.  
- `catboost` for the main fraud model (handles categorical features natively).[web:64][web:213]

---

## 4. Training Summary (what the model expects)

Model training (done in `basic_eda.ipynb` or an equivalent training script) performs:

1. **Parsing & feature engineering (from raw schema)**  
   - Convert `timestamp` → datetime; drop invalid rows.  
   - Parse `velocity_last_hour` into:
     - `vel1h_num_transactions`  
     - `vel1h_total_amount`  
     - `vel1h_unique_merchants`  
     - `vel1h_unique_countries`  
     - `vel1h_max_single_amount`  
   - Engineer:
     - `amount_log1p = log(1 + amount)`  
     - `hour` from `transaction_hour`  
     - `is_night` (hour in 0–5)  
     - `is_odd_hour` (hour in 1–4)  
     - `is_weekend` from `weekend_transaction`

2. **Cleaning**  
   - Convert `high_risk_merchant` and weekend flag to 0/1.  
   - Drop ID and leaky columns:  
     - `transaction_id`, `customer_id`, `card_number`,  
       `device_fingerprint`, `ip_address`, `card_present`,  
       `channel`, `timestamp`, `weekend_transaction`.

3. **Model**  
   - Train/valid/test split: 80% / 10% / 10% (stratified).  
   - Model: `CatBoostClassifier` with AUC metric and class weights to handle ~20% fraud positives, following common practice in fraud detection.[web:213][web:218]

Result: a pickled model file `catboost_fraud_model.pkl` that expects the following 23 engineered features as input:

```
['merchant_category','merchant_type','merchant','amount','currency',
 'country','city','city_size','card_type','device','distance_from_home',
 'high_risk_merchant','transaction_hour','vel1h_num_transactions',
 'vel1h_total_amount','vel1h_unique_merchants','vel1h_unique_countries',
 'vel1h_max_single_amount','amount_log1p','hour','is_night',
 'is_odd_hour','is_weekend']
```

---

## 5. Scripts

### 5.1 `testing.py` – for **RAW schema** CSV/Excel

Use this when your input file has **original columns**, including `timestamp` and `velocity_last_hour`:

```
['transaction_id','customer_id','card_number','timestamp',
 'merchant_category','merchant_type','merchant','amount','currency',
 'country','city','city_size','card_type','card_present','device',
 'channel','device_fingerprint','ip_address','distance_from_home',
 'high_risk_merchant','transaction_hour','weekend_transaction',
 'velocity_last_hour']
```

**What it does:**

- Loads model `catboost_fraud_model.pkl`.  
- Reads the CSV/Excel with the raw schema.  
- Converts `timestamp` -> datetime and drops invalid rows.  
- Parses `velocity_last_hour` into `vel1h_*` behaviour features.  
- Engineers `amount_log1p`, `hour`, `is_night`, `is_odd_hour`, `is_weekend`.  
- Drops ID and leaky columns.  
- Builds a feature matrix with the 23 expected columns.  
- Predicts fraud probability and label for each row.  
- Saves an output CSV (e.g. `predicted_transactions.csv`) with:
  - `fraud_proba`  
  - `is_fraud_pred` (0/1)

**How to run:**

```
python testing.py
```

Edit the input/output filenames at the top of `testing.py` as needed.

---

### 5.2 `testing1.py` – for **ENGINEERED schema** CSVs

Use this when your input file already has **engineered columns**, e.g. `train_split.csv`, `valid_split.csv`, or `test_split.csv`:

```
merchant_category, merchant_type, merchant, amount, currency,
country, city, city_size, card_type, device,
distance_from_home, high_risk_merchant, transaction_hour,
vel1h_num_transactions, vel1h_total_amount,
vel1h_unique_merchants, vel1h_unique_countries,
vel1h_max_single_amount, amount_log1p, hour,
is_night, is_odd_hour, is_weekend, is_fraud
```

**What it does:**

- Loads model `catboost_fraud_model.pkl`.  
- Reads the CSV with engineered schema.  
- Treats `is_fraud` as label (`y_test`) and the first 23 columns as features (`X_test`).  
- Builds a CatBoost `Pool` using the same categorical indices as in training.  
- Computes evaluation metrics:
  - ROC‑AUC (if both classes present), PR‑AUC, accuracy.[web:254][web:260]  
- Adds:
  - `fraud_proba` (predicted probability of fraud)  
  - `fraud_pred` (0/1 label)  
- Saves to `test_with_predictions.csv`.

**How to run:**

```
python testing1.py
```

This script is ideal for offline evaluation and for generating labelled prediction files for analysis or dashboards.

---

## 6. Requirements

Minimal `requirements.txt`:

```
pandas==2.2.2
numpy==1.26.4
scikit-learn==1.4.2
catboost==1.2.5
matplotlib==3.8.4
seaborn==0.13.2
```

CatBoost is chosen because it handles categorical features natively, performs well on tabular data, and is widely used in financial fraud detection tasks.
```