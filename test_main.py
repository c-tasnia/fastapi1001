import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base, get_db
from typing import List

# ---------------- Test DB Setup ----------------
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Override get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables in test DB
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# ---------------- Tests ----------------
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bookshop API running!"}

def test_create_book():
    response = client.post("/books/", json={
        "bookname": "1984",
        "year": 1949,
        "author": "George Orwell",
        "quantity": 5,
        "price": 12.5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["bookname"] == "1984"
    assert data["author"] == "George Orwell"
    assert "bookid" in data

def test_read_books():
    client.post("/books/", json={
        "bookname": "Brave New World",
        "year": 1932,
        "author": "Aldous Huxley",
        "quantity": 7,
        "price": 15.0
    })
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_read_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.json()
    assert data["bookid"] == 1