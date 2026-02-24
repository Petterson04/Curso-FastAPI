from fastapi import FastAPI

app= FastAPI()


#Endpoint que regresa el libro favortio (Escrito en la misma peticion GET)
@app.get("/books/favorite")
async def favorite_book():
    return {"book": "The Great Gatsby"}

#Endpoint que recibe un ID del libro al buscar (Parametro de ruta) y regresa el ID 
@app.get("/books/{book_id}")
async def get_book(book_id: int):
    return {"book_id": book_id}