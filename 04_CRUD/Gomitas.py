from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field


app = FastAPI()


class Cuenta(BaseModel):
    titular: str = Field()
    saldo: float = Field()
    pedido: str = Field()
    id: int = Field()

