#  GITHUB AI ASSISTANT

Asistente inteligente que combina **GitHub API**, **OpenAI**, y **Web Scraping** para analizar repositorios, consultar trending repos, y responder preguntas sobre proyectos de GitHub mediante un chatbot con function calling.

---

##  Descripción

**GitHub AI Assistant** es un proyecto evolutivo que integra múltiples tecnologías para interactuar con repositorios de GitHub de forma inteligente:

- **Consume GitHub API** para obtener información detallada de repositorios (estrellas, forks, lenguajes, descripción)
- **Chatbot con IA** que responde preguntas sobre repos guardados usando OpenAI GPT-4
- **Function calling** para que el LLM pueda buscar, guardar y consultar repos en tiempo real
- **Web scraping** para extraer repositorios trending (datos no disponibles en la API oficial)
- **API REST** con FastAPI para integración con sistemas externos
- **Automatización con n8n** para sincronización semanal y reportes por email

---

##  Funcionalidades principales

###  **CLI Interactivo**
1. **Buscar y guardar repositorios** - Consume GitHub API y almacena datos localmente
2. **Chatbot inteligente** - Conversación natural con IA sobre tus repos guardados
3. **Trending repos** - Scraping de repositorios en tendencia por lenguaje y periodo

###  **Chatbot con Function Calling**
El LLM puede ejecutar funciones automáticamente según la intención del usuario:
- `load_repositories` - Lista todos los repos guardados localmente
- `get_repo_info` - Busca información de un repo específico (sin guardar)
- `save_repository` - Busca y guarda un repo en la base de datos local
- `get_trending_repos` - Obtiene repos trending mediante scraping (por lenguaje y periodo)

### 🌐 **API REST**
Endpoints con FastAPI para integración externa:
- `GET /repositories` - Lista repos guardados
- `POST /repositories` - Guarda un nuevo repo
- Documentación automática en `/docs` (Swagger)

###  **Automatización con n8n**
Workflow programado que se ejecuta semanalmente:
- Sincroniza repos específicos automáticamente
- Actualiza información de repos existentes
- Genera reporte con análisis del LLM
- Envía reporte por email (Gmail)

---

##  Tecnologías utilizadas

| Categoría | Tecnología | Propósito |
|-----------|------------|-----------|
| **Lenguaje** | Python 3.14 | Core del proyecto |
| **APIs** | GitHub REST API | Obtener datos de repositorios |
| | OpenAI API (GPT-4) | Chatbot inteligente y function calling |
| **Web Scraping** | BeautifulSoup4 | Parseo de HTML para trending repos |
| | lxml | Parser rápido para BeautifulSoup |
| **Web Framework** | FastAPI | API REST endpoints |
| | Uvicorn | Servidor ASGI para FastAPI |
| **Automatización** | n8n (self-hosted) | Workflows programados y webhooks |
| **Otros** | python-dotenv | Gestión de variables de entorno |
| | requests | Cliente HTTP para APIs |

---

## 📁 Estructura del proyecto

```
github-analyzer/
├── src/
│   ├── config.py              # Variables de entorno (GitHub + OpenAI tokens)
│   ├── github_client.py       # Cliente para GitHub API
│   ├── openai_client.py       # Cliente para OpenAI API
│   ├── chat_service.py        # Lógica del chatbot con function calling
│   ├── scraper.py             # Web scraper para trending repos
│   ├── api.py                 # API REST con FastAPI
│   ├── api_models.py          # DTOs de Pydantic para FastAPI
│   └── main.py                # CLI con menú interactivo
├── data/
│   ├── repositories.json      # Repos guardados localmente
│   └── conversations/         # Historial de conversaciones del chatbot
├── n8n/
│   └── workflow.json          # Workflow de sincronización semanal
├── requirements.txt           # Dependencias del proyecto
├── .env                       # API keys (no incluido en git)
├── .gitignore                 # Archivos ignorados por git
└── README.md                  # Documentación del proyecto
```

---

##  Instalación y configuración

### 1. **Clonar el repositorio**
```bash
git clone https://github.com/F3rchex/github-analyzer.git
cd github-analyzer
```

### 2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Configurar variables de entorno**
Crea un archivo `.env` en la raíz del proyecto:
```env
# GitHub API
GITHUB_TOKEN=ghp_tu_token_aqui

# OpenAI API
OPENAI_API_KEY=sk-tu_api_key_aqui
```

**Obtener tokens:**
- **GitHub:** https://github.com/settings/tokens (Permisos: `public_repo`)
- **OpenAI:** https://platform.openai.com/api-keys

---

##  Uso

### **CLI Interactivo**

```bash
python -m src.main
```

**Menú:**
```
=== ¿Qué quieres realizar? ===
1. Buscar información de repositorio
2. Consultar con Chatbot
3. Obtener repositorios en tendencia (Scraping)
0. SALIR
```

### **Ejemplos de uso del Chatbot**

El chatbot usa **function calling** para ejecutar acciones automáticamente:

```
Tú: ¿Qué repos tengo guardados?
Bot: [Llama a load_repositories() automáticamente]

Tú: Busca información de facebook/react
Bot: [Llama a get_repo_info("facebook", "react")]

Tú: Guarda el repo de microsoft/vscode
Bot: [Llama a save_repository("microsoft", "vscode")]

Tú: ¿Cuáles son los repos trending de Python hoy?
Bot: [Llama a get_trending_repos(language="python", since="daily")]

Tú: Dame el trending de las últimas 24h
Bot: [Llama a get_trending_repos(language="", since="daily")]
```

### **API REST**

Iniciar servidor FastAPI:
```bash
uvicorn src.api:app --reload
```

Documentación Swagger: http://localhost:8000/docs

### **Scraper independiente**

```bash
python src/scraper.py
```

---

##  Tools disponibles del chatbot

| Tool | Descripción | Parámetros | Cuándo se llama |
|------|-------------|------------|-----------------|
| `load_repositories` | Lista repos guardados | Ninguno | "¿Qué repos tengo?", "Lista mis repositorios" |
| `get_repo_info` | Busca info de un repo (sin guardar) | `owner`, `repo_name` | "Busca info de facebook/react" |
| `save_repository` | Busca y guarda un repo | `owner`, `repo_name` | "Guarda el repo de microsoft/vscode" |
| `get_trending_repos` | Obtiene trending mediante scraping | `language` (opcional), `since` (opcional) | "Trending de Python hoy", "Repos populares esta semana" |

**Valores de `since`:** `daily`, `weekly`, `monthly`

---

##  Dependencias

```txt
requests==2.31.0           # Cliente HTTP para consumir APIs
python-dotenv==1.0.0       # Cargar variables de entorno desde .env
openai==1.54.0             # Cliente oficial de OpenAI para GPT-4
beautifulsoup4==4.15.0     # Parseo de HTML para web scraping
lxml==6.1.1                # Parser XML/HTML rápido
fastapi                    # Framework web moderno para APIs REST
uvicorn                    # Servidor ASGI para FastAPI
```

---

##  Workflow de n8n

**Sincronizador Semanal de Repos**

- **Trigger:** Cada domingo a las 23:00
- **Acciones:**
  1. Llama a la API local para guardar repos específicos (react, vue, vscode)
  2. Loop sobre cada repo para actualizar datos
  3. Genera reporte con LLM sobre cambios detectados
  4. Envía reporte por Gmail

**Tecnologías:**
- Docker para n8n self-hosted
- HTTP Request nodes para llamar a FastAPI
- Code nodes (JavaScript) para transformar datos
- Gmail OAuth2 para envío de emails


---

##  Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.


