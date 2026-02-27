from fastapi import FastAPI, HTTPException
from typing import Dict
import joblib
import numpy as np
import os

from .schemas import TransactionInput, FraudResponse

# -------------------------------------------------
# APP CONFIG
# -------------------------------------------------
app = FastAPI(
    title="Real-Time Transaction Fraud Detection API",
    version="1.0.0"
)

# -------------------------------------------------
# LOAD MODEL (SAFE FOR LOCAL + RENDER)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(
    os.path.dirname(BASE_DIR),
    "artifacts",
    "fraud_model.pkl"
)

model = None
EXPECTED_FEATURES = 7

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("✅ Fraud model loaded successfully")
        if hasattr(model, "n_features_in_"):
            print("📊 Model expects features:", model.n_features_in_)
    else:
        print("❌ Model file not found:", MODEL_PATH)
except Exception as e:
    print("❌ Model loading failed:", str(e))

# -------------------------------------------------
# ROOT
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Fraud Detection API is running",
        "docs": "/docs",
        "health": "/health"
    }

# -------------------------------------------------
# HEALTH
# -------------------------------------------------
@app.get("/health", response_model=Dict[str, str])
def health():
    return {
        "status": "OK",
        "service": "fraud-detection",
        "version": "1.0.0"
    }

# -------------------------------------------------
# PREDICT
# -------------------------------------------------
@app.post("/predict", response_model=FraudResponse)
def predict(data: TransactionInput):

    # 1️⃣ Check model loaded
    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Fraud model not loaded"
        )

    # 2️⃣ Prepare features safely
    try:
        features = np.array([[ 
            float(data.amount),
            float(data.hour),
            float(data.feature_3),
            float(data.feature_4),
            float(data.feature_5),
            float(data.feature_6),
            float(data.feature_7)
        ]])
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input values: {str(e)}"
        )

    # 3️⃣ Validate feature count
    if hasattr(model, "n_features_in_"):
        if features.shape[1] != model.n_features_in_:
            raise HTTPException(
                status_code=500,
                detail=f"Model expects {model.n_features_in_} features but received {features.shape[1]}"
            )

    # 4️⃣ Make prediction safely
    try:
        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(features)[0][1])
        else:
            # fallback if model has no predict_proba
            prediction = model.predict(features)[0]
            probability = float(prediction)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

    # 5️⃣ Risk logic
    fraud = probability >= 0.5

    if probability < 0.30:
        risk = "LOW"
    elif probability < 0.70:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return FraudResponse(
        fraud=fraud,
        probability=round(probability, 4),
        risk_level=risk
    )