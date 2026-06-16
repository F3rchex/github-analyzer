from src.openai_client import OpenAIClient

# Crear el cliente
client = OpenAIClient()

# Definir un mensaje simple de prueba
messages = [
    {"role": "system", "content": "Eres un asistente útil y conciso."},
    {"role": "user", "content": "Explícame en 3 líneas qué es Javascript."}
]

print("=== Probando streaming ===\n")
print("Respuesta del bot: ", end='')

# Llamar al método chat_stream
for palabra in client.chat_stream(messages):
    print(palabra, end='', flush=True)

print("\n\n=== Prueba completada ===")