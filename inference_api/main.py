from fastapi import FastAPI
from typing import Dict
import joblib
import numpy as np
import os

from inference_api.schemas import TransactionInput, FraudResponse

app = FastAPI(
    title="Real-Time Transaction Fraud Detection API",
    version="1.0"
)

MODEL_PATH = os.path.join("artifacts", "fraud_model.pkl")
model = joblib.load(MODEL_PATH)

@app.get("/health", response_model=Dict[str, str])
def health():
    return {
        "status": "API running",
        "service": "fraud-detection",
        "version": "1.0"
    }

@app.post("/predict", response_model=FraudResponse)
def predict(data: TransactionInput):
    features = np.array([[
        data.amount,
        data.hour,
        data.v1,
        data.v2,
        data.v3,
        data.v4,
        data.v5
    ]])

    probability = model.predict_proba(features)[0][1]
    fraud = probability > 0.5

    if probability < 0.3:
        risk = "LOW"
    elif probability < 0.7:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return FraudResponse(
        fraud=fraud,
        probability=round(float(probability), 4),
        risk_level=risk
    )