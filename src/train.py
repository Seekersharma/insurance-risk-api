import pandas as pd
from src.app_logger import logger
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

np.random.seed(42)

# Create synethic insurance data

n = 1000

df = pd.DataFrame({
    "age": np.random.randint(18,80, n),
    "premium": np.random.randint(500, 5000, n),
    "claim_count": np.random.randint(0,6, n),
    "years_customer": np.random.randint(1, 20, n),
})

# Simple business rules for risk classification

df["risk"] = np.where( 
    (df["claim_count"] >= 3) | 
    (df["age"] < 25), 
    "High",
    np.where(df["years_customer"] > 10, "Low", "Medium")        
)

X = df[["age", "premium", "claim_count", "years_customer"]]
y = df["risk"]

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X,y_encoded)
logger.info("Training completed successfully")


os.makedirs("models", exist_ok=True)
logger.info("Model saved successfully")
joblib.dump( model,"models/risk_model.pkl")
joblib.dump(encoder,"models/label_encoder.pkl")

print("Model and Encoder save successfully!")
