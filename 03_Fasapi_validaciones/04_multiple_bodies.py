from fastapi import FastAPI, Query
from pydantic import BaseModel 
from typing import Annotated, Literal

app=FastAPI()

class Item(BaseModel):
    name:str
    descripcion: str | None= None
    price: float
    
class User(BaseModel):
    username:str
    full_name: str | None=None
    
    


@app.put("/items/{item_id}")
async def update_item(item_id:int, item: Item, user: User):
    return{
        "item_id": item_id,
        "item": item,
        "User":user
    }  