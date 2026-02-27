from fastapi import FastAPI, Depends, HTTPException
from typing import Dict, Optional
import joblib
import numpy as np
import os
from sqlalchemy.orm import Session

# -----------------------------
# SCHEMAS (always required)
# -----------------------------
from .schemas import TransactionInput, FraudResponse

# -----------------------------
# OPTIONAL DATABASE (safe for Render)
# -----------------------------
try:
    from .database import SessionLocal, engine, Base
    from .models import FraudPrediction
    DB_AVAILABLE = True
except Exception as e:
    print("⚠️ Database disabled:", e)
    SessionLocal = None
    engine = None
    Base = None
    FraudPrediction = None
    DB_AVAILABLE = False

# -----------------------------
# APP CONFIG
# -----------------------------
app = FastAPI(
    title="Real-Time Transaction Fraud Detection API",
    version="1.0"
)

# -----------------------------
# CREATE TABLES (ONLY IF DB EXISTS)
# -----------------------------
if DB_AVAILABLE and engine:
    Base.metadata.create_all(bind=engine)

# -----------------------------
# DATABASE DEPENDENCY
# -----------------------------
def get_db() -> Optional[Session]:
    if not DB_AVAILABLE or SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# MODEL LOADING
# -----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
MODEL_PATH = os.path.join(PROJECT_ROOT, "artifacts", "fraud_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print("✅ ML model loaded successfully")
except Exception as e:
    print("❌ Model load failed:", e)
    model = None

# -----------------------------
# ROOT ENDPOINT
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "Fraud Detection API is running",
        "docs": "/docs",
        "health": "/health"
    }

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health", response_model=Dict[str, str])
def health():
    return {
        "status": "API running",
        "service": "fraud-detection",
        "version": "1.0"
    }

# -----------------------------
# PREDICTION ENDPOINT
# -----------------------------
@app.post("/predict", response_model=FraudResponse)
def predict(
    data: TransactionInput,
    db: Optional[Session] = Depends(get_db)
):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        # -------------------------
        # FEATURE ENGINEERING
        # -------------------------
        v1 = data.amount / 10000
        v2 = data.hour / 24
        v3 = (data.amount * data.hour) / 100000
        v4 = data.amount % 5000
        v5 = (data.hour - 12) ** 2

        features = np.array([[
            data.amount,
            data.hour,
            v1, v2, v3, v4, v5
        ]])

        # -------------------------
        # MODEL PREDICTION
        # -------------------------
        probability = float(model.predict_proba(features)[0][1])
        fraud = probability >= 0.5

        if probability < 0.30:
            risk = "LOW"
        elif probability < 0.70:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        # -------------------------
        # SAVE TO DB (OPTIONAL)
        # -------------------------
        if DB_AVAILABLE and db is not None:
            record = FraudPrediction(
                amount=data.amount,
                probability=probability,
                fraud=fraud,
                risk_level=risk
            )
            db.add(record)
            db.commit()

        # -------------------------
        # RESPONSE
        # -------------------------
        return FraudResponse(
            fraud=fraud,
            probability=round(probability, 4),
            risk_level=risk
        )

    except Exception as e:
        print("❌ Prediction error:", e)
        raise HTTPException(status_code=500, detail="Prediction failed")