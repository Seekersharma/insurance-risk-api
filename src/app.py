from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from src.app_logger import logger

app = FastAPI()
logger.info("API started successfully")

model = joblib.load("models/risk_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")


class Customer(BaseModel):
    age:int
    premium: int
    claim_count: int
    years_customer: int

@app.get("/")
def home():
    return {"message": "Insurance Risk API Running"}

@app.post("/predict")
def predict(customer: Customer):
    try:
        logger.info("Prediction request recieved")
        sample=pd.DataFrame([customer.model_dump()])
        prediction = model.predict(sample)
        risk = encoder.inverse_transform(prediction)
        logger.info("Prediction completed successfully")
        return {"risk": risk[0]}
    except Exception as e:
        
        logger.error(f"Prediction failed: {e}")
        
        raise HTTPException(status_code=500, detail="Prediction failed")