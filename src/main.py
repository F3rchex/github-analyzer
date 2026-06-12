from src.github_client import GitHubClient

def main():
    #creamos instancia del cliente
    client = GitHubClient()
    
    #pedimos datos al usuario
    print("=== Github Repository Analyzer ===\n")
    owner = input('Ingresa el owner del repositorio\n')
    repo_name = input('Ingresa el nombre del repositorio\n')
    
    #obtener informacion del repo
    print(f'\nObteniendo información de {owner}/{repo_name}...\n')
    repo_info = client.get_repo_info(owner, repo_name)
    
    #verificamos si hubo error
    if repo_info is None:
        print(f'No se pudo obtener información del repositorio')
        return
    
    #En caso que no haya error..
    print(f'=== INFORMACIÓN DEL REPOSITORIO ===\n')
    print(f'Nombre: {repo_info['name']}\n')
    print(f'Descripcion: {repo_info['description']}\n')
    print(f'Estrellas: {repo_info['stargazers_count']}\n')
    print(f'Forks: {repo_info['forks_count']}\n')
    print(f'Lenguaje principal: {repo_info['language']}\n')
    
    #obtenemos los lenguajes
    print(f'=== LENGUAJES UTILIZADOS ===\n')
    languages = client.get_repo_languages(owner, repo_name)
    
    if languages:
        for lang, bytes_code in languages.items():
            print(f'{lang}: {bytes_code} bytes')
    else:
        print(f'No se pudieron obtener los lenguajes')
        
        
if __name__ == '__main__':
    main()
    