from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

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
    sample=pd.DataFrame([customer.dict()])
    prediction = model.predict(sample)
    risk = encoder.inverse_transform(prediction)
    
    return {"risk": risk[0]}