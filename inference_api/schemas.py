from pydantic import BaseModel


class TransactionInput(BaseModel):
    amount: float
    hour: int
    v1: float
    v2: float
    v3: float
    v4: float
    v5: float


class FraudResponse(BaseModel):
    fraud: bool
    probability: float
    risk_level: str