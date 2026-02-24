from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session
from contextlib import asynccontextmanager

class Hero(SQLModel, table= True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None= Field (default=None)
    secret_name: str

sqlite_file_name = "database.db"
sqlite_url= f"sqlite:///{sqlite_file_name}"
engine= create_engine (
    sqlite_url,
    connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
#Crear session y dependencia
def get_session():
    with Session(engine) as session:
        yield session

SessionDep= Annotated [Session, Depends (get_session)]

#Lifespand Events 
@asynccontextmanager
async def lifespan(app: FastAPI):
    #Codigo que se ejecutara antes de iniciar el servidor
    create_db_and_tables()
    yield
    #Codigo que se ejecutara despues de cerrar el servidor

app= FastAPI(lifespan=lifespan)

