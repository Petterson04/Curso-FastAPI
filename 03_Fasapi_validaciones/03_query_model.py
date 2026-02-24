from typing import Annotated, Literal
from fastapi import FastAPI, Query 
from pydantic import BaseModel, Field

app= FastAPI()

class FilterParams(BaseModel):
    limit: Annotated[int, Field(gt=0)]
    offset:int
    order_by: Literal["created-at","updatted_at"] ="created-at"

@app.get("/items/")
async def read_itemn(filter_query:Annotated[FilterParams, Query()] ):
    return {
        "mesage" : "Todo al millon pa,", **filter_query.model_dump()
    }