from pydantic import BaseModel


class TransactionInput(BaseModel):
    """
    User-facing input schema.
    Only real-world features are accepted.
    Engineered features (v1–v5) are generated internally.
    """
    amount: float
    hour: int


class FraudResponse(BaseModel):
    """
    API response schema.
    """
    fraud: bool
    probability: float
    risk_level: str