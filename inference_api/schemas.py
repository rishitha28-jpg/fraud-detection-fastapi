from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
    # Required fields
    amount: float = Field(..., example=200.0)
    hour: int = Field(..., ge=0, le=23, example=14)

    # Optional ML internal features (auto-filled if not provided)
    feature_3: float = Field(default=0.0, example=1.0)
    feature_4: float = Field(default=0.0, example=0.0)
    feature_5: float = Field(default=0.0, example=0.5)
    feature_6: float = Field(default=0.0, example=3.0)
    feature_7: float = Field(default=0.0, example=0.0)


class FraudResponse(BaseModel):
    fraud: bool
    probability: float
    risk_level: str