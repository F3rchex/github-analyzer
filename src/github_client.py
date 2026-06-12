import requests
#importamos libreria para peticiones HTTP

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
        url = f'{self.base_url}/repos/{owner}/{repo_name}'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error al obtener información del repositorio {e}')
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