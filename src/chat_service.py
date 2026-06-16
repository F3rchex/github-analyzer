import json
from src.openai_client import OpenAIClient
from datetime import datetime

class ChatService:
    def __init__(self):
        self.openai_client = OpenAIClient()
        #historial de conversacion
        self.messages = []
        
    def load_repositories(self):
        file_path = "data/repositories.json"
        
        try:
            with open(file_path, "r") as file:
                repos = json.load(file)
                return repos
        except (FileNotFoundError, json.JSONDecodeError):
            print(f'No se encontraron repositorios. Ejecuta primero la opcion de actualizar repositorios')
            return []
    
    #convertimos json en texto para el mensaje system del LLM
    def build_context(self, repos):
        if not repos:
            return "Aun no tienes repositorios guardados"
        
        context = "Tienes acceso a los siguientes repositorios de Github:\n"
        
        for i, repo in enumerate(repos, 1):
            name = repo.get('name', 'Desconocido')
            language = repo.get('language', 'No especificado')
            stars = repo.get('stargazers_count', 0)
            description = repo.get('description', 'Sin descripción')
            
            context += f'{i} {name}\n'
            context += f"   - Lenguaje: {language}\n"
            context += f"   - Stars: {stars}\n"
            context += f"   - Descripción: {description}\n\n" 
            
            
        return context
    
    def start_conversation(self):
        repos = self.load_repositories()
        context = self.build_context(repos)
        #Opcional, le damos 'context' para que sepa que datos tenemos, tambien podriamos indicar solo el comportamiento que queremos que tenga.
        system_message = {
            "role": "system",
            "content": f'{context}\n\nEres un asistente que ayuda a analizar estos repositorios. Responde de forma clara y concisa.'
        }
        
        #Agregamos al historial
        self.messages.append(system_message)
        
    def chat(self, user_message):
        #Agregamos mensaje del usuario al historial
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        #Llamamos a OpenAI con streaming
        stream = self.openai_client.chat_stream(
            messages=self.messages,
            temperature=0.75,
            max_tokens=700
        )
        
        #Variable para acumular la respuesta completa
        full_response = ""
        
        #Iteramos sobre el streaming
        for chunk in stream:
            full_response += chunk
            yield chunk     #Devolvemos cada pedazo para mostrar en pantalla
            
        #Agregamos respuesta completa del bot al historial
        self.messages.append({
            "role": "assistant",
            "content": full_response
        })
        
    def save_conversation(self):
        #Generamos nombre de archivo con fecha y nombre
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data/conversations/session_{timestamp}.json"
        
        #Guardamos el historial
        with open(filename, "w") as file:
            json.dump(self.messages, file, indent=4)
        
        print(f"Conversación guardada correctamente en {filename}")
        
        