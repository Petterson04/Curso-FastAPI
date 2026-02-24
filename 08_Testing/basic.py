from fastapi import FastAPI, BackgroundTasks
from fastapi.testclient import TestClient
app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "HELLO WORD"}

client= TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code==200
    assert response.json() == {"msg": "HELLO WORD"}