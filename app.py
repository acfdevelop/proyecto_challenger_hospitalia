from agente import ejecutar_agente
from rag import inicializar


print("=== HospitalIA ===")
if __name__ == "__main__":
    inicializar()
    while True:

        pregunta = input("\nTú: ")

        if pregunta.lower() == "salir":
            break

        respuesta = ejecutar_agente(pregunta)

        print("\nHospitalIA:", respuesta)

