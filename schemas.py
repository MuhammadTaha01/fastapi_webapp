from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    price: int
    publication_year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True