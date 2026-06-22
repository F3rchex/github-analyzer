from fastapi import FastAPI
from src.chat_service import ChatService
from src.api_models import ChatRequest, ChatResponse, RepositoryRequest
from src.github_client import GitHubClient

app = FastAPI()

#Instancias de los servicios
github_client = GitHubClient()


#Creamos nueva instancia para que el historial no sea compartido entre usuarios y que cada request sea independiente
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    chat = ChatService()
    chat.start_conversation()
    respuesta = chat.chat(request.message)
    return ChatResponse(response=respuesta)

@app.get("/repositories")
def get_repositories():
    chat_service = ChatService()
    repos = chat_service.load_repositories()
    return {"repositories":repos}

@app.post("/repositories")
def add_repository(request: RepositoryRequest):
    repo = github_client.save_repository(request.owner, request.repo_name)
    if repo is None:
        return {"status":"error","message":"No se pudo guardar el repositorio"}
    
    return {"status":"Guardado", "repo":f"{request.owner}/{request.repo_name}"}
