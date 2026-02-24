from fastapi import FastAPI, BackgroundTasks
from app.routers import user


app = FastAPI()

app.include_router(user.router)

