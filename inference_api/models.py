from sqlalchemy import Column, Integer, Float, Boolean, String, DateTime
from datetime import datetime
from .database import Base

class FraudPrediction(Base):
    __tablename__ = "fraud_predictions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    probability = Column(Float)
    fraud = Column(Boolean)
    risk_level = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)