from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

from prompts import PROMPT_TRIAJE

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

def realizar_triaje(pregunta):

    prompt = f"""
        {PROMPT_TRIAJE}

        Pregunta:

        {pregunta}
    """

    respuesta = llm.invoke(prompt)

    return respuesta.content.strip()

if __name__ == "__main__":

    preguntas = ["Cuales son los derechos del paciente", 
                 "Cual es el horario de visitas", 
                 "Donde puedo presentar un reclamo"]
    
    for pregunta in preguntas:
        print("*"*30)
        print(pregunta)
        print()
        print(realizar_triaje(pregunta))