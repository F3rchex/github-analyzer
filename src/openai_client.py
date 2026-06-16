from openai import OpenAI
from src.config import OPENAI_API_KEY
from datetime import datetime
import json

class OpenAIClient:
    def __init__(self):
        #Creamos el cliente usando la API KEY
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-4o-mini"
        
    def chat(self, messages, temperature=0.75, max_tokens=750):
        #llamamos a la API de OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        #Devolvemos el contenido de la respuesta
        return response.choices[0].message.content
    
    def chat_stream(self, messages, temperature=0.75, max_tokens=750):
        #Llamamos a la API con el stream activado
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )
        
        #Devolvemos cada pedazo de texto que va generando
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    