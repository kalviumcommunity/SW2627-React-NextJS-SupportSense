"""
ChurnShield ML Model Training Pipeline
======================================
Trains an XGBoost / Random Forest classifier to predict customer churn probability,
calculate health scores, extract key churn drivers, and generate actionable recommendations.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "customers.csv")
MODEL_DIR = os.path.join(PROJECT_ROOT, "ml_service", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_FILE = os.path.join(MODEL_DIR, "churn_model.joblib")
METADATA_FILE = os.path.join(MODEL_DIR, "model_metadata.joblib")

FEATURE_COLS = [
    "mrr",
    "subscription_age_months",
    "total_tickets",
    "unresolved_tickets",
    "escalated_tickets",
    "avg_csat",
    "avg_resolution_hours",
    "payment_delay_days",
    "product_usage_score"
]

TARGET_COL = "churn_flag"

def load_and_preprocess_data():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Customer dataset not found at {RAW_DATA_PATH}")
    
    df = pd.read_csv(RAW_DATA_PATH)
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    return X, y, df

def train_churn_model():
    print("🤖 Initiating ChurnShield ML Model Training...")
    X, y, df = load_and_preprocess_data()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        min_samples_split=4,
        random_state=42,
        class_weight="balanced"
    )
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    
    print("--------------------------------------------------")
    print(f"✅ Model Training Complete!")
    print(f"📊 Accuracy:  {acc * 100:.2f}%")
    print(f"🎯 Precision: {prec * 100:.2f}%")
    print(f"🔍 Recall:    {rec * 100:.2f}%")
    print(f"📈 F1-Score:  {f1 * 100:.2f}%")
    print(f"🌟 ROC-AUC:   {auc * 100:.2f}%")
    print("--------------------------------------------------")
    
    # Save model and metadata
    joblib.dump(model, MODEL_FILE)
    
    feature_importances = dict(zip(FEATURE_COLS, model.feature_importances_))
    metadata = {
        "features": FEATURE_COLS,
        "metrics": {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "auc": auc},
        "feature_importances": feature_importances,
        "trained_at": pd.Timestamp.now().isoformat()
    }
    joblib.dump(metadata, METADATA_FILE)
    print(f"💾 Model artifact saved to: {MODEL_FILE}")
    return model, metadata

if __name__ == "__main__":
    train_churn_model()
