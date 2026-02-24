from fastapi import FastAPI
import time
import asyncio

app= FastAPI()
#Bloquea y se pausa la ejecucion de la funcion 
#procesando en el main thread
#llega la primera reequest y ya que finaliza se empieza a porcesar la segunda request, por lo que se bloquea el proceso
@app.get("/async-sin-await")
async def async_sin_await():
    print("HOLA")
    time.sleep(5)
    print("ADIOS")
#No se bloquea el main thread 
#La funcion se pausa para esperar el await 
#las funciones se ejecutan en el mismo tiempo de ejecucion no es necesario esperar a que termina la primera request
#Existe la concurrencia 

@app.get("/async-con-await")
async def async_con_await():
    print("HOLA")
    await asyncio.sleep(5)
    print("ADIOS")
#Lo corre en un segundo hilo para que no afecte el main thread 
#Puede manda peticiones a distintos hilos para que se puedan hacer en paralelo 

@app.get("/sync")
def sync():
    print("HOLA")
    time.sleep(5)
    print("ADIOS")