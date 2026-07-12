from typing import TypedDict
from rag import responder_pregunta
from triaje import realizar_triaje

class EstadoAgente(TypedDict):
    pregunta: str
    decision: str
    respuesta: str

    def nodo_rag(state):

        respuesta = responder_pregunta(
            state["pregunta"]
        )

        return {
            "respuesta": respuesta
        }
    
    def nodo_triaje(state):

        respuesta = realizar_triaje(
            state["pregunta"]
        )

        return {
            "respuesta": respuesta
        }