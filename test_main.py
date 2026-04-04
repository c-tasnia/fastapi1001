# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bookshop API running 🚀"}

# Test GET all books (should start empty)
def test_get_books_empty():
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == []

# Test creating a book
def test_create_book():
    book_data = {
        "bookname": "Python Basics",
        "year": 2023,
        "author": "Jabed",
        "quantity": 10,
        "price": 450
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["bookname"] == "Python Basics"
    assert data["author"] == "Jabed"
    assert data["quantity"] == 10
    assert data["price"] == 450
