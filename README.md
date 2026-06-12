###GITHUB-ANALYZER

##Arquitectura del proyecto

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