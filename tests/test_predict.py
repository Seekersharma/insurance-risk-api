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
    
    assert response.status_code ==200