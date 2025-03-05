# FastAPI components (FastAPI, Depends, Request) → For defining API routes and handling dependencies.
# SQLAlchemy (Session) → For interacting with the database.
# Jinja2Templates → For rendering HTML pages.
# StaticFiles → For serving static assets (CSS, JavaScript, images).
# CORSMiddleware → To allow cross-origin requests.
# Models, Schemas, CRUD → Importing ORM models, Pydantic schemas, and CRUD functions.
# Database (SessionLocal, engine) → Importing the database connection.
# RedirectResponse → For redirecting users after actions like deleting a book.
from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.responses import RedirectResponse

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup database
# Ensures that all database tables are created based on the models (models.py)./
models.Base.metadata.create_all(bind=engine)

# Setup Jinja2 templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home Page
@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    books = crud.get_books(db)
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

# Add Book Page
@app.get("/add")
def add_book_page(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})

# Add Book API
@app.post("/books/")
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

# Edit Book Page
@app.get("/edit/{book_id}")
def edit_book_page(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)
    return templates.TemplateResponse("edit_book.html", {"request": request, "book": book})

# Update Book
@app.post("/books/update/{book_id}")
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)

# Delete Book
@app.get("/books/delete/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    crud.delete_book(db, book_id)
    return RedirectResponse(url="/", status_code=303)