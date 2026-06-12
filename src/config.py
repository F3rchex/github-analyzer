import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Variables de configuración
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_API_URL = 'https://api.github.com'

# Validación: asegurar que el token existe
if not GITHUB_TOKEN:
    raise ValueError(
        "GITHUB_TOKEN no está configurado. "
        "Por favor, añade tu token en el archivo .env"
    )
