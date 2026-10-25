

from fastapi import Body,FastAPI

newapp=FastAPI()

Books = [
    {"title":"title one", "author":"author one", "category":"science"},
    {"title":"title two", "author":"author two", "category":"fiction"},
    {"title":"title three", "author":"author three", "category":"comic"},
    {"title":"title four", "author":"author four", "category":"comic"}
    
]

@newapp.get("/firstapi")
def first_api():
    return Books

# @newapp.get("/firstapi/{book_name}")
# def get_using_path_parameters(book_name):
#     for book in Books:
#         if book_name=='title one':
#             return book.get('author')
#     return "Not a Valid Book Name"
        
@newapp.get("/firstapi/{author_name}")       
def get_using_path_and_query_parameters(category : str, author_name : str ):
    for book in Books:
        if book.get('category')==category and book.get('author')==author_name:
            return book.get("title")
    
    return "No Combination Found"


@newapp.post("/firstapi/create_book")
def add_book_to_existing_books(newbook = Body()):
    Books.append(newbook)
    
    
@newapp.put("/firstapi/update_book")
def update_existing_books(updatebook=Body()):
    for book in Books:
        if book.get('title')==updatebook.get("title"):
            print("Inside Book ", book.get('title'), book.get('category'))
            if book.get('category')!=updatebook.get("category"):
                book['category']=updatebook.get("category")
                break
            # book['category']= updatebook.get("category")
            # Books.append(book)
            # break
            
@newapp.delete("/firstapi/delete_book/{book_title}")
def delete_book(book_title:str):
    for book in Books:
        print(book.get('title'),book_title)
        if book.get('title')==book_title:
            Books.remove(book)
            break
            
            
    
    

        