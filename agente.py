from typing import TypedDict
from rag import responder_pregunta,inicializar
from triaje import realizar_triaje
from langgraph.graph import StateGraph, START, END


class EstadoAgente(TypedDict):
    pregunta: str
    decision: str
    respuesta: str

def nodo_rag(state):

    print("Nodo RAG recibe:", state)

    respuesta = responder_pregunta(
        state["pregunta"]
    )

    return {
        "respuesta": respuesta
    }

def nodo_triaje(state):

    print("Nodo Triaje recibe:", state)

    decision = realizar_triaje(
        state["pregunta"]
    )
    print("Triaje decidió:", decision)
    return {
        "decisión": decision
    }
def nodo_pedir_info(state):

    return {
        "respuesta": "¿Puede indicar su número de atención?"
    }
def nodo_abrir_ticket(state):

    return {
        "respuesta": "Abriendo ticket de reclamo."
    }
def ejecutar_agente(pregunta):

    resultado = graph.invoke({
        "pregunta": pregunta
    })

    return resultado["respuesta"]

def decidir_ruta(state):

    if state["decision"] == "AUTO_RESOLVER":
        return "rag"

    elif state["decision"] == "ABRIR_TICKET":
        return "ticket"

    elif state["decision"] == "PEDIR_INFO":
        return "pedir_info"

builder = StateGraph(EstadoAgente)

builder.add_node("triaje", nodo_triaje)
builder.add_node("rag", nodo_rag)
builder.add_node("pedir_info", nodo_pedir_info)
builder.add_node("abrir_ticket", nodo_abrir_ticket)

builder.add_edge(START,"triaje")

builder.add_conditional_edges(
    "triaje",
    decidir_ruta
)
builder.add_edge("abrir_ticket", END)
builder.add_edge("pedir_info", END)
builder.add_edge("rag",END)

graph = builder.compile()

if __name__ == "__main__":
    print("Iniciando agente...")
    inicializar()
    pregunta = "¿Qué necesito para hospitalizarme?"

    respuesta = ejecutar_agente(pregunta)

    print("\nRespuesta:")
    print(respuesta)