#use this script when we have orignal columns ['transaction_id', 'customer_id', 'card_number', 'timestamp', 'merchant_category', 'merchant_type', 'merchant', 'amount', 'currency', 'country', 'city', 'city_size', 'card_type', 'card_present', 'device', 'channel', 'device_fingerprint', 'ip_address', 'distance_from_home', 'high_risk_merchant', 'transaction_hour', 'weekend_transaction', 'velocity_last_hour']

import pandas as pd
import numpy as np
import json
from ast import literal_eval
import pickle
from catboost import Pool

# -------------------------------------------------
# 1) CONFIG
# -------------------------------------------------
INPUT_PATH = "tp.csv"   # or .xlsx
MODEL_PATH = "catboost_fraud_model.pkl"
OUTPUT_PATH = "predicted_transactions.csv"

# -------------------------------------------------
# 2) LOAD DATA
# -------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    if path.lower().endswith((".xls", ".xlsx")):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    return df

df = load_data(INPUT_PATH)

# -------------------------------------------------
# 3) BASIC CLEANUP
# -------------------------------------------------
# timestamp → datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])  # simple

# -------------------------------------------------
# 4) PARSE velocity_last_hour INTO COLUMNS
# -------------------------------------------------
def parse_velocity(x):
    if pd.isna(x):
        return {}
    if isinstance(x, dict):
        return x
    if isinstance(x, str):
        x = x.strip()
        try:
            return json.loads(x)
        except Exception:
            try:
                return literal_eval(x)
            except Exception:
                return {}
    return {}

if "velocity_last_hour" in df.columns:
    vel = df["velocity_last_hour"].map(parse_velocity)
    vel_df = pd.json_normalize(vel).add_prefix("vel1h_")
    for c in vel_df.columns:
        vel_df[c] = pd.to_numeric(vel_df[c], errors="coerce")
    vel_df = vel_df.fillna(0)
    df = pd.concat([df.drop(columns=["velocity_last_hour"]), vel_df], axis=1)
else:
    # if already parsed, just ensure columns exist
    pass

# -------------------------------------------------
# 5) FEATURE ENGINEERING
# -------------------------------------------------
# amount-based features
df["amount_log1p"] = np.log1p(df["amount"])

# hour from transaction_hour
df["hour"] = df["transaction_hour"].astype("int16", errors="ignore")
df["is_night"] = df["hour"].isin([0, 1, 2, 3, 4, 5]).astype("int8")
df["is_odd_hour"] = df["hour"].isin([1, 2, 3, 4]).astype("int8")

# booleans to int
df["is_weekend"] = (
    df["weekend_transaction"]
    .fillna(False)
    .astype(bool)
    .astype("int8")
)

df["high_risk_merchant"] = (
    df["high_risk_merchant"]
    .fillna(False)
    .astype(bool)
    .astype("int8")
)

# -------------------------------------------------
# 6) DROP ID / LEAK COLUMNS
# -------------------------------------------------
drop_cols = [
    "transaction_id", "customer_id", "card_number",
    "device_fingerprint", "ip_address",
    "card_present", "channel",
    "timestamp", "weekend_transaction"
]
drop_cols = [c for c in drop_cols if c in df.columns]
X = df.drop(columns=drop_cols, errors="ignore")

# -------------------------------------------------
# 7) ALIGN FEATURE SET TO TRAINING COLUMNS
# -------------------------------------------------
# These are the feature columns you trained on (X.columns order):
feature_cols = [
    "merchant_category", "merchant_type", "merchant",
    "amount", "currency", "country", "city", "city_size",
    "card_type", "device", "distance_from_home",
    "high_risk_merchant", "transaction_hour",
    "vel1h_num_transactions", "vel1h_total_amount",
    "vel1h_unique_merchants", "vel1h_unique_countries",
    "vel1h_max_single_amount", "amount_log1p", "hour",
    "is_night", "is_odd_hour", "is_weekend"
]

# keep only those, in that order
missing = [c for c in feature_cols if c not in X.columns]
if missing:
    raise ValueError(f"Missing required feature columns: {missing}")

X = X[feature_cols]

# -------------------------------------------------
# 8) LOAD MODEL
# -------------------------------------------------
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# -------------------------------------------------
# 9) CATEGORICAL COLUMN INDICES (same as training)
# -------------------------------------------------
categorical_cols = [
    "merchant_category", "merchant_type", "merchant",
    "currency", "country", "city", "city_size",
    "card_type", "device"
]
categorical_cols = [c for c in categorical_cols if c in X.columns]
cat_idx = [X.columns.get_loc(c) for c in categorical_cols]

pool = Pool(X, cat_features=cat_idx)

# -------------------------------------------------
# 10) PREDICT (FRAUD / NOT FRAUD)
# -------------------------------------------------
proba = model.predict_proba(pool)[:, 1]
pred = (proba >= 0.5).astype(int)

df["fraud_proba"] = proba
df["is_fraud_pred"] = pred

# -------------------------------------------------
# 11) SAVE OR RETURN
# -------------------------------------------------
df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved predictions to {OUTPUT_PATH}")
