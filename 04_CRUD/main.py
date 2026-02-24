from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional
from itertools import count

id_generator= count(start=1)

def obtener_nuevo_id()->int:
    return next (id_generator)
    

class TareaBase(BaseModel):
    titulo: Annotated[str,Field(min_length=3)]
    estado: Literal["pendiente", "completado"]= "pendiente"
    

class Tarea(TareaBase):
    id: Annotated[int, Field(gt=0)]
    
class CrearTarea(TareaBase):
    pass

class EditarTarea(BaseModel):
    titulo: Annotated[str,Field(min_length=3)]
    estado: Literal["pendiente", "completado"]
    



fake_db: list[tarea]=[
    Tarea(id=obtener_nuevo_id(), titulo= "Lavar la ropa", estado= "completado"),
    Tarea(id=obtener_nuevo_id(), titulo= "Estudiar Python", estado= "pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo= "Leer un libro", estado= "pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo= "Ir al gimnasio", estado= "completado"),
    Tarea(id=obtener_nuevo_id(), titulo= "Comprar comida", estado= "pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo= "Limpiar el cuarto", estado= "pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo= "Pagar cuentas", estado= "completado"),
    Tarea(id=obtener_nuevo_id(), titulo= "Llamar a mamá", estado= "pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo= "Revisar correo", estado= "pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo= "Lavar carro", estado= "pendiente"),
]

class FilterParams(BaseModel):
    limit: Annotated[int, Field(ge1)]=5
    offset: Annotated[int, Field(ge=0)]=0
    estado: Literal["pendiente", "completado"] |None = None
    buscador: str|None=None


app= FastAPI()

@app.get("/tareas/", response_model=list[Tarea])
async def get_tareas(fiel_query:Annotated[FilterParams,Query()]):
#    if fiel_query:
#        tareas_filtradas= [tarea for tarea in fake_db if tarea.estado == fiel_query.estado]
#    else:
#        tareas_filtradas=fake_db

    tareas_filtradas=([
        tarea for tarea in fake_db if tarea.estado == fiel_query.estado] if fiel_query.estado else fake_db   
                )
#Intento de buscador
    if fiel_query.buscador:
        tareas_filtradas= [
            t for t in tareas_filtradas if fiel_query.buscador.lower() in t.titulo.lower()
        ]
        
        

    return tareas_filtradas[fiel_query.offset: fiel_query.offset + fiel_query.limit]

@app.get("/tareas/{id}", response_model=Tarea)
def get_tarea_id(id:int):
    for tarea in fake_db:
        if tarea.id == id:
            return tarea 
    raise HTTPException(status_code=404, detail="tarea no encontrada")

@app.post("/tareas/", response_model=Tarea, status_code=201)
def crear_tarea(tarea:CrearTarea):
    nuevo_id: int = obtener_nuevo_id()
    nueva_tarea:Tarea= Tarea(id=nuevo_id, **tarea.model_dump())
    fake_db.append(nueva_tarea)
    return nueva_tarea 

@app.put("/tareas/{id}", response_model=Tarea)
def editar_tarea(id: int, datos: EditarTarea):
    for i,tarea in enumerate(fake_db):
        if tarea.id== id:
            tarea_actualizada= tarea.model_copy(update= datos.model_dump())
            fake_db[i]= tarea_actualizada
            return tarea_actualizada
    raise HTTPException (status_code=404, detail="Tarea no encontrada")

@app.delete("/tareas/{id}",status_code=204)
def eliminarTarea(id:int):
    for i,t in enumerate(fake_db):
        if t.id == id:
            del fake_db[i]
            return
        
    raise HTTPException (status_code=404, detail="tarea no encontrada")
    
    