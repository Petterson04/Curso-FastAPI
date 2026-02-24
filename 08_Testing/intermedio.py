from fastapi import FastAPI, HTTPException, Header
from typing import Annotated 
from pydantic import BaseModel

fake_secret_token = "misupertoken"

class User (BaseModel):
    id: str
    name: str
    email:str 

fake_db: dict[str, User]={
    "1": User(id="1",name="User1", email="Username1"),
    "2": User(id="2",name="User2",email= "Username2")
}
app= FastAPI()

@app.get("/users/{user_id}", response_model=User)
async def get_user( user_id:str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise (HTTPException (status_code=400, detail="Invalid token"))
    if user_id not in fake_db:
        raise (HTTPException (status_code=404, detail="User not found"))
    return fake_db[user_id]

@app.post("/users/", response_model=User)
async def create_user( user:User, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise (HTTPException (status_code=400, detail="Invalid token"))
    if user.id in fake_db:
        raise (HTTPException( status_code= 409, detail="User already exist"))
    fake_db[user.id]=user
    return user
    
    