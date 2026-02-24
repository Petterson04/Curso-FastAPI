from typing import Annotated
from fastapi import Depends, FastAPI, Query, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager

#Modelo base 

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None= Field (default=None, index=True)
#MODELO DB
class Hero(HeroBase,table= True):
    id: int | None = Field( default=None, primary_key=True)
    secret_name: str
#MODELO PUBLICO 

class HeroPublic(HeroBase):
    id:int 
 #MODELO DE CREACION
class HeroCreate(HeroBase):
    secret_name: str
    
#MODELO DE ACTUALIZACION
class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None= None
    secret_name: str | None = None

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

#GET 
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heros(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated [int, Query(le=100)]=100
):
    heroes= session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

#Get hero por id
@app.get("/heroes/{hero_id}", response_model= HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero= session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

#POST
@app.post("/heroes/", response_model=HeroPublic)
def createHero(hero: HeroCreate, session: SessionDep):
    db_hero= Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

#Actualizar 
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def updateHero( hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_id:
        HTTPException (status_code=404, detail="Hero not found")
    hero_data= hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

#DELETE
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id:int, session: SessionDep):
    hero= session.get(Hero, hero_id)
    if not hero:
        HTTPException (status_code=404, detail="Heroe not found")
    session.delete(hero)
    session.commit()
    return {"ok":True}
    
        
        
