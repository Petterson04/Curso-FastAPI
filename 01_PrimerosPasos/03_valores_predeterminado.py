from enum import Enum
from fastapi import FastAPI

class CarDealer(Enum):
    HONDA = "Honda"
    Ford="Ford"
    BMW = "BMW"

app= FastAPI()

#Endpoint que devuelve la informacion del concesianorio de autos segun el car_dealer que se pase como parametro
@app.get("/models/{car_dealer}")
async def get_model(car_dealer: CarDealer):
    if car_dealer is CarDealer.HONDA:
        return{"car_dealer": car_dealer, "message": "Honda es conocido por su fiabilidad y eficiencia de combustible."}
    if car_dealer is CarDealer.Ford:
        return{"car_dealer": car_dealer, "message": "Ford es famoso por su durabilidad y diseño."}
    
    return{"car_dealer": car_dealer, "message": "BMW es famoso por su rendimiento y lujo."}