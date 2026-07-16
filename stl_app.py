import streamlit as st

from agente import ejecutar_agente
from rag import inicializar

# Inicializar una sola vez
if "inicializado" not in st.session_state:
    inicializar()
    st.session_state.inicializado = True

st.title("🏥 HospitalIA")
st.write(
    "Soy tu asistente inteligente. "
    "Realiza una consulta sobre la documentación del Hospital San Gabriel."
)

pregunta = st.text_input("Escribe tu pregunta")

if st.button("Consultar"):

    if pregunta.strip():

        with st.spinner("Buscando respuesta..."):
            respuesta = ejecutar_agente(pregunta)

        st.success("Respuesta")
        st.write(respuesta)