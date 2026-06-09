import joblib
import pandas as pd
from app_logger import logger

model = joblib.load("models/risk_model.pkl")
encoder = joblib.load("models/label_encoder.pkl")
logger.info("Model loaded successfully")

sample = pd.DataFrame([{
    "age": 45,
    "premium": 2000,
    "claim_count": 1,
    "years_customer": 10
}])

prediction = model.predict(sample)
logger.info( "Prediction completed successfully")

risk = encoder.inverse_transform(prediction)

print("Predicted Risk:", risk[0])