from src.github_client import GitHubClient
from src.chat_service import ChatService

def buscar_repositorio():
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
        



def consultar_chatbot():
    service = ChatService()
    
    print(f"\nIniciando conversación... ")
    
    #Iniciar conversación (carga repos y construye contexto)
    service.start_conversation()
    print("Listo, escribe 'salir' para terminar la conversación\n")
    
    #Loop de conversación
    while True:
        user_input = input("Tú: ")
        
        if user_input.lower() in ['salir', 'exit', 'fin', 'quit']:
            print(f"\nCerrando chat...")
            service.save_conversation()
            break
        
        if not user_input.strip():
            continue
        
        print(f"Bot: ", end='', flush=True)
        for chunk in service.chat(user_input):
            print(chunk, end='', flush=True )
        print(f"\n")    #Nueva linea de respuesta
    
    
    
    
    
    
    
    
def main():
    while True:
        print(f"=== ¿Que quieres realizar? ===\n")
        print(f"1. Buscar información de repositorio\n")
        print(f"2. Consultar con Chatbot\n")
        print(f"0. SALIR\n")
        try:
            opcion = int(input("Elige una opción\n"))
            match opcion:
                case 1:
                    buscar_repositorio()
                case 2:
                    consultar_chatbot()
                case 0:
                    break
                case __:
                    print(f"La opción no es valida")
        except ValueError:
            print(f"El formato debe ser un numero, por favor intentelo de nuevo")
        
        
                  
if __name__ == '__main__':
    main()
    