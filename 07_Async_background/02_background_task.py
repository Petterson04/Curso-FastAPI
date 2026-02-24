from fastapi import FastAPI, BackgroundTasks
import time
app= FastAPI()

def write_notification(email:str, message=""):
    time.sleep(4)
    with open("log.txt", mode="w") as emai_file:
        content = f"NOtificaciones para {email}: {message}"
        emai_file.write(content)
    print("termino la tarea")
        
@app.post("/send-notification/{email}")
async def send_notification(email: str, background_task: BackgroundTasks):
    background_task.add_task(
        write_notification, email, message= "alguna notificvacion "
    )
    return {"message": "Tarea mandada a segundo plano"}