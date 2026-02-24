#After
#Before 
#Wrap

from typing_extensions import Self
from pydantic import BaseModel, model_validator

class Usermodel(BaseModel):
    username: str
    password:str
    password_repeat:str
    
    @model_validator(mode="after")
    def chek_password(self)-> Self:
        if self.password != self.password_repeat:
            raise ValueError("Password not match")
        return self
    
usuario1:Usermodel= Usermodel(username="Jorge", password="123", password_repeat="123")            