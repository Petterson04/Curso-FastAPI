from fastapi import FastAPI

app= FastAPI() 

# Endpoint raíz que devuelve un mensaje de bienvenida

@app.get("/")
async def root():
    return {"message": "¡Hola, FastAPI!"}