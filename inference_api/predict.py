import numpy as np
from inference_api.model_loader import model

def predict_fraud(data):
    X = np.array([[
        data.amount,
        data.hour,
        data.v1,
        data.v2,
        data.v3,
        data.v4,
        data.v5
    ]])

    prob = model.predict_proba(X)[0][1]

    if prob > 0.8:
        risk = "HIGH"
    elif prob > 0.5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return prob > 0.5, round(prob, 4), risk