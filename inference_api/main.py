from fastapi import FastAPI, Depends, HTTPException
from typing import Dict
import joblib
import numpy as np
import os
from sqlalchemy.orm import Session

# ✅ RELATIVE IMPORTS
from .database import SessionLocal, engine, Base
from .models import FraudPrediction
from .schemas import TransactionInput, FraudResponse

# --------------------------------------------------
# APP CONFIG
# --------------------------------------------------

app = FastAPI(
    title="Real-Time Transaction Fraud Detection API",
    version="1.0"
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# --------------------------------------------------
# DATABASE DEPENDENCY
# --------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
MODEL_PATH = os.path.join(PROJECT_ROOT, "artifacts", "fraud_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Failed to load model:", e)
    model = None

# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health", response_model=Dict[str, str])
def health():
    return {
        "status": "API running",
        "service": "fraud-detection",
        "version": "1.0"
    }

# --------------------------------------------------
# PREDICTION ENDPOINT
# --------------------------------------------------

@app.post("/predict", response_model=FraudResponse)
def predict(data: TransactionInput, db: Session = Depends(get_db)):

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # --------------------------------------------------
    # 🔹 Internal Feature Engineering (Industry Style)
    # --------------------------------------------------

    # Normalize amount
    v1 = data.amount / 10000

    # Time normalization
    v2 = data.hour / 24

    # Interaction feature
    v3 = (data.amount * data.hour) / 100000

    # Amount modulo behavior
    v4 = data.amount % 5000

    # Distance from typical business hours
    v5 = (data.hour - 12) ** 2

    features = np.array([[
        data.amount,
        data.hour,
        v1,
        v2,
        v3,
        v4,
        v5
    ]])

    # --------------------------------------------------
    # 🔹 Model Prediction
    # --------------------------------------------------

    probability = float(model.predict_proba(features)[0][1])
    fraud = probability >= 0.5

    # Risk tier logic
    if probability < 0.30:
        risk = "LOW"
    elif probability < 0.70:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    # --------------------------------------------------
    # 🔹 Save to Database
    # --------------------------------------------------

    record = FraudPrediction(
        amount=data.amount,
        probability=probability,
        fraud=fraud,
        risk_level=risk
    )

    db.add(record)
    db.commit()

    # --------------------------------------------------
    # 🔹 API Response
    # --------------------------------------------------

    return FraudResponse(
        fraud=fraud,
        probability=round(probability, 4),
        risk_level=risk
    )