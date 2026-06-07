from fastapi.testclient import TestClient
from src.app import app
client = TestClient(app)

def test_prediction(): 
    
    payload = {
        "age":45,
        "premium":2000,
        "claim_count":1,
        "years_customer":5
    }
    
    response = client.post(
        "/predict",
        json=payload
    )
    data = response.json()
    assert "risk" in data
    assert data["risk"] in ["Low", "Medium", "High"]
    assert response.status_code ==200
    
    
def test_invalid_input():
    payload = {
        "age": 45
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422