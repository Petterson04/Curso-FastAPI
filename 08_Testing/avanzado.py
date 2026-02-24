from fastapi import FastAPI, HTTPException, Depends
import asyncio
from typing import Annotated
app = FastAPI()

class MockDatabase: 
    def __init__(self):
        self.items: dict[str, dict]={ }
    async def get_item (self, item_id: str) -> dict:
        await asyncio.sleep(0.1)
        if item_id not in self.items:
            raise (HTTPException (status_code= 404, detail="Item not found"))
        return self.items.get(item_id)
    
    async def create_item(self, item: dict)-> dict:
        await asyncio.sleep(0.1)
        if item["id"] in self.items:
            raise HTTPException (status_code=409, detail="Item already exist")
        self.items[item["id"]] = item
        return item
    
async def get_db():
    db = MockDatabase
    yield db


@app.get("/items/{item_id}")
async def get__item(item_id: str, db: Annotated[MockDatabase, Depends(get_db)]):
    return await db.get_item(item_id)

@app.post("/items/")
async def create__item(item: dict, db: Annotated[MockDatabase, Depends(get_db)]):
    return await db.create_item(item)
