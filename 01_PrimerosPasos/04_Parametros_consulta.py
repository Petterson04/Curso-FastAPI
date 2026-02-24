from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

#Dicciionario de coches para simular una base de datos
cars_list: list[dict]=[
    {"car_name": "I10"},
    {"car_name": "Swift"},
    {"car_name": "Creta"},
    {"car_name": "Tiguan"},
    {"car_name": "Polo"},
    {"car_name": "XUV700"},
    {"car_name": "Fortuner"}
    
]

class Car(BaseModel):
    car_name:str
    
@app.get("/cars/")
async def get_cars(skip: int=0, limit: int=10,):
    return cars_list[skip : skip + limit]

@app.post("/cars/")
async def create_car(car: Car):
    cars_list.append(car.model_dump())
    return {"mensaje": "Coche añadido correctamente", "datos_coche": car}