### GITHUB-ANALYZER

## Arquitectura del proyecto

github-analyzer/
├── .env                    # Credenciales (NUNCA en git)
├── .gitignore             # Qué ignorar en git
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Documentación
├── src/
│   ├── __init__.py       # Marca src como paquete Python
│   ├── config.py         # Carga variables de entorno
│   ├── github_client.py  # Lógica de llamadas a API
│   └── main.py           # Punto de entrada

Separamos responsabilidades: config, cliente API, y lógica principal están separados

## Descripcion

Github Analyzer es un proyecto el cual nos permite obtener información de cualquier repositorio alojado en GITHUB, aportando la información necesaria (owner-nombre-repositorio) se realiza un consulta API.

## Funcionamiento

- Asegurarse de activar el entorno virtual en local:

    source venv/bin/activate

- Ejecutar el modulo para correrlo en local:

    python3 -m src.main

