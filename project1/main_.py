from pydantic import BaseModel, Field  
from fastapi import FastAPI, status, Query, Path, HTTPException
from typing import Optional, Annotated

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


app = FastAPI()

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
def create_book(book: BookRequest):
    new_book = Book(**book.model_dump())
    BOOKS.append(new_book)

@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
def get_book(book_id: Annotated[int, Path(ge=1, le=5)]):
    for book in BOOKS:
        if book.id == book_id:
            return book
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Book with id: {book_id} not found")
        
#  Get book by rating
@app.get("/books/", status_code=status.HTTP_200_OK)
def get_book_by_rating(rating: Annotated[int, Query(ge=1, le=5)]):
    book_returned = []
    for book in BOOKS:
        if book.rating == rating:
            book_returned.append(book)

    return book_returned

@app.get("/books/{year}")
def get_book(
    year: Annotated[int, Path(ge=2020, le=2032)],
    book_id: Annotated[int | None, Query(ge=1)] = None
):
    book_return = []

    for book in BOOKS:
        if book_id is None:
            if book.published_date == year:
                book_return.append(book)
        else:
            if book.published_date == year and book.id == book_id:
                return book

    if book_return and len(book_return) > 0:
        return book_return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.put("/update/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book_id: int, update_book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            new_book = Book(**update_book.model_dump())
            new_book.id = book_id
            BOOKS[i] = new_book
            break


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')