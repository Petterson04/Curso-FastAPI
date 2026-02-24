#OAuth2 Flujo de pwd -> Bearer Token
# Front( username+password ) -> Back( Bearer Token ) -> API Resource 

from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

oauth2_Scheme:OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

app.get("/items/")
async def read_items(token: Annotated [str, Depends(oauth2_Scheme)]):
    return {"token": token}


