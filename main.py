from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel, ConfigDict
from typing import List

# ---------------- Database Setup ----------------
DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ---------------- Models ----------------
class Book(Base):
    __tablename__ = "books"

    bookid = Column(Integer, primary_key=True, index=True)
    bookname = Column(String, index=True)
    year = Column(Integer)
    author = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)

# Create table
Base.metadata.create_all(bind=engine)

# ---------------- Schemas ----------------
class BookCreate(BaseModel):
    bookname: str
    year: int
    author: str
    quantity: int
    price: float

class BookResponse(BaseModel):
    bookid: int
    bookname: str
    year: int
    author: str
    quantity: int
    price: float

    # Pydantic v2
    model_config = ConfigDict(from_attributes=True)

# ---------------- FastAPI App ----------------
app = FastAPI(title="📚 Bookshop API")

# ---------------- Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Routes ----------------

# Root
@app.get("/")
def read_root():
    return {"message": "Bookshop API running 🚀"}

# Create Book
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Get All Books
@app.get("/books/", response_model=List[BookResponse])
def read_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

# Get Single Book
@app.get("/books/{bookid}", response_model=BookResponse)
def read_book(bookid: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.bookid == bookid).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db_book

# Update Book
@app.put("/books/{bookid}", response_model=BookResponse)
def update_book(bookid: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.bookid == bookid).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book.model_dump().items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

# Delete Book
@app.delete("/books/{bookid}")
def delete_book(bookid: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.bookid == bookid).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

# Search Books by Author
@app.get("/books/search/", response_model=List[BookResponse])
def search_books(author: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.author.contains(author)).all()
    return books