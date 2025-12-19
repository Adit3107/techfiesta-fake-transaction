#use this script when we have columns merchant_category, merchant_type, merchant, amount, currency, country, city, city_size, card_type, device, distance_from_home, high_risk_merchant, transaction_hour, vel1h_num_transactions, vel1h_total_amount, vel1h_unique_merchants, vel1h_unique_countries, vel1h_max_single_amount, amount_log1p, hour, is_night, is_odd_hour, is_weekend, is_fraud



import pandas as pd
import pickle
from catboost import Pool
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score

# 1) Load model and test data
with open("catboost_fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

df = pd.read_csv("tp.csv")

print("Columns:", df.columns.tolist())

# 2) Split X, y
target = "is_fraud"
y_test = df[target].astype(int)
X_test = df.drop(columns=[target])

# 3) Categorical features (same as training)
categorical_cols = [
    "merchant_category","merchant_type","merchant",
    "currency","country","city","city_size",
    "card_type","device"
]
categorical_cols = [c for c in categorical_cols if c in X_test.columns]
cat_idx = [X_test.columns.get_loc(c) for c in categorical_cols]

test_pool = Pool(X_test, label=y_test, cat_features=cat_idx)

# 4) Predict and evaluate
proba = model.predict_proba(test_pool)[:, 1]
pred  = (proba >= 0.5).astype(int)

roc = roc_auc_score(y_test, proba)
pr  = average_precision_score(y_test, proba)
acc = accuracy_score(y_test, pred)

print(f"ROC-AUC: {roc:.4f}  |  PR-AUC: {pr:.4f}  |  Accuracy: {acc:.4f}")
df["fraud_proba"] = proba
df["fraud_pred"]  = pred

df.to_csv("test_with_predictions.csv", index=False)
print("Saved predictions to test_with_predictions.csv")