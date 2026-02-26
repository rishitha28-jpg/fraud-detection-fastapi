from fastapi import FastAPI, Depends
from typing import Dict
import joblib
import numpy as np
import os
from sqlalchemy.orm import Session

# ✅ RELATIVE IMPORTS
from .database import SessionLocal, engine, Base
from .models import FraudPrediction
from .schemas import TransactionInput, FraudResponse

app = FastAPI(
    title="Real-Time Transaction Fraud Detection API",
    version="1.0"
)

# ✅ Create DB tables automatically
Base.metadata.create_all(bind=engine)

# ✅ DB session dependency
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

print("Loading model from:", MODEL_PATH)

model = joblib.load(MODEL_PATH)

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.get("/health", response_model=Dict[str, str])
def health():
    return {
        "status": "API running",
        "service": "fraud-detection",
        "version": "1.0"
    }


@app.post("/predict", response_model=FraudResponse)
def predict(data: TransactionInput, db: Session = Depends(get_db)):

    # ✅ INTERNAL / AUTO-GENERATED FEATURES
    v1 = 0.0
    v2 = 0.0
    v3 = 0.0
    v4 = 0.0
    v5 = 0.0

    features = np.array([[
        data.amount,
        data.hour,
        v1, v2, v3, v4, v5
    ]])

    probability = model.predict_proba(features)[0][1]
    fraud = probability > 0.5

    if probability < 0.3:
        risk = "LOW"
    elif probability < 0.7:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    # ✅ SAVE RESULT TO MYSQL
    record = FraudPrediction(
        amount=data.amount,
        probability=float(probability),
        fraud=fraud,
        risk_level=risk
    )

    db.add(record)
    db.commit()

    return FraudResponse(
        fraud=fraud,
        probability=round(float(probability), 4),
        risk_level=risk
    )