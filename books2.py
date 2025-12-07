from fastapi import FastAPI, Path, Query,HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self,id, title, author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description = 'ID is not needed on create', default = None)
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 1)
    description: str = Field(min_length = 1, max_length = 100)
    rating: int = Field(gt =0, lt = 6)
    published_date: int = Field(gt =1900, lt = 2030)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "Sohail",
                "description": "Book about space",
                "rating": 5,
                "published_date": 2025
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro','codingwithSohail','A very good book', 5,2012),
    Book(2, 'FastAPI','codingwithSohail','A very BE book', 5,2013),
    Book(3, 'HP1','Author 1','book description', 4, 2014),
    Book(4, 'HP2','Author 2','book description', 3, 2015),
    Book(5, 'HP3','Author 3','book description', 2, 2015),
    Book(6, 'HP4','Author 4','book description', 1, 2026),

]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS    

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code = 404, detail = 'Item not found')
        
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/published_date/", status_code=status.HTTP_200_OK)
async def get_books_by_published_date(published_date: int = Query(gt =1900, lt = 2030)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


# async def create_books(book_request= Body()):
@app.post("/create-books", status_code = status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):

    new_book = Book(**book_request.dict())
    # new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    # return BOOKS


def find_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if(len(BOOKS) > 1) else 0
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    return book


@app.put("/books/update_book",status_code = status.HTTP_204_NO_CONTENT)
async def update_books(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed: 
        raise HTTPException(status_code = 404, detail = 'Item not found')

@app.delete("/books/{book_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed: 
        raise HTTPException(status_code = 404, detail = 'Item not found')

# @app.put("/books/update_book")
# async def update_books(book_request: BookRequest):
#     for book in BOOKS:
#         if book.id == book_request.id:
#             book = book_request
