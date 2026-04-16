from fastapi import FastAPI, Header, status
from fastapi.exceptions import HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World"}

@app.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello {name}", "age": age}

class BookCreateModel(BaseModel):
    title: str
    author: str


@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

@app.get("/get_headers", status_code = 200)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
):
    request_headers = {}

    request_headers["Accept"] = accept
    request_headers["Content_Type"] = content_type
    request_headers["User_Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers

Books = [
    {
        "id": 1,
        "title":  "12",
        "author": "123",
        "publisher": "1234",
        "publisher_data": "2021-02-02",
        "page_count": 12345,
        "language": "English"
    },
    {
        "id": 2,
        "title":  "21",
        "author": "321",
        "publisher": "4321",
        "publisher_data": "2021-03-01",
        "page_count": 1234,
        "language": "English"
    },
]

class Book(BaseModel):
        id: int
        title:  str
        author: str
        publisher: str
        publisher_data: str
        page_count: int
        language: str

@app.get("/books", response_model=List[Book])
async def get_all_books():
    return Books

@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in Books:
        if book["id"] == book_id:
            return book
        
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = "Book not found"
            )

@app.post("/books", status_code = status.HTTP_201_CREATED)
async def create_a_books(book_data: Book) -> dict:
    new_book = book_data.model_dump()

    Books.append(new_book)

    return new_book

class BookUpdateModel(BaseModel):
        title:  str
        author: str
        publisher: str
        page_count: int
        language: str

@app.patch("/book/{book_id}")
async def update_book(
    book_id: int,
    book_update_data: BookUpdateModel
) -> dict:
    for Book in Books:
        if Book['id'] == book_id:
            Book['title'] = book_update_data.title
            Book['author'] = book_update_data.author
            Book['publisher'] = book_update_data.publisher
            Book['page_count'] = book_update_data.page_count
            Book['language'] = book_update_data.language

            return Book
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Book not found"
    )

@app.delete("/book/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for Book in Books:
        if Book["id"] == book_id:
            Books.remove(Book)

            return {}
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Book not found"
    )

@app.get("/books")
async def get_all_books():
    pass