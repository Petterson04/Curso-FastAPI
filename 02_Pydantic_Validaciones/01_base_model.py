from fastapi import FastAPI 
from pydantic import BaseModel

class User(BaseModel):
    id:int
    nombre:str
    edad:int | None = None
    email:str
    activo:bool

app=FastAPI()

@app.get("/users/")
def read_users():
    ...


#Crear un nuevo usuario (endpoint POST) se usa para crear recusrsos usandoido la clase usuario que definimos en la parte inicial
@app.post("/users/")
def create_user(user:User):
    return {"mensaje": f"Usuario creado correctamente {user.nombre.capitalize()}", "datos_usuario": user}

#endpoint para actualizar un usuario (PUT) que recibe el ID del usuario a actualizar y los nuevos datos del usuario 
@app.put("/users/{user_id}")
def update_user(user_id:int, user:User, q: str |None=None):
    result:dict= {
        "user_id": user_id,
        **user.model_dump()
        
    }
    if q:
        result.update({"q":q})
    return result