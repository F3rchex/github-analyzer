import requests
#importamos libreria para peticiones HTTP
import json

from src.config import GITHUB_TOKEN, GITHUB_API_URL

class GitHubClient:
    def __init__(self):
        self.base_url = GITHUB_API_URL
        self.headers = {
            'Authorization': f'Bearer {GITHUB_TOKEN}',
            #opcional pero es buena practica indicar el formato de respuesta
            'Accept': 'application/vnd.github.v3+json'
        }
        
    def get_repo_info(self, owner, repo_name):
        # Solo busca información, NO guarda
        url = f'{self.base_url}/repos/{owner}/{repo_name}'

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error al obtener información del repositorio {e}')
            return None

    def save_repository(self, owner, repo_name):
        # Busca Y guarda el repositorio
        repo_data = self.get_repo_info(owner, repo_name)

        if repo_data:
            repo_data['owner'] = owner
            repo_data['repo_name'] = repo_name
            self.save_json(repo_data)
            return repo_data

        return None
        
        
    def get_repo_languages(self, owner, repo_name):
        url = f'{self.base_url}/repos/{owner}/{repo_name}/languages'
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'No se pudieron obtener los lenguajes del repositorio')
            return None
        
        
    def save_json(self, repo_data):
        file_path = "data/repositories.json"
        try:
            #Primero intentamos leer los datos existentes, si hay.
            with open(file_path, "r") as file:
                repo_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            repo_list = []
        #obtenemos el nombre y propietario del repositorio para ver si ya esta en el archivo  
        repo_id = f'{repo_data.get('owner')}/{repo_data.get('name')}'
        existing_repo = [repo for repo in repo_list if f'{repo.get('owner')}/{repo.get('name')}' == repo_id]
        
        if existing_repo:
            repo_list.remove(existing_repo[0])
            repo_list.append(repo_data)
            print(f'Repositorio {repo_id} actualizado.')
        else:
            repo_list.append(repo_data)
            print(f'Repositorio {repo_id} agregado correctamente.')
        
        
        #Guardamos todos los datos  
        with open(file_path, "w") as file:
            json.dump(repo_list, file, indent=4)
            
        
            
    # def load_json(self, response):
    #     file_response = "data_response.json"
    #     with open(file_response, "r") as file:
    #         recovered_data = json.load(file)
    #         file_response.clear()
    #         file_response.extend(recovered_data)
    #     print(f"Datos recuperados")