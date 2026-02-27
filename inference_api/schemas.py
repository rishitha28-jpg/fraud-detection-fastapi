from pydantic import BaseModel, Field

class TransactionInput(BaseModel):
    amount: float = Field(..., example=200.0)
    hour: int = Field(..., ge=0, le=23, example=14)

    # Optional features with safe defaults
    feature_3: float = Field(0.0, example=0.0)
    feature_4: float = Field(0.0, example=0.0)
    feature_5: float = Field(0.0, example=0.0)
    feature_6: float = Field(0.0, example=0.0)
    feature_7: float = Field(0.0, example=0.0)


class FraudResponse(BaseModel):
    fraud: bool
    probability: float
    risk_level: str