#after corre despues de las validaciones de pydantic 
#before corre antes de las validaciones/transformaciones de pydantic
#Plain  similar a before termina al retornar el valor 
# Wrap flexible se puede correr antes o despues de las validaciones de pydantic
from typing import Annotated

from pydantic import AfterValidator, BaseModel, field_validator

#Annotated
def es_par(value:int)-> int:
    if value %2 ==1:
        raise ValueError(f"{value} no wa numero par")
    return value
    
    
NumeroPar = Annotated [int, AfterValidator(es_par)]


class Model1(BaseModel):
  myNumber: NumeroPar

#ejemplo: Model1= Model1(myNumber=2)  
    
class Model2(BaseModel):
    other_numbre:Annotated[NumeroPar, AfterValidator(lambda v: v+2)]    
#ejemplo2:Model2= Model2(other_numbre=4)
#print(ejemplo2)


class Model3(BaseModel):
    lista_pares:list[NumeroPar]
#ejemplo3:Model3= Model3(lista_pares=[2,4,6,8,41,12])

#----------------------------- DECORATOR------------------

class item(BaseModel):
    item_id: int
    price: float
    
    @field_validator("item_id", "price")
    def check_positive(cls, value: int):
            if value<0:
                raise ValueError("Item ID debe de ser positivo")
            return value

banana:item= item(item_id=2,price=-25.51)

