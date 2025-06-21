from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model.pkl"))
model = joblib.load(MODEL_PATH)
app = FastAPI()

class Feature(BaseModel):
    status: int
    size: int
    method: int
    path: int
    user_agent: int
    hour_of_day: int

@app.post("/predict_one")
def predict_one(feature: Feature):
    data = np.array([[feature.status, feature.size, feature.method,
                      feature.path, feature.user_agent, feature.hour_of_day]])
    prediction = model.predict(data)[0]
    is_anomaly = bool(prediction == -1)
    return {"anomaly": is_anomaly}

class Features(BaseModel):
    data: list[Feature]

@app.post("/predict_batch")
def predict_batch(features: Features):
    if not features.data:
        return {"error": "No data provided"}

    inputs = [[f.status, f.size, f.method, f.path, f.user_agent, f.hour_of_day]
              for f in features.data]
    predictions = model.predict(inputs)
    
    return {
        "results": [
            {"index": i, "anomaly": bool(pred == -1)}
            for i, pred in enumerate(predictions)
        ]
    }
