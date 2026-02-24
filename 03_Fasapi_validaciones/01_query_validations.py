from fastapi import FastAPI, Query
from typing import Annotated

app=FastAPI()
#STRINGS
#max_length
#min_length
#pattern

#Numbers (int Float)
#gt: greater than 
#ge: greater than or equal
#lt: less than 
#le: lees than or equal


#MEtadata
#Titulo 
#descripcion 
#alias
#deprecate

def check_id(id:str):
    if id % 2 != 0:
        raise ValueError("necesita ser par")
    return id 


@app.get("/items")
async def read_items(q:Annotated[int |None, Query(gt=5, title="Query", description= "Lo que se va a buscar")]=None):
    results: dict={"mensaje": "Accesoa a get (read_items)"}
    if q:
        results.update({"q":q})
    return results



