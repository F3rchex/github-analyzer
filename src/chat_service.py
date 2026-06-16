import json
from src.openai_client import OpenAIClient
from datetime import datetime
from src.github_client import GitHubClient

class ChatService:
    def __init__(self):
        self.openai_client = OpenAIClient()
        #historial de conversacion
        self.messages = []
        self.github_client = GitHubClient()
        
    def load_repositories(self):
        file_path = "data/repositories.json"
        
        try:
            with open(file_path, "r") as file:
                repos = json.load(file)
                return repos
        except (FileNotFoundError, json.JSONDecodeError):
            print(f'No se encontraron repositorios. Ejecuta primero la opcion de actualizar repositorios')
            return []
    
    #convertimos json en texto para el mensaje system del LLM, NECESARIO
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
        #1. Agregar mensaje del usuario
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        #2. Obtener tools disponibles
        tools = self.get_available_tools()
        
        #3. Llamar a OpenAI con tools
        response_message = self.openai_client.chat_with_tools(
            messages=self.messages,
            tools=tools
        )
        
        #4. Revisar si hay tool_calls
        if response_message.tool_calls:
            #5. Agregar mensaje assistant con tool_call al historial
            self.messages.append(response_message)
            
            #6. Ejecutar cada función llamada
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                #7. Ejecutar la función
                function_result = self.execute_function(function_name, arguments)
                
                #8. Agregar resultado como mensaje tool
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(function_result)
                })
            
            #9 . Llamar a OpenAI de nuevo con los resultados
            final_response = self.openai_client.chat_with_tools(
                messages=self.messages,
                tools=tools
            )
            
            #10. Agregar respuesta final al historial
            self.messages.append(final_response)
            
            #11. Devolver el contenido
            return final_response.content
        
        else:
            # No hubo tool_calls, respuesta directa
            self.messages.append(response_message)
            return response_message.content
        
    def save_conversation(self):
        #Generamos nombre de archivo con fecha y nombre
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data/conversations/session_{timestamp}.json"
        
        # Convertir mensajes a diccionarios serializables
        messages_to_save = []
        for msg in self.messages:
            if hasattr(msg, 'model_dump'):  # Es objeto de OpenAI
                messages_to_save.append(msg.model_dump())
            else:  # Ya es dict (mensaje system o user)
                messages_to_save.append(msg)
        
        # Guardar el historial
        with open(filename, "w") as file:
            json.dump(messages_to_save, file, indent=4)
        
        print(f"Conversación guardada correctamente en {filename}")
        
    
    def get_available_tools(self):
        #Devuelve la lista de funciones disponibles para el LLM
        return [
                {
                    "type": "function",
                    "function": {
                        "name": "load_repositories",
                        "description": "Obtiene la lista completa de repositorios guardados localmente con toda su información (nombre, estrellas, lenguaje, descripción).",
                        "parameters": {
                            "type": "object",
                            "properties": {},  # ← Vacío porque no necesita parámetros
                            "required": []
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_repo_info",
                        "description": "Busca información de un repositorio publico de Github, Devuelve nombre, descripcion, estrellas, lenguaje, etc. ",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "owner": {
                                    "type":"string",
                                    "description": "El dueño del repositorio (Ej: 'facebook', 'microsoft')"
                                },
                                "repo_name":{
                                    "type": "string",
                                    "description": "El nombre del repositorio (Ej: 'react', 'vscode')"
                                }
                            },
                            "required": ["owner", "repo_name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "save_repository",
                        "description": "Busca un repositorio en GitHub y lo guarda en la lista local. Si ya existe, lo actualiza.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "owner": {
                                    "type":"string",
                                    "description": "El dueño del repositorio (Ej: 'facebook', 'microsoft')"
                                },
                                "repo_name":{
                                    "type": "string",
                                    "description": "El nombre del repositorio (Ej: 'react', 'vscode')"
                                }
                                },
                            "required": ["owner", "repo_name"]
                        }
                    }
                }
        ]
        
    #Segun el nombre de la funcion se ejecuta el código correspondiente
    def execute_function(self, function_name, arguments):
        if function_name == "load_repositories":
            result = self.load_repositories()
            return result
        elif function_name == "get_repo_info":
            result = self.github_client.get_repo_info(arguments["owner"], arguments["repo_name"])
            return result
        elif function_name == "save_repository":
            result = self.github_client.save_repository(arguments["owner"], arguments["repo_name"])
            return result
        else:
            return {"error": f"Función {function_name} no encontrada"}