# Session is imported from SQLAlchemy's ORM (Object Relational Mapper).
# It is used to create a database session, which manages connections and transactions with the database.
from sqlalchemy.orm import Session

# models: Typically contains SQLAlchemy ORM models that define the database structure.
# schemas: Usually contains Pydantic schemas used for data validation and serialization.
import models, schemas

def get_books(db: Session):
    return db.query(models.Book).all()

# db: Session → This is a SQLAlchemy database session that allows interaction with the database.
# book: schemas.BookCreate → This is a Pydantic schema (BookCreate), which validates and structures the input data.
def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def update_book(db: Session, book_id: int, book_data: schemas.BookCreate):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        for key, value in book_data.dict().items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return book