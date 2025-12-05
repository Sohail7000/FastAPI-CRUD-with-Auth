from fastapi import FastAPI
from fastapi import Body
app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author' : 'Author One' , 'category': 'science'},
    {'title': 'Title Two', 'author' : 'Author Two' , 'category': 'science'},
    {'title': 'Title Three', 'author' : 'Author Three' , 'category': 'history'},
    {'title': 'Title Four', 'author' : 'Author Four' , 'category': 'math'},
    {'title': 'Title Five', 'author' : 'Author Five' , 'category': 'math'},
    {'title': 'Title Six', 'author' : 'Author One' , 'category': 'math'},
]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_by_book_title(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/author/{book_author}")
async def read_author_category_by_query(book_author: str,category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            print(book)
            books_to_return.append(book)
    return books_to_return

@app.get("/books/by_author/")
async def read_books_by_author_path(author:str):
    books_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() == author.casefold():
            books_to_return.append(BOOKS[i])
    return books_to_return


@app.post("/books/create_books")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return BOOKS
    
@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] == updated_book


    
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS[i].pop(i)
            break




























# @app.get("/books/mybook")
# async def read_all_books():
#     return {'mybook': 'Lunax'}

# @app.get("/books/{book_title}")
# async def read_all_books(book_title: str):
#     for book in BOOKS:
#         if book.get('title').casefold() == book_title.casefold():
#             return book

# @app.get("/books/{book_title}")
# async def read_category_by_query(book_title: str,category: str):
#     books_to_return = []
#     for book in BOOKS:
#         if book.get('category').casefold() == category.casefold() and book.get('title').casefold() == book_title.casefold():
#             books_to_return.append(book)
#     return books_to_return



