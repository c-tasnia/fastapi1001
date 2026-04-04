# test_main.py
from fastapi.testclient import TestClient
from main import app  # make sure your FastAPI app is called 'app' in main.py

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bookshop API running 🚀"}
