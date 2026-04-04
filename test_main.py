from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bookshop API running 🚀"}
