import requests
from bs4 import BeautifulSoup 
from typing import List, Dict


class GitHubScraper:
    BASE_URL = "https://github.com/trending"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-agent': 'Mozilla/5.0'
        })
    
    def _parse_repo_article(self, article) -> Dict:
        try:
            h2 = article.find('h2', class_='h3')
            link = h2.find('a')
            
            #Extraer owner y name del href
            full_name = link['href'].strip('/')  # Ejemplo: "microsoft/vscode"
            owner, repo_name = full_name.split('/')
            
            #Extraer descripción
            description_element = article.find('p', class_='col-9')
            description = description_element.get_text(strip=True) if description_element else ""
            
            #Extraer lenguaje
            language_element = article.find('span', itemprop='programmingLanguage')
            language = language_element.get_text(strip=True) if language_element else "Unknown"
        
            # 5. Devolver diccionario
            return {
                'owner': owner,
                'name': repo_name,
                'full_name': full_name,
                'description': description,
                'language': language,
                'url': f"https://github.com/{full_name}"
            }
        except Exception as e:
            print(f"Error parseando articulo: {e}")
            return None
    
    def get_trending_repos(self, language="", since="daily"):
        #Construimos URL
        url = f"{self.BASE_URL}/{language}?since={since}"
        
        try:
            response = self.session.get(url, timeout=10)
            #Lanza una excepción si el status HTTP es 4xx o 5xx (como 404, 500).
            response.raise_for_status()
            
            
            #Parseamos HTML con BeautifulSoup
            soup = BeautifulSoup(response.text, 'lxml')
            #Buscamos todos los repos
            articles = soup.find_all('article', class_='Box-row')
            repos = []
            
            for article in articles:
                repo_data = self._parse_repo_article(article)
                if repo_data:
                    repos.append(repo_data)
                
            return repos
        except requests.RequestException as e:
            print(f"Error al hacer scraping: {e}")
            return []
        
        