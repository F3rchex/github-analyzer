from pydantic import BaseModel


#Para recibir mensajes del usuario
class ChatRequest(BaseModel):
    message:str

#Para devolver la respuesta del chatbot    
class ChatResponse(BaseModel):
    response:str #Respuesta del LLM
    
class RepositoryRequest(BaseModel):
    owner:str
    repo_name:str