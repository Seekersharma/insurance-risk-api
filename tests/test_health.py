import sys
import os
sys.path.insert(0, os.path.abspath("."))

from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code ==200
    
