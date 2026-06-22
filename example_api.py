from fastapi import FastAPI
from pydantic import BaseModel

#Creamos la app
app = FastAPI()

#Modelo de datos
class Message(BaseModel):
    text:str
    author:str
    
    
#Endpoint GET
@app.get("/")
def home():
    return {"message": "API funcionando"}

#Endpoint con parametro
@app.get("/hello/{name}")
def hello(name):
    return {"greeting": f"Hola {name}!"}

#Endpoint con POST
@app.post("/messages")
def create_message(message: Message):
    return{
        "status":"recibido",
        "content": message.text,
        "from": message.author
    }