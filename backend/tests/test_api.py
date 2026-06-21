import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "models_loaded" in data

def test_simplify_validation():
    response = client.post("/api/simplify", json={"query": "ab"})
    assert response.status_code == 422 # unprocessable entity (min length 3)
