from fastapi import FastAPI, Path, Query
from typing import Annotated

app=FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int,Path(ge=1, title="Id of item")],
    q: Annotated[str| None, Query(alias="Item-id")] =None):
    ...